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

A queue line is one JSON object: date, title, track, lead, room, link,
status, added_by, added_at. Only date is required; the rest are optional
strings, and an absent or empty one is simply left out of the output entry
so the render-time `default` fallbacks in layouts/partials/home/schedule.html
apply. date is re-validated here even though the sender is expected to have
validated it already — never trust the queue. status is kept only when it is
exactly "cancelled" or "moved"; any other value is dropped as if absent.
added_by/added_at are audit-only and never copied into the output entry.

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


def parse_line(line):
    """One raw queue line -> (entry, error); `entry` is None when `error` is set.

    Never raises: a malformed line is the sender's problem, not a reason to
    abort the rest of the queue.
    """
    try:
        raw = json.loads(line)
    except json.JSONDecodeError as e:
        return None, f"invalid JSON ({e})"
    if not isinstance(raw, dict):
        return None, "not a JSON object"
    date = raw.get("date")
    if not isinstance(date, str):
        return None, "missing date"
    try:
        datetime.date.fromisoformat(date)
    except ValueError:
        return None, f"invalid date {date!r}"
    entry = {"date": date}
    for field in OPTIONAL_STR_FIELDS:
        value = raw.get(field)
        if isinstance(value, str) and value:
            entry[field] = value
    if raw.get("status") in VALID_STATUSES:
        entry["status"] = raw["status"]
    return entry, None


def drain(lines, current):
    """Valid entries parsed from `lines`, appended to `current`, sorted by date.

    Returns (merged, warnings): `warnings` is one (raw_line, reason) pair per
    line that failed to parse, in file order, for the caller to print. A
    blank line is silently skipped, not warned about.
    """
    merged = list(current)
    warnings = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        entry, error = parse_line(line)
        if entry is None:
            warnings.append((line, error))
            continue
        merged.append(entry)
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
