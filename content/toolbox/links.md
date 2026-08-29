+++
title = "Links"
weight = 1
description = "Curated external tools, platforms, and references, grouped by what you are trying to do."
icon = "fa-solid fa-link"
+++

A link with no context is useless — you don't know when to click it. Every
entry below says what the thing is and when to reach for it.

Everything here is a public tool or learning platform. Use it against your
lab VM, a CTF box, or anything you are authorized to test — never against a
target you do not own or have written permission to touch.

## Comprehensive Guide

- **[CyberSecurity — Berkanktk](https://github.com/Berkanktk/CyberSecurity?tab=readme-ov-file#links)** — a huge, actively maintained security link list covering nearly everything on this page and more. Start here to go broad before you go deep.

## Practice Platforms

- **[TryHackMe](https://tryhackme.com)** — guided rooms with a walkthrough built in. Best first stop if you are new.
- **[Hack The Box](https://www.hackthebox.com)** — boxes with no hand-holding. Go here once TryHackMe stops feeling hard.
- **[OverTheWire](https://overthewire.org)** — wargames over SSH, starting with Bandit. The best place to get comfortable in a Linux terminal.
- **[picoCTF](https://picoctf.org)** — beginner CTF challenges, always open, not just during the yearly competition.
- **[Root-Me](https://www.root-me.org)** — hundreds of self-contained challenges. Good for drilling one category at a time.
- **[VulnHub](https://www.vulnhub.com)** — downloadable vulnerable VMs you run yourself, no time limit, no internet needed.
- **[PortSwigger Web Security Academy](https://portswigger.net/web-security)** — free, structured web app labs, one vulnerability class at a time. The best single resource for web security.
- **[pwn.college](https://pwn.college)** — a full binary exploitation curriculum with an in-browser environment. Go here once ready for pwn beyond basics.
- **[CryptoHack](https://cryptohack.org)** — cryptography challenges that teach the math by making you break it.
- **[crackmes.one](https://crackmes.one)** — reverse-engineering challenges ranked by difficulty, for practicing on small disposable binaries.

## Learning Platforms & Courses

- **[SANS](https://www.sans.org)** — the industry-standard training org. Expensive, but the material is real. Watch for their free webcasts.
- **[Cybrary](https://www.cybrary.it)** — free and paid courses across most security domains.
- **[Professor Messer](https://www.professormesser.com)** — free video courses for Security+ and Network+. Start here before paying for anything.
- **[Cisco Networking Academy](https://www.netacad.com)** — free networking fundamentals, useful before Security+ if ports and subnets still feel shaky.
- **[Antisyphon Training](https://www.antisyphontraining.com)** — pay-what-you-can live training from working practitioners, red and blue both.

## Reference & Cheat Sheets

- **[OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org)** — the correct answer to "how do I fix this web vulnerability," from the people who catalog them.
- **[PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings)** — a huge payload and bypass-technique repo, organized by vulnerability class.
- **[GTFOBins](https://gtfobins.github.io)** — Unix binaries abusable for shell breakout or privilege escalation. Check this the moment `sudo -l` shows something unexpected.
- **[LOLBAS](https://lolbas-project.github.io)** — the Windows equivalent of GTFOBins: built-in binaries abusable for the same purpose.
- **[CyberChef](https://gchq.github.io/CyberChef/)** — a drag-and-drop tool for encoding, decoding, and transforming data. Try this before scripting a one-off decode.
- **[Explainshell](https://explainshell.com)** — paste any shell command and it breaks down every flag.
- **[MITRE CVE](https://cve.org)** — the canonical record for any vulnerability. Start here, not a random blog.
- **[NVD](https://nvd.nist.gov)** — CVEs with severity scoring layered on top. Use once you've found the CVE and need to know how bad it is.
- **[Exploit-DB](https://www.exploit-db.com)** — a searchable public exploit archive, mirrored locally by the `searchsploit` CLI tool.

## Tooling — Recon & Web

- **[Nmap](https://nmap.org)** — the port scanner. Everyone's first move against a target. Learn its flags properly.
- **[Shodan](https://www.shodan.io)** — a search engine for devices exposed to the internet.
- **[theHarvester](https://github.com/laramies/theHarvester)** — gathers emails, subdomains, and names for a target domain from public sources. Standard first OSINT step.
- **[Burp Suite](https://portswigger.net/burp)** — the standard web traffic interception tool. Free Community edition covers most of what you need to learn.
- **[OWASP ZAP](https://www.zaproxy.org)** — a free, open-source alternative to Burp with a built-in automated scanner.
- **[sqlmap](https://sqlmap.org)** — automates finding and exploiting SQL injection. Use it to confirm and extract, not to find every bug for you.
- **[ffuf](https://github.com/ffuf/ffuf)** — a fast web fuzzer for hidden directories, files, and parameters.
- **[gobuster](https://github.com/OJ/gobuster)** — another fast directory/DNS brute-forcer, similar job to ffuf.

## Tooling — Binary & Reverse Engineering

- **[Ghidra](https://ghidra-sre.org)** — the NSA's free disassembler and decompiler. The standard starting point — no license, no excuse.
- **[IDA Free](https://hex-rays.com/ida-free/)** — the free tier of the other major disassembler. Weaker decompiler, still worth knowing.
- **[radare2](https://rada.re)** — a terminal-first reverse engineering framework. Steep curve, fast once it clicks.
- **[pwntools](https://github.com/Gallopsled/pwntools)** — a Python library for writing exploits: process interaction, packing, ROP helpers.
- **[pwndbg](https://github.com/pwndbg/pwndbg)** — a GDB plugin with far better memory, pointer, and heap views than stock GDB.

## Tooling — Forensics & Defense

- **[Wireshark](https://www.wireshark.org)** — packet capture and analysis with a window and color-coded protocols, the easier way to see a handshake.
- **[Volatility](https://volatilityfoundation.org)** — the standard framework for memory forensics: processes, connections, injected code from a RAM dump.
- **[Autopsy](https://www.autopsy.com)** — a free disk forensics platform: file recovery, timelines, keyword search.
- **[Zeek](https://zeek.org)** — turns raw network traffic into structured logs instead of a wall of packets. Used in production SOCs.
- **[Suricata](https://suricata.io)** — an open-source intrusion detection and prevention engine. Pair with Zeek for a full picture.
- **[osquery](https://osquery.io)** — query a live system's state — processes, files, connections — with SQL.
- **[Sysmon](https://learn.microsoft.com/sysinternals/downloads/sysmon)** — a Sysinternals tool logging detailed process, network, and file activity on Windows. Backbone of most Windows endpoint detection.

## Windows & Active Directory

AD runs most corporate networks. Practicing only on Linux boxes means missing half the job.

- **[Impacket](https://github.com/fortra/impacket)** — a Python toolset for working with Windows network protocols directly. Underpins most AD attack tooling.
- **[Mimikatz](https://github.com/gentilkiwi/mimikatz)** — extracts credentials and tickets from Windows memory. Know what it does and how to detect it.
- **[NetExec](https://github.com/Pennyw0rth/NetExec)** — a network protocol swiss-army-knife for AD: auth testing, execution, enumeration, all in one tool. Successor to CrackMapExec.
- **[Active Directory Domain Services overview — Microsoft Learn](https://learn.microsoft.com/windows-server/identity/ad-ds/get-started/virtual-dc/active-directory-domain-services-overview)** — read this before you attack AD. You can't break what you don't understand.
- **[ADSecurity.org](https://adsecurity.org)** — Sean Metcalf's blog, dense and specific to AD attack and defense. Nothing else free covers AD internals this well.

## Blue Team / Defense Resources

- **[MITRE ATT&CK](https://attack.mitre.org)** — the standard taxonomy of attacker tactics and techniques. Most detection and reporting work assumes you already think in these terms.
- **[MITRE D3FEND](https://d3fend.mitre.org)** — ATT&CK's defensive counterpart. Maps a detection or control back to the technique it addresses.
- **[Sigma](https://github.com/SigmaHQ/sigma)** — a shareable detection-rule format that converts to whatever SIEM you actually run.
- **[CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks)** — free, detailed hardening guides per OS and software. Check these when told to "harden this box."
- **[NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)** — the framework most US orgs structure their security program around.
- **[The DFIR Report](https://thedfirreport.com)** — detailed writeups of real intrusions, start to finish. See what an actual incident looks like, not the CTF version.

## Cryptography

- **[CryptoHack](https://cryptohack.org)** — see Practice Platforms above. Still the best starting point if crypto is your gap.
- **[dCode](https://www.dcode.fr)** — a huge collection of classical cipher solvers. Use to identify or break a cipher fast; read up separately on how it actually works.
- **[RsaCtfTool](https://github.com/RsaCtfTool/RsaCtfTool)** — automates common RSA attacks against CTF-style challenges. Try before hand-rolling your own.
- **[CyberChef](https://gchq.github.io/CyberChef/)** — see Reference above. Also handles most encoding-layer crypto (base64-in-hex-in-rot13) with no code.

## Staying Current

Pick a couple of these and actually check them — don't just bookmark and forget.

- **[Krebs on Security](https://krebsonsecurity.com)** — Brian Krebs' investigative reporting on breaches and cybercrime. Slower, deeper than most security news.
- **[The Hacker News](https://thehackernews.com)** — daily security news, broad coverage, good for a fast scan.
- **[r/netsec](https://www.reddit.com/r/netsec)** — a curated subreddit for technical writeups and tool releases, less noise than most security subs.
- **[CTFtime](https://ctftime.org)** — the CTF calendar and ranking site, and an archive of writeups after events end. Check it to find a CTF to enter this weekend.
- **[SecLists.org](https://seclists.org)** — archives of major security mailing lists, including Full Disclosure. Raw vulnerability disclosures as they happen.

## Career & Certifications

- **[CompTIA Security+](https://www.comptia.org/certifications/security)** — the standard entry-level cert. Vendor-neutral, widely recognized by HR filters.
- **[Offensive Security (OSCP)](https://www.offsec.com)** — a certification that tests actual hands-on exploitation, not multiple choice. Respected because it's hard.
- **[(ISC)² CISSP](https://www.isc2.org)** — a management-and-breadth cert for more senior roles. Not your first cert as a student.
- **[GIAC](https://www.giac.org)** — certifications tied to SANS courses, deep and specific per topic. Expensive; the material is excellent.

## FAU / Club

- **[Club Wiki Repo](https://github.com/dxcently/fau-cyber-security-club-wiki)** — the source for this site. Found a broken link or a gap? Open a pull request.
- **[Discord](http://discord.gg/2Yun8WAUuy)** — where the club actually talks day to day. Join this before anything else on this page.
- **[Owl Central](https://fau.campuslabs.com/engage/organization/cybersecurity)** — the official FAU org page: meeting times, events, and how to officially join.
