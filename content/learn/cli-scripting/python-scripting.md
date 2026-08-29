+++
title = "Python for Security"
weight = 2
description = "Enough Python to read and write scripts for security work, without a full CS course."
icon = "fa-brands fa-python"
+++

Python is the most common scripting language in security. It ships on most systems, has a massive library ecosystem, and you can go from idea to working script in minutes.

You do not need to learn Python comprehensively. Learn enough to read and write scripts.

---

## Basic Script Structure

```python
#!/usr/bin/env python3

import sys
import os

def main():
    if len(sys.argv) < 2:
        print("Usage: script.py <target>")
        sys.exit(1)

    target = sys.argv[1]
    print(f"Target: {target}")

if __name__ == "__main__":
    main()
```

Run it:

```bash
python3 script.py 192.168.1.1
```

---

## Reading Files

```python
# Read a file line by line
with open("wordlist.txt", "r") as f:
    for line in f:
        word = line.strip()
        print(word)

# Read all at once
with open("data.txt") as f:
    content = f.read()
```

---

## Making HTTP Requests

Install `requests` if not available:

```bash
pip3 install requests
```

```python
import requests

# Simple GET
r = requests.get("https://example.com")
print(r.status_code)
print(r.text[:500])

# POST with data
r = requests.post("https://example.com/login", data={
    "username": "admin",
    "password": "password"
})

# With custom headers
headers = {"Authorization": "Bearer TOKEN"}
r = requests.get("https://api.example.com/users", headers=headers)
```

---

## Working with Sockets

```python
import socket

# Simple TCP connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.1.1", 80))
s.send(b"GET / HTTP/1.0\r\n\r\n")
response = s.recv(4096)
print(response.decode())
s.close()
```

Sockets are the foundation of network tools. Understanding this level matters for CTF challenges and writing custom exploits.

---

## Running System Commands

```python
import subprocess

# Run a command and get output
result = subprocess.run(["nmap", "-sV", "192.168.1.1"], 
                        capture_output=True, text=True)
print(result.stdout)
```

---

## Parsing Output

```python
import re

log = "Failed password for root from 192.168.1.5 port 22"

# Extract IP with regex
match = re.search(r'(\d+\.\d+\.\d+\.\d+)', log)
if match:
    print(f"IP: {match.group(1)}")
```

`re` (regex) is useful for pulling structured data out of messy text — log files, HTML, tool output.

---

## Useful Libraries

| Library | Use |
|---|---|
| `requests` | HTTP requests |
| `socket` | Raw TCP/UDP |
| `subprocess` | Run system commands |
| `re` | Regular expressions |
| `os`, `sys` | File system and system calls |
| `argparse` | Parse command-line arguments |
| `pwntools` | CTF exploitation (install separately) |
| `scapy` | Packet crafting and manipulation |

---

## In CTF Environments

Python is the primary CTF scripting language. Most exploit scripts, automation, and crypto challenges are solved in Python.

**Web challenge — brute forcing a login:**
```python
import requests

url = "http://target.htb/login"
with open("/usr/share/wordlists/rockyou.txt", "r", errors="ignore") as f:
    for password in f:
        password = password.strip()
        r = requests.post(url, data={"username": "admin", "password": password})
        if "Invalid" not in r.text:
            print(f"Password found: {password}")
            break
```

**Crypto challenge — XOR decryption:**
```python
ciphertext = bytes.fromhex("1a2b3c4d5e6f")
key = b"secret"

# XOR each byte with repeating key
plaintext = bytes(c ^ key[i % len(key)] for i, c in enumerate(ciphertext))
print(plaintext)
```

**Pwn challenge — interacting with a service:**
```python
from pwn import *

# Connect to remote service
conn = remote("target.htb", 4444)

# Receive banner
print(conn.recvuntil(b">"))

# Send payload
payload = b"A" * 64 + p64(0xdeadbeef)   # overflow + overwrite return addr
conn.sendline(payload)

conn.interactive()   # drop into interactive shell if exploit worked
```

**Forensics — extracting strings from a binary file:**
```python
import re

with open("challenge.bin", "rb") as f:
    data = f.read()

# Find all printable ASCII strings of length >= 6
strings = re.findall(rb'[ -~]{6,}', data)
for s in strings:
    print(s.decode())
```

**Parsing structured output:**
```python
import subprocess, json

result = subprocess.run(["nmap", "-oJ", "-", "192.168.1.1"],
                        capture_output=True, text=True)
# or parse XML, grep output, whatever the tool gives you
```

---

## Using AI

Python for CTFs has a tight feedback loop — AI fits well into it.

**Where it helps:**

- **Writing boilerplate fast:** Socket connections, HTTP sessions, file I/O — the setup is mechanical. Describe what you need and start from AI output.
- **Crypto math:** RSA, modular arithmetic, number theory. Describe the algorithm or paste the challenge parameters. AI knows standard attacks (small e, common modulus, Wiener's attack) and can sketch the approach.
- **pwntools patterns:** Constructing payloads, setting up ROP chains, dealing with buffering — the pwntools API is large. AI knows it.
- **Regex:** Same as Bash. Describe the pattern you want to extract, get a draft, tweak it.
- **Debugging:** Paste the traceback. AI is fast at spotting type errors, encoding issues, and off-by-one mistakes.

**Example prompt that works well:**
> "I have a CTF web challenge. The server is running at target.htb:8080. It takes a POST request to /api/login with JSON body `{username, password}`. I want to brute force the password using rockyou.txt. Write a Python script with requests, handle rate limiting with a 0.5s delay, and print any response that doesn't contain 'Invalid credentials'."

**Where it fails:**

- It does not know the target. You have to feed it the right context.
- Crypto attacks: it will sketch the right approach but get implementation details wrong. Verify the math.
- pwntools exploit scripts: the structure it produces is usually right, the offsets and addresses are always wrong — those come from your analysis.

---

> [!info] How the Club Uses This
> TODO: Add Python scripts the club has written for CTFs, competition automation, or tooling demos.

---

**References**

- [Python 3 documentation](https://docs.python.org/3/)
- [Automate the Boring Stuff (free)](https://automatetheboringstuff.com/)
- [pwntools documentation](https://docs.pwntools.com/)
- [scapy documentation](https://scapy.readthedocs.io/)
