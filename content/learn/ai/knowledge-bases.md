+++
title = "Knowledge Bases as Agent Context"
weight = 4
description = "Knowledge graphs against vector retrieval in plain terms, and what document structure actually helps an agent — with this wiki as the worked example."
icon = "fa-solid fa-book"
+++

An agent is only as good as what it can read. A model knows what was in its
training data and nothing about your club, your lab, or the incident you are
working. Getting the right information in front of it is most of the
engineering.

There are two ways to do that, and a great deal of marketing about which one
wins. This page gives the plain version, then covers the part you can act on
today: how to structure documents so an agent can use them.

---

## Two Ways To Retrieve

### Vector retrieval

An **embedding** turns a piece of text into a list of numbers. Texts with
similar meaning get similar numbers. To answer a question, you embed the
question, find the stored chunks whose numbers are nearest, and paste those
chunks into the prompt.

That last step has a name: **retrieval-augmented generation** (RAG). Search a
corpus, put the hits in the prompt, ask the question.

Vector retrieval answers one question well: does this chunk of text sound like
the question. It knows nothing about how two chunks relate.

### Knowledge graphs

A **knowledge graph** stores entities as nodes and explicit relationships as
edges. `(web server) -[runs]-> (nginx 1.24)` and
`(nginx 1.24) -[affected by]-> (CVE-2024-XXXX)`.

The structure is asserted by whoever built the graph. It is not inferred from
similarity. That is the whole difference: a graph knows that two things are
connected and how, even when the two documents describing them share no
wording at all.

### When each one wins

**Vector retrieval wins** on a flat corpus of documents where most questions
are lookups. It needs no schema, it adapts to whatever document types you
throw at it, and standing one up is a short job. It also catches loose
similarity a graph has no edge for.

**A knowledge graph wins** when the corpus has real relational structure — who
reports to whom, what depends on what, what caused what — and the questions
are **multi-hop**, meaning the answer requires following two or more links.
"Which of our hosts run a service affected by this advisory" is a multi-hop
question. Vector search will find you documents that sound relevant and miss
the connection.

Graphs also give you an auditable answer. You can see the exact path the
system walked to reach a conclusion. A similarity score does not explain
itself.

### The honest tradeoffs

Building a graph means deciding what the entity types are and what
relationships exist between them. That work is the cost, and it is much larger
than setting up vector search.

Extraction is also lossy. Turning a paragraph into entity-and-relationship
triples throws away context the paragraph carried. A graph is a summary of
your source material, with the same risks as any summary.

### What is marketing

Two claims to distrust.

**"Graphs replace vector search."** In practice most working systems use
both — vector search finds candidate entry points, graph traversal expands
from there. Hybrid is the credible consensus, not one side winning.

**Any win-rate percentage you see quoted secondhand.** Numbers comparing the
two approaches trace back to specific benchmark papers under specific
conditions. Read the paper before you repeat the number. This wiki does not
publish one for exactly that reason.

The tooling is worth knowing about.
[GraphRAG](https://microsoft.github.io/graphrag/) is an open-source
implementation that extracts a graph from raw text, builds a hierarchy of
communities, and summarizes them, so it can answer questions about a whole
corpus rather than one matching chunk. Its own documentation is upfront that
running it on your data out of the box "may not yield the best possible
results." Tuning is the job.

---

## Documents As Agent Context

Now the part that matters more for a club wiki than any retrieval strategy.

A human skims a page, finds the heading that looks right, and ignores the
rest. An agent cannot skim cheaply. It either loads a whole page it did not
need and burns context on it, or it needs enough external structure to decide
it can skip the page without reading it.

Structure is what makes skipping possible. That is the entire argument.

### What actually helps

**One topic per page.** Published guidance on
[context engineering for agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
makes the point about tools, and it transfers exactly: if a human engineer
cannot say which of two options applies, an agent will not do better. Two
pages with overlapping scope create that ambiguity.

**Stable URLs.** The same guidance recommends just-in-time retrieval — an
agent keeps lightweight identifiers such as file paths and links, and loads
the content at runtime instead of pre-loading everything. A link that stops
resolving breaks that. Renaming a page is not a cosmetic change.

**Explicit headings, used consistently.** Markdown headers delineate sections,
and an agent uses them the same way a table of contents works for you. Keep
the same heading structure across similar pages so the shape is predictable.

**Metadata the machine can read.** Title, ordering, and a one-line
description, stored in a fixed format, give an index that does not require
reading the body.

**Cross-links instead of duplication.** Copying a paragraph to a second page
creates two answers to the same question, and neither the agent nor the reader
knows which one is current. Link.

**Plain Markdown alongside the rendered page.** Navigation, styling and
scripts are context an agent pays for and gets nothing from.

### llms.txt

There is an emerging convention for this.
[llms.txt](https://llmstxt.org/) is a plain Markdown index file at the root of
a site, proposed by Jeremy Howard, "to provide information to help agents use
a website" instead of making them crawl the HTML.

The format is simple: an H1 title, a one-line summary as a blockquote, then
H2 sections listing pages as `[name](url): details`. The specification also
recommends serving a plain `.md` version of every page.

Copy the idea whether or not you adopt the file. Keep an index. Keep the URLs
stable. Serve clean text.

### One protocol worth knowing by name

`llms.txt` is a static file. The **Model Context Protocol** (MCP) is the live
counterpart: one standard way for an application to expose data and tools to a
model, instead of a custom integration per data source.

It matters when you want an agent to query a knowledge base — search it, pull
one section — rather than read a page it was handed. A static site does not
need one. Know the term exists and move on.

---

## This Wiki As The Worked Example

Everything above describes this site, which is a convenient accident and a
useful thing to look at.

- **The directory structure is the URL structure is the navigation.** A page
  at `content/learn/linux/permissions.md` is served at
  `/learn/linux/permissions/`. Paths are stable because moving a file moves a
  URL, and everyone here knows it.
- **One topic per page.** Sections get an `_index.md`, every other topic gets
  its own file. The Linux pages do not explain networking.
- **Front matter is the machine-readable index.** Every page carries a title,
  a weight for ordering, and a one-sentence description. The site builds its
  entire navigation and its card grids from those fields — no menu file
  exists. The same fields tell an agent what a page is without opening it.
- **Cross-links, not duplication.** The Learn pages explain concepts. The
  [Toolbox](/toolbox/) pages cover practical use. Each links to the other and
  neither repeats it. That is why this page sends you to
  [Choosing an AI Model](/toolbox/ai/) instead of restating it.
- **Content is Markdown on disk.** The rendered site is for you. The source
  files are clean text an agent can read directly from the repository.
- **There is an `AGENTS.md` at the repository root.** It states the rules for
  anything editing this wiki: what may be published, the writing style, the
  file format, and the sourcing rule that no number or date ships without a
  primary source cited inline.

That last file is the part worth copying. The pages in this section were
drafted with agent help under those rules, and the rules are what made the
result reviewable. Structure is not decoration. It is what lets a person check
the work.

---

## If You Build One

Start with structure and stable paths. You can change retrieval strategy
later — swapping vector search for a graph is a weekend. A corpus with no
structure stays hard forever.

Then read [Agentic Graphs](agentic-graphs/) for how the retrieval step fits
into a larger system, and [AI on Both Sides](blue-and-red/) for why a
knowledge base an agent writes to is also a place an attacker wants to write
to.
