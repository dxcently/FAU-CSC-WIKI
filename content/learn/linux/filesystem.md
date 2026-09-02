+++
title = "The Filesystem"
weight = 1
description = "How the Linux filesystem is laid out and why understanding it matters for security work."
icon = "fa-solid fa-folder-tree"
+++

In Linux, everything is a file. Devices, sockets, processes — all represented as files somewhere in the tree. Understanding the layout is step one.

There is exactly one tree. Windows gives you `C:` and `D:`; Linux gives you `/`
and hangs everything off it, including your second disk and your USB stick.
Learn this shape once and you can find your way around any Linux box you are
ever dropped onto.

---

## The Tree

```tree
- / | folder | secondary
  - bin | folder | grey
  - boot | folder | grey
  - dev | folder | cyan
  - etc | folder | red
  - home | folder | green
    - you | folder | green
      - .ssh | folder | red
      - .bashrc | file | orange
  - lib | folder | grey
  - opt | folder | grey
  - proc | folder | cyan
  - root | folder | red
  - sbin | folder | grey
  - srv | folder | grey
  - tmp | folder | orange
  - usr | folder | grey
    - bin | folder | grey
    - local | folder | grey
    - share | folder | grey
  - var | folder | orange
    - log | folder | red
    - www | folder | orange
```

The colours are the security read, not part of the standard:

| Colour | Means | Why you care |
| --- | --- | --- |
| 🔴 Red | Secrets and control | Configuration, keys, credentials. Where an attacker looks first, and what a defender watches. |
| 🟠 Orange | Writable or volatile | Anyone can write to `/tmp`. Web roots and logs get attacker-influenced content. |
| 🔵 Cyan | Not real files | `/proc` and `/dev` are the kernel pretending to be a filesystem. Nothing here is on your disk. |
| 🟢 Green | Yours | Your files, your dotfiles, your keys. |
| ⚪ Grey | Programs | Binaries and libraries. Mostly read-only, and a change here is worth noticing. |

Two things surprise people coming from Windows:

**`/proc` is fake.** It is a view into the running kernel rendered as text
files. `cat /proc/self/status` tells you about the process that ran `cat`.
Nothing under `/proc` exists on disk, which is why it survives no reboot and
why it is the fastest way to inspect a live system.

**`/root` is not `/`.** `/root` is the superuser's home directory. `/` is the
top of the tree. They are different places, and mixing them up in a command is
how people delete things they did not mean to.

---

## Key Directories

| Path | What lives there |
|---|---|
| `/` | Root of the entire filesystem |
| `/home/username` | Your personal files |
| `/etc` | System configuration files |
| `/var` | Logs, databases, runtime data |
| `/tmp` | Temporary files — cleared on reboot |
| `/usr/bin` | User-installed executables |
| `/bin`, `/sbin` | Core system executables |
| `/proc` | Virtual filesystem exposing kernel/process info |
| `/dev` | Device files |

When you are looking for a config file, start in `/etc`. When you are looking for a binary, check `/usr/bin`. When you are debugging a process, look in `/proc`.

---

## Navigation

```bash
pwd               # print current directory
ls -la            # list files with permissions and hidden files
cd /path/to/dir   # change directory
cd ..             # go up one level
cd ~              # go to your home directory
```

---

## Finding Files

```bash
find / -name "passwd" 2>/dev/null    # find by name, suppress errors
find /etc -type f -name "*.conf"     # find config files
locate filename                       # faster search using a database
which python3                         # find where a binary lives
```

`find` searches in real time. `locate` uses a cached index — run `updatedb` first if results are stale.

---

## Reading Files

```bash
cat /etc/passwd          # dump entire file
less /var/log/syslog     # paginated view, q to quit
head -n 20 file.txt      # first 20 lines
tail -n 20 file.txt      # last 20 lines
tail -f /var/log/syslog  # follow a log in real time
grep "error" file.txt    # search for pattern
```

---

## Identify Before You Trust

The extension is a suggestion. The bytes are the truth.

```bash
file mystery.bin       # what a file actually is, read from its contents
file *                 # every file in the directory
xxd file | head        # hex dump. The first bytes (the "magic number") name the format.
strings file | less    # printable text hidden inside a binary
```

A CTF file named `photo.jpg` that `file` calls a ZIP archive is the challenge telling you what to do next.

Hidden files start with a dot. `ls` skips them. `ls -la` does not, and neither should you. Reference: [file(1)](https://man7.org/linux/man-pages/man1/file.1.html).

---

## Disk, Links, and Environment

```bash
df -h                          # free space per filesystem
du -sh * | sort -rh | head     # what is using the space, biggest first
ln -s /real/path linkname      # a symbolic link: a pointer to another path
readlink -f linkname           # where a link actually points
tree -L 2                      # the directory as a picture, two levels deep
env                            # every environment variable. Secrets get left here.
```

Two directories are writable by everyone on almost every Linux system: `/tmp` and `/dev/shm`. When you cannot write anywhere else, you can write there. `/dev/shm` lives in RAM and is gone after a reboot.

---

## In CTF Environments

On a Linux CTF box (HackTheBox, TryHackMe, etc.), filesystem enumeration is your first move after getting a shell.

**Initial orientation after landing a shell:**
```bash
whoami && id          # who are you
pwd                   # where are you
ls -la                # what is here
uname -a              # kernel version (useful for kernel exploits)
cat /etc/os-release   # distro info
```

**Hunt for credentials and interesting files:**
```bash
# Config files that often contain passwords
find / -name "*.conf" 2>/dev/null | xargs grep -l "password" 2>/dev/null
find / -name "*.env" 2>/dev/null
find / -name "id_rsa" 2>/dev/null    # SSH private keys

# World-readable sensitive files
find / -readable -type f 2>/dev/null | grep -v proc | grep -v sys

# Recently modified files (attacker activity or fresh config)
find / -mmin -10 -type f 2>/dev/null | grep -v proc

# Files owned by current user outside home dir
find / -user $(whoami) 2>/dev/null | grep -v proc | grep -v sys
```

**Checking for flags specifically:**
```bash
find / -name "flag*" -o -name "user.txt" -o -name "root.txt" 2>/dev/null
find / -name "*.txt" -readable 2>/dev/null | xargs grep -l "flag{" 2>/dev/null
```

---

## Using AI

**Where it helps on filesystem tasks:**

- **Understanding find syntax:** The flags are cryptic. Describe what you want to find and AI will produce the right `find` command. Then learn what each flag does.
- **Reading unfamiliar config files:** Paste a `sshd_config`, nginx config, or cron file. Ask what is misconfigured or interesting from a security perspective.
- **Explaining output:** Paste the output of `ls -la` on an unusual directory and ask what the permissions mean.
- **Building enumeration checklists:** "What files and directories should I check after getting a low-privilege shell on a Linux box?" AI knows the standard checklist — use it as a prompt, then verify manually.

---

> [!info] How the Club Uses This
> TODO: Add specific lab exercises or CTF challenges where filesystem navigation was key.

---

**References**

- [Linux Filesystem Hierarchy Standard](https://refspecs.linuxfoundation.org/FHS_3.0/fhs/index.html)
- [explainshell.com](https://explainshell.com/) — paste any command and get it explained
- [linuxcommand.org](http://linuxcommand.org/)
