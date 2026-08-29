# Research notes: Agent harnesses

Scope: what a "harness" is, why it dominates agent behavior/safety, its architectural
pieces, harness-specific failure modes, and how it differs from a plain chat-API script.

Every claim below is sourced. `[FETCHED]` = full page content retrieved via WebFetch.
`[SEARCH-ONLY]` = seen only in search-result snippets, not independently fetched — treat
these as lower confidence and re-verify before citing directly in wiki copy.

---

## 1. What a harness is, precisely

**Definition (community consensus, not yet an Anthropic term of art):** the harness is
"every piece of code, configuration, and execution logic that isn't the model itself." A
raw model becomes an agent once a harness gives it state, tool execution, feedback loops,
and enforceable constraints. Shorthand: **Agent = Model + Harness**.
Source: Hugging Face glossary post, "Harness, Scaffold, and the AI Agent Terms Worth
Getting Right" — https://huggingface.co/blog/agent-glossary `[SEARCH-ONLY, summarized by search tool — did not fetch full page]`

**Simon Willison's operational definition of "agent"** (the primary source most worth
citing on the wiki): "An LLM agent runs tools in a loop to achieve a goal."
He unpacks the two load-bearing halves:
- "tools in a loop": "the LLM is given the ability to request actions to be executed by
  its harness, and the outcome of those tools is fed back into the model so it can
  continue to reason through and solve the given problem."
- "to achieve a goal": "these are not infinite loops — there is a stopping condition."
Source (fetched in full): https://simonw.substack.com/p/i-think-agent-may-finally-have-a
`[FETCHED]`

This is the cleanest primary-source framing for the wiki: **model** = the thing that
predicts the next token / decides what tool to call and with what arguments. **Harness**
= the surrounding program that actually executes that request, decides what goes into the
model's context on the next turn, enforces limits, and decides when to stop. **Agent** =
the combination running as a system.

Willison also notes the loop has memory built in "for free": "the 'tools in a loop' model
has a fundamental form of memory baked in: those tool calls are constructed as part of a
conversation with the model, and the previous steps in that conversation provide
short-term memory." Persistent (cross-session) memory needs "an extra set of tools" —
i.e., it's a harness feature, not a model feature. Same source. `[FETCHED]`

**What the harness owns, concretely** (cross-checked against Anthropic's own products):
- Tool dispatch — matching a model's tool-call request to real code and executing it.
- Context assembly — what system prompt, tool schemas, and history go into each API call.
- Session/state management — files like progress logs, git history, task-tracking state
  that persist across turns or across restarts.
- Permissions/approval gates — whether an action executes automatically or waits for a
  human (or a classifier) to approve it.
- Sandboxing — filesystem/network isolation for anything the model asks to execute.
- Retries and error surfacing — turning a failed tool call into an `is_error` result the
  model can react to.
- Subagent spawning — creating additional model instances with their own context windows
  for sub-tasks.
These are enumerated (in Claude Code's specific implementation) at
https://code.claude.com/docs/en/security and https://code.claude.com/docs/en/agent-sdk/overview.
`[FETCHED, both]`

---

## 2. Why the harness — not the model — dominates practical behavior and safety

Anthropic's own Agent SDK overview states this almost as a mission statement: the SDK
"gives you the same tools, agent loop, and context management that power Claude Code" —
i.e., Claude Code's usefulness is explicitly attributed to loop/tool/context engineering
that is reusable independent of which model sits inside it.
Source: https://code.claude.com/docs/en/agent-sdk/overview `[FETCHED]`

Anthropic's context-engineering guide makes the same point about tool design specifically:
"If a human engineer can't definitively say which tool should be used in a given
situation, an AI agent can't be expected to do better." — the harness's tool surface, not
raw model capability, sets the ceiling on decision quality.
Source: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents `[FETCHED]`

Anthropic's multi-agent research post is the strongest primary-source *evidence* (not just
claim) that harness-level architecture change alone moves outcomes: "a multi-agent system
with Claude Opus 4 as the lead agent and Claude Sonnet 4 subagents outperformed
single-agent Claude Opus 4 by 90.2% on our internal research eval." Same architecture
change also multiplies cost: "agents typically use about 4× more tokens than chat
interactions, and multi-agent systems use about 15× more tokens than chats." Both figures
are Anthropic's own internal eval numbers, not third-party benchmarks — cite as
self-reported.
Source: https://www.anthropic.com/engineering/multi-agent-research-system `[FETCHED]`

On safety specifically: Claude Code's security page frames essentially all of its safety
posture as harness-level controls (permission modes, sandboxing, working-directory
boundaries, network approval, isolated context windows for fetched web content) — none of
this is a model property; it is all enforced by the surrounding program regardless of
which model is answering. Source: https://code.claude.com/docs/en/security `[FETCHED]`
— full detail in section 3 below.

---

## 3. Common architectural pieces

### System prompt assembly
When you call the Claude API with a `tools` parameter, the API auto-constructs a system
prompt around your tool definitions. Anthropic publishes the literal template:

```
In this environment you have access to a set of tools you can use to answer the user's question.
{{ FORMATTING INSTRUCTIONS }}
String and scalar parameters should be specified as is, while lists and objects should use JSON format. Note that spaces for string values are not stripped. The output is not expected to be valid XML and is parsed with regular expressions.
Here are the functions available in JSONSchema format:
{{ TOOL DEFINITIONS IN JSON SCHEMA }}
{{ USER SYSTEM PROMPT }}
{{ TOOL CONFIGURATION }}
```
Source: https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools `[FETCHED]`

Anthropic's context-engineering guide separately recommends organizing hand-written system
prompts "into distinct sections (like background_information, instructions, tool
guidance, output description, etc) using XML tagging or Markdown headers," calibrated to
"the right altitude" — specific enough to steer behavior, general enough not to be brittle.
Source: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents `[FETCHED]`

### Tool/function schemas
A tool definition is `name` (regex `^[a-zA-Z0-9_-]{1,64}$`), `description` (plaintext,
Anthropic recommends 3–4+ sentences covering what it does, when to use/not use it, and
what each parameter means), and `input_schema` (a JSON Schema object). Example from the
docs:
```json
{
  "name": "get_weather",
  "description": "Get the current weather in a given location",
  "input_schema": {
    "type": "object",
    "properties": {
      "location": {"type": "string", "description": "The city and state, e.g. San Francisco, CA"},
      "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
    },
    "required": ["location"]
  }
}
```
Source: https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools `[FETCHED]`

Design guidance from Anthropic's applied-engineering post on tool-writing:
- Name parameters unambiguously: "instead of a parameter named `user`, try a parameter
  named `user_id`."
- Return only high-signal information: "tool implementations should take care to return
  only high signal information back to agents. They should prioritize contextual
  relevance over flexibility."
- Write actionable errors, not opaque codes/tracebacks — this steers the agent toward a
  fix rather than a repeat failure.
- Truncation and error-message design "can steer agents towards more token-efficient
  tool-use behaviors (using filters or pagination)."
Source: https://www.anthropic.com/engineering/writing-tools-for-agents `[FETCHED]`

### Tool-result feedback (the actual wire format)
This is the concrete mechanic of "outcome fed back into the model." Claude does **not**
use a separate `tool` role — tool results are `tool_result` content blocks inside a
`user`-role message:
```json
{
  "role": "user",
  "content": [
    {"type": "tool_result", "tool_use_id": "toolu_01A09q90qw90lq917835lq9", "content": "15 degrees"}
  ]
}
```
Hard formatting rules straight from the docs: tool_result blocks must immediately follow
their tool_use blocks with no messages in between; inside that user message, tool_result
blocks must come **before** any plain text. Errors are signaled with `"is_error": true`
plus an instructive message string (e.g. `"Rate limit exceeded. Retry after 60 seconds."`)
— Anthropic notes Claude "will retry 2-3 times with corrections before apologizing to the
user" on invalid tool calls.
Source: https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls `[FETCHED]`

Same page carries an explicit security note that is directly relevant to a cybersecurity
wiki: "Tool results often carry content from sources outside your control: web pages,
inbound email, user uploads, third-party APIs. Treat that content as untrusted... Keep
untrusted content inside `tool_result` blocks rather than `system` prompts or plain user
`text` blocks." This is Anthropic's own mitigation advice for indirect prompt injection at
the wire-format level. `[FETCHED]`

### Context compaction / summarization
Anthropic's context-engineering guide: as a conversation nears the context limit,
"compaction" distills history down — "the model preserves architectural decisions,
unresolved bugs, and implementation details while discarding redundant tool outputs." The
harness also supports **structured note-taking** outside the context window: agents
"regularly write notes persisted to memory outside of the context window. These notes get
pulled back into the context window at later times." Multi-agent designs use sub-agents
with **separate context windows** as a compression strategy — the lead agent gets back a
condensed summary (Anthropic's multi-agent post cites reports of roughly 1,000–2,000
tokens) rather than the sub-agent's full transcript.
Sources: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents `[FETCHED]`,
https://www.anthropic.com/engineering/multi-agent-research-system `[FETCHED]`

### File-system vs API tools / MCP as a standardization layer
Model Context Protocol (MCP) is Anthropic's open standard "for connecting AI applications
to external systems" — data sources, tools, and prompts/workflows. Official framing: "MCP
is like a USB-C port for AI applications... a standardized way to connect AI applications
to external systems," reducing bespoke integration work per tool/data source.
Source: https://modelcontextprotocol.io/introduction `[FETCHED]`

### Approval gates / human-in-the-loop and sandboxing/permissions
Claude Code's security docs are the most concrete primary source for this whole section.
Key mechanisms, quoted directly:
- "In Manual mode, Claude Code starts with read-only permissions. When Claude Code needs
  to edit files, run tests, or execute commands, it asks you first, and you choose whether
  to approve the action once or allow it from then on."
- Auto mode substitutes a classifier for the human: "a separate classifier model reviews
  actions instead of you and blocks the ones it judges unsafe."
- **Sandboxed bash tool**: "Sandbox bash commands with filesystem and network isolation,
  reducing permission prompts while maintaining security."
- **Working directory boundary**: in Manual mode "Claude Code can only write to the folder
  where it was started and its subfolders, and can't modify files in parent directories
  without explicit permission."
- **Isolated context windows**: "Web fetch uses a separate context window to avoid
  injecting potentially malicious prompts" — a harness-level mitigation for indirect
  prompt injection via fetched web content.
- **Trust verification**: "First-time codebase runs and new MCP servers require trust
  verification."
- Cloud execution: "Each cloud session runs in an isolated, Anthropic-managed VM,"
  network access "limited by default," git push "restricted to the current working
  branch," "All operations in cloud sessions are logged."
Source: https://code.claude.com/docs/en/security `[FETCHED]`

---

## 4. Failure modes specific to harnesses

**Context exhaustion.** Anthropic's own long-running-agent case study: the harness "would
run out of context in the middle of its implementation, leaving the next session to start
with a feature half-implemented and undocumented." Their fix was harness-level (structured
progress files, git history, feature-tracking JSON, compaction) — not a model change.
Source: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents `[FETCHED]`

**Premature/false completion ("one-shotting").** Same source: "After some features had
already been built, a later agent instance would look around, see that progress had been
made, and declare the job done" without verifying end-to-end — a harness/verification gap,
not a reasoning failure per se. `[FETCHED]`

**Runaway loops / unbounded cost.** Not explicitly named "runaway loop" in the fetched
Anthropic sources, but the mechanism is directly implied: Willison's definition requires
an explicit stopping condition ("these are not infinite loops — there is a stopping
condition") precisely because the loop has no natural termination without one built into
the harness. Source: https://simonw.substack.com/p/i-think-agent-may-finally-have-a `[FETCHED]`.
The Anthropic multi-agent post's token multipliers (4× for single agents, 15× for
multi-agent systems, vs. plain chat) are the concrete cost consequence of loop/subagent
architecture choices — cost scales with harness design, not just task difficulty. Source:
https://www.anthropic.com/engineering/multi-agent-research-system `[FETCHED]`

**Tool-result poisoning / prompt injection via tool output.** This is the harness's most
security-relevant failure mode, and there are two strong primary sources:

1. Anthropic's own handle-tool-calls docs: "Tool results often carry content from sources
   outside your control: web pages, inbound email, user uploads, third-party APIs. Treat
   that content as untrusted: an attacker who can influence it may embed instructions that
   try to redirect Claude (indirect prompt injection)." Source:
   https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls `[FETCHED]`

2. Simon Willison's "lethal trifecta" — the sharpest public framing of *when* this becomes
   exploitable, not just possible. Three conditions, and risk appears when a harness gives
   an agent all three simultaneously:
   - Access to private data.
   - Exposure to untrusted content ("any mechanism by which text ... controlled by a
     malicious attacker could become available to your LLM").
   - External communication ability (exfiltration channel — HTTP requests, APIs, etc.).
   Willison: "LLMs follow instructions in content" regardless of source, so combining all
   three means "an attacker can easily trick it into accessing your private data and
   sending it to that attacker." His stated primary mitigation is architectural avoidance
   — don't combine all three — rather than trusting a guardrail/classifier, because
   guardrails claiming "95% of attacks" blocked are not good enough for a security context.
   Source: https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/ `[FETCHED]`
   (Willison cites, without me independently fetching, the CaMeL paper as a promising
   research direction for structural mitigation — flag as `[SEARCH-ONLY]`/secondary if
   citing CaMeL specifics.)

Claude Code's own countermeasures against this exact failure mode (network command
approval requirement for `curl`/`wget`, isolated context window for web-fetched content,
"context-aware analysis" of requests) are documented at
https://code.claude.com/docs/en/security `[FETCHED]` — a real-world harness implementing
mitigations for the lethal-trifecta pattern.

---

## 5. Harness vs. a plain "chat with an API" script

The distinguishing feature is the loop plus feedback channel. A plain chat script sends
one message, gets one text response, done — there is no mechanism for the model to cause
an action in the world and see the result. The minimum viable **agent** loop, per
Anthropic's own docs, requires exactly these primitives:

1. Send a request with a `tools` array (JSON-schema tool definitions) alongside the
   `messages` history.
2. If the response's `stop_reason` is `tool_use`, extract `name`, `id`, `input` from the
   `tool_use` content block(s).
3. Execute the corresponding real function in your own code (this step is entirely outside
   the model — it is pure harness).
4. Send a new `user`-role message containing a `tool_result` block
   (`tool_use_id` + `content`, `is_error` on failure) immediately following the assistant's
   tool_use message, tool_result blocks first in the content array.
5. Repeat from step 1 until the model responds without requesting a tool (or the harness
   hits its own stop condition — turn limit, cost cap, task-complete signal).

Source for steps 1–4 (fetched, includes exact JSON shapes):
https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools and
https://platform.claude.com/docs/en/agents-and-tools/tool-use/handle-tool-calls `[FETCHED, both]`

Anthropic explicitly separates "implementing the tool loop yourself" (Client SDK — direct
API access) from "not implementing the tool loop yourself" (Agent SDK — the loop, context
management, permissions, and subagent support are provided for you). This is Anthropic's
own dividing line between a chat script and a harness:
> "Calling the API directly and implementing the tool loop yourself" → Client SDK, "You
> implement the tool loop yourself."
> vs. "Building an agent without implementing the tool loop yourself" → Agent SDK, "A
> library that runs the agent loop in your own process."
Source: https://code.claude.com/docs/en/agent-sdk/overview `[FETCHED]`

Concretely: a plain chat script is steps 1 and (implicitly) 5 with no tools array — one
request, one response, no state carried forward except literal message history you choose
to resend. A harness adds: tool dispatch (step 3), the feedback channel (step 4), a stop
condition, and — per section 3 above — context assembly rules, compaction, permissions,
and sandboxing around step 3. The model does not change between the two; everything that
changes is harness.

---

## UNVERIFIED / DO NOT PUBLISH

- The Hugging Face glossary post ("Harness, Scaffold, and the AI Agent Terms Worth Getting
  Right," https://huggingface.co/blog/agent-glossary) — used only via search-tool summary,
  not fetched directly. The "Agent = Model + Harness" shorthand and the harness definition
  quoted in section 1 should be re-verified against the live page before publishing as a
  direct quote.
- CaMeL (referenced by Willison as a mitigation direction for prompt injection) — not
  independently fetched; only know of it via Willison's secondary mention. Do not cite
  CaMeL's own claims without going to the paper directly.
- No number/statistic beyond the two Anthropic self-reported figures (90.2% eval
  improvement, 4×/15× token multipliers, both from
  https://www.anthropic.com/engineering/multi-agent-research-system) was used anywhere in
  these notes. Do not add other benchmark numbers found elsewhere (e.g. any figures from
  Databricks, Firecrawl, Parallel.ai, or other SEO/vendor blog posts surfaced by search —
  none of those pages were fetched, and none of their claims are used above) without
  fetching and checking the primary source first.
- "Agent harness" as a formal Wikipedia-recognized term — a Wikipedia page titled "Agent
  harness" appeared in search results but was not fetched or verified. Do not cite
  Wikipedia as authoritative for this fast-moving, informally-defined term; the definitions
  actually used above come from Willison and Anthropic/Claude Code docs instead.
- Several vendor blog posts (Olostep, Firecrawl, Parallel.ai, Databricks, dev.to pieces)
  surfaced heavily in search for "agent harness" — none were fetched or used as sources
  above because they are marketing/aggregator content rather than primary sources. If the
  wiki page wants a "who uses this term" survey, those would need individual fetching and
  scrutiny first.
