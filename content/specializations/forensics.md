+++
title = "Forensics"
weight = 3
+++

Digital forensics is investigating what happened. You examine artifacts — memory dumps, disk images, network captures, logs — and reconstruct events or extract hidden data.

In the real world, this is what happens after a breach. In CTFs, it shows up as file analysis, steganography, and memory/network challenges.

---

## Branches

**Memory forensics:** Analyze a RAM dump. Find running processes, open network connections, encryption keys, credentials, injected code.

**Disk forensics:** Examine a disk image. Recover deleted files, examine file system metadata, find artifacts left by malware or an attacker.

**Network forensics:** Analyze packet captures. Reconstruct sessions, find transmitted data, identify malicious traffic patterns.

**Steganography:** Find data hidden inside files — images, audio, video. Often shows up in CTFs as a separate category.

---

## Core Skills

- **File identification** — knowing what type of file you are looking at, even when the extension lies
- **Hex analysis** — reading raw bytes to understand file structure
- **Timeline reconstruction** — ordering events using timestamps across different artifacts
- **Artifact knowledge** — knowing where data lives on Windows and Linux systems (registry, event logs, prefetch, browser history, etc.)

---

## Tools

| Tool | Purpose |
|---|---|
| [Volatility](https://www.volatilityfoundation.org/) | Memory analysis framework. Industry standard. |
| [Autopsy](https://www.autopsy.com/) | Disk forensics GUI built on Sleuth Kit |
| [The Sleuth Kit](https://www.sleuthkit.org/) | Command-line disk forensics tools |
| [Wireshark](https://www.wireshark.org/) | Network capture analysis |
| [binwalk](https://github.com/ReFirmLabs/binwalk) | Extract embedded files from firmware and images |
| [exiftool](https://exiftool.org/) | Read metadata from images and other files |
| [steghide](https://steghide.sourceforge.net/) | Hide/extract data in image and audio files |
| [zsteg](https://github.com/zed-0xff/zsteg) | Detect steganography in PNG and BMP files |
| [foremost / scalpel](https://github.com/korczis/foremost) | File carving — recover files from raw data |

---

## Getting Started

For memory forensics: download a memory sample from the [Volatility samples page](https://github.com/volatilityfoundation/volatility/wiki/Memory-Samples) and practice running plugins against it.

For disk forensics: [Digital Corpora](https://digitalcorpora.org/) has real disk images from training exercises.

For CTF forensics: PicoCTF has approachable forensics challenges. TryHackMe has dedicated forensics rooms.

---

## Real-World Context

Forensics analysts work in incident response, law enforcement, and corporate security. After an attacker is detected, forensics answers: what did they do, how did they get in, and what did they take?

The [SANS FOR508](https://www.sans.org/cyber-security-courses/advanced-incident-response-threat-hunting-training/) course is the industry standard for advanced forensics, though expensive. The free materials from SANS and their CTF events (DFIR CTFs) are good substitutes.

---

> [!info] How the Club Uses This
> TODO: Add forensics challenges the club has worked through, and any forensics-focused competition results or demos.

---

**References**

- [Volatility documentation](https://volatility3.readthedocs.io/)
- [SANS DFIR blog](https://www.sans.org/blog/digital-forensics/)
- [CTF101 — Forensics](https://ctf101.org/forensics/overview/)
- [Digital Corpora — forensics datasets](https://digitalcorpora.org/)
