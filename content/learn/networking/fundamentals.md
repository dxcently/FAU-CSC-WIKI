+++
title = "IP, Ports & Subnets"
weight = 1
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

> [!info] How the Club Uses This
> TODO: Add examples from CCDC, CTFs, or lab exercises where subnetting and port identification were relevant.

---

**References**

- [Subnet Calculator](https://www.subnet-calculator.com/)
- [RFC 1918 — Private Address Space](https://www.rfc-editor.org/rfc/rfc1918)
- [IANA Port Assignments](https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml)
