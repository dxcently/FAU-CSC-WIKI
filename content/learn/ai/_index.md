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

This section covers what a **large language model** (LLM) is, what an agent
system is made of, what runs the loop, and how knowledge gets in front of one.
It covers what happens when the same technology is pointed at you. Then the
practical half: which model to pick, how to wire one into a script, and what
never goes in a prompt.

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

## You Are Still Accountable

IBM put it on a training slide in 1979: *a computer can never be held
accountable, therefore a computer must never make a management decision.*
Nothing since has made it less true.

A model will draft the plan, write the script, and read the logs for you. It
will not answer for any of it. When the pipeline wipes the wrong target, when
the agent follows an instruction buried in a page it was told to read, when a
summary quietly drops the one line that mattered — that lands on you. The tool
is not in the room when it goes wrong.

So the rule underneath this whole section: stay in control of your systems and
understand what is happening inside them. Not trust the model, not trust the
output — understand it well enough to catch it when it is wrong. It is the same
reason your fundamentals matter, from the other direction: a decision you
cannot check is a decision you have already handed away.

---

{{< section-grid >}}
