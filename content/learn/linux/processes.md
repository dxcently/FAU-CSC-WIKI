+++
title = "Processes & Services"
weight = 3
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
