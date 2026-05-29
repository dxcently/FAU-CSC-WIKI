+++
title = "System Concepts"
weight = 2
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

> [!info] How the Club Uses This
> TODO: Add examples from competitions or labs where system-level concepts were exploited or defended (CCDC hardening tasks, privilege escalation challenges, etc.).

---

**References**

- [Linux Privilege Escalation techniques — HackTricks](https://book.hacktricks.xyz/linux-hardening/privilege-escalation)
- [PEAS-ng — automated privilege escalation enumeration](https://github.com/peass-ng/PEASS-ng)
- [Understanding /etc/passwd and /etc/shadow](https://www.cyberciti.biz/faq/understanding-etcpasswd-file-format/)
