+++
title = "CTF Categories"
weight = 2
+++

CTF challenges are grouped into categories. Each one requires different knowledge and tools. Pick one to start with and go deep.

---

## Web

Web challenges involve attacking a website or web application. SQL injection, cross-site scripting, broken authentication, file inclusion, insecure deserialization — all of it shows up here.

**Start with:** [OWASP Juice Shop](https://owasp.org/www-project-juice-shop/) — a deliberately vulnerable web app you can run locally.

**Essential tools:** Burp Suite, browser DevTools, curl, sqlmap (for learning, not as a crutch)

**Learn:** [PortSwigger Web Security Academy](https://portswigger.net/web-security) — free, excellent, structured.

---

## Pwn (Binary Exploitation)

You exploit memory vulnerabilities in compiled programs — buffer overflows, format string bugs, heap exploitation, return-oriented programming.

This is the deepest and most technically demanding category. Start here only if you are comfortable with C and want to understand how programs work at the memory level.

**Start with:** [pwn.college](https://pwn.college/) — structured binary exploitation curriculum.

**Essential tools:** GDB with pwndbg/peda, pwntools, Ghidra or IDA Free

---

## Cryptography

You break or reverse cryptographic operations. Weak implementations of RSA, AES, XOR ciphers, hash collisions, padding oracles — real math applied to real systems.

You do not need to be a mathematician. You need to recognize patterns and know which attacks apply to which schemes.

**Start with:** [Cryptopals](https://cryptopals.com/) — practical crypto challenges from basic to advanced.

**Essential tools:** Python with `pycryptodome`, SageMath for math-heavy challenges

---

## Forensics

You examine artifacts — disk images, memory dumps, network captures, steganographic files — and reconstruct what happened or extract hidden data.

Strong overlap with real incident response work.

**Start with:** TryHackMe's forensics rooms, PicoCTF forensics challenges.

**Essential tools:** Wireshark, Volatility (memory), Autopsy/FTK Imager (disk), binwalk, exiftool, steghide

---

## Reverse Engineering

You take a compiled binary and figure out what it does. No source code. Read assembly, understand control flow, identify algorithms.

Closely related to pwn. Necessary for malware analysis.

**Start with:** [Reverse Engineering for Beginners (free book)](https://beginners.re/)

**Essential tools:** Ghidra, IDA Free, Binary Ninja (paid), strings, ltrace, strace

---

## OSINT

Open-Source Intelligence. You find information using only publicly available sources — social media, DNS records, WHOIS, image metadata, archived pages.

Requires creativity and attention to detail more than technical depth.

**Start with:** [Trace Labs](https://www.tracelabs.org/) for real OSINT practice. [OSINT Framework](https://osintframework.com/) for tools.

---

## Misc / Steganography

Catch-all for things that don't fit elsewhere. Hidden data in images, audio files, video, QR codes, obscure encoding schemes.

These often require recognizing the format and knowing which tool to throw at it.

**Essential tools:** CyberChef, steghide, stegsolve, zsteg, exiftool

---

{{< mermaid >}}
flowchart LR
    A([You]) --> B{What interests you?}
    B --> C[Web Apps] --> D[Web category]
    B --> E[How programs work] --> F[Pwn / Rev]
    B --> G[Math & algorithms] --> H[Crypto]
    B --> I[Investigations & files] --> J[Forensics / OSINT]
{{< /mermaid >}}

---

> [!info] How the Club Uses This
> TODO: Add which categories the club focuses on in competitions, which members specialize in which areas, and any category-specific study sessions or resources.

---

**References**

- [CTF101 field guide](https://ctf101.org/)
- [PicoCTF](https://picoctf.org/) — practice across all categories
- [PortSwigger Web Security Academy](https://portswigger.net/web-security)
- [pwn.college](https://pwn.college/)
- [Cryptopals](https://cryptopals.com/)
