+++
title = "Network Defense"
weight = 4
description = "What network defense covers and why it is the focus of competitions like CCDC."
icon = "fa-solid fa-shield"
+++

Network defense is keeping attackers out and detecting them when they get in. It is the blue team side of security — monitoring, hardening, and response.

This is the primary focus of competitions like CCDC.

---

## Core Concepts

**Hardening:** Reducing the attack surface. Disable services you don't need, apply patches, enforce strong authentication, restrict permissions to the minimum required.

**Monitoring:** Knowing what is normal so you can detect what is not. Logs, alerts, dashboards, traffic baselines.

**Detection:** Identifying attacker behavior in logs and network traffic. SIEM tools aggregate and correlate events.

**Response:** When something is detected, contain it. Isolate the affected system, revoke credentials, block IPs, assess the damage.

---

## Key Technologies

| Technology | What it does |
|---|---|
| **Firewall** | Controls which traffic is allowed in and out based on rules |
| **IDS/IPS** | Intrusion Detection/Prevention System — inspects traffic for attack signatures |
| **SIEM** | Security Information and Event Management — aggregates logs and alerts |
| **VPN** | Encrypts network traffic between endpoints or sites |
| **Network segmentation** | Isolates systems into zones so a breach doesn't spread freely |
| **EDR** | Endpoint Detection and Response — monitors endpoints for malicious behavior |

---

## Tools

| Tool | Type |
|---|---|
| [pfSense](https://www.pfsense.org/) | Open-source firewall/router |
| [OPNsense](https://opnsense.org/) | Alternative to pfSense, active development |
| [Snort](https://www.snort.org/) | Open-source IDS/IPS |
| [Suricata](https://suricata.io/) | Modern IDS/IPS, multi-threaded |
| [Zeek](https://zeek.org/) | Network security monitoring framework |
| [Splunk](https://www.splunk.com/) | SIEM — free tier available |
| [Elastic Stack (ELK)](https://www.elastic.co/) | Open-source log aggregation and SIEM |
| [Wazuh](https://wazuh.com/) | Open-source EDR and SIEM |

---

## Hardening Basics

These apply to any Linux server:

```bash
# Disable unnecessary services
systemctl disable service_name

# Check what is listening
ss -tulnp

# Review sudo configuration
cat /etc/sudoers

# Check for SUID binaries
find / -perm -4000 2>/dev/null

# Review open ports and firewall rules
iptables -L -n -v
```

---

## CCDC Context

CCDC (Collegiate Cyber Defense Competition) is an attack/defend competition. Blue teams defend infrastructure against red teams of professional penetration testers.

The skills tested: hardening systems quickly, monitoring for attackers, responding to incidents, and keeping services running while under active attack.

> [!info] How the Club Uses This
> TODO: Add how the club prepares for CCDC — systems practiced on, hardening scripts, incident response playbooks, roles on the team, past results.

---

**References**

- [CCDC official site](https://www.nationalccdc.org/)
- [Awesome Cyber Defense resources](https://github.com/fabacab/awesome-cybersecurity-blueteam)
- [Blue Team Labs Online](https://blueteamlabs.online/) — defensive security challenges
- [TryHackMe SOC Level 1 path](https://tryhackme.com/path/outline/soclevel1)
