+++
title = "IP, Ports & Subnets"
weight = 1
description = "IP addresses, ports, and subnets — the foundation of everything in networking."
icon = "fa-solid fa-sitemap"
+++

Every device on a network has an IP address. Every service on that device runs on a port. Subnets define which devices are in the same network segment.

These three concepts are the foundation of everything in networking.

---

## IP Addresses

An IPv4 address is four numbers from 0–255, separated by dots. Example: `192.168.1.10`

**Private ranges** — not routable on the public internet:

| Range | Example |
|---|---|
| `10.0.0.0/8` | `10.0.0.1` |
| `172.16.0.0/12` | `172.16.5.3` |
| `192.168.0.0/16` | `192.168.1.1` |

If you see an IP in these ranges, it is a private address — on a local network or a VM.

IPv6 is longer and looks like `2001:db8::1`. It is increasingly common. The concepts are the same.

---

## Subnets and CIDR

A subnet groups IPs together. CIDR notation (`/24`) tells you how many bits are fixed.

| CIDR | Hosts | Example |
|---|---|---|
| `/24` | 254 | `192.168.1.0/24` → `192.168.1.1` to `.254` |
| `/16` | 65,534 | `10.0.0.0/16` → `10.0.0.1` to `10.0.255.254` |
| `/30` | 2 | Point-to-point links |

`/24` is the most common subnet you will see in home and small office networks.

A subnet calculator is your friend. [Use this one.](https://www.subnet-calculator.com/)

---

## Ports

A port is a number from 0–65535. It tells the OS which application should receive a packet.

**Well-known ports (0–1023):**

| Port | Service |
|---|---|
| 22 | SSH |
| 80 | HTTP |
| 443 | HTTPS |
| 21 | FTP |
| 25 | SMTP |
| 53 | DNS |
| 3306 | MySQL |
| 5432 | PostgreSQL |
| 8080 | HTTP alt / web proxies |

Services above 1024 can be used by any process. Finding unexpected services on high ports is a common finding in pentests.

---

## Real-World Context

When scanning a network or a target host, you are looking for open ports. Each open port is a potential entry point. Each service running behind that port has its own attack surface.

The first step in almost every engagement is a port scan.

---

## In CTF Environments

Every CTF engagement starts with the same question: what is running and where? IP, ports, and subnets are how you answer it.

**Standard recon sequence for an HTB/THM box:**
```bash
# You are given one IP. Start there.
TARGET=10.10.10.5

# Fast port sweep — all 65535 ports, high rate
nmap -p- --min-rate 5000 -T4 $TARGET -oN allports.txt

# Extract open ports into a variable
PORTS=$(grep "open" allports.txt | cut -d'/' -f1 | tr '\n' ',' | sed 's/,$//')

# Deep scan: version detection + default scripts on open ports only
nmap -sV -sC -p$PORTS $TARGET -oN detailed.txt
```

Doing `-sV -sC` against all 65535 ports wastes time. Do the fast sweep first, then go deep on what is open.

**Identifying interesting ports fast:**

| Port you see | What to check first |
|---|---|
| 21 (FTP) | Anonymous login: `ftp <ip>`, user `anonymous` |
| 22 (SSH) | Username enumeration, key-based auth, version exploits |
| 80 / 443 | Web app — run gobuster/ffuf, check robots.txt, view source |
| 139 / 445 (SMB) | `smbclient -L //<ip>`, check null sessions |
| 3306 (MySQL) | Try `mysql -h <ip> -u root` with no password |
| 8080 / 8443 | Second web app, often less hardened than the main one |

**CCDC — subnet enumeration after first foothold:**

CCDC gives you a scored network with many hosts. After you understand your subnet layout, you can identify which hosts are yours to defend and which belong to the red team.

```bash
# Discover hosts in your subnet
nmap -sn 192.168.x.0/24 -oN hosts.txt

# Check all hosts for open management ports (SSH, RDP, WinRM)
nmap -p 22,3389,5985 192.168.x.0/24 --open
```

**Subnetting gotcha in competitions:**

CTF machines and CCDC environments often use `/24` subnets. If your machine has IP `10.10.10.15` with a `/24` mask, the gateway is probably `10.10.10.1` and the target range is `10.10.10.0/24`. Do not scan past your subnet without confirming you have permission.

---

> [!info] How the Club Uses This
> Port scanning is the first move on every CTF box. In CCDC, subnet awareness tells you the full scope of what you are defending before the red team maps it for you.

---

**References**

- [Subnet Calculator](https://www.subnet-calculator.com/)
- [RFC 1918 — Private Address Space](https://www.rfc-editor.org/rfc/rfc1918)
- [IANA Port Assignments](https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml)
