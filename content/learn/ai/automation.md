+++
title = "Automating Security Work"
weight = 8
description = "How to wire a model into a repeatable pipeline for triage, summarizing, and first-pass review — and what never goes in the prompt."
icon = "fa-solid fa-wand-magic-sparkles"
+++

Running a model by hand, one prompt at a time, is fine for a one-off
question. Automation is different: you wire the model into a script that
runs the same way every time, on output you did not write and may not have
read yet. That raises the stakes. This page covers where that pays off,
the pattern to build it on, and the policy rules that apply the moment you
pipe real data into a model.

---

## Where Automation Actually Pays Off

Automation works when the task is repetitive, high-volume, and you can
check the result. It fails when you cannot verify the answer, or the task
needs facts the model does not have.

**Good fits:**

- **Triage.** Rank a pile of alerts or scan hits by severity. You still
  check the top of the list yourself.
- **Summarizing large output.** Logs, scan results, packet captures — data
  too long to read line by line, but small enough to skim once summarized.
- **First-pass code review.** Catch the obvious problems before a human
  reviews the code. It is a filter, not a replacement for review.
- **Throwaway parsing scripts.** A quick script that reshapes one file's
  format. Read the script before you run it — "throwaway" describes its
  lifespan, not your attention.
- **Drafting writeups from notes.** Turn rough notes into a readable draft.
  You still check every technical claim in it.

**Bad fits:**

- **Anything you cannot verify.** If you have no way to check the answer
  against ground truth, you cannot catch the model when it is wrong. It
  will state a wrong answer with the same confidence as a right one.
- **Anything that needs ground truth you do not have.** The model only
  knows what is in the prompt. Ask it a question about your network that
  you did not already answer for it, and it will guess.

---

## The Pipeline Pattern

Automation means treating the model as one stage in a pipeline, not a
source of answers. The pattern has four stages:

```
tool output -> model -> structured result -> your decision
```

- **Tool output.** Raw text from a scanner, a log file, a capture. You
  produced this yourself; you know where it came from.
- **Model.** One processing step. It has no memory of your target beyond
  what you put in the prompt this run.
- **Structured result.** A fixed-shape answer — see below — not a
  paragraph of prose.
- **Your decision.** The model does not act on its own conclusion. You
  read the result and decide what happens next.

A small example: a script that runs a scan, asks the model to prioritize
the findings, and prints them sorted by risk.

```python
import json
import subprocess

TARGET = "TARGET_IP"  # your lab VM, never a real host

def scan(target: str) -> str:
    result = subprocess.run(
        ["nmap", "-sV", target], capture_output=True, text=True
    )
    return result.stdout

def triage(scan_output: str) -> list[dict]:
    prompt = f"""Review this scan output. Return JSON only: a list of
objects with keys "port", "service", "risk" ("low", "medium", or "high"),
and "reason". No text outside the JSON.

{scan_output}"""
    response = chat([{"role": "user", "content": prompt}])
    return json.loads(response.text)  # raises if the model didn't comply

findings = triage(scan(TARGET))
for f in sorted(findings, key=lambda f: f["risk"]):
    print(f"[{f['risk']}] port {f['port']} ({f['service']}): {f['reason']}")
```

Nothing here runs an exploit or touches the target beyond the scan you
already chose to run. The model reads text and returns text. You still
decide what to do about port 8080 running something old.

---

## Structured Output

Free-form prose is for a human to read once. A pipeline needs something a
script can parse without a human re-reading it every run. That is why you
ask for JSON, or any fixed schema: a list of fields with known names and
known types, instead of a paragraph.

Asking for a schema does not guarantee you get one. Treat the model's
output like input from an untrusted source:

- Parse it. If it does not parse, that is a signal, not a crash you paper
  over with a retry loop that hides the problem.
- Check the required keys exist.
- Check the values are in the range you expect (`"risk"` is one of three
  strings, not one of three strings *or* a sentence explaining the risk).
- Fail loudly when it does not fit. A pipeline that silently drops bad
  output is worse than one that stops and tells you.

---

## Loops and Agents

Everything above is a single pass through the pipeline: one batch of tool
output in, one structured result out. Wiring that into a loop — the model
deciding what to run next based on what it just saw, and running it again
— is the agent pattern.

That loop, its patterns, and the safety rules for running it are covered
on [AI Workflows & Agents](/learn/ai/workflows/). Read that page for the
loop itself; this page is about the pipeline stage the loop is built on.

---

## Verification Is the Job

Automation does not remove the need to check the work. It changes what
checking looks like — you are reviewing a pipeline's output, not typing
each command yourself. The skill worth having is directing and checking,
not copy-pasting.

Two habits that are not optional:

- **Never run a generated command you do not understand.** If you cannot
  explain what every flag does, look it up before you run it. A command
  you cannot explain is a command you cannot be responsible for.
- **Test a generated script on a lab VM first.** Never point a
  model-written script at a real target or your daily machine on the
  first run. Run it somewhere a mistake costs nothing.

---

## What Not to Feed a Model

A hosted model runs on somebody else's server. The moment you paste
something into it, that data leaves your machine. Assume it is logged.
Running a model locally avoids this (see
[Choosing an AI Model](/learn/ai/choosing-a-model/)), but the rules below apply either
way — make them a habit, not a per-tool decision.

Never put any of the following in a prompt, a scan file, or an example you
paste in:

- **Credentials or API keys.** Not even to check if one is still valid.
- **Real target hostnames or IP addresses.** Use `TARGET_IP`,
  `example.com`, or a named lab or CTF machine instead.
- **Personal information about club members.** Real names, contact
  details, anything they have not already published themselves.
- **Copyrighted course material.** Textbook PDFs, a professor's slides,
  anything licensed that is not yours to redistribute.
- **Exam questions or graded assignment content.** FAU's academic
  integrity policy names this as misconduct, not a gray area.

If a script pulls files automatically before handing them to a model —
grabbing every log in a directory, say — check what is in that directory
first. Automation makes it easy to feed a model something you never meant
to paste in.
