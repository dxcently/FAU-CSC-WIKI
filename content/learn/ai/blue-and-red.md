+++
title = "AI on Both Sides"
weight = 5
description = "Defensive and offensive application of AI, and the part a cyber club uniquely needs: how agent systems themselves get attacked and defended."
icon = "fa-solid fa-shield-halved"
+++

Both sides use the same tools. Defenders use them to read more alerts than a
person can read. Attackers use them to understand more code than a person can
read. There is no version of this where one side has the technology and the
other does not.

This page covers three things: where it helps defensive work, where it helps
offensive work, and — most importantly for this club — how the agent systems
themselves get attacked.

The middle part comes with a rule attached. Every technique here is scoped to
a system you own, a lab VM you built, or a CTF box you are entered in. That
is not a disclaimer, it is the condition under which any of this is legal.

---

## Defensive Work

The pattern is the same every time: the system reads a large volume of
material and ranks it, and a human decides.

**Alert and log triage.** **Triage** means sorting a pile by urgency so the
important item gets looked at first. Feed in the alert queue, get back a
ranked list with a one-line reason for each. You still read the top of the
list yourself.

**Summarizing long output.** Crash logs, stack traces, scan results, a packet
capture too long to read line by line. A summary you can scan in ten seconds
tells you where to look in the raw data. It does not replace the raw data.

**First-pass review.** Run it over a configuration or a piece of code before a
person reviews it. It catches the obvious problems. It is a filter in front of
review, not a replacement for review.

**Drafting reports.** Turn rough incident notes into a readable draft. Check
every technical claim in the result, because it will state a wrong detail with
the same confidence as a right one.

**Watching a feed.** Periodic checks against a source, flagging what changed
or what crossed a threshold. Read the security note on this pattern below
before you build one.

Notice what these have in common. Fixed steps, a clear definition of success,
and a human reviewing the end. That is a workflow, not an autonomous agent —
see [Agentic Graphs](agentic-graphs/) for why that distinction saves you
trouble. For how to actually build one, read
[Automating Security Work](/toolbox/ai-automation/).

The division of labor is worth stating plainly. The system supplies speed,
scale and consistency. The analyst supplies judgment, context, and
accountability. Nobody has automated the third one.

---

## Offensive Work

Scope first. Only against a system you own, a lab VM, or a CTF box you are
entered in. If you would not run the scan by hand, do not have a model run it
for you. Start at [CTF](/compete/ctf/) if you want targets that are legal by
construction.

**Recon summarization.** A full port scan of a lab network produces more
output than anyone reads carefully. Summarizing it into "here are the hosts,
here are the exposed services, here are the versions worth checking" is a
real time saving, and the raw output is still there to check against.

**Understanding unfamiliar code.** This is the strongest use. Point it at a
binary's disassembly, an obfuscated script, or a codebase in a language you
do not know, and ask what it does. You get oriented in minutes instead of
hours. Then verify, because a plausible explanation of code is easy to
generate and hard to distinguish from a correct one.

**CTF assistance.** Good at recognizing known patterns — a cipher, a common
web vulnerability class, a familiar exploitation primitive. Weak at genuinely
novel puzzles, which is exactly what the interesting challenges are. Use it to
get unstuck, not to skip the learning. A solved challenge you did not
understand taught you nothing, and the club's competitions do not let you
bring it.

**Where the field is going.** Earlier offensive tooling used a model to plan
an attack and drive existing scanners. Current autonomous offensive agents
reason about application logic and adapt their approach as they go, instead of
running a fixed list of payloads, which lets them find context-dependent bugs
a signature-based scanner misses. A
[2026 research note from Cloud Security Alliance Labs](https://labs.cloudsecurityalliance.org/research/csa-research-note-ai-autonomous-red-team-agent-findings-2026/)
surveys this. Note that the specific statistics circulating about these
systems trace back to vendor announcements, not independent measurement —
treat them accordingly.

---

## The Security Of Agent Systems

This is the part a cyber club is uniquely positioned to care about, and it is
the reason this section exists at all.

### The core problem, in one sentence

A model has one channel. The text it is asked to process and the text that
instructs it arrive the same way, and nothing in the architecture separates
them.

A traditional parser has that separation. A prepared SQL statement knows the
difference between the query and the value, which is why parameterized
queries kill SQL injection. A language model has no equivalent. Instructions
are just text, and so is data.

**Prompt injection** is the attack that follows: an attacker puts text in
something the agent will read, and the agent follows it.

The whole problem, stated plainly: the agent read the web page, and then it
did what the web page said.

Every defensive use case above involves reading attacker-reachable text. A
ticket, an email, a log line, a scanned page, a file name. An agent that
watches a feed is an agent that reads whatever an attacker puts in the feed.
That is not a hypothetical risk you add later. It is the deployment.

### How bad, measured

Two primary sources, both from NIST, both worth reading in full.

In a January 2025 technical blog on agent hijacking evaluations, NIST tested
one commercial assistant model using **AgentDojo**, an open-source evaluation
framework from ETH Zurich that puts an agent in simulated environments where
the data it reads contains malicious embedded instructions. The model showed
an 11% success rate for previously tested hijacking attacks and an 81% success
rate for new attacks developed specifically against it. Separately, repeating
an attack 25 times instead of once raised the average success rate from 57% to
80%
([NIST, January 2025](https://www.nist.gov/news-events/news/2025/01/technical-blog-strengthening-ai-agent-hijacking-evaluations)).

Two lessons from those numbers. Robustness against known attacks says almost
nothing about robustness against attacks written for your system. And any
defense measured on a single attempt looks far better than it will perform
against an attacker who gets to try repeatedly.

In March 2026, NIST's CAISI published results from a large-scale red-teaming
competition run with the UK AI Security Institute, covering 13 frontier models
across tool-use, coding and computer-use agent scenarios, with more than
250,000 attack attempts from more than 400 participants. They found at least
one successful attack against all of the target models. They also found that
attack success did not correlate cleanly with general model capability, and
that attacks developed against more robust models tended to transfer to less
robust ones
([NIST CAISI, March 2026](https://www.nist.gov/blogs/caisi-research-blog/insights-ai-agent-security-large-scale-red-teaming-competition)).

The conclusion to carry away: no tested model was immune. Design as though
injection will eventually succeed, and bound what it can do when it does.

### The categories to know

The OWASP GenAI Security Project publishes a
[Top 10 for Agentic Applications](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/),
extending their existing list for language models into agent-specific risks.
The categories, in short:

| ID | Risk | What it means |
|---|---|---|
| ASI01 | Agent Goal Hijack | The agent's objective is redirected through text it reads |
| ASI02 | Tool Misuse & Exploitation | Harmless tools chained into a harmful action |
| ASI03 | Identity & Privilege Abuse | An attacker uses the agent's credentials or delegated authority |
| ASI04 | Agentic Supply Chain | A compromised third-party model, plugin or tool gets loaded |
| ASI05 | Unexpected Code Execution | Generated or externally influenced code runs when it should not |
| ASI06 | Memory & Context Poisoning | Malicious data lands in stored memory and shapes later runs |
| ASI07 | Insecure Inter-Agent Communication | Weak authentication between agents allows spoofing |
| ASI08 | Cascading Failures | One fault propagates through a multi-agent system |
| ASI09 | Human-Agent Trust Exploitation | The attacker exploits your trust in the agent's recommendation |
| ASI10 | Rogue Agents | An agent acts outside its authorized scope |

ASI06 deserves a second look. Anything written into persistent memory is a
future prompt. Poison the notes an agent keeps and you have poisoned every run
after it, long after the original malicious input is gone.

### What to do about it

None of this prevents injection. All of it bounds the damage.

- **Least privilege on tools.** Give an agent the smallest set of tools and
  the narrowest credentials the task needs. The **blast radius** is everything
  the agent can reach — make it small on purpose.
- **Separate identity per agent.** Its own credentials, short-lived, revocable
  without touching anything else.
- **Sandbox execution.** Run agent actions where a mistake cannot reach
  anything you did not hand over. No network route out unless the task needs
  one.
- **Human approval on irreversible actions.** Deleting, sending, deploying,
  paying. A checkpoint costs seconds.
- **Treat all external text as untrusted input.** The same instinct you
  already have for user input in a web application, applied to everything an
  agent reads.
- **Log every tool call.** When something goes wrong you need the sequence of
  actions, not the model's explanation of them.
- **Do not chain read-untrusted into write-anywhere.** A node that reads the
  internet feeding a node that can write files or send messages, with nothing
  in between, is the standard shape of a successful attack.

The reason this differs from scoping a normal service account is worth saying
out loud. A service account does what its code does. An agent can be talked
into using the access it legitimately holds, by content it merely read.

---

## Everyday Application

Outside security, the same shapes apply and the same rule holds.

Reading a queue and ranking it. Summarizing a long document into something you
can act on. Drafting a first version of writing you will edit. Tedious
multi-file chores — open several files, pull one field out of each, put the
results somewhere. Getting oriented in an unfamiliar codebase or a language
you have never used.

The rule that carries across all of it: use it where you can check the result.
If you have no way to verify the answer, you have not automated a task, you
have delegated a guess.

---

## Where To Go Next

- [Agentic Graphs](agentic-graphs/) — the structures these systems are built
  from, and where to put the checkpoints.
- [Fundamentals for the AI Era](fundamentals/) — why local models matter when
  the data is sensitive.
- [Automating Security Work](/toolbox/ai-automation/) — the practical build,
  including what never goes into a prompt.
- [CTF](/compete/ctf/) — targets you are allowed to attack.
