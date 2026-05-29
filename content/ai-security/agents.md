+++
title = "Building Agents"
weight = 5
+++

A single AI model answering questions is useful. An agent that can run tools, observe results, and adapt its next action is a different category of useful.

The systems that won CTF competitions and topped bug bounty leaderboards were not chat interfaces — they were agents with tool access operating in loops.

---

## What Makes Something an Agent

A chat model takes input, produces output, stops. An agent:

1. Receives a goal
2. Decides what action to take
3. Executes the action (runs a tool, writes a file, makes a request)
4. Observes the result
5. Decides the next action based on the result
6. Repeats until the goal is achieved or it gives up

The key addition is **tool use** and **a loop.** Everything else is engineering around those two things.

---

## Architectures That Won Competitions

### ReAct (Reason + Act)

The simplest architecture that works. The model alternates between reasoning about the problem and acting on it.

```
Thought: I need to find the open ports on this target.
Action: nmap -sV -p- target.htb
Observation: [nmap output]
Thought: Port 8080 is running an old Tomcat. I should check for CVEs.
Action: searchsploit apache tomcat 8.5
Observation: [exploits listed]
...
```

This is what Palisade Research used to hit 95% on InterCode-CTF. No exotic architecture — just prompting and tool use in a loop.

### Planner + Executor (HackSynth)

Two modules: a Planner that reasons about the overall strategy, and an Executor that runs commands. The Planner sees summarized results — not raw output — so it doesn't get lost in noise.

```
Planner: "We have a web service on port 80. Plan: 1) fuzz directories 2) check for SQLi on login form 3) try default credentials"
Executor: runs ffuf, reports results back
Planner: "Directory fuzz found /admin. Update plan: focus on admin panel."
```

HackSynth uses this with a Summarizer as a third module — it compresses tool output before it goes back to the Planner.

### Hierarchical Agents (HPTSA / UIUC)

A manager agent breaks the problem into subtasks and spawns specialized sub-agents for each one. Sub-agents report back and the manager synthesizes the results.

```
Manager: "Exploit target: spin up Web Agent and Network Agent in parallel"
Web Agent: tests HTTP endpoints, returns findings
Network Agent: scans ports, identifies services
Manager: "Web Agent found SQLi. Spawn SQL Exploitation Agent."
SQL Agent: extracts database contents, finds credentials
Manager: synthesizes full report
```

This architecture outperformed single agents by 4.3× on zero-day exploitation in the UIUC research.

---

## Building a Simple Agent in Python

This is the minimum viable agent — a loop with tool execution:

```python
import anthropic
import subprocess
import json

client = anthropic.Anthropic()

# Define tools the agent can call
tools = [
    {
        "name": "run_command",
        "description": "Run a shell command and return the output",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The shell command to execute"
                }
            },
            "required": ["command"]
        }
    }
]

def run_tool(tool_name: str, tool_input: dict) -> str:
    if tool_name == "run_command":
        result = subprocess.run(
            tool_input["command"], shell=True,
            capture_output=True, text=True, timeout=30
        )
        return result.stdout + result.stderr
    return "Unknown tool"

def agent_loop(goal: str, max_turns: int = 20) -> str:
    messages = [{"role": "user", "content": goal}]

    for _ in range(max_turns):
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            tools=tools,
            messages=messages
        )

        # Agent is done
        if response.stop_reason == "end_turn":
            return response.content[-1].text

        # Agent wants to use a tool
        messages.append({"role": "assistant", "content": response.content})

        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                print(f"[agent] running: {block.input.get('command', '')}")
                output = run_tool(block.name, block.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": output[:4000]   # truncate large output
                })

        messages.append({"role": "user", "content": tool_results})

    return "Max turns reached"

# Run it
result = agent_loop(
    "Enumerate the web service at http://localhost:8080. "
    "Find open endpoints and check for common vulnerabilities. "
    "Report your findings."
)
print(result)
```

This is the skeleton. From here you add:
- More tools (`read_file`, `write_file`, `http_request`)
- Better output truncation and summarization
- A separate planner pass for complex goals
- Logging so you can review what it did

---

## Safety Considerations

Agents that run commands autonomously can cause damage. Before running one:

- **Scope it.** Tell it exactly what target and what actions are in bounds.
- **Run it in a VM.** Give it access to a sandboxed environment, not your host.
- **Review logs.** Know what commands it executed. Agents get creative.
- **Rate limit.** Add delays between tool calls so it doesn't hammer a target.
- **No credentials in context.** Don't put API keys or real passwords in the agent's working memory.

> [!warning] Authorization
> An agent that can run commands inherits your legal responsibilities. Only point it at systems you own or have explicit written permission to test.

---

## Using CAI Instead of Building From Scratch

For CTF work specifically, [CAI](https://github.com/aliasrobotics/CAI) is production-ready and battle-tested in competition. It handles tool routing, model switching, output summarization, and multi-category CTF challenge types.

Build your own when you need custom behavior — specific target types, custom tools, integration with your own infra.

---

**References**

- [Anthropic tool use docs](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)
- [HackSynth paper](https://arxiv.org/abs/2412.01778) — Planner + Summarizer architecture
- [UIUC HPTSA paper](https://arxiv.org/abs/2406.01637) — hierarchical agents on zero-days
- [LangChain agents](https://python.langchain.com/docs/concepts/agents/) — higher-level framework
- [CAI source code](https://github.com/aliasrobotics/CAI) — production CTF agent
