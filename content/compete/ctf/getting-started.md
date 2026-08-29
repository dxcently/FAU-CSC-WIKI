+++
title = "Getting Started with CTFs"
weight = 1
description = "How to pick a CTF platform, approach a challenge, and use AI without skipping the thinking."
icon = "fa-solid fa-play"
+++

A CTF (Capture the Flag) is a security competition where you solve challenges to find a hidden string called a flag. Flags are usually formatted like `flag{some_text_here}`.

They are the best way to apply what you have learned in a structured, consequence-free environment.

---

## Formats

**Jeopardy-style:** A set of challenges across different categories. Solve a challenge, get a flag, earn points. You pick what to work on. Most beginner CTFs use this format.

**Attack/Defend:** Two or more teams each run identical vulnerable systems. You attack the other teams' services while defending your own. CCDC uses this format.

Start with jeopardy. Attack/defend comes later.

---

## Where to Start

| Platform | Why |
|---|---|
| [PicoCTF](https://picoctf.org/) | Best starting point. Beginner-friendly, excellent progression. |
| [TryHackMe](https://tryhackme.com/) | Guided rooms with walkthroughs. Good for learning specific topics. |
| [HackTheBox](https://www.hackthebox.com/) | Harder. Good for intermediate to advanced. |
| [CTFtime.org](https://ctftime.org/) | Calendar of upcoming CTF events worldwide. |
| [OverTheWire](https://overthewire.org/wargames/) | Linux and exploitation wargames. Bandit is the entry point. |

Start on PicoCTF or TryHackMe. Do not skip to HackTheBox and wonder why it is hard.

---

## How to Approach a Challenge

1. **Read the description carefully.** The intended vulnerability is usually hinted at.
2. **Enumerate.** What do you have? A file? A web service? A binary? Network access?
3. **Identify the category.** Is this web? Crypto? Forensics? (See [Categories](./categories).)
4. **Try the obvious thing first.** Beginners often over-think. Check the simple cases.
5. **Search.** Look up the technology, the error message, the behavior. CTF knowledge is cumulative.
6. **Ask for a nudge, not an answer.** Getting pointed in the right direction is fine. Getting the solution handed to you teaches you nothing.

---

## Writing Writeups

After you solve a challenge, write it down. Even a rough Markdown file with what you tried and what worked.

- It solidifies your understanding.
- It helps your teammates who got stuck.
- It becomes a reference when you see the same technique again.

Good writeups explain *why* something worked, not just *what* commands you ran.

---

## Tools You Will Reach For

These are not category-specific — they come up everywhere:

- **CyberChef** — decode, encode, transform data with a GUI. [Try it.](https://gchq.github.io/CyberChef/)
- **strings** — extract printable strings from a binary file
- **file** — identify what type of file something is
- **xxd** / **hexdump** — view raw bytes of a file
- **Burp Suite** — intercept and modify HTTP traffic

---

## Using AI in CTFs

AI is a legitimate tool in CTF work. Knowing how to use it well is a skill in itself.

**Where it genuinely helps:**

- **Identifying encodings:** Paste an unknown string. "What encoding is this and how do I decode it?" AI recognizes base64, hex, rot13, URL encoding, JWT, and many others instantly.
- **Explaining vulnerability classes:** "What is a padding oracle attack and how does it work against AES-CBC?" Better than reading a dry Wikipedia article.
- **Scripting:** Tell it the protocol, the port, and what the service responds with. Ask for a Python socket script to interact with it. Use that as the starting frame.
- **Stuck on a hint:** Paste the challenge description and say "I've tried X and Y, what categories or techniques should I look into?" It will not give you the flag — it will point you in a direction.
- **Reading assembly:** Paste a short disassembled function and ask what it does. Speeds up reverse engineering significantly.
- **CyberChef recipes:** Describe the transformation you need. AI will write the CyberChef recipe.

**Where it fails in CTFs:**

- Custom or novel challenges: AI has not seen them and will hallucinate solutions.
- Specific offsets, addresses, or binary internals: it cannot run the binary.
- The actual solve: it can outline an approach, but you have to execute it.

Use AI to accelerate learning and eliminate grunt work — not to skip the thinking.

---

> [!info] How the Club Uses This
> TODO: Add which CTFs the club participates in, how teams are formed, where writeups are posted, and any club-specific tooling or setup.

---

**References**

- [PicoCTF](https://picoctf.org/)
- [CTFtime.org](https://ctftime.org/)
- [CTF101 — beginner field guide](https://ctf101.org/)
- [LiveOverflow YouTube](https://www.youtube.com/@LiveOverflow) — CTF writeup videos
