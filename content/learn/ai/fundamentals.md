+++
title = "Fundamentals for the AI Era"
weight = 1
description = "What to actually learn now that models write code: the framings worth knowing, the case for small local models, and why the rest of the roadmap matters more."
icon = "fa-solid fa-brain"
+++

The question every student asks, in some form: if a model can write the code,
why learn the code? It is a fair question and it deserves a straight answer.

The answer is that the fundamentals got more valuable, not less. You cannot
direct work you do not understand, and you cannot verify it either. That is
not encouragement — it is the specific, mechanical reason the rest of
Everything on the [roadmap](/start/) still matters.

This page is the conceptual map. It leans on two people worth following:
**Andrej Karpathy**, who teaches how these models are built, and **Matt
Pocock**, who teaches how to build software with them.

---

## Software 1.0, 2.0, 3.0

Karpathy's 2017 essay
[Software 2.0](https://karpathy.medium.com/software-2-0-a64152b37c35) split
software into two kinds.

**Software 1.0** is code a human writes. Python, C, a shell script. You state
every rule.

**Software 2.0** specifies the behavior you want with a dataset and a rough
network architecture. An optimization process finds the actual program — the
weights. Nobody writes those weights by hand, and nobody reads them either.

In January 2023 he added a line that got repeated everywhere:
["The hottest new programming language is English."](https://x.com/karpathy/status/1617979122625712128)
That became **Software 3.0** in his June 2025 talk: the prompt is the
program. His words for the direction: "Software 3.0 is eating 1.0/2.0"
([talk recap](https://www.latent.space/p/s3)).

Why you care: a modern system contains all three at once. Hand-written code
calls a trained model, and a prompt steers the model. When it breaks, you
need to know which of the three layers broke.

---

## The Model as a New Kind of Computer

A **large language model** (LLM) is a program that predicts the next piece of
text, trained on a very large amount of text. That is the whole mechanism.
Everything else is built on top of it.

Karpathy's simplest framing, from his November 2023 talk
[Intro to Large Language Models](https://www.youtube.com/watch?v=zjkBMFhNj_g):
a model is two files. A **parameters file** holds the weights. A **run file**
holds the code that runs the network. The mystery goes away fast once you can
name the two pieces.

From there he pushed a longer metaphor: the model as the kernel of a new kind
of operating system. The context window works like RAM, tool use like system
calls, tokens per second like a clock speed.

Take that metaphor for one thing — it tells you where the limits are. A
context window fills up. Tool calls are the only way the model touches
anything outside itself. Nothing persists between runs unless you store it.

---

## Jagged Intelligence

Karpathy coined **jagged intelligence** in July 2024 for a fact that confuses
every new user: a model can solve a hard problem and then fail a trivial one.
Not sometimes. Reliably, and unpredictably.

His own description, from his
[2025 year in review](https://karpathy.bearblog.dev/year-in-review-2025/): a
model is "simultaneously a genius polymath and a confused and cognitively
challenged grade schooler."

His explanation for why is the useful part. In an April 2026 talk he framed
traditional software as automating what you can specify, and models as
automating
["what you can verify"](https://karpathy.bearblog.dev/sequoia-ascent-2026/).
Capability grows fastest where checking the answer is cheap and automatic —
code, math, tests. It grows slowly where checking is hard, like taste and
judgment. The capability is uneven because the training signal is uneven.

A second limit is worth naming. In his 2025 talk he compared a model to a
coworker with **anterograde amnesia**, a condition where a person cannot form
new long-term memories. The model works well inside one session and keeps
nothing structural between sessions. A bigger context window is a workaround,
not a fix.

Practical consequence: never assume that a model which did the hard thing can
do the easy thing. Check the easy thing too.

---

## Build It To Understand It

Karpathy's standing justification for teaching from scratch, said on the
[Dwarkesh Patel podcast](https://www.dwarkesh.com/p/andrej-karpathy) in
October 2025: "If I can't build it, I don't understand it."

His general recipe for getting good at anything is the same shape. Take on
concrete projects and go deep. Learn on demand instead of reading a whole
textbook first. Explain what you learned in your own words. Compare yourself
only to your younger self.

The material, in the order it is worth taking:

1. **[Intro to Large Language Models](https://www.youtube.com/watch?v=zjkBMFhNj_g)**
   (November 2023, about one hour). No code, no math needed. Builds the
   mental map. It also covers jailbreaks, prompt injection, and data
   poisoning — relevant to this club specifically.
2. **Deep Dive into LLMs** (February 2025, three and a half hours). The full
   training stack: collect text, tokenize, pretrain, fine-tune into an
   assistant, then hallucinations and tool use.
3. **[Neural Networks: Zero to Hero](https://karpathy.ai/zero-to-hero.html)**.
   Eight lectures that build neural networks from scratch in code. It starts
   with a tiny autograd engine and ends at a working transformer and a
   tokenizer. Stated prerequisites are solid Python and "intro-level math
   (e.g. derivative, gaussian)." Code at
   [nn-zero-to-hero](https://github.com/karpathy/nn-zero-to-hero).
4. **[nanoGPT](https://github.com/karpathy/nanoGPT)**. The cleaned-up,
   minimal repository for training and fine-tuning a real GPT-style model.
   Roughly 300 lines for the training loop and 300 for the model.
5. **[nanochat](https://github.com/karpathy/nanochat)**. The full modern
   pipeline, end to end. See the next section.

One honesty note: his own education company and its course are not his active
focus right now. He took a research role in 2026 and said he plans to return
to education work later
([his announcement](https://x.com/karpathy/status/2056753169888334312)). The
material above is all published and all still works.

---

## The Case for Small Models

This is the part a security person should read twice.

### Models are bigger than they need to be

Pretraining on a huge pile of internet text does two things at once. It
teaches the model to reason, and it makes the model memorize an enormous
amount of world knowledge. Most of the parameter budget pays for recall.

Recall is the part you can look up. Reasoning is not.

### The cognitive core

In 2026 Karpathy proposed the
[cognitive core](https://x.com/karpathy/status/1938626382248149433): a small
model, a few billion parameters, that deliberately gives up encyclopedic
knowledge and keeps the reasoning. Strip out memorized facts and the model is
forced to look things up instead of guessing from memory. What stays behind
is what he described as the algorithms for thought.

The design he sketched runs always-on and locally, handles more than text,
uses tools aggressively, and hands off to a larger remote model when one is
available.

The trade is explicit. You lose raw knowledge and some problem-solving power.
You gain low latency, access to private local data, operation with no network,
and control over the model you run.

### The small-and-cheap projects prove the stack is not a secret

[nanochat](https://github.com/karpathy/nanochat) is the argument in code. It
runs the whole pipeline — tokenization, pretraining, fine-tuning, evaluation,
and web serving — end to end, producing a small model you can actually talk
to. Per
[the project's own introduction](https://github.com/karpathy/nanochat/discussions/1),
that run takes about four hours on a single eight-GPU node and costs about
$100, across roughly 8,000 lines in 45 files. The stated goal is to push what
is possible in micro models on small budgets.

The lesson: the expensive part of a frontier model is scale, not secret
knowledge. The pipeline is public, small enough to read, and cheap enough for
a student club to run once.

### Distillation and data quality

Two standard techniques carry most of the weight in making small models good.

**Distillation** trains a small model on the outputs of a large one, so the
small model copies the behavior without paying for the size. It is how a model
that fits on a laptop can act better than its parameter count suggests.

**Data quality** decides the ceiling. A large model can absorb junk and still
work, because it has room to spare. A small model has no room. What it reads
is what it can do.

### Why this matters to you specifically

Because of where the data goes.

Send a log file to a hosted service and you have disclosed it. That is fine
for a CTF box. It is not fine for a client's logs, a malware sample, an
unreleased finding, an internal network map, or anything covered by an
agreement you signed. A model that runs on your own machine turns that
disclosure back into ordinary local analysis.

Local models also work in an isolated lab with no network route out, which is
where malware analysis belongs anyway.

The selection criteria for local against hosted are in
[Choosing an AI Model](/learn/ai/choosing-a-model/). This page is the reason the choice
exists.

---

## The LLM Wiki Idea: What Is Real

Karpathy has talked about **LLM knowledge bases** as a genuinely new category
of application: take messy unstructured source material and compile it into a
structured wiki with summaries and cross-links, then keep it maintained.
Classical code cannot do that robustly. His test question for finding this
kind of application, from the
[April 2026 talk](https://karpathy.bearblog.dev/sequoia-ascent-2026/): "What
information transformation was impossible before, but is now natural?"

Separately he floated an **idea file**: in the agent era, sharing a finished
application matters less than sharing the idea, because the recipient's own
agent can build a version fitted to them. An LLM wiki was his example
([the post](https://x.com/karpathy/status/2040470801506541998)).

Now the honest part. There is no published Karpathy LLM-wiki tool. No
repository, no product, nothing to install. The idea is the artifact.

That is the point, not a disappointment. Treat it as a design pattern and
build your own. What structure a knowledge base needs is covered in
[Knowledge Bases as Agent Context](knowledge-bases/).

---

## Engineering Fundamentals Are the Leverage Layer

[Matt Pocock](https://www.mattpocock.com/) taught TypeScript for years and
now teaches AI engineering full time at [AI Hero](https://www.aihero.dev/).
His thesis runs against the usual pitch: engineering fundamentals are not
obsolete, they are the thing that makes agents useful at all.

The reasoning is plain. An agent is fast at producing code and bad at
deciding what code should exist. Decomposition, testability, and a clear
definition of done are the inputs it needs from you. Skip them and you get a
large volume of code nobody can debug.

His workflow, in order:

**Plan before you delegate.** His
[`/grill-me`](https://www.aihero.dev/skills-grill-me) skill runs a structured
interview against a vague idea, in rounds, until there are no open questions
left. It writes no files. It does not need a plan up front — "producing that
plan is what the session is for."

**Cut work into vertical slices.** A **vertical slice** cuts through every
layer of the system at once — schema, service, minimal interface — and ships.
The opposite is finishing one layer at a time and having nothing that works
until the end. A slice gives an agent a visible finish line.

**Keep each task's context small.** Output quality falls as a context window
fills up. His workshop calls the healthy part of the window the smart zone.
Give each task a fresh, small context. Review code in a clean context, not the
one the agent already filled while writing it.

**Let tests be the specification.** Write a failing test. Have the agent make
it pass. Refactor. A failing test is a concrete target an agent optimizes
against. A paragraph of prose requirements is not.

**Decide what runs unattended.** Split work into tasks that need a human in
the loop and tasks defined well enough to run without one. Track which tasks
block which, so independent work can run in parallel. His
[Ralph](https://www.aihero.dev/events/turn-ai-agents-into-autonomous-software-engineers-with-ralph)
technique is the unattended version — an agent in a loop, driven by a written
specification and a feedback signal, not tied to any single tool.

**Delegate the legwork, keep the decisions.** His
[`/research`](https://www.aihero.dev/skills-research) skill sends a
background agent to read the sources that own the answer, and it "leaves a
cited Markdown file in the repo." Notice the shape: the agent does the
reading, a human makes the call, and every claim carries a link.

---

## What This Means For a Student

Nothing on the roadmap got deleted. It got more load-bearing.

Karpathy's line for it, from the April 2026 talk: "You can outsource your
thinking, but you can't outsource your understanding."

He also draws a distinction worth keeping. Producing software with a model
raises the floor — anyone can make something now. Directing many fallible
agents while holding quality and security raises the ceiling, and that is a
professional skill built on more knowledge, not less.

The bar for shipping has not moved either: "Demo is works.any(), product is
works.all()."

So keep going through [Linux](/learn/linux/),
[Networking](/learn/networking/), and
[CLI & Scripting](/learn/cli-scripting/). Then read
[Agentic Graphs](agentic-graphs/) for how these systems are put together,
and [AI on Both Sides](blue-and-red/) for how they get attacked.
