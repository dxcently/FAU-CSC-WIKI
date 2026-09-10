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
only ever grows: there is no live state to re-scan, only whatever the queue
hands off since the last drain. Correcting or removing an entry means hand-
editing that JSON file directly, same as content/_index.md's
[[params.sessions]] today.

A queue line is one JSON object, distinguished by an `op` key. `op` absent
means "add", same as before this script had an `op` at all:

  date, title, track, lead, room, link, status, added_by, added_at. Only
  date is required; the rest are optional strings, and an absent or empty
  one is simply left out of the output entry so the render-time `default`
  fallbacks in layouts/partials/home/schedule.html apply. date is
  re-validated here even though the sender is expected to have validated it
  already — never trust the queue. status is kept only when it is exactly
  "cancelled" or "moved"; any other value is dropped as if absent.
  added_by/added_at are audit-only and never copied into the output entry.

  Every added entry gets an `id`: the next integer after the highest `id`
  already present in the in-memory list at that point in the drain (an
  entry with no `id` — everything on disk today, and any hand-edited one —
  counts as 0), so several adds in one queue file each get a distinct,
  increasing id. That id is how an update below finds the entry again; it
  is assigned here and never changes afterward.

`op: "update"` looks like:

  {"op": "update", "id": 7, "fields": {<zero or more of: date, title,
   track, lead, room, link, status>}, "added_by": "...", "added_at": "..."}

  `id` is required and must look up exactly one entry already in the
  running list (see drain() below for the "running" part). Zero matches or
  more than one (a hand-edited file could duplicate an id) both drop the
  line with a warning naming the id and the reason; nothing is modified.
  `fields` is validated key by key with the same rules an add entry's
  fields get; an invalid value drops just that key (with a warning) while
  the rest of `fields` still applies, and `fields` empty after validation
  drops the whole line ("no valid fields to apply"). `fields` can never
  change `id` — an "id" key inside `fields` is dropped with a warning, not
  applied, same as any other invalid key.

`op: "delete"` looks like:

  {"op": "delete", "id": 7, "added_by": "...", "added_at": "..."}

  `id` is required and must look up exactly one entry already in the
  running list, same lookup `update` uses. Zero matches or more than one
  both drop the line with a warning naming the id and the reason, and
  change nothing. A missing or non-integer `id` is dropped with a warning,
  same as `update`. A delete removes the matched entry from the running
  list outright, so an add followed by a delete of that same just-assigned
  id, in the same queue file, resolves to the entry not being present at
  all in the result.

content/_index.md's hand-written [[params.sessions]] never gets an id —
this script does not read that file and never will — so an update or
delete by id can only ever reach a bot-owned entry in
data/discord-schedule.json. That front-matter file stays exclusively
hand-edited, same as data/postings.toml is for jobs; it is a structural
boundary, not a rule this script has to enforce by checking anything.

Any other `op` value is invalid and drops the line with a warning naming
the bad op.

A line that fails to parse, whose date is missing or invalid (add), or
whose id is missing or not an integer (update/delete), is dropped with one
stderr line naming the problem and the raw line — never raised, so one bad
line does not abort the rest of the queue. Queue lines are processed
strictly in file order against a single running list, so an add followed
by an update or delete of that same just-added entry, in the same queue
file, resolves correctly. The list is sorted by date only once, at the end.

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


def _is_valid_date(value):
    if not isinstance(value, str):
        return False
    try:
        datetime.date.fromisoformat(value)
        return True
    except ValueError:
        return False


def _is_valid_status(value):
    return value in VALID_STATUSES


def _is_nonempty_str(value):
    return isinstance(value, str) and bool(value)


# Per-field validity, shared by an add entry's own fields and an update's
# `fields` object — see the module docstring. Not used for `date` on the
# add path directly, since a missing add-path date gets a different error
# message ("missing date") than an invalid one; see _load_object/parse_line.
FIELD_VALIDATORS = {
    "date": _is_valid_date,
    "status": _is_valid_status,
    "title": _is_nonempty_str,
    "track": _is_nonempty_str,
    "lead": _is_nonempty_str,
    "room": _is_nonempty_str,
    "link": _is_nonempty_str,
}


def _load_object(line):
    """One raw queue line -> (raw_dict, error); `raw_dict` is None when `error` is set."""
    try:
        raw = json.loads(line)
    except json.JSONDecodeError as e:
        return None, f"invalid JSON ({e})"
    if not isinstance(raw, dict):
        return None, "not a JSON object"
    return raw, None


def _parse_add_fields(raw):
    """An already-parsed add object -> (entry, error); `entry` is None when `error` is set."""
    date = raw.get("date")
    if not isinstance(date, str):
        return None, "missing date"
    if not _is_valid_date(date):
        return None, f"invalid date {date!r}"
    entry = {"date": date}
    for field in OPTIONAL_STR_FIELDS:
        value = raw.get(field)
        if _is_nonempty_str(value):
            entry[field] = value
    if _is_valid_status(raw.get("status")):
        entry["status"] = raw["status"]
    return entry, None


def parse_line(line):
    """One raw add-op queue line -> (entry, error); `entry` is None when `error` is set.

    Never raises: a malformed line is the sender's problem, not a reason to
    abort the rest of the queue.
    """
    raw, error = _load_object(line)
    if raw is None:
        return None, error
    return _parse_add_fields(raw)


def _next_id(merged):
    """The id to assign to the next added entry: highest existing id + 1.

    An entry with no `id` counts as 0, per the module docstring, so a list
    with no ids yet starts at 1.
    """
    ids = [e["id"] for e in merged
           if isinstance(e.get("id"), int) and not isinstance(e.get("id"), bool)]
    return (max(ids) if ids else 0) + 1


def _validate_update_fields(fields_raw, warnings, line):
    """raw `fields` -> valid subset, dict-updated in place; bad keys warn and drop."""
    valid = {}
    if not isinstance(fields_raw, dict):
        fields_raw = {}
    for key, value in fields_raw.items():
        if key == "id":
            warnings.append((line, "field 'id' cannot be changed"))
            continue
        validator = FIELD_VALIDATORS.get(key)
        if validator is None:
            warnings.append((line, f"unknown field {key!r} ignored"))
            continue
        if not validator(value):
            warnings.append((line, f"invalid {key} {value!r}"))
            continue
        valid[key] = value
    return valid


def _require_id(raw, op, warnings, line):
    """raw["id"] as a non-bool int, or None with a warning appended.

    Shared by update and delete — both require the same shape of `id`.
    """
    id_val = raw.get("id")
    if not isinstance(id_val, int) or isinstance(id_val, bool):
        warnings.append((line, f"{op} requires an integer id"))
        return None
    return id_val


def _find_one_by_id(id_val, merged, warnings, line):
    """The single entry in `merged` matching `id_val`, or None with a warning.

    Shared by update and delete — both treat zero or multiple matches as
    ambiguous and change nothing.
    """
    matches = [e for e in merged if e.get("id") == id_val]
    if not matches:
        warnings.append((line, f"no entry with id {id_val}"))
        return None
    if len(matches) > 1:
        warnings.append((line, f"multiple entries with id {id_val}"))
        return None
    return matches[0]


def _apply_update(raw, merged, warnings, line):
    """Apply one op="update" line to `merged` in place, or warn and change nothing."""
    id_val = _require_id(raw, "update", warnings, line)
    if id_val is None:
        return
    # fields.id is rejected inside _validate_update_fields, but the whole
    # id lookup below still needs to run against whatever fields survive.
    valid_fields = _validate_update_fields(raw.get("fields"), warnings, line)
    if not valid_fields:
        warnings.append((line, "no valid fields to apply"))
        return
    match = _find_one_by_id(id_val, merged, warnings, line)
    if match is None:
        return
    # A plain dict update: fields only ever sets or overwrites a key, it
    # never clears one back to absent. No clear mechanism is provided.
    match.update(valid_fields)


def _apply_delete(raw, merged, warnings, line):
    """Apply one op="delete" line to `merged` in place, or warn and change nothing."""
    id_val = _require_id(raw, "delete", warnings, line)
    if id_val is None:
        return
    match = _find_one_by_id(id_val, merged, warnings, line)
    if match is None:
        return
    merged[:] = [e for e in merged if e is not match]


def drain(lines, current):
    """Valid queue lines applied to `current`: adds appended, updates merged in place.

    Returns (merged, warnings): `warnings` is one (raw_line, reason) pair per
    problem worth reporting, in file order, for the caller to print — some
    warnings drop the whole line, others just drop one bad key inside an
    update's `fields`, see the module docstring. A blank line is silently
    skipped, not warned about. Lines are processed strictly in order against
    a single running list, so an update can match an entry added earlier in
    the same call. The result is sorted by date only once, at the end.
    """
    merged = list(current)
    warnings = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        raw, error = _load_object(line)
        if raw is None:
            warnings.append((line, error))
            continue
        op = raw.get("op", "add")
        if op == "add":
            entry, error = _parse_add_fields(raw)
            if entry is None:
                warnings.append((line, error))
                continue
            entry["id"] = _next_id(merged)
            merged.append(entry)
        elif op == "update":
            _apply_update(raw, merged, warnings, line)
        elif op == "delete":
            _apply_delete(raw, merged, warnings, line)
        else:
            warnings.append((line, f"unrecognized op {op!r}"))
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
        print(f"schedule queue: {error}: {line}", file=sys.stderr)

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
