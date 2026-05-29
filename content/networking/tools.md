+++
title = "Networking Tools"
weight = 3
+++

These are the tools you will use constantly. Learn the basics of each one — not every flag, just what it does and when to reach for it.

---

## ping

Tests basic connectivity. Sends ICMP echo requests and waits for replies.

```bash
ping 192.168.1.1           # continuous ping (Ctrl+C to stop)
ping -c 4 192.168.1.1      # send exactly 4 packets
ping -i 0.2 192.168.1.1    # faster pinging (0.2s between packets)
```

If there's no response: the host may be down, or ICMP may be blocked by a firewall.

---

## traceroute / tracepath

Shows the path packets take to reach a destination. Each hop is a router.

```bash
traceroute google.com
tracepath google.com      # similar, no root required
```

High latency on a specific hop often indicates a problem at that router.

---

## netstat / ss

Shows open network connections and listening ports.

```bash
ss -tulnp                 # listening ports and owning process (preferred)
netstat -tulnp            # older equivalent, may not be installed
ss -s                     # summary statistics
```

`ss` is the modern replacement for `netstat`. Both do the same thing.

---

## nmap

Network scanner. Finds hosts, open ports, services, and OS fingerprints.

```bash
nmap 192.168.1.1              # basic scan (top 1000 ports)
nmap -sV 192.168.1.1          # detect service versions
nmap -p 1-65535 192.168.1.1   # scan all ports
nmap -sn 192.168.1.0/24       # ping sweep (host discovery only)
nmap -A 192.168.1.1           # aggressive — OS, scripts, traceroute
```

> [!warning] Only scan networks you own or have explicit permission to scan.
> Unauthorized network scanning is illegal in most jurisdictions.

- [nmap documentation](https://nmap.org/docs.html)

---

## Wireshark

Packet capture and analysis tool with a GUI. Captures live traffic or reads `.pcap` files.

Use it to see exactly what data is going over the wire. Essential for protocol analysis, debugging, and CTF forensics challenges.

- [Wireshark documentation](https://www.wireshark.org/docs/)

For terminal-only environments, use `tcpdump`:

```bash
tcpdump -i eth0                     # capture on interface eth0
tcpdump -i eth0 port 80             # filter to port 80
tcpdump -w capture.pcap -i eth0     # write to file
```

---

## curl / wget

Make HTTP requests from the command line.

```bash
curl https://example.com                          # GET request
curl -X POST -d "user=foo&pass=bar" http://site   # POST with form data
curl -H "Authorization: Bearer TOKEN" http://api  # with a header
curl -I https://example.com                       # headers only
wget https://example.com/file.zip                 # download a file
```

`curl` is for inspecting and interacting with HTTP. `wget` is for downloading.

---

## dig / nslookup

DNS query tools.

```bash
dig google.com              # A record (IP)
dig google.com MX           # mail server records
dig google.com ANY          # all records
nslookup google.com         # simpler alternative
```

---

## In CTF Environments

**Recon workflow on a new machine:**
```bash
# 1. Discover open ports (fast scan first)
nmap -p- --min-rate 5000 -T4 10.10.10.5 -oN ports.txt

# 2. Pull open ports into a variable
ports=$(grep "open" ports.txt | cut -d'/' -f1 | tr '\n' ',' | sed 's/,$//')

# 3. Deep scan only open ports
nmap -sV -sC -p$ports 10.10.10.5 -oN detailed.txt
```

**Network forensics — analyzing a .pcap in a CTF:**
```bash
# Filter HTTP traffic from a capture
tcpdump -r capture.pcap -A port 80

# Extract files from a pcap (Wireshark can also do this via File → Export Objects)
tcpdump -r capture.pcap -w http_only.pcap port 80

# Find credentials in cleartext traffic
strings capture.pcap | grep -i "pass\|user\|login\|auth"
```

**Pivoting — finding what else is reachable from a compromised host:**
```bash
# Scan the internal network from a foothold
# (use a static nmap binary uploaded to the victim, or proxychains)
./nmap-static -sn 10.10.10.0/24    # host discovery
./nmap-static -p 22,80,443,3306 10.10.10.0/24   # targeted port scan
```

**CTF web recon:**
```bash
# Directory brute force
ffuf -u http://target.htb/FUZZ -w /usr/share/wordlists/dirb/common.txt

# Subdomain enumeration
ffuf -u http://FUZZ.target.htb -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt -H "Host: FUZZ.target.htb"

# Check what a server exposes
curl -I http://target.htb           # headers
curl -s http://target.htb/robots.txt   # often reveals hidden paths
```

---

## Using AI

Networking tools generate a lot of output. AI is useful for making sense of it quickly.

**Where it helps:**

- **Interpreting nmap output:** Paste the scan results and ask "what attack surface does this expose?" AI will flag interesting services, unusual ports, and known vulnerable versions.
- **Wireshark display filters:** The filter syntax is not intuitive. Describe what you are looking for and ask for the filter. Example: "show only HTTP POST requests containing the word password."
- **Writing recon scripts:** "Write a bash script that runs nmap against a /24, extracts open port 80 hosts, and runs gobuster against each one."
- **Protocol analysis:** Paste a hex dump or ASCII stream and ask what protocol it is or what it contains.
- **Identifying services:** Unknown port or service banner? Paste it and ask.

**What AI cannot do:** actually run the scan, know what is on your specific network, or replace looking at the traffic yourself. Use it to accelerate interpretation, not replace it.

---

> [!info] How the Club Uses This
> TODO: Add which tools the club uses in competitions (CCDC network defense, CTF recon challenges, etc.) and any club-specific configurations or scripts.

---

**References**

- [nmap book (free)](https://nmap.org/book/toc.html)
- [Wireshark — sample captures for practice](https://wiki.wireshark.org/SampleCaptures)
- [curl docs](https://curl.se/docs/)
