+++
title = "Models & When to Use Them"
weight = 2
+++

Different models have different strengths. For security work the relevant axes are: reasoning depth, code quality, context window, cost, and whether you can run it locally.

---

## Cloud Models

### Claude (Anthropic)

**Claude Sonnet** is the best coding and reasoning model for day-to-day work. It handles long context well, is precise about what it does not know, and produces clean code.

**Claude Opus** is slower and more expensive — use it for hard problems that need deeper reasoning: novel exploit chains, complex reverse engineering, architectural decisions.

Both support [extended thinking](https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking) — the model reasons through a problem before responding. Useful for multi-step CTF challenges.

Best for: CTF scripting, code review, understanding vulnerability classes, agent orchestration.

---

### GPT-4o (OpenAI)

Strong all-rounder. Slightly better than Claude at some math-heavy crypto challenges in benchmarks. Multimodal — can read screenshots, which matters for some CTF challenges.

CTFAgent (2025) benchmarked GPT-4o against Gemini 2.5 Pro and DeepSeek-V3 — GPT-4o came out ahead on pwn and web challenges.

Best for: mixed CTF work, anything visual, when you want a different second opinion than Claude.

---

### Gemini 2.5 Pro (Google)

Largest context window of the major models (1M tokens). That matters when you are feeding in large code bases, full binary disassembly, or long log files.

Competitive with GPT-4o on reasoning benchmarks. Somewhat behind on code generation quality.

Best for: large context analysis, feeding in entire repos or dump files.

---

### DeepSeek-V3 / R1

Strong open-weights reasoning model. Comparable to GPT-4o on many tasks. Significantly cheaper via API or free to run locally.

DeepSeek-R1 has an explicit reasoning chain (similar to Claude's extended thinking) — it shows its work.

Best for: cost-sensitive automation, running locally for sensitive targets, crypto math.

---

## Local Models

Running models locally means no data leaves your machine. Relevant when you are working on sensitive targets or restricted networks.

### Ollama

[Ollama](https://ollama.com/) is the easiest way to run local models. One command to pull and run a model.

```bash
# Install ollama, then:
ollama pull llama3.2       # Meta's Llama 3.2 (good general use)
ollama pull deepseek-r1    # DeepSeek R1 (strong reasoning)
ollama pull codellama      # Code-focused Llama variant
ollama pull qwen2.5-coder  # Alibaba's code model, strong on security tasks

# Run a model
ollama run llama3.2

# Use it via API (compatible with OpenAI API format)
curl http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "llama3.2", "messages": [{"role": "user", "content": "explain XSS"}]}'
```

### Which local model for security?

| Model | Size | Best for |
|---|---|---|
| Llama 3.2 (3B/11B) | Small | Fast responses, quick tasks |
| Llama 3.1 (70B) | Large | Reasoning, better code |
| DeepSeek-R1 (7B-70B) | Medium–Large | Math-heavy crypto, reasoning |
| Qwen2.5-Coder (7B/32B) | Medium–Large | Code generation, scripting |
| CodeLlama (7B/34B) | Medium–Large | Focused code tasks |

You need a GPU for anything 13B+. On CPU it is usable for 7B models but slow.

---

## Comparison for Security Tasks

| Task | Best model |
|---|---|
| CTF scripting (Python/pwntools) | Claude Sonnet or GPT-4o |
| Hard reasoning (exploit chains, crypto) | Claude Opus or GPT-4o |
| Large file analysis (full disassembly, large pcap) | Gemini 2.5 Pro |
| Cost-sensitive automation | DeepSeek-V3 or local Qwen |
| Sensitive/offline work | Local Ollama model |
| Reading screenshots / visual CTF | GPT-4o |
| Code review | Claude Sonnet |

No single model wins everywhere. The practical answer is: use Claude for most things, reach for GPT-4o when you want a different perspective, use Gemini for long context, run local when you need privacy.

---

**References**

- [Anthropic Claude docs](https://docs.anthropic.com/)
- [OpenAI API docs](https://platform.openai.com/docs/)
- [Ollama model library](https://ollama.com/library)
- [DeepSeek API](https://platform.deepseek.com/)
- [Gemini API](https://ai.google.dev/)
