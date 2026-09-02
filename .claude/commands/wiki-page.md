# Wiki Page Workflow

You are adding or updating content in the FAU Cybersecurity Club wiki at `/home/khoa/Projects/cybersec-wiki`.

This is a Hugo static site using the Relearn theme. Content lives under `content/` as Markdown files.

## Writing Style

- **Sentences:** 1–4 per paragraph. Short. Direct. Say the thing.
- **No filler:** no "feel free to", no hedging, no "it's important to note".
- **Tone:** blunt but encouraging. Respect the reader's intelligence. Point them in a direction, don't hand-hold.
- **Length:** don't write an article. Write enough to orient the reader and send them somewhere good.
- **Commands:** show standard/generic commands. Do not lock content to one specific tool's CLI.
- **Links:** always provide links to authoritative references. Encourage self-learning over exhaustive explanation.

## Front Matter (TOML, +++ delimiters)

Section chapter (landing page for a section):
```toml
+++
title = "Section Title"
weight = N
type = "chapter"
+++
```

Regular page:
```toml
+++
title = "Page Title"
weight = N
+++
```

## File Structure

New section with sub-pages:
```
content/<section-name>/
  _index.md         # chapter page — overview, what's covered
  <subtopic1>.md    # first sub-page
  <subtopic2>.md    # second sub-page
```

Single page within an existing section:
```
content/<existing-section>/<new-page>.md
```

## Required Sections in Each Page

Every page should include:

1. **A short intro** (2–3 sentences). What is this thing and why does it matter.
2. **The substance** — concepts, commands, tools, comparisons. Use tables and code blocks. Keep it tight.
3. **Real-world context** — one short paragraph connecting this to actual security work.
4. **Club usage placeholder** — always include this notice block:

```
> [!info] How the Club Uses This
> TODO: Add how FAU CSC uses this in practice — competitions, demos, labs, etc.
```

5. **References** — 3–5 links to authoritative external resources.

## Tool Comparison Format

When listing multiple tools, use a table:

| Tool | What it does | When to use |
|---|---|---|
| Tool A | ... | ... |
| Tool B | ... | ... |

## Your Task

Ask the user:
1. What topic or page are they adding/updating?
2. Is it a new section (multiple pages) or a single page within an existing section?
3. What should it cover? (subtopics, specific angles)
4. Is there club-specific context to fill in the TODO placeholder right now?

Then create or update the appropriate files.

After writing, run `hugo` from the project root to verify the build compiles without errors.
