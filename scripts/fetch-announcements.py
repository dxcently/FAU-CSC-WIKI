#!/usr/bin/env python3
"""Sync the newest club Discord announcements into data/announcements.json.

Reads DISCORD_BOT_TOKEN and DISCORD_CHANNEL_ID from the environment — never the
repo. Keeps the newest messages that carry text, softens @everyone/@here so the
homepage does not shout, trims each to a teaser (full text stays a click away in
Discord), and writes the {date, author, text, url} shape the panel expects.
Commits and pushes only when the output changed, so the timer stays quiet while
nothing is posted. Run with --dry-run to print the JSON without touching git.
"""
import json, os, re, subprocess, sys, urllib.request

API = "https://discord.com/api/v10"
SHOW, WINDOW, MAXLEN = 5, 30, 240
OUT = "data/announcements.json"

TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
CHANNEL = os.environ.get("DISCORD_CHANNEL_ID")
DRY = "--dry-run" in sys.argv


def api(path):
    req = urllib.request.Request(API + path, headers={
        "Authorization": f"Bot {TOKEN}",
        # Discord 403s the default Python-urllib UA; it wants a DiscordBot one.
        "User-Agent": "DiscordBot (https://github.com/dxcently/fau-cyber-security-club-wiki, 1.0)",
    })
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def clean(text):
    text = text.replace("@everyone", "everyone").replace("@here", "here")
    text = re.sub(r"<a?(:\w+:)\d+>", r"\1", text)   # custom emoji -> :name:
    text = re.sub(r"<[@#][!&]?\d+>", "", text)       # raw id mentions -> drop
    text = re.sub(r"\s*\n\s*", " ", text)             # newlines -> spaces
    text = re.sub(r"\s{2,}", " ", text).strip()
    if len(text) > MAXLEN:
        text = text[:MAXLEN].rsplit(" ", 1)[0].rstrip() + "\u2026"
    return text


def build():
    guild = api(f"/channels/{CHANNEL}")["guild_id"]
    out = []
    for m in api(f"/channels/{CHANNEL}/messages?limit={WINDOW}"):   # newest first
        if m.get("type") not in (0, 19):     # skip system / join / pin
            continue
        text = clean(m.get("content", ""))
        if not text:                          # skip image-only / empty
            continue
        a = m["author"]
        out.append({
            "date": m["timestamp"],
            "author": a.get("global_name") or a.get("username"),
            "text": text,
            "url": f"https://discord.com/channels/{guild}/{CHANNEL}/{m['id']}",
        })
        if len(out) >= SHOW:
            break
    return json.dumps(out, indent=2, ensure_ascii=False) + "\n", len(out)


def git(*args):
    subprocess.run(["git", *args], check=True)


def main():
    if not TOKEN or not CHANNEL:
        sys.exit("DISCORD_BOT_TOKEN / DISCORD_CHANNEL_ID not set in the environment")
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    payload, n = build()
    if DRY:
        sys.stdout.write(payload)
        return
    # sync to main so the push is a fast-forward. Safe: the timer runs in its own
    # dedicated clone, nothing here is hand-edited.
    git("fetch", "--quiet", "origin", "main")
    git("reset", "--quiet", "--hard", "origin/main")
    old = open(OUT, encoding="utf-8").read() if os.path.exists(OUT) else ""
    if payload == old:
        print("no change"); return
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(payload)
    git("add", OUT)
    if subprocess.run(["git", "diff", "--cached", "--quiet"]).returncode == 0:
        print("no staged change"); return
    git("-c", "user.name=fau-csc-wiki-announcements",
        "-c", "user.email=announcements@necoconeco.net",
        "commit", "--quiet", "-m", "announcements: sync from Discord")
    git("-c", "credential.helper=!gh auth git-credential", "push", "--quiet", "origin", "HEAD:main")
    print(f"pushed {n} announcements")


if __name__ == "__main__":
    main()
