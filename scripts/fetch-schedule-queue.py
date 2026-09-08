#!/usr/bin/env python3
"""Drain the Discord slash-command schedule queue into data/discord-schedule.json.

This never talks to Discord's API and needs no bot token. Something outside
this repo — a wsgi endpoint that does not exist yet — receives the `/schedule`
slash command and appends one JSON object per line to the file named by
SCHEDULE_QUEUE_PATH. This script's only job is to validate and drain that
queue; it is not documented from the Discord side because that side is not
built yet.

Unlike data/discord-postings.json, which fetch-postings.py rebuilds wholesale
from Discord's live reaction state on every run, data/discord-schedule.json
only ever grows through this script: there is no live state to re-scan, only
whatever the queue hands off since the last drain.

A queue line is one JSON object, and its `op` key says what to do with it.

`op` absent, or `op: "add"` — add a new entry: date, title, track, lead,
room, link, status, added_by, added_at. Only date is required; the rest are
optional strings, and an absent or empty one is simply left out of the
output entry so the render-time `default` fallbacks in
layouts/partials/home/schedule.html apply. date is re-validated here even
though the sender is expected to have validated it already — never trust the
queue. status is kept only when it is exactly "cancelled" or "moved"; any
other value is dropped as if absent. added_by/added_at are audit-only and
never copied into the output entry.

`op: "update"` — change fields already sitting in discord-schedule.json:
    {"op": "update", "match_date": "...", "match_title": "...",
     "fields": {<zero or more of: date, title, track, lead, room, link,
     status>}, "added_by": "...", "added_at": "..."}
`match_date`/`match_title` must exactly equal a stored entry's `date` and
`title` — no normalization beyond what an add already applies to a stored
entry — and must match exactly one entry in discord-schedule.json. Zero
matches or more than one match drops the whole line with a warning; this
script never guesses. `fields` uses the same key names a stored entry uses
(never "new_date"/"new_title" — any renaming from Discord command options to
these names happens upstream, outside this script). Each key in `fields` is
validated with the same per-field rule an add applies to that field; a key
that fails validation is dropped on its own, with a warning naming it, while
the rest of `fields` still applies. A `fields` left empty after that — or
never containing a recognized key — drops the whole line with a warning,
same as a zero-match update.

An update can only ever match an entry already written by this script into
discord-schedule.json. It never reads or writes content/_index.md's
hand-edited `[[params.sessions]]` front matter — that stays exclusively
hand-edited, the same way data/postings.toml is for jobs. An update aimed at
a session that exists only in the front matter simply finds no match here;
that is correct, not a bug to work around. (The wsgi endpoint that will
enqueue these does its own pre-check before ever writing an update line, so
an officer gets instant feedback when nothing matches — but this script
defends itself as if that check never happened, same as every other
Discord-adjacent script in this repo.)

Any other `op` value is invalid and drops the line with a warning naming the
bad op.

Queue lines are processed strictly in the order they appear, against one
running in-memory list, so an update can match an entry an earlier line in
the very same queue file just added. The result is sorted by date only once,
at the very end.

A line that fails to parse, or whose date is missing or invalid, is dropped
with one stderr line naming the problem and the raw line — never raised, so
one bad line does not abort the rest of the queue.

Commits and pushes only when data/discord-schedule.json actually changes,
using the same git identity / rebase-onto-main / gh credential-helper
pattern the sibling sync scripts use. Supports --dry-run identically:
prints the result, touches neither file. The queue file is truncated to
empty only as the very last step, after a successful write (or after a
no-op run that still consumed and reported on the whole queue) — never
before, so a failure partway through leaves its lines in the queue rather
than losing them.
"""
import datetime
import json
import os
import subprocess
import sys

OUT = "data/discord-schedule.json"

# All but `date` are optional strings; see the module docstring for the
# empty/absent -> omitted-key rule. added_by/added_at are read from the raw
# queue object but deliberately not in this list.
OPTIONAL_STR_FIELDS = ("title", "track", "lead", "room", "link")
VALID_STATUSES = {"cancelled", "moved"}


def _is_valid_date_str(value):
    """True when `value` is a string holding a valid ISO calendar date."""
    if not isinstance(value, str):
        return False
    try:
        datetime.date.fromisoformat(value)
    except ValueError:
        return False
    return True


def _is_nonempty_str(value):
    return isinstance(value, str) and value != ""


def _is_valid_status(value):
    return value in VALID_STATUSES


# Shared by an add's per-field checks and an update's `fields` validation —
# one rule per stored-entry key, so neither path can drift from the other.
FIELD_VALIDATORS = {
    "date": _is_valid_date_str,
    "title": _is_nonempty_str,
    "track": _is_nonempty_str,
    "lead": _is_nonempty_str,
    "room": _is_nonempty_str,
    "link": _is_nonempty_str,
    "status": _is_valid_status,
}


def _parse_add(raw):
    date = raw.get("date")
    if not isinstance(date, str):
        return None, "missing date"
    if not _is_valid_date_str(date):
        return None, f"invalid date {date!r}"
    entry = {"date": date}
    for field in OPTIONAL_STR_FIELDS:
        value = raw.get(field)
        if _is_nonempty_str(value):
            entry[field] = value
    if _is_valid_status(raw.get("status")):
        entry["status"] = raw["status"]
    return entry, None


def _parse_update(raw):
    match_date = raw.get("match_date")
    if not _is_nonempty_str(match_date):
        return None, "missing or invalid match_date"
    match_title = raw.get("match_title")
    if not _is_nonempty_str(match_title):
        return None, "missing or invalid match_title"

    raw_fields = raw.get("fields")
    if not isinstance(raw_fields, dict):
        raw_fields = {}
    fields = {}
    field_warnings = []
    for key, is_valid in FIELD_VALIDATORS.items():
        if key not in raw_fields:
            continue
        value = raw_fields[key]
        if is_valid(value):
            fields[key] = value
        else:
            field_warnings.append((key, f"invalid value {value!r}"))

    return {
        "op": "update",
        "match_date": match_date,
        "match_title": match_title,
        "fields": fields,
        "field_warnings": field_warnings,
    }, None


def parse_line(line):
    """One raw queue line -> (result, error); `result` is None when `error` is set.

    For `op` absent or `"add"`, `result` is the parsed entry ready to
    append — the same shape this returned before `op` existed. For
    `op: "update"`, `result` is a dict tagged with `"op": "update"` (an add
    entry never has an "op" key, so `drain` tells the two apart on that
    alone) carrying the match keys and the validated `fields` for `drain` to
    apply against its own running list — matching needs that list, which
    this function never sees.

    Never raises: a malformed line is the sender's problem, not a reason to
    abort the rest of the queue.
    """
    try:
        raw = json.loads(line)
    except json.JSONDecodeError as e:
        return None, f"invalid JSON ({e})"
    if not isinstance(raw, dict):
        return None, "not a JSON object"

    op = raw.get("op", "add")
    if op == "add":
        return _parse_add(raw)
    if op == "update":
        return _parse_update(raw)
    return None, f"unrecognized op {op!r}"


def drain(lines, current):
    """Valid adds and updates from `lines`, applied to `current`, sorted by date.

    Processes `lines` strictly in file order against one running in-memory
    list, so an update can match an entry an earlier line in this same call
    just added. Sorts by date only once, at the very end.

    Returns (merged, warnings): `warnings` is one (raw_line, reason) pair
    per problem found, in file order, for the caller to print — a line that
    failed to parse outright, an update matching zero or more than one
    entry, an update left with no valid fields, or a single invalid field
    inside an otherwise-fine update. A blank line is silently skipped, not
    warned about.
    """
    merged = [dict(e) for e in current]
    warnings = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        result, error = parse_line(line)
        if result is None:
            warnings.append((line, error))
            continue
        if isinstance(result, dict) and result.get("op") == "update":
            for key, reason in result["field_warnings"]:
                warnings.append((line, f"field {key!r}: {reason}"))
            fields = result["fields"]
            if not fields:
                warnings.append((line, "no valid fields to apply"))
                continue
            match_date, match_title = result["match_date"], result["match_title"]
            matches = [e for e in merged
                       if e.get("date") == match_date and e.get("title") == match_title]
            if len(matches) != 1:
                reason = "no matching entry" if not matches else "multiple matching entries"
                warnings.append(
                    (line, f"{reason} (date={match_date!r}, title={match_title!r})"))
                continue
            # A plain dict update: fields only ever sets or overwrites a
            # key, never clears one back to absent. No clear mechanism
            # exists here on purpose — nothing has asked for one yet.
            matches[0].update(fields)
            continue
        merged.append(result)
    merged.sort(key=lambda e: e["date"])
    return merged, warnings


def load_current(path):
    """The current data/discord-schedule.json, defaulting to [] when it is
    missing or unparseable — warning on stderr in the unparseable case only.
    """
    if not os.path.exists(path):
        return []
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(f"{path}: unreadable ({e}), starting from []", file=sys.stderr)
        return []
    if not isinstance(data, list):
        print(f"{path}: not a JSON list, starting from []", file=sys.stderr)
        return []
    return data


def sync(queue_path, out_path, dry_run=False, publish=None):
    """Drain `queue_path` into `out_path`; the whole script minus argv/env parsing.

    An unset, missing, or empty queue does nothing and returns immediately —
    the normal case on almost every run. `publish(out_path)` performs the
    commit+push side effect and is injected so tests can stand in for git,
    the same way fetch-postings.py injects `api`; it is only called when the
    write actually changes `out_path` and this is not a dry run. The queue
    is truncated as the very last step, only once everything above —
    including `publish` — has returned without raising, and never on a dry
    run.
    """
    if not queue_path or not os.path.exists(queue_path):
        return
    with open(queue_path, encoding="utf-8") as f:
        raw = f.read()
    if not raw.strip():
        return

    current = load_current(out_path)
    merged, warnings = drain(raw.splitlines(), current)
    for line, error in warnings:
        print(f"drop queue line ({error}): {line}", file=sys.stderr)

    new = json.dumps(merged, indent=2, ensure_ascii=False) + "\n"
    old = open(out_path, encoding="utf-8").read() if os.path.exists(out_path) else ""

    if dry_run:
        print(new)
        return

    if new != old:
        os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(new)
        if publish is not None:
            publish(out_path)

    with open(queue_path, "w", encoding="utf-8"):
        pass  # truncate: marks every line above as drained


def git_publish(out_path):
    """Commit `out_path` as the sync bot and push straight to main.

    Same identity / rebase-onto-main / gh credential-helper pattern the
    sibling sync scripts use.
    """
    ident = ["-c", "user.name=csc-announcements-bot",
             "-c", "user.email=csc-announcements-bot@users.noreply.github.com"]
    push  = ["-c", "credential.helper=!gh auth git-credential"]
    subprocess.run(["git", "add", out_path], check=True)
    subprocess.run(["git", *ident, "commit", "-q", "-m", "schedule: sync from Discord"], check=True)
    subprocess.run(["git", "pull", "--rebase", "--quiet", "origin", "main"], check=True)
    subprocess.run(["git", *push, "push", "-q", "origin", "HEAD:main"], check=True)


def main():
    sync(os.environ.get("SCHEDULE_QUEUE_PATH"), OUT,
         dry_run="--dry-run" in sys.argv, publish=git_publish)


if __name__ == "__main__":
    main()
