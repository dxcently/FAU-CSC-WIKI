# Coding-agent harnesses — research notes

Compiled 2026-08-29 for FAU Cybersecurity Club president's request. Research
only — no site content was touched.

**Methodology note (read this first):** initial `WebSearch` and `WebFetch`
calls returned inconsistent, sometimes contradictory summaries (e.g. one pass
claimed opencode's repo is `github.com/sst/opencode`, another said
`anomalyco/opencode`; OpenClaw was described two different ways in two
fetches). Rather than trust the AI-generated search/fetch summaries at face
value, every tool below was cross-checked against the **raw GitHub REST API**
(`api.github.com/repos/<owner>/<repo>`) and, where relevant, the **raw
LICENSE/README file contents** via `raw.githubusercontent.com`. That's ground
truth: it returns the actual repo metadata GitHub itself serves, not a
model's paraphrase of a page. Anything below sourced only from a search
summary is labeled as such.

---

## 1. opencode

1. **What it is:** Open-source AI coding agent with a terminal UI (TUI),
   desktop app, and IDE extension.
2. **Who makes it / repo:** Originally built by the SST (Serverless Stack)
   team; the org has since rebranded to **Anomaly**. Repo:
   `https://github.com/anomalyco/opencode` (the old `sst/opencode` URL now
   **301-redirects** here — confirmed via `curl -I`). Site: https://opencode.ai
3. **License:** **MIT.** Confirmed via GitHub API
   (`license.spdx_id: "MIT"`) on `anomalyco/opencode`. FETCHED.
4. **Where it runs:** Terminal (primary), desktop app (macOS/Windows/Linux,
   marked BETA in the README), and IDE extension. Not a cloud/hosted product
   per se.
5. **Model-agnostic:** Yes. Site copy: "connect any model from any provider,
   including Claude, GPT, Gemini and more," via 75+ providers through
   Models.dev, including local models. FETCHED (opencode.ai).
6. **Distinguishing feature:** Multi-surface single codebase (same agent as
   terminal TUI, desktop app, and IDE extension) with very broad
   provider/model support out of the box.

Sources (FETCHED): `https://opencode.ai/`,
`https://api.github.com/repos/anomalyco/opencode`,
`https://raw.githubusercontent.com/anomalyco/opencode/dev/README.md`,
redirect check on `https://github.com/sst/opencode`.

---

## 2. OpenClaw

**Existence: CONFIRMED — but it is NOT primarily a coding agent.** Flag this
to the president: OpenClaw is a general-purpose **personal AI assistant /
multi-channel gateway**, not a coding-agent harness in the same category as
the other four. It can be given coding tools, but that's not its core
identity.

1. **What it is:** A self-hosted "Gateway" that connects LLMs, tools, and
   messaging channels (WhatsApp, Telegram, Slack, Discord, Signal, iMessage,
   etc.) plus optional companion apps, for a single operator or a trusted
   team. README's own framing: "trusted gateway, untrusted execution,
   deterministic policy."
2. **Who makes it / repo:** "Developed in the open by the OpenClaw
   Foundation" (per docs site). Repo: `https://github.com/openclaw/openclaw`.
   Docs: https://docs.openclaw.ai/. Site: https://openclaw.ai
3. **License:** LICENSE file text is standard **MIT** (fetched raw:
   "MIT License / Copyright (c) 2026 OpenClaw Foundation..."), **but** the
   GitHub API's automated license detector flags the repo as
   `license.key: "other"` / `spdx_id: "NOASSERTION"` rather than a clean
   MIT match — most likely because the LICENSE file appends a non-standard
   sentence ("Third-party notices ... recorded in THIRD_PARTY_NOTICES.md")
   that breaks exact-template matching. Net effect: it reads as MIT, but
   don't cite it as a clean SPDX-verified MIT repo without that caveat.
   FETCHED both the API response and the raw LICENSE file.
4. **Where it runs:** Self-hosted, cross-platform installer (macOS, Linux,
   Windows via installer script; also npm/Docker/Nix per docs). Has a CLI,
   TUI, web "Control UI," and companion apps — not a traditional single
   "terminal or IDE" tool, more of a background daemon/gateway.
5. **Model-agnostic:** Yes — README states it "works with hosted and local
   model providers."
6. **Distinguishing feature:** It's chat-platform-native — the whole design
   center is being reachable from WhatsApp/Telegram/Slack/etc. rather than
   living in a terminal or editor, which sets it apart from every other tool
   on this list.

Sources (FETCHED): `https://docs.openclaw.ai/`,
`https://raw.githubusercontent.com/openclaw/openclaw/main/README.md`,
`https://raw.githubusercontent.com/openclaw/openclaw/main/LICENSE`,
`https://api.github.com/repos/openclaw/openclaw`, GitHub search API
(`api.github.com/search/repositories?q=openclaw`).

Note: earlier `WebSearch` results also surfaced several arXiv papers with
"OpenClaw" in the title (safety/forensics analyses). Those were **not
fetched or verified** — listed in the UNVERIFIED section below.

---

## 3. hermes-agent

**Existence: CONFIRMED — and yes, it is a different thing from the Nous
Research "Hermes" model family**, exactly as flagged in the task. Nous
Research's Hermes models (Hermes 2/3/4 etc., fine-tunes of Llama/Mistral/
Qwen bases) are LLMs. `hermes-agent` is a separate, newer product: an agent
*harness* built by the same company that can be pointed at Hermes models or
any other model.

1. **What it is:** "The self-improving AI agent built by Nous Research" —
   a general-purpose agent with a persistent memory/skill-learning loop,
   not a coding-agent-only tool (though it explicitly can "spawn Claude Code
   or Codex for heavy coding tasks," per an earlier search summary — that
   specific claim was seen only in a search snippet, not fetched from the
   README itself, so treat it as UNVERIFIED).
2. **Who makes it / repo:** Nous Research. Repo:
   `https://github.com/NousResearch/hermes-agent`. Docs/site:
   https://hermes-agent.nousresearch.com
3. **License:** **MIT.** Confirmed both via GitHub API
   (`license.spdx_id: "MIT"`) and the README badge/text pointing to the
   LICENSE file. FETCHED.
4. **Where it runs:** CLI/TUI plus chat platforms (Telegram, Discord, Slack,
   WhatsApp, Signal) via a gateway process, and multiple sandboxed backends
   (local, Docker, SSH, Singularity, Modal, Daytona, Vercel Sandbox) — so
   effectively terminal + chat + cloud/serverless.
5. **Model-agnostic:** Yes, explicitly. README: "Use any model you want —
   Nous Portal, OpenRouter, OpenAI, your own endpoint, and many others.
   Switch with `hermes model` — no code changes, no lock-in."
6. **Distinguishing feature:** Persistent, self-writing skill/memory system
   ("closed learning loop") that improves across sessions — none of the
   other four tools claim this kind of long-term self-modification.

Sources (FETCHED): `https://raw.githubusercontent.com/NousResearch/hermes-agent/main/README.md`,
`https://api.github.com/repos/NousResearch/hermes-agent`, GitHub search API.

---

## 4. Claude Code

1. **What it is:** Anthropic's agentic coding tool that runs in the
   terminal, understands a codebase, and executes coding tasks via natural
   language.
2. **Who makes it / repo:** Anthropic. Repo:
   `https://github.com/anthropics/claude-code`. Docs:
   https://code.claude.com/docs/en/overview
3. **License: proprietary / source-available terms, NOT open source.**
   Raw `LICENSE.md` content (fetched directly): *"© Anthropic PBC. All
   rights reserved. Use is subject to Anthropic's Commercial Terms of
   Service."* GitHub's API also reports `license: None` (no SPDX license
   detected) — consistent with "all rights reserved." The public repo holds
   docs, plugins, and examples; the CLI binary/agent itself is closed-source
   and distributed as a compiled package (installer script / npm / Homebrew
   / WinGet), not buildable from this source tree.
4. **Where it runs:** Terminal (primary), IDE (VS Code/JetBrains
   integrations), and cloud/CI via `@claude` GitHub mentions/Actions — all
   three surfaces, per the README ("Use it in your terminal, IDE, or tag
   @claude on Github").
5. **Model-agnostic: No — locked to Anthropic's Claude models.** There is
   no multi-provider model switch; it is Anthropic's product for Anthropic's
   models.
6. **Distinguishing feature:** Deepest single-vendor integration of any tool
   here — same company controls the model, the harness, and the commercial
   terms, with official first-party IDE and GitHub-Actions integrations
   rather than community-built ones.

Sources (FETCHED): `https://raw.githubusercontent.com/anthropics/claude-code/main/README.md`,
`https://raw.githubusercontent.com/anthropics/claude-code/main/LICENSE.md`,
`https://api.github.com/repos/anthropics/claude-code`.

---

## 5. Codex (OpenAI Codex CLI) — and why it's NOT the same as "OpenAI Codex" the model

**Two different things share the "Codex" name — do not conflate them:**

- **OpenAI Codex (2021, language model):** a code-generation LLM
  (`code-davinci` family) that powered early GitHub Copilot. It was a
  *model*, not an agent/harness, and OpenAI deprecated/shut down API access
  to it in March 2023. It has no relationship to the tool below beyond the
  shared name.
- **Codex CLI (2025–, coding agent / harness):** the thing actually meant
  by "Codex" in this list. Per Wikipedia's "Codex (AI agent)" article
  (fetched): released April 16, 2025 as "an open source coding tool for
  terminals," and the article explicitly cross-references the separate
  "OpenAI Codex (language model)" article to keep the two apart.

Details for Codex CLI:

1. **What it is:** "A coding agent from OpenAI that runs locally on your
   computer" — a lightweight terminal coding agent, with IDE extensions
   (VS Code/Cursor/Windsurf), a desktop app, and a separate cloud-hosted
   variant ("Codex Web" at chatgpt.com/codex).
2. **Who makes it / repo:** OpenAI. Repo: `https://github.com/openai/codex`
3. **License: Apache-2.0 — genuinely open source.** Confirmed via GitHub
   API (`license.spdx_id: "Apache-2.0"`). FETCHED.
4. **Where it runs:** All three — terminal CLI, IDE extension, and cloud
   (Codex Web / Codex App), per the README's own routing text at the top.
5. **Model-agnostic: No — built around OpenAI's models,** used either via a
   ChatGPT plan sign-in (Plus/Pro/Business/Edu/Enterprise) or an OpenAI API
   key. No first-party support for third-party model providers, unlike
   opencode/hermes-agent/OpenClaw.
6. **Distinguishing feature:** Tightest coupling to a single company's
   *product* ecosystem (ChatGPT plans, not just API billing) — you can pay
   for it through a ChatGPT subscription rather than needing a separate API
   key, which none of the others offer.

Sources (FETCHED): `https://raw.githubusercontent.com/openai/codex/main/README.md`,
`https://api.github.com/repos/openai/codex`,
`https://en.wikipedia.org/wiki/Codex_(AI_agent)`.

---

## Other notable OPEN SOURCE agent harnesses (verified via GitHub API)

All of the below were checked directly against `api.github.com/repos/...`
for current org/license — several had moved/renamed since older references,
noted where relevant.

| Tool | Repo (current) | License | Note |
|---|---|---|---|
| **Aider** | `Aider-AI/aider` | Apache-2.0 | Terminal-only "AI pair programming" tool; one of the older/most established in this space. Model-agnostic (works with most LLM APIs). |
| **Goose** | `aaif-goose/goose` | Apache-2.0 | Originally `block/goose` (Block, formerly Square) — that URL now 301-redirects to the new org. "An open source, extensible AI agent that goes beyond code suggestions." Model-agnostic. |
| **Cline** | `cline/cline` | Apache-2.0 | "Autonomous coding agent as an SDK, IDE extension, or CLI assistant" — VS Code-extension-first, unlike the terminal-first tools above. |
| **OpenHands** (formerly OpenDevin) | `OpenHands/OpenHands` | MIT | Org also renamed: old `All-Hands-AI/OpenHands` reference now resolves under the `OpenHands` org. Broader "AI software developer" framework with a sandboxed execution environment, not just a CLI. |
| **Continue** | `continuedev/continue` | Apache-2.0 | Self-described "open-source coding agent," IDE-extension-centric (VS Code/JetBrains), model-agnostic. |

All five of the above are genuinely OSI-license open source (Apache-2.0 or
MIT), confirmed via GitHub API license field — unlike Claude Code, which is
not open source, and OpenClaw, whose LICENSE text is MIT but whose GitHub
license-detector flags it as non-standard (see caveat above).

---

## UNVERIFIED / DO NOT PUBLISH

Do not put any of the following in wiki content without independent
verification — these were only seen in `WebSearch` result snippets/summaries
and were never fetched or cross-checked against a primary source:

- Any star counts, contributor counts, or "N million monthly developers"
  figures for any tool (opencode "195k/202k stars," OpenClaw "100k stars in
  a week" / "360k+ stars, 6th most-starred repo on GitHub," hermes-agent
  "237k stars," etc.). GitHub API did return live star counts during this
  research (opencode ~202k, OpenClaw ~388k, hermes-agent ~238k, Codex CLI
  ~120k, Claude Code ~143k) but star counts change constantly and are not
  something a wiki page should hardcode — if you want a number, pull it live
  or don't quote one.
- The claim that hermes-agent "can spawn Claude Code or Codex for heavy
  coding tasks and bring results back into its own memory" — plausible given
  its architecture, but seen only in a search-summary paraphrase, not in the
  fetched README excerpt.
- Several arXiv paper titles referencing "OpenClaw" in safety/forensics
  contexts (e.g. "Your Agent, Their Asset: A Real-World Safety Analysis of
  OpenClaw") — titles only, not read. If the club wants to cite security
  research about OpenClaw specifically, fetch and read those papers first;
  do not cite by title alone.
- Any characterization of "Anomaly" (opencode's parent org) as a company —
  only saw a copyright line ("©2026 Anomaly, anoma.ly"), didn't dig into
  who/what Anomaly is.

## Confirmation summary (for the five named tools)

| Tool | Exists? | Category caveat |
|---|---|---|
| opencode | **CONFIRMED** | Genuine coding-agent harness, MIT, model-agnostic |
| OpenClaw | **CONFIRMED** | Real project, but general personal-assistant gateway, not primarily a coding agent — flag this before including it alongside the other four |
| hermes-agent | **CONFIRMED, and distinct from Nous's "Hermes" model family** | Real, separate product from the Hermes LLMs; general-purpose agent (memory/skills focus), can reportedly delegate to coding-specific agents |
| Claude Code | **CONFIRMED** | Real, but proprietary — not open source, contrary to how it might get lumped in with the others |
| Codex (Codex CLI) | **CONFIRMED, and distinct from the 2021 "OpenAI Codex" model** | Real, genuinely open source (Apache-2.0), the model of the same name is unrelated and deprecated since 2023 |
