+++
title = "AI Workflows & Agents"
weight = 7
description = "The agent loop, common agent patterns, and vendor-neutral workflows for using AI in security work."
icon = "fa-solid fa-diagram-project"
+++

A single model answering questions is useful. A model that can run tools,
observe results, and adapt its next action is a different category of
useful. This page covers both: the loop that makes something an "agent," and
practical workflows for using AI — agentic or not — in security work.

---

## What Makes Something an Agent

A chat model takes input, produces output, stops. An agent:

1. Receives a goal
2. Decides what action to take
3. Executes the action (runs a tool, writes a file, makes a request)
4. Observes the result
5. Decides the next action based on the result
6. Repeats until the goal is achieved or it gives up

The key addition is **tool use** and **a loop**. Everything else is
engineering around those two things.

---

## Agent Patterns

### ReAct (Reason + Act)

The simplest pattern that works. The model alternates between reasoning
about the problem and acting on it.

```
Thought: I need to find the open ports on this target.
Action: nmap -sV -p- target.htb
Observation: [nmap output]
Thought: Port 8080 is running an old Tomcat. Check for CVEs.
Action: searchsploit apache tomcat 8.5
Observation: [exploits listed]
...
```

No exotic architecture — just prompting and tool use in a loop. Enough for
most enumeration and scripting tasks.

### Planner + Executor

A Planner reasons about overall strategy; an Executor runs commands. The
Planner sees summarized results, not raw output, so it does not get lost in
noise on longer engagements. Add a Summarizer role once tool output gets too
large to hand the Planner directly.

```
Planner: "Web service on port 80. Plan: fuzz directories, check
          login form for SQLi, try default credentials."
Executor: runs the directory fuzz, reports results back
Planner: "Found /admin. Update plan: focus on the admin panel."
```

Scale this up to **hierarchical agents** — a manager spawning specialized
sub-agents (web, network, ...) that report back — once a single agent's
context gets crowded with unrelated subtasks. Otherwise it's overhead for no
benefit.

---

## A Minimal Agent Loop

The skeleton, independent of any specific provider. `chat()` stands in for
whatever API call your provider uses.

```python
def agent_loop(goal: str, max_turns: int = 20) -> str:
    messages = [{"role": "user", "content": goal}]

    for _ in range(max_turns):
        response = chat(messages, tools=TOOL_DEFINITIONS)
        if response.done:
            return response.text

        messages.append({"role": "assistant", "content": response.raw})
        for call in response.tool_calls:
            output = run_tool(call.name, call.args)   # e.g. shell exec
            messages.append({"role": "tool", "call_id": call.id,
                              "content": output[:4000]})  # truncate

    return "max turns reached"
```

From here you add more tools (`read_file`, `http_request`), better output
truncation, a separate planner pass, and logging so you can review what it
actually did.

### Safety

Scope it to a specific target and set of allowed actions. Run it in a VM,
not your host. Review its logs — agents get creative. Rate limit it so it
does not hammer a target. Keep credentials out of its context entirely.

> [!warning] Authorization
> An agent that runs commands inherits your legal responsibilities. Only
> point it at systems you own or have explicit written permission to test.

---

## Practical Workflows

Repeatable patterns, not one-off prompts.

### CTF / Recon Loop

```
1. Enumerate manually — understand what you actually have
2. Ask the model to analyze the enumeration output
3. Generate an exploit or script with the model
4. Run it, get output
5. Feed the output back for interpretation
6. Iterate
```

AI is most useful at steps 2, 3, and 5. You own steps 1, 4, and the final
call on whether the result makes sense.

### Hardening Review (Blue Team)

Collect state, then hand it over in one batch instead of describing it from
memory:

```bash
sudo -l > sudo_config.txt
find / -perm -4000 2>/dev/null > suid_bins.txt
ss -tulnp > open_ports.txt

cat *.txt | chat "review this system configuration for security issues,
list findings by severity, suggest specific fixes"
```

---

## Beyond One-Off Workflows

The workflows above are things you run by hand, chat window open, when you
need them. Wire the same pattern into a script — tool output piped
straight into `chat()`, running on a schedule or every time a scan
finishes — and it stops being a habit and becomes automation.

See [Automating Security Work](/learn/ai/automation/) for the pipeline
pattern, structured output, and what never goes in the prompt.

---

## What Kills These Workflows

- Trusting output you have not verified — a plausible-looking exploit that
  does not work, or an analysis that misses the one line that mattered.
- Letting the model write domain-specific logic it does not understand. It
  produces confident garbage and you lose hours debugging it.
- Skipping step 1. If you do not understand what you are enumerating, you
  cannot tell whether the model's read on it is right.

The skill worth building is directing and verifying model output, not
copy-pasting it.
