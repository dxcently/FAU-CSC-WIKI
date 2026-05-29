+++
title = "Practical Workflows"
weight = 4
+++

These are repeatable patterns — not one-off prompts. Build them into habits and you get compounding results.

---

## CTF Workflow with AI

The loop that works:

```
1. Enumerate manually (understand what you have)
2. Ask AI to analyze the enumeration output
3. Generate exploit / script with AI
4. Run it, get output
5. Feed output back to AI for interpretation
6. Iterate
```

AI is most useful at steps 2, 3, and 5. You own steps 1, 4, and the final judgment call.

---

### Web Challenge

```bash
# 1. Recon
curl -I http://target.htb
curl -s http://target.htb/robots.txt
ffuf -u http://target.htb/FUZZ -w wordlist.txt -o ffuf_out.json

# 2. Feed to AI
cat ffuf_out.json | claude "analyze this ffuf output, identify interesting paths, 
suggest what vulnerabilities to test first"

# 3. Intercept a request in Burp, export as curl command
# 4. Ask AI to generate SQLi/XSS/SSRF payloads for that specific endpoint
# 5. Run payloads, paste any interesting response back for interpretation
```

---

### Forensics / File Analysis

```bash
# Dump what a file is
file mystery_file
strings mystery_file > strings_out.txt
xxd mystery_file | head -50 > hex_head.txt

# Ask AI
claude "here is the hex header and strings from a file. 
what format is this and how should I analyze it?"

# For a pcap
tcpdump -r capture.pcap -A > traffic.txt
claude "analyze this network capture, find anything interesting — 
credentials, flags, unusual protocols"
```

---

### Pwn Challenge

```bash
# Gather binary intel
file challenge
checksec challenge
strings challenge | grep -E 'flag|win|shell|system'
objdump -d challenge | grep -A5 "win\|shell"

# Paste to AI
claude "binary: 64-bit ELF, no PIE, no canary, NX enabled.
has a win() function at 0x401234. buffer overflow at offset 72.
write a pwntools script to exploit this locally and remotely"

# Run the generated script, iterate on errors
python3 exploit.py
```

---

## Recon Automation Pipeline

Combine tools into a pipeline that feeds AI at the end:

```bash
#!/bin/bash
TARGET=$1
OUTPUT_DIR="recon_$TARGET"
mkdir -p $OUTPUT_DIR

echo "[*] Port scan..."
nmap -sV -p- --min-rate 5000 $TARGET -oN $OUTPUT_DIR/ports.txt

echo "[*] Web check..."
curl -sI http://$TARGET > $OUTPUT_DIR/http_headers.txt
curl -s http://$TARGET/robots.txt > $OUTPUT_DIR/robots.txt 2>/dev/null

echo "[*] Dir fuzz..."
ffuf -u http://$TARGET/FUZZ \
     -w /usr/share/wordlists/dirb/common.txt \
     -o $OUTPUT_DIR/dirs.json -of json -s

echo "[*] Sending to AI for analysis..."
cat $OUTPUT_DIR/*.txt $OUTPUT_DIR/*.json | \
  claude "summarize attack surface, list top 5 things to investigate"
```

Run it once, get an AI-generated prioritized attack plan.

---

## Building a Security Tool with AI Assistance

For hackathons or club projects, the workflow that works:

```
1. Define exactly what the tool does in one sentence
2. Ask AI to outline the architecture (what modules, what data flow)
3. Have AI generate the skeleton / boilerplate
4. Fill in domain-specific logic yourself (AI gets this wrong most often)
5. Have AI write tests and a README
6. Code review with AI before presenting
```

**Example:** "Build a tool that takes an nmap XML output file and generates a prioritized list of attack vectors."

```bash
# Step 1: Generate the skeleton
claude "build a Python CLI tool that:
- takes an nmap XML file as argument
- parses all open ports and service versions
- for each service, lists known attack vectors
- outputs a markdown report sorted by severity
use argparse, lxml, and requests"

# Step 2: Review what it produced
# Step 3: Add the actual vulnerability data source (NVD API, your own lookup table, etc.)
# Step 4: Test it on a real scan
```

---

## Hardening and Blue Team Workflows

AI is useful on the defense side too.

**Reviewing a system for misconfigurations:**

```bash
# Collect system state
sudo -l > sudo_config.txt
find / -perm -4000 2>/dev/null > suid_bins.txt
crontab -l > crons.txt
cat /etc/sudoers >> sudo_config.txt
ss -tulnp > open_ports.txt

# Ask for a hardening review
cat *.txt | claude "review this Linux system configuration for security issues.
list findings by severity. suggest specific fixes."
```

**Reviewing firewall rules:**

```bash
iptables -L -n -v > firewall_rules.txt
claude "review these iptables rules for gaps, overly permissive rules, 
and missing protections. suggest improvements."
```

**Log analysis:**

```bash
tail -n 500 /var/log/auth.log | \
  claude "analyze this auth log for suspicious activity — 
  brute force attempts, unusual users, privilege escalation, lateral movement"
```

---

> [!info] How the Club Uses This
> TODO: Add which of these workflows the club uses in CCDC prep, weekly demos, and CTF competitions. Note any custom scripts or configurations the team has built.

---

**References**

- [Claude Code docs](https://docs.anthropic.com/en/docs/claude-code)
- [LangChain for chaining AI steps](https://www.langchain.com/)
- [CAI source for agent workflow reference](https://github.com/aliasrobotics/CAI)
