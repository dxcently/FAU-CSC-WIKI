+++
title = "Agentic Graphs"
weight = 2
description = "Nodes, edges, state and cycles: the vocabulary for describing systems built from many model calls, the named patterns, and the failure modes."
icon = "fa-solid fa-diagram-project"
+++

One prompt gets you one answer. Real systems chain many model calls, tool
calls and checks together, and the interesting question stops being "what did
it say" and becomes "what shape is this thing."

**Agentic graph** is the vocabulary for that shape. It is not a new
technology. It is a way to draw the system so you can reason about how it
fails before you run it.

This page covers the concepts. For the loop mechanics and hands-on workflows,
read [AI Workflows & Agents](/toolbox/ai-workflows/).

---

## What "Graph" Means Here

A graph is a flowchart with memory. Three parts.

### Nodes

A **node** is one step. It is a model call, a tool call, or a plain function.
Nodes are where work happens.

Keep each node small enough to describe in one sentence. If you cannot say
what a node does, you cannot tell whether it did it.

### Edges

An **edge** is what runs next. A plain edge always goes to the same place. A
**conditional edge** looks at the current state and picks between several
next steps.

Edges are the control flow. In a hand-written script this is your `if`
statement. Drawing it as an edge just makes it visible.

### State

**State** is a shared object that every node reads and writes. It is the
graph's memory for one run: the original goal, what has been tried, what came
back.

State is also where errors hide. A wrong value written early stays there and
every later node treats it as fact.

### Cycles and DAGs

A **DAG** is a directed acyclic graph — flow moves forward and never comes
back. A fixed pipeline is a DAG. It is predictable and it always finishes.

A **cycle** is an edge that goes backward. Retry, self-correction and "try
again with the critic's feedback" all need a cycle. Most behavior people call
agentic requires one.

Cycles are the source of most power and most trouble in these systems. Put a
step limit on every cycle. Without one, nothing guarantees the run ends.

| | DAG | Graph with cycles |
|---|---|---|
| Flow | Forward only | Can go back |
| Ends? | Always | Only if you make it |
| Good for | Fixed pipelines | Retry, refine, adapt |
| Cost | Bounded | Bounded only by your step limit |

---

## Why People Left the Single Prompt Loop

The first agents were one model in a `while` loop. Prompt it, run whatever
tool it asked for, feed the result back, repeat until it says it is done.

That works, and it is opaque. You cannot see the shape of the process, you
cannot put a checkpoint in the middle, you cannot run two independent steps at
the same time, and you cannot route around a step that failed.

Making the structure explicit fixes all four. The value is not the word
"graph." The value is that you can look at the diagram and ask: does this
loop? where does it stop? which step touches something I cannot undo?

---

## Workflow or Agent

These two words get used as if they mean the same thing. They do not, and the
distinction decides how much trouble you are signing up for.

A **workflow** orchestrates models and tools through code paths you wrote in
advance. You decide the steps. The model fills in the content of each step.

An **agent** directs its own process. It decides which tools to use and in
what order, and it keeps control of how the task gets done.

Workflows are predictable, auditable and cheaper. Agents handle tasks you
cannot decompose ahead of time, and they cost more and fail in more ways.

The standing advice, from the December 2024 engineering guide that gave the
field most of this vocabulary and quoted approvingly by
[Simon Willison](https://simonwillison.net/2024/Dec/20/building-effective-agents/):
"finding the simplest solution possible, and only increasing complexity when
needed."

Most work labeled "agent" is a workflow. Build the workflow.

---

## The Named Patterns

Six shapes cover almost everything you will see.

### Chaining

Split the task into fixed sequential steps. Each step processes the previous
step's output. Put a plain programmatic check between steps, so a bad
intermediate result stops the chain instead of feeding the next one.

Reach for it when the task decomposes cleanly into subtasks you can name in
advance. It trades speed for accuracy.

### Routing

Classify the input first, then send it down a path specialized for that
category.

Reach for it when the inputs fall into distinct categories, and one generic
prompt would do a mediocre job on all of them. Alert triage is the obvious
security example: a failed login and a suspicious outbound connection do not
need the same follow-up.

### Parallelization

Two flavors.

**Sectioning** splits a task into independent subtasks, runs them at the same
time, and combines the results. **Voting** runs the same task several times
and compares the answers.

Reach for sectioning when the subtasks genuinely do not depend on each other.
Reach for voting when you want more confidence in one answer and are willing
to pay several times for it.

### Orchestrator-Workers

A central model breaks the task into subtasks, hands each to a worker model,
and combines what comes back.

This looks like parallelization and it is not. The difference is that the
subtasks are not fixed ahead of time — the orchestrator decides them at
runtime, based on the input.

Reach for it when you cannot predict what the subtasks are. Accept that you
have also given up the ability to predict what it will do.

### Evaluator-Optimizer

One model produces a result. A second model evaluates it against criteria and
gives feedback. The first model revises. Repeat.

This is the critic loop, and it needs a cycle. Reach for it when you have
clear evaluation criteria and revision measurably improves the result. Skip it
when "better" is a matter of taste, because then the evaluator is just
another opinion.

### Human-in-the-Loop Checkpoints

Not really a pattern. It is a property you add to any of the above: the graph
pauses at a chosen edge and waits for a person.

Put a checkpoint before every irreversible action, and on every cycle that has
no other bound. This is the cheapest safety mechanism available and people
skip it because it feels like it defeats the point. It does not. It is the
difference between a system that made a mistake and a system that made a
mistake three hundred times.

---

## Reading a Graph Before You Run It

Four questions. Ask them about every design, including your own.

1. **Where are the cycles, and what stops them?** A step limit, a token
   budget, or a human. Pick one.
2. **Which node does something you cannot undo?** Writing files, sending
   messages, changing a system. Put a checkpoint in front of it.
3. **Where does untrusted text enter?** Any node that reads a web page, a
   ticket, an email or a log is reading text an attacker may have written.
   See [AI on Both Sides](blue-and-red/).
4. **What happens to state if step two is wrong?** Trace it forward. If a
   wrong value at step two silently changes step seven, you need a check
   between them.

---

## Failure Modes

Be honest about these. They are not edge cases.

### Compounding error

The most common way these systems fail. A wrong assumption early does not
crash anything. It gets written into state, and every later node builds on it
as if it were true. By the time the mistake is visible, a lot of downstream
work already assumed it.

Cycles make this worse. A loop that can revise itself can also loop on a bad
premise and reinforce it each time around.

The defense is checks between steps, not a better prompt.

### Unverifiable output

A summary can be fluent, confident and wrong. There is no stack trace for
"the reasoning drifted." Several steps deep, checking the answer can cost as
much as doing the work yourself.

If you cannot check a step's output, that step is not automation. It is a
guess you have decided to trust.

### Cost

Every step, retry and parallel branch is another paid model call. A cycle
without a bound is how an automation bill becomes a story. More capable graph
shapes buy better results by spending more time and more money — that trade is
real, and you should make it on purpose.

### Untrusted input

Any node that reads outside text is an attack surface. A "watch the feed" or
"summarize incoming tickets" graph reads attacker-reachable text by
definition. This is covered in full on [AI on Both Sides](blue-and-red/), and
it is the single most important thing on this page for a security student.

### More graph is not better

Every node is another place to fail, another call to pay for, and another
thing to debug. A four-node chain that works beats a twelve-node agent that
usually works.

Start with one model call. Add a step only when a specific failure makes you.

---

## Implementations

Open-source frameworks model this directly. LangGraph, for example, is built
on state, nodes and edges, and supports cycles specifically so an agent can
loop back to retry or correct itself.

You do not need a framework. A graph is a data structure, and plain Python
with a dictionary for state and a loop for edges is a legitimate
implementation that you can read end to end.

Learn the shapes. They outlive whichever library is popular this year.
