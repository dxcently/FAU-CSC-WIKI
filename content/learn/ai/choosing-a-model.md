+++
title = "Choosing an AI Model"
weight = 6
description = "Selection criteria for picking an AI model for security work — not a product comparison."
icon = "fa-solid fa-robot"
+++

AI is not a shortcut. It is a force multiplier, and only if you know what you
are asking it for. This page is not a list of which model is "best" — that
list is out of date by the time you read it. These are the criteria to weigh
when picking one for a security task.

---

## The Criteria That Matter

### Reasoning Depth

Some tasks are one-shot: decode this string, explain this error. Others need
the model to hold a multi-step plan in its head — chaining a foothold into
privilege escalation into lateral movement, or working through a non-obvious
crypto attack. For the second kind, use the provider's strongest reasoning
tier. For the first, a fast cheap model is a good default.

### Context Window

Some inputs are just big: a full binary disassembly, a large pcap, an entire
codebase you are auditing. A small context window forces you to chop the
input up and lose the connections between pieces — exactly where multi-stage
attacks hide. When your input is large, window size matters more than raw
reasoning quality.

### Code Quality

If you are asking for exploit scripts, parsers, or tooling, the model's
actual code output is what you are paying for. This varies by model and
changes fast — check recent, task-specific comparisons rather than trusting
a general reputation.

### Cost

Cost compounds. A single query is cheap regardless of model. An agent looping
hundreds of times against a target, or a pipeline processing thousands of log
lines, is not. Cheaper models are often fine for high-volume, low-difficulty
steps — summarizing tool output, classifying log lines — saving the expensive
model for the step that actually needs judgment.

### Local vs. Cloud

Running a model locally (tools like Ollama make this close to one command)
means nothing you send it leaves your machine. That matters when the target,
data, or environment is sensitive — a real engagement, a restricted network,
anything under an NDA. The tradeoff: local models you can run on a laptop or
single GPU are meaningfully weaker than the largest cloud models. Use local
when privacy is non-negotiable, cloud otherwise.

---

## When Each Axis Wins

| Situation | What to prioritize |
|---|---|
| Multi-step exploit chain, novel vulnerability | Reasoning depth |
| Full disassembly, large pcap, whole codebase | Context window |
| Generating an exploit script or a tool | Code quality |
| High-volume automation (log triage, bulk scanning output) | Cost |
| Sensitive target, restricted network, NDA | Local |

No model wins on every axis. Pick per task, not once for everything.

---

## The Actual Skill

The durable skill here is not prompting. It is **directing and verifying**
model output — knowing what to ask for, and knowing enough to catch it when
the answer is confidently wrong. A model will hand you a plausible-looking
exploit that does not work, or an analysis that misses the one detail that
mattered. If you cannot tell the difference, the model is not helping you,
it is just moving the failure later.

Copy-pasting output you do not understand is not using AI. It is gambling
with extra steps.
