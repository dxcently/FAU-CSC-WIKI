+++
title = "Processes & Services"
weight = 3
description = "What a Linux process is and how to inspect what is running and as whom."
icon = "fa-solid fa-gears"
+++

A process is a running program. Understanding what is running, as whom, and why is essential for both offense and defense.

---

## Viewing Processes

```bash
ps aux                    # all running processes with details
ps aux | grep nginx       # find a specific process
top                       # interactive real-time process viewer
htop                      # better version of top (install separately)
pgrep processname         # get PID of a named process
```

Key columns in `ps aux`: `USER` (who is running it), `PID` (process ID), `%CPU`, `%MEM`, `COMMAND` (what it is).

---

## Killing Processes

```bash
kill PID              # send SIGTERM (polite stop)
kill -9 PID           # send SIGKILL (force kill, no cleanup)
killall processname   # kill all processes with that name
pkill pattern         # kill by pattern match
```

Use `kill -9` only when a process won't respond to a normal kill. It skips any cleanup the process would normally do.

---

## Background Jobs

```bash
command &             # run in background
jobs                  # list background jobs
fg %1                 # bring job 1 to foreground
bg %1                 # resume stopped job in background
Ctrl+Z                # suspend foreground process
nohup command &       # run and keep running after logout
```

---

## Services (systemd)

Most modern Linux distros use systemd to manage services.

```bash
systemctl status nginx          # is this service running?
systemctl start nginx           # start it
systemctl stop nginx            # stop it
systemctl restart nginx         # restart
systemctl enable nginx          # start on boot
systemctl disable nginx         # do not start on boot
systemctl list-units --type=service   # all running services
```

---

## Checking Open Connections

```bash
ss -tulnp             # listening ports and which process owns them
netstat -tulnp        # older equivalent
lsof -i :80           # what is using port 80
```

---

## Who Spawned What

Every process has a parent. The tree shows how something got started. A shell running under a web server is a finding.

```bash
pstree -p               # the whole tree, with PIDs
ps -ef --forest         # the same, with full command lines
```

Every process also has a directory under `/proc`. It answers questions the process itself might lie about.

```bash
ls -l /proc/1234/exe                       # the real binary, even if it was deleted after launch
ls -l /proc/1234/cwd                       # its working directory
cat /proc/1234/cmdline | tr '\0' ' '       # the exact command line
cat /proc/1234/environ | tr '\0' '\n'      # its environment. Credentials end up here.
ls -l /proc/1234/fd                        # every file and socket it has open
```

---

## Logs Live in journalctl

On a systemd system, `cat /var/log/syslog` is the old way, and the file is often not there. Ask the journal instead.

```bash
journalctl -u nginx                      # logs for one service
journalctl -f                            # follow everything, live
journalctl -u ssh --since "1 hour ago"
journalctl -p err -b                     # errors since boot
```

Reference: [journalctl(1)](https://www.freedesktop.org/software/systemd/man/latest/journalctl.html).

---

## Keep a Session Alive

A shell dies when the connection drops, and so does everything running in it. Run long jobs inside `tmux`. Detach, reconnect later, and the job is still there.

```bash
tmux              # start a session
# Ctrl-b d        # detach. The session keeps running.
tmux ls           # list sessions
tmux attach       # come back to it
```

`screen` does the same job on older systems. Learn one of them before your first long scan over a flaky VPN. The [tmux wiki](https://github.com/tmux/tmux/wiki) is the reference.

---

## What Is It Actually Doing

When a program misbehaves and the logs say nothing, watch its system calls.

```bash
strace -f -p 1234                     # attach to a running process
strace -e trace=openat ./program      # which files does it try to open?
```

`strace -e trace=openat` is how you find the config file a program reads without telling you. Reference: [strace](https://strace.io/).

---

## In CTF Environments

**After landing a shell — understand what is running:**
```bash
# What is running and as whom?
ps aux

# Any process running as root that looks unusual?
ps aux | grep root | grep -v '\[' | grep -v systemd

# What ports are open internally that were not visible from outside?
ss -tulnp
# Common find: database running on localhost only (3306 mysql, 5432 postgres)
# — useful for port forwarding back to your machine

# What services are running?
systemctl list-units --type=service --state=running
```

**Port forwarding an internal service to your machine:**
```bash
# On your machine — forward remote port 3306 to local 3306 via SSH
ssh -L 3306:localhost:3306 user@target.htb

# Then connect to MySQL locally
mysql -u root -p -h 127.0.0.1
```

**Looking for running processes that expose credentials:**
```bash
# Watch what processes run (catches cron jobs)
watch -n 1 "ps aux --sort=-%cpu | head -20"

# Check process command lines for embedded credentials
cat /proc/*/cmdline 2>/dev/null | tr '\0' ' ' | grep -i "pass\|key\|secret"
```

**Blue team / CCDC — detecting attacker processes:**
```bash
# Processes connecting outbound (reverse shells)
ss -tulnp | grep ESTABLISHED

# Check for unusual listening ports that appeared recently
ss -tulnp

# Suspicious process names or paths
ps aux | grep -E '(nc|ncat|bash -i|/tmp/|python -c)'
```

---

## Using AI

**Where it helps with processes:**

- **Interpreting `ps aux` output:** Paste an unusual process line. Ask what it is doing and whether it is suspicious.
- **Writing monitoring scripts:** "Write a bash script that watches for new processes connecting to external IPs and logs them with a timestamp." This is the kind of one-off defensive tooling that AI produces well.
- **Understanding systemd unit files:** Paste a `.service` file and ask what it does, what user it runs as, and whether there is anything misconfigured.
- **Port forwarding syntax:** SSH forwarding flags are not obvious. Describe the scenario and get the exact command.

---

> [!info] How the Club Uses This
> TODO: Add examples from competition scenarios where process analysis was relevant (blue team, forensics challenges, etc.).

---

**References**

- [systemd documentation](https://systemd.io/)
- [Linux process management — DigitalOcean](https://www.digitalocean.com/community/tutorials/process-management-in-linux)
- `man ps`, `man kill`, `man systemctl` — in your terminal
