+++
title = "What AI Can Actually Do"
weight = 1
+++

Skip the hype. Here is what AI has demonstrably done in security competitions and research, with numbers.

---

## CTF Benchmarks

### picoCTF-level challenges — effectively solved

**Palisade Research (Dec 2024):** A plain ReAct-based agent with plan-and-solve prompting hit **95% overall** on the InterCode-CTF benchmark — 100% on General Skills, Binary Exploitation, and Web Exploitation. Most challenges were solved in 1–2 turns. The benchmark is now considered saturated at this difficulty level.

Paper: [arXiv:2412.02776](https://arxiv.org/abs/2412.02776)

**HackSynth (Dec 2024):** Dual-module Planner + Summarizer architecture tested on 200 challenges across picoCTF and OverTheWire. Best results with GPT-4o.

Paper: [arXiv:2412.01778](https://arxiv.org/abs/2412.01778) | Code: [github.com/aielte-research/HackSynth](https://github.com/aielte-research/HackSynth)

**CTFAgent (2025):** Plan-and-execute agent with a stateful task tree. Tested with GPT-4o, Gemini 2.5 Pro, and DeepSeek-V3 against PicoCTF. In automated mode: **outperformed 88% of human teams.** With human-in-the-loop: ~94%.

---

## Live Competition Wins

### CAI by Alias Robotics

CAI (Cybersecurity AI) is an open-source framework backed by a security-specialized 500B-parameter model. 2025 competition results:

- **Neurogrid CTF:** Rank 1. 41/45 flags captured. **$50,000 prize.**
- **Dragos OT/ICS CTF 2025:** Reached Rank 1 in hours 7–8. Averaged 1,846 points/hour vs. top-5 humans averaging 1,347 pts/hr — 37% faster. Completed 32/34 challenges before voluntarily pausing at hour 24 due to competition rules.
- **Hack The Box "AI vs Humans" (2025):** Top-performing AI team across 8,129 competing teams.

Framework: [github.com/aliasrobotics/CAI](https://github.com/aliasrobotics/CAI) | Case study: [aliasrobotics.com](https://aliasrobotics.com/case-study-dragos-CTF.php)

---

## Real-World Vulnerability Exploitation

### UIUC — GPT-4 on One-Day CVEs (Apr 2024)

Richard Fang et al. at University of Illinois gave GPT-4 a set of 15 critical one-day CVEs with their descriptions. GPT-4 autonomously exploited **87% of them.** Every other model tested — GPT-3.5, open-source LLMs, Metasploit, ZAP — scored 0%.

Without the CVE description: GPT-4 dropped to 7%. The description is the key input.

Paper: [arXiv:2404.08144](https://arxiv.org/abs/2404.08144)

### UIUC — Teams of LLM Agents on Zero-Days (Jun 2024)

Follow-up from the same team. Hierarchical Planner + Task-Specific Agents (HPTSA) tested on **14 real zero-day vulnerabilities**. A team of agents outperformed a single agent by **up to 4.3×.**

Paper: [arXiv:2406.01637](https://arxiv.org/abs/2406.01637) | Code: [github.com/uiuc-kang-lab/HPTSA](https://github.com/uiuc-kang-lab/HPTSA)

---

## Bug Bounty

### XBOW — #1 on HackerOne US Leaderboard (2025)

XBOW is an autonomous pen-testing AI. It reached **#1 on HackerOne's US leaderboard**, submitting ~1,060 vulnerability reports with near-zero false positives. All findings were generated autonomously; a human reviewed before submission.

Blog: [xbow.com/blog/top-1-how-xbow-did-it](https://xbow.com/blog/top-1-how-xbow-did-it)

---

## What This Means for You

Beginner and intermediate CTF challenges are now solvable by a well-prompted agent with tool access. That does not make CTFs pointless — it raises the floor. You need to understand what the AI is doing, catch when it is wrong, and handle the edge cases it cannot.

The humans who will be competitive are the ones who understand the techniques well enough to direct and verify AI output — not the ones who hand everything to the model and copy-paste.

> [!tip] The New Skill
> Knowing how to write a good prompt for a security task, pipe tool output into a model, and evaluate the response critically — that is a real skill worth developing now.

---

**References**

- [Palisade Research — Hacking CTFs with Plain Agents](https://palisaderesearch.org/blog/intercode-ctf)
- [NYU CTF Bench](https://nyu-llm-ctf.github.io/) — [arXiv:2406.05590](https://arxiv.org/abs/2406.05590)
- [CSAW Agentic Automated CTF](https://www.csaw.io/agentic-automated-ctf)
- [HTB AI vs Humans results](https://www.hackthebox.com/blog/ai-vs-human-ctf-hack-the-box-results)
