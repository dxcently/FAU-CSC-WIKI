+++
title = "Setting Up Your AI Toolkit"
weight = 3
+++

Three setups worth knowing: Claude Code with ECC for daily security work, a local Ollama stack for offline or sensitive targets, and CAI for automated CTF solving.

---

## Claude Code + ECC (Recommended Starting Point)

Claude Code is Anthropic's CLI tool. It reads your project context and runs tools in your terminal — write files, run commands, search code, browse the web.

ECC (Emerging Claude Code) is a rule and skill framework that configures Claude Code for specific workflows.

### Install Claude Code

```bash
npm install -g @anthropic/claude-code
claude                  # first run walks you through auth
```

You need an [Anthropic API key](https://console.anthropic.com/). The free tier is limited — for serious use, pay-as-you-go or a Pro subscription.

### What ECC adds

ECC installs rules files that tell Claude Code how to behave for your stack. For security work it means:

- Consistent scripting patterns
- Agent orchestration (spin up sub-agents for parallel analysis)
- Custom slash commands you define (like the `/wiki-page` command in this repo)
- Hooks that run automatically after file edits

The rules are already installed globally on this machine. For your own setup:

```bash
# Clone ECC
git clone https://github.com/anthropics/claude-code-ecc
cd claude-code-ecc

# Install web rules (for building tools/frontends)
./install.sh web

# Install Python rules (for scripting)
./install.sh python
```

### Useful Claude Code patterns for security

```bash
# Start a session in your CTF working directory
cd ~/ctf/challenge
claude

# Ask it to analyze a binary
# (inside Claude Code session):
# "Analyze this binary with strings and file, then look for vulnerabilities"

# Have it write an exploit script
# "Write a pwntools script for a 64-bit binary with no PIE and no canary,
#  stack overflow at offset 72, has a win() function at 0x401234"

# Pipe nmap output into a session
nmap -sV target.htb > scan.txt
claude "analyze scan.txt and tell me what attack surface this exposes"
```

---

## Ollama — Local Model Stack

Use this when you are on a restricted network, dealing with sensitive data, or want free unlimited inference.

```bash
# Install (Linux)
curl -fsSL https://ollama.com/install.sh | sh

# Pull a model
ollama pull qwen2.5-coder:7b    # good starting point for code tasks
ollama pull deepseek-r1:7b      # better for reasoning

# Run it
ollama run qwen2.5-coder:7b
```

**Connect it to Claude Code:**

Claude Code can use any OpenAI-compatible API. Ollama exposes one at `localhost:11434`.

```bash
ANTHROPIC_BASE_URL=http://localhost:11434/v1 \
ANTHROPIC_API_KEY=ollama \
claude --model qwen2.5-coder:7b
```

> [!warning] Local model quality
> Local 7B models are significantly weaker than Claude Sonnet or GPT-4o. They are useful for simple tasks, quick lookups, and offline work. Don't expect the same results on complex challenges.

---

## CAI — Automated CTF Agent

CAI is the framework that won the Neurogrid CTF ($50k prize) and topped the Dragos OT CTF in 2025. It is open source.

```bash
git clone https://github.com/aliasrobotics/CAI
cd CAI
pip install -e .

# Configure your API keys
export ANTHROPIC_API_KEY=your_key
export OPENAI_API_KEY=your_key    # optional, it supports multiple backends

# Run against a CTF target
cai --target http://target.htb --category web
```

CAI uses LiteLLM under the hood, so it can route to any model — Claude, GPT-4o, Gemini, DeepSeek, or local Ollama.

It is most effective on jeopardy-style CTFs. Attack/defend competitions require more situational awareness than current agents handle reliably.

---

## Open WebUI — Chat Interface for Local Models

If you want a ChatGPT-style interface on top of your local Ollama models:

```bash
docker run -d -p 3000:8080 \
  -v open-webui:/app/backend/data \
  --name open-webui \
  ghcr.io/open-webui/open-webui:main
```

Open `http://localhost:3000`. Connect it to Ollama in settings. Now you have a local chat UI with no data leaving your machine.

---

## Simple Python Wrapper — Any Model, Any Task

When you want to script AI into your CTF tooling without a full framework:

```python
import anthropic   # or openai, or google.generativeai

client = anthropic.Anthropic()   # reads ANTHROPIC_API_KEY from env

def ask(prompt: str, context: str = "") -> str:
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": f"{context}\n\n{prompt}" if context else prompt}
        ]
    )
    return message.content[0].text

# Example: analyze nmap output
import subprocess
scan = subprocess.run(["nmap", "-sV", "target.htb"], capture_output=True, text=True)
analysis = ask("What attack surface does this expose?", context=scan.stdout)
print(analysis)
```

Swap `anthropic` for `openai` and point at `base_url="http://localhost:11434/v1"` to use a local model.

---

**References**

- [Claude Code docs](https://docs.anthropic.com/en/docs/claude-code)
- [Ollama](https://ollama.com/)
- [CAI — Alias Robotics](https://github.com/aliasrobotics/CAI)
- [Open WebUI](https://github.com/open-webui/open-webui)
- [LiteLLM](https://docs.litellm.ai/) — unified API across all major models
