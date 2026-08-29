+++
title = "AI"
weight = 9
description = "What language models and agents actually are, how agent systems are built, and why they are both a tool and a target."
icon = "fa-solid fa-robot"
+++

Every security club now has an argument about this, so here is the club's
position up front: these tools change what one person can do in an afternoon,
and they are a new attack surface. Both statements are true at the same time.
Neither one cancels the other out.

This section is the conceptual half. It covers what a **large language model**
(LLM) is, what an agent system is made of, what runs the loop, how knowledge gets in front of one,
and what happens when the same technology is pointed at you. The practical
half — which model to pick, how to wire one into a script, what never goes in
a prompt — lives in the [Toolbox](/toolbox/).

---

## Why This Is Here

Three reasons.

**It changes the leverage of one person.** A student with a lab VM, a shell,
and a model that can read a thousand log lines is doing work that used to
need a team. That is real. It is also the exact reason your fundamentals
matter more than they did before — you cannot check work you do not
understand.

**It is a target.** An agent that reads a web page, a ticket, or a log file
is reading text an attacker can write. The model has no built-in separation
between "text to process" and "instructions to follow." That single fact
generates a whole class of attacks, and a cyber club is exactly the place to
learn it.

**It is already on both sides.** Defenders use it for triage and
summarization. Attackers use it for recon and for finding bugs. Neither side
gets to opt out, so learn how it works.

---

## The Five Pages

**[Fundamentals for the AI Era](fundamentals/)** — what to actually learn,
and why the rest of the roadmap got more valuable, not less. Draws on Andrej
Karpathy's teaching material and framings, his case for small locally
runnable models, and Matt Pocock's argument that engineering fundamentals are
what make agents useful.

**[Agentic Graphs](agentic-graphs/)** — the vocabulary for describing a
system built from many model calls. Nodes, edges, state, and cycles. The
named patterns, when to reach for each, and the honest failure modes.

**[Harnesses & the Agent Loop](harnesses-and-loops/)** — the mechanism
underneath all of it. What a harness is, what it owns, why stop conditions
are not optional, and the named tools people actually run — with their
licences, because "open source" is claimed more often than it is true.

**[Knowledge Bases as Agent Context](knowledge-bases/)** — knowledge graphs
against vector retrieval in plain terms, and what document structure actually
helps an agent. This wiki is the worked example.

**[AI on Both Sides](blue-and-red/)** — defensive and offensive application,
scoped to systems you are authorized to touch, plus the part a security club
uniquely needs: how to attack and defend agent systems themselves.

---

## Read the Toolbox for the Practical Side

These pages explain concepts. They deliberately do not repeat the how-to.

- [Choosing an AI Model](/toolbox/ai/) — the selection criteria, including
  local against hosted.
- [AI Workflows & Agents](/toolbox/ai-workflows/) — the agent loop and
  hands-on workflows.
- [Automating Security Work](/toolbox/ai-automation/) — pipelines,
  verification, and what never goes into a prompt.

---

{{< section-grid >}}
