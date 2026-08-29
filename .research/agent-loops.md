# Research notes: The agent loop

Status: research notes only. Not site content. Written for whoever drafts the
wiki page on agentic loops.

Fetch status key: **[FETCHED]** = WebFetch pulled the actual page/paper and
quotes below are drawn from that content. **[SEARCH ONLY]** = only saw it in
search-result snippets, did not fetch the primary page directly — treat quotes
from these as lower-confidence paraphrase, not verbatim.

---

## 1. The basic loop

Vocabulary and mechanics, straight from Anthropic's own API docs for tool use
— this is the most precise, implementation-level description of "the loop"
available from a primary source.

**[FETCHED]** https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works

> "Tool use is a contract between your application and the model... The model
> never executes anything on its own. It emits a structured request, your
> code (or Anthropic's servers) runs the operation, and the result flows back
> into the conversation."

The canonical loop shape, quoted directly:

> "The canonical shape is a `while` loop keyed on `stop_reason`:
> 1. Send a request with your `tools` array and the user message.
> 2. Claude responds with `stop_reason: "tool_use"` and one or more `tool_use`
>    blocks.
> 3. Execute each tool. Format the outputs as `tool_result` blocks.
> 4. Send a new request containing the original messages, the assistant's
>    response, and a user message with the `tool_result` blocks.
> 5. Repeat from step 2 while `stop_reason` is `"tool_use"`."

> "The loop exits on any other stop reason (`"end_turn"`, `"max_tokens"`,
> `"stop_sequence"`, or `"refusal"`), which means Claude has either produced a
> final answer or stopped for another reason that your application should
> handle."

Note the vocabulary split: the piece of software driving the while-loop
(sending requests, executing tools, feeding results back) is not the model —
in agent-building circles this piece is commonly called the "harness." The
Anthropic docs don't use that word, but the mechanical role they describe
(steps 1, 3, 4 above) is exactly what "harness" refers to elsewhere.

Anthropic also documents a second variant, the **server-side loop**, where
tool execution happens on Anthropic's infrastructure rather than the caller's
loop:

> "This internal loop has an iteration limit. If the model is still iterating
> when it hits the cap, the response comes back with `stop_reason:
> "pause_turn"` instead of `"end_turn"`."

Anthropic's higher-level framing of what an agent *is*, from a separate blog
post (see §2 for full citation):

> "Agents: LLMs autonomously using tools in a loop."
— **[FETCHED]** https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents

**Where the "propose action → execute → observe → repeat" framing originates
academically**: this is the general shape used by the ReAct paper (§2) and by
classical RL agent-environment loops; ReAct is the specific paper that
popularized applying it to LLMs with interleaved natural-language reasoning.

---

## 2. Named loop patterns

### ReAct (reason + act)

**[FETCHED]** https://arxiv.org/abs/2210.03629 — "ReAct: Synergizing
Reasoning and Acting in Language Models," Shunyu Yao, Jeffrey Zhao, Dian Yu,
Nan Du, Izhak Shafran, Karthik Narasimhan, Yuan Cao. arXiv:2210.03629,
presented at ICLR 2023.

Abstract (exact quote):

> "While large language models (LLMs) have demonstrated impressive
> capabilities across tasks in language understanding and interactive
> decision making, their abilities for reasoning (e.g. chain-of-thought
> prompting) and acting (e.g. action plan generation) have primarily been
> studied as separate topics. In this paper, we explore the use of LLMs to
> generate both reasoning traces and task-specific actions in an interleaved
> manner, allowing for greater synergy between the two: reasoning traces help
> the model induce, track, and update action plans as well as handle
> exceptions, while actions allow it to interface with external sources, such
> as knowledge bases or environments, to gather additional information."

**One-line summary**: the model alternates writing a short "thought" and
taking an "action" (a tool/environment call), observing the result, and
repeating — the thought step is what lets it plan, notice things went wrong,
and revise, rather than acting blind.

**When it earns the extra calls**: any task where a single shot of reasoning
isn't enough because the model needs facts from outside its own head
(search, a knowledge base, code execution) *and* needs to keep revising its
plan as those facts come in — i.e., most real agentic tool-use tasks. This is
effectively the pattern underlying Anthropic's basic tool-use loop in §1.

### Plan-then-execute / plan-and-solve

Two related but distinct primary sources here — worth keeping straight:

**[SEARCH ONLY, abstract paraphrased from search snippets]**
"Plan-and-Solve Prompting: Improving Zero-Shot Chain-of-Thought Reasoning by
Large Language Models," Lei Wang, Wanyu Xu, Yihuai Lan, Zhiqiang Hu, Yunshi
Lan, Roy Ka-Wei Lee, Ee-Peng Lim. arXiv:2305.04091, ACL 2023.
https://arxiv.org/abs/2305.04091 — this is a *prompting* technique (single
model call structure), not a multi-call agent architecture: it splits a
reasoning prompt into "devise a plan" then "carry out the plan" as one
continuous generation, to fix calculation/missing-step/semantic errors in
zero-shot chain-of-thought.

**[SEARCH ONLY]** "Architecting Resilient LLM Agents: A Guide to Secure
Plan-then-Execute Implementations," arXiv:2509.08646,
https://arxiv.org/abs/2509.08646 — this is the multi-call *agent
architecture* sense of the term: a planner LLM call produces a full plan
(sequence of allowed tool calls) up front, then a separate executor
loop/module runs it, as opposed to interleaving planning and acting step by
step (contrast with ReAct). Search snippet also surfaced arXiv:2506.08837
("Design Patterns for Securing LLM Agents against Prompt Injections") citing
plan-then-execute as a prompt-injection defense, since the plan is fixed
before untrusted tool output ever reaches the model.

**One-line summary**: decide the whole sequence of steps before executing
any of them, instead of deciding one step at a time as ReAct does.

**When it's worth it**: tasks where the shape of the work is knowable in
advance (so a plan doesn't go stale) and where you want predictability, lower
cost (fewer back-and-forth model calls), and — per the security papers above
— resistance to a compromised tool result steering the model into
unplanned actions.

### Reflection / self-critique — Reflexion

**[FETCHED]** https://arxiv.org/abs/2303.11366 — "Reflexion: Language Agents
with Verbal Reinforcement Learning," Noah Shinn, Federico Cassano, Edward
Berman, Ashwin Gopinath, Karthik Narasimhan, Shunyu Yao. arXiv:2303.11366
(submitted March 2023, NeurIPS 2023).

> Reflexion agents "verbally reflect on task feedback signals, then maintain
> their own reflective text in an episodic memory buffer to induce better
> decision-making in subsequent trials."

Benchmark number, cited in-line per the rules (do not repeat this number
without this citation): "91% pass@1 accuracy on the HumanEval coding
benchmark, surpassing the previous state-of-the-art GPT-4 that achieves 80%"
— per arXiv:2303.11366.

**One-line summary**: after a failed attempt, the agent writes itself a
natural-language postmortem ("what went wrong, what to try differently") and
carries that text into the next attempt, instead of updating model weights.

**When it's worth it**: multi-try tasks where you get a pass/fail or scalar
signal per attempt (unit tests passing, a game score) and can afford multiple
attempts — the postmortem substitutes for gradient-based learning.

**Important caveat, from a different primary source**: reflection only works
when there's an outside signal to reflect *on*. When a model second-guesses
its own reasoning with no external check, it doesn't reliably improve:

**[FETCHED]** https://arxiv.org/abs/2310.01798 — "Large Language Models
Cannot Self-Correct Reasoning Yet," Jie Huang, Xinyun Chen, Swaroop Mishra,
Huaixiu Steven Zheng, Adams Wei Yu, Xinying Song, Denny Zhou. arXiv:2310.01798,
ICLR 2024.

> "In the context of reasoning, our research indicates that LLMs struggle to
> self-correct their responses without external feedback, and at times, their
> performance even degrades after self-correction."

This is the load-bearing distinction for §5 (verification): reflection/
self-critique needs a ground-truth signal from outside the model (test
results, a second independent check) to be reliable — an LLM grading its own
unaided reasoning is not a substitute.

### Evaluator-optimizer, orchestrator-workers, routing, chaining, parallelization

**[FETCHED]** https://www.anthropic.com/research/building-effective-agents —
Anthropic engineering blog, "Building Effective Agents." This is the primary
source for all five of these named patterns as a set; it is the piece that
put this specific vocabulary into wide circulation.

Anthropic's foundational framing (worth quoting because the wiki page should
get this distinction right):

> Workflows are "systems where LLMs and tools are orchestrated through
> predefined code paths." Agents are "systems where LLMs dynamically direct
> their own processes and tool usage, maintaining control over how they
> accomplish tasks."

**Prompt chaining** — decompose a task into a fixed sequence of LLM calls,
each processing the previous call's output, with programmatic checks
("gates") in between.
> "ideal for situations where the task can be easily and cleanly decomposed
> into fixed subtasks" — trades latency for accuracy.
Example given: draft marketing copy, then translate it.

**Routing** — classify the input first, then send it down one of several
specialized paths.
> "works well for complex tasks where there are distinct categories that are
> better handled separately."
Example given: routing different classes of customer-service queries to
different specialized flows, or routing by difficulty to differently-sized
models.

**Parallelization** — run multiple LLM calls at once and aggregate
programmatically. Two sub-variants named: **sectioning** (split into
independent subtasks run in parallel) and **voting** (run the same task
multiple times for diverse takes, then combine).
> "effective when the divided subtasks can be parallelized for speed, or when
> multiple perspectives or attempts are needed."
Examples given: parallel guardrail-screening + response-generation; multiple
independent code reviews for vulnerabilities.

**Orchestrator-workers** — a central LLM call breaks a task into
sub-components *dynamically* (not pre-defined), delegates each to a worker
LLM call, and synthesizes the results.
> "well-suited for complex tasks where you can't predict the subtasks
> needed." Anthropic's own coding agents use this for multi-file GitHub
> issue fixes.
Distinguishing feature vs. parallelization: subtasks aren't fixed in advance,
the orchestrator decides them per-input.

**Evaluator-optimizer** — one LLM call generates a candidate response, a
second LLM call evaluates it and gives feedback, looped until acceptable.
> "particularly effective when we have clear evaluation criteria, and when
> iterative refinement provides measurable value."
Example given: literary translation refinement.

**Autonomous agents (the loop pattern proper)** — distinguished from all the
above workflow patterns by being open-ended rather than a fixed code path:

> "During execution, it's crucial for the agents to gain 'ground truth' from
> the environment at each step (such as tool call results or code
> execution)."
> "it's also common to include stopping conditions (such as a maximum number
> of iterations) to maintain control."
> "Agents can then pause for human feedback at checkpoints or when
> encountering blockers."
> Best suited for "open-ended problems where it's difficult or impossible to
> predict the required number of steps" — i.e. "where you can't hardcode a
> fixed path." Examples: solving SWE-bench GitHub issues, computer-use tasks.

This single Anthropic post is the cleanest one-stop primary source for
questions 2, 3, and 6 of the assignment simultaneously (patterns, stop
conditions, human-in-the-loop) — worth reading in full when drafting.

---

## 3. Stop conditions

Primary-source material on stop conditions is thinner than the rest — most of
what's out there is secondary blog commentary, not papers or vendor docs with
precise claims. What's verifiable:

- **Turn/iteration limits**: directly documented by Anthropic for the
  server-side tool loop — **[FETCHED]**
  https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works:
  "This internal loop has an iteration limit. If the model is still iterating
  when it hits the cap, the response comes back with `stop_reason:
  "pause_turn"` instead of `"end_turn"`."
- **Goal checks / stopping conditions generally**: Anthropic, "Building
  Effective Agents" (see §2 citation): "it's also common to include stopping
  conditions (such as a maximum number of iterations) to maintain control."
- **The client-side loop's natural stop signal** is the API's `stop_reason`
  field itself — the loop in §1 runs `while stop_reason == "tool_use"` and
  exits on `end_turn`, `max_tokens`, `stop_sequence`, or `refusal`. That's a
  goal-check-by-proxy: the model itself signals "I'm done" via `end_turn`.
- **Budget limits** (token/cost caps) are a standard operational control but
  I did not find a primary source spelling this out distinctly from turn
  limits — flagging as thin coverage rather than fabricating a citation.
- **"Loop until dry"**: searched for this as a named pattern/phrase. Did not
  find a primary source using this exact phrase — it does not appear to be
  an established term of art, just descriptive language for "keep going
  until there's nothing left to do." Treat as a paraphrase, not a citable
  term. See UNVERIFIED section.
- **What happens with no stop condition**: not something a primary vendor
  source states directly (nobody documents "if you don't do this, X breaks,"
  as a numbered claim) — but it follows logically from the loop mechanics in
  §1: without a stop condition the `while stop_reason == "tool_use"` loop has
  no exit clause other than the model eventually choosing `end_turn` on its
  own, which is not guaranteed. This is an inference from the documented
  mechanics, not a separately-cited claim — flag it as such when writing.

---

## 4. Context management inside the loop

**[FETCHED]** https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
— Anthropic engineering blog, "Effective context engineering for AI agents."
Released alongside Claude Sonnet 4.5 (per search-result framing, dated
September 2025 — that dating is **[SEARCH ONLY]**, not independently
confirmed by fetching the article's own byline/date, so treat the specific
month as unverified).

**Definition, exact quote:**

> "Context engineering refers to the set of strategies for curating and
> maintaining the optimal set of tokens (information) during LLM inference,
> including all the other information that may land there outside of the
> prompts."

Framed as the question: "what configuration of context is most likely to
generate our model's desired behavior?"

**Why the loop degrades as context fills** — this is the "context rot"
mechanism, tied to the transformer architecture itself:

> "As the number of tokens in the context window increases, the model's
> ability to accurately recall information from that context decreases."

> "LLMs are based on the transformer architecture, which enables every token
> to attend to every other token across the entire context. This results in
> n² pairwise relationships for n tokens."

> "Models develop their attention patterns from training data distributions
> where shorter sequences are typically more common than longer ones."

The post is explicit that this isn't a cliff but a gradient: "diminishing
marginal returns" — the model doesn't suddenly break, it shows "reduced
precision for information retrieval" as the window fills. Important nuance
for the wiki: don't overstate this as "the agent breaks at token N" — the
source explicitly frames it as continuous degradation, not a hard failure
threshold.

**Compaction**, defined exactly:

> "Compaction is the practice of taking a conversation nearing the context
> window limit, summarizing its contents, and reinitiating a new context
> window with the summary."

Implementation guidance quoted:

> "Carefully tuning your prompt on complex agent traces. Start by maximizing
> recall to ensure your compaction prompt captures every relevant piece of
> information from the trace."

This directly connects to the agent loop: every iteration of the loop in §1
appends more tool calls and tool results to the context, so a long-running
agent loop is exactly the scenario that produces context rot — compaction
(or other context-engineering strategies the same post likely covers, e.g.
tool-result trimming, sub-agent isolation) is the mitigation.

---

## 5. Verification inside the loop

No single vendor doc treats "verification" as its own named pattern, but
three already-fetched primary sources combine to make the point cleanly —
worth synthesizing rather than treating as one citation:

1. **External ground truth beats no ground truth.** Anthropic's own
   description of what makes autonomous agents work at all (§2 citation,
   "Building Effective Agents"): "it's crucial for the agents to gain
   'ground truth' from the environment at each step (such as tool call
   results or code execution)." A test suite passing/failing, a linter
   erroring, code actually executing — these are ground truth. Model
   self-assessment in prose is not.
2. **A second model call checking the first is the evaluator-optimizer
   pattern** (§2): "particularly effective when we have clear evaluation
   criteria" — i.e., it works when the evaluator has something concrete to
   check against, not vibes.
3. **Unaided self-correction (no external signal) does not reliably work.**
   arXiv:2310.01798 (§2 citation), directly on point: "LLMs struggle to
   self-correct their responses without external feedback, and at times,
   their performance even degrades after self-correction."

Put together, the throughline for the wiki page: an agent that "checks its
own work" only behaves differently/better than one that doesn't when the
check has access to something outside the model's own generation — a test
result, a linter's exit code, a second independent evaluation with defined
criteria. An agent asking itself "are you sure?" with nothing external to
check against is not verification in any sense the sources above support.

---

## 6. Human-in-the-loop

**[FETCHED]** Anthropic, "Building Effective Agents" (§2 citation):

> "Agents can then pause for human feedback at checkpoints or when
> encountering blockers."

**[FETCHED]** https://developers.openai.com/api/docs/guides/agents/guardrails-approvals
— OpenAI, Agents SDK docs, "Guardrails and human review." This is a
concrete, mechanism-level description of an approval gate, useful as a
second vendor's implementation of the same idea:

> "Approvals are the human-in-the-loop path for tool calls. The model can
> still decide that an action is needed, but the run pauses until you
> approve or reject it."

Mechanism, quoted in sequence:

> "The run records an approval interruption instead of executing the tool."
> "The result returns `interruptions` plus a resumable `state`."
> "Your application approves or rejects the pending items."
> "You resume the same run from `state` instead of starting a new user
> turn."

For long reviews: "If the review might take time, serialize `state`, store
it, and resume later. That's still the same run."

**Placement guidance, quoted exactly** — this is the most directly useful
line for the "where do you put the gate" part of the ask:

> "If you need checks around every custom tool call in a manager-style
> workflow, don't rely only on agent-level input or output guardrails. Put
> validation next to the tool that creates the side effect."

Read together with the loop mechanics from §1: the natural place for an
approval gate is the moment between step 2 (model emits a `tool_use` block)
and step 3 (your harness executes it) — i.e., right before the side-effecting
action runs, not before or after the whole agent turn. OpenAI's line above
makes that explicit ("next to the tool that creates the side effect") rather
than at the outer workflow boundary.

---

## UNVERIFIED / DO NOT PUBLISH

- **"Loop until dry"** as a named term of art. Could not find any primary
  source (paper, vendor doc, or named author's own writing) using this exact
  phrase as an established pattern name. Search results only produced
  generic secondary "AI agent loop" explainer blogs (Atlan, Oracle blogs,
  MindStudio) paraphrasing the general concept of iterating until a resource
  or task queue is exhausted. If the wiki page wants this phrase, attribute
  it as informal/descriptive language, not a citable pattern name — or drop
  it in favor of "iterate until no more work remains" / "run to
  exhaustion," described plainly.
- **Exact publication month of Anthropic's context-engineering post**
  (search snippets said "September 2025, released alongside Claude Sonnet
  4.5") — this was seen only in search-result summaries, not confirmed by
  reading a byline/dateline on the fetched page itself. Don't cite the month
  without checking the page's own dateline first.
- **OpenAI Agents SDK human-in-the-loop guide**
  (https://openai.github.io/openai-agents-js/guides/human-in-the-loop/) — a
  WebFetch of this exact URL returned only navigation chrome, no article
  body; I substituted developers.openai.com's "Guardrails and human review"
  page instead, which *did* fetch cleanly and is quoted above. Don't
  attribute the human-in-the-loop quotes in §6 to the .github.io guide — they
  came from developers.openai.com/api/docs/guides/agents/guardrails-approvals.
- **No number/statistic beyond the two explicitly cited in-line** (Reflexion's
  91%/80% HumanEval comparison, cited with its source in §2) is used anywhere
  in these notes. Do not add other benchmark numbers from secondary sources
  without independently fetching and citing the primary paper.
- **Plan-and-Solve (arXiv:2305.04091) and the plan-then-execute agent
  architecture papers (arXiv:2509.08646, arXiv:2506.08837)** were reviewed
  via WebSearch snippets only, not fetched directly — the summaries above
  are paraphrase of search-engine summaries, not verified quotes. Fetch the
  actual PDFs/abstracts before quoting anything from them verbatim in
  published content.
