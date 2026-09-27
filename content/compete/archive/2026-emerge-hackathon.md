+++
title = "2026 eMERGE Hackathon — Project Scalpel"
weight = 3
description = "The club's eMERGE hackathon entry, Project Scalpel — a tiered AI Cowrie honeypot that makes a Raspberry Pi pass as a real Linux server."
icon = "fa-solid fa-lightbulb"
+++

---

**Project SCALPEL** was the club's entry at eMERGE 2026 (Team 07, Miami Beach):
a high-interaction SSH honeypot built on [Cowrie](https://docs.cowrie.org/)
that makes a Raspberry Pi look like a real, lived-in Linux server to an
attacker — while spending as little compute as possible doing it.

The hackathon's red team SSHed into every team's Pi and probed it. Each probe
was scored on two axes: did the answer look real, and did the Pi answer it
itself instead of calling out to the cloud.

## The problem

A honeypot fails the moment an attacker notices it's fake. There are three ways
that happens, and stock Cowrie has all three:

| Failure mode | How SCALPEL defends |
|---|---|
| **Inconsistent responses** — output doesn't match a real system | Answers captured from a clean ground-truth Pi, replayed verbatim |
| **Latency anomalies** — a slow answer gives away a cloud call | Cloud only on commands a real Pi is naturally slow on |
| **Implausible filesystem** — too empty, too generic | A decoy filesystem populated from a real Pi, plus per-session state |

## Scoring shaped the design

```
realism    = 100 × (probes − demerits)    / probes
efficiency = 100 × (probes − escalations) / probes
final      = 0.4 × realism + 0.4 × efficiency + 0.2 × presentation
```

Efficiency was the first tiebreaker. A wrong-but-local answer and a
right-but-cloud answer cost the same points, but only the cloud one hurts the
tiebreaker — so the rule became **local first, even if imperfect**. A Cowrie
crash, worth about ten demerits, was the one thing worse than either; a
watchdog kept it alive.

## One router, no fall-through

Every command an attacker types is classified into exactly **one** dispatch
level. There's no slow chain of "try this, then that" — if the chosen level
fails, exactly one backup is tried, then a safe stub.

{{< mermaid >}}
flowchart TD
    A([Attacker over SSH]) --> B[Cowrie]
    B --> C{dispatch.py<br/>classify → one level}
    C --> D[LOCAL_CACHE<br/>static table · ~0.1 ms]
    C --> E[LOCAL_RUNTIME<br/>session state · 1–5 ms]
    C --> F[EDGE_INFER<br/>Ollama on the Pi · 1–3 s]
    C --> G[CLOUD_SYNC<br/>AWS Bedrock · 3–8 s]
    C --> H[FALLBACK<br/>inline stub · instant]
{{< /mermaid >}}

| Level | Handles | Backed by |
|---|---|---|
| `LOCAL_CACHE` | Invariant output — `uname`, `/etc/os-release`, config reads, version strings | Static table, ~185 entries |
| `LOCAL_RUNTIME` | Stateful commands — `uptime`, `cd`/`pwd`, `ps`, files the attacker created | Generated from session state |
| `EDGE_INFER` | Unpredictable but cheap-to-fake commands | `qwen2.5:1.5b` via Ollama, on the Pi |
| `CLOUD_SYNC` | Complex or rare recon that needs a stronger model | Claude Haiku 4.5 on AWS Bedrock |
| `FALLBACK` | Anything that errors — the shell never crashes | Inline stub |

### Why cloud only on slow commands

Every cloud call adds latency an attacker can measure. So escalation is
limited to commands where a real Pi is *already* slow — `find`, `apt`,
`dpkg`, `journalctl`, `tar`, `du`. A 1.5 s `ls` is a dead giveaway; a 1.5 s
`find / -name foo` is normal.

### Why `qwen2.5:1.5b`

The team benchmarked four models on Pi 5 hardware with the real prompt. The
budget for a local answer was about 800 ms before timing analysis flags it.

| Model | Avg latency | Result |
|---|---|---|
| qwen2.5:0.5b | 290 ms | Backup |
| **qwen2.5:1.5b** | **480 ms** | **Chosen** |
| phi3:mini | 1,100 ms | Too slow |
| gemma2:2b | 980 ms | Too slow |

Ollama unloads an idle model after five minutes, and the reload takes about
35 seconds — a guaranteed finding. `keep_alive: "24h"` plus a periodic warmup
kept it resident.

## Staying in character

The Pi presents as `pi-sensor-gateway` — Debian 13 (trixie), aarch64, a
distributed sensor node. The stateful layer keeps that identity consistent
under probing: `uptime` advances on the wall clock, `cd /tmp; pwd` persists,
`touch x; ls` shows the new file, and `ps` includes the attacker's own shell.

The agent's own modules have deliberately boring names — `telemetry_cache.py`,
`node_runtime.py`, `edge_inference.py`, `upstream_sync.py` — so an attacker who
enumerates the real OS sees sensor software, not honeypot tooling.

## Testing it before the red team did

The team built its own red-team harness to score itself against ground truth
without needing Ollama or AWS: 138 probes across attack stages — pre-auth,
fingerprinting, post-login, lateral movement, exfiltration, crash attempts,
injection, and latency distribution.

```bash
cd honeypot
python -m pytest tests/red_team -q
```

## Materials

- **Writeup and code:** [ethanrxla/Cowrie_Honeypot_IAE_Emerge_Hackathon](https://github.com/ethanrxla/Cowrie_Honeypot_IAE_Emerge_Hackathon) — the consolidated repo, with architecture notes, playbook, and test harness
- **Slide deck:** [PDF](https://github.com/ethanrxla/Cowrie_Honeypot_IAE_Emerge_Hackathon/blob/main/presentation/Project-SCALPEL.pdf) · [PPTX](https://github.com/ethanrxla/Cowrie_Honeypot_IAE_Emerge_Hackathon/blob/main/presentation/Project-SCALPEL.pptx)

### Earlier working repos

- https://github.com/RohanDS2024/Emirge
- https://github.com/caol777/Cowrie-honeypot
