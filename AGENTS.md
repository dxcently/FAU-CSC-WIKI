# AGENTS.md

This file is for agents that EDIT this wiki's content. It is not wiki content.
It does not get published. It lives next to `CLAUDE.md` and does not repeat
what that file already covers (Hugo commands, theme, front matter). Read
`CLAUDE.md` first.

This file has two jobs: keep the wiki inside FAU policy, and keep the prose
readable. Neither job is optional. Neither is hard, if you follow the
checklists below.

Scope: applies to every page under `content/`. `CLAUDE.md` governs mechanics
(shortcodes, front matter, build). This file governs what you're allowed to
say and how you say it. Where the two disagree on tone, `CLAUDE.md`'s voice
rule wins — this file only adds the STE constraints on top of it (see
"STE vs. club voice" below).

---

## Part 1 — FAU policy compliance

The FAU Cyber Security Club is a Registered Student Organization (RSO), not
an arm of the university. Its members are FAU students bound by FAU's
regulations. The wiki is public. Write like both of those facts are true on
every page.

### Verified sources

Only these were confirmed by fetching the actual document. Cite them by name
if you cite anything.

- **Regulation 4.007, Student Code of Conduct** (Sept. 9, 2025) —
  https://www.fau.edu/regulations/documents/chapter4/reg-4-007-09092025.pdf
- **Regulation 4.001, Code of Academic Integrity** (Aug. 2024) —
  https://www.fau.edu/regulations/documents/chapter4/reg4-001-august2024.pdf
- **RSO Trademark Licensing Guidelines** (Feb. 19, 2024) —
  https://www.fau.edu/public-affairs/documents/rso-trademark-guidelines.pdf
- **Registered Student Organization Manual 2024–2025** —
  https://www.fau.edu/involvement/files/2024-2025-rso-manual.pdf
- IT policy titles listed (not full text — see flags below) at
  https://www.fau.edu/nit/it/policies/: "Acceptable Use of Technology
  Resources" and "Responsible Use of Data Access."

### Rules an agent follows

1. **No credentials, API keys, or real target hostnames/IPs.** Reg 4.007
   treats unauthorized entry and unauthorized access as misconduct. Never
   publish a working target. Use `10.0.0.0/8`, `example.com`,
   `TARGET_IP`, or a named lab machine from a public CTF.

2. **No attack instructions against systems the reader doesn't own or isn't
   authorized to test.** Scope every technique to a lab, a CTF box, or a
   system the reader controls. Say so in the text: "on your lab VM," "on the
   CTF box," not just "the target."

3. **No exam questions, quiz banks, or graded assignments, reproduced in
   whole or in part.** Reg 4.001 lists "uploading exam items online" as
   cheating, by name. This is not a gray area. Link to the course or the
   professor's page instead of pasting the material.

4. **No plagiarism.** Reg 4.001 defines it as presenting another person's
   words, or an AI's words, without citation — including paraphrase without
   citation. Quote and cite. Write it yourself when you can.

5. **No personal information about members** beyond what they've published
   about themselves (a public GitHub handle, a CTF team name they use
   publicly). No real names on a leaderboard unless the member opted in.

6. **No FAU name or marks in the wiki's own branding.** The RSO Trademark
   Guidelines are explicit: "The letters or words FAU, Florida Atlantic
   University, Florida Atlantic, FAU Owls, Florida Atlantic University Owls
   or Florida Atlantic Owls may not be included in the logo." Design your
   own mark. If a page needs the official FAU logo for any reason, route it
   through Student Involvement & Leadership (involvement@fau.edu) first —
   don't add it yourself.

7. **Don't imply the wiki is an official FAU publication.** An RSO
   "identifies as a student-based organization not to be confused with a
   University department, program, or initiative" (RSO Trademark
   Guidelines). Keep the club's own name in front-facing copy; don't write
   as if the university itself is speaking.

8. **No restricted institutional data** — SSNs, grades tied to a named
   student, medical records, card numbers, anything FERPA-protected. This is
   a general obligation under state and federal law, not something specific
   this research could pin to an FAU-numbered policy (see flags).

### Flags — needs a club officer

- The **Acceptable Use of Technology Resources** and **Responsible Use of
  Data Access** policies exist and are titled as such on FAU's own IT
  policy page, but both sit behind a JS-rendered policy portal
  (`faupub.cfmnetwork.com`) that this research could not pull text from. No
  policy number, effective date, or specific prohibited-conduct list is
  verified. An officer with portal access should pull the actual text and
  the citation should be updated here.
- No explicit rule was found requiring a "not an official FAU page"
  disclaimer on an RSO website. Rule 7 above is inferred from the trademark
  and manual language, not a quoted disclaimer requirement. Confirm with
  Student Involvement & Leadership whether a footer disclaimer is expected.
- No FAU-specific data classification policy (levels, definitions) was
  found published by FAU itself; other Florida universities publish one,
  FAU's equivalent wasn't locatable in this pass. Rule 8 is written to the
  general obligation, not a cited FAU policy number.

---

## Part 2 — Simplified Technical English (ASD-STE100), distilled

Unless `CLAUDE.md` says otherwise for the case in front of you, wiki prose
follows this. It's a big spec. Here's the part you need while writing
Markdown.

- **One word, one meaning.** Pick one term per concept and reuse it across
  the whole wiki. Don't switch between "attacker," "adversary," and "threat
  actor" in the same section — pick one.
- **One meaning, one word.** Don't reuse a word for two different things.
  If "session" means a shell session in one page, don't use it for an HTTP
  session somewhere else without saying which.
- **Security jargon has no approved-word list.** Define it on first use in
  a page, plain and short, then use the term consistently for the rest of
  that page: "privilege escalation (getting higher access than you
  started with)."
- **Procedural sentences: short.** Aim for 20 words or fewer. If a step
  needs "and," it's probably two steps.
- **Descriptive sentences: a bit longer is fine.** Up to ~25 words when
  you're explaining why, not telling the reader what to type.
- **One instruction per sentence.** Sequential steps get separate numbered
  sentences, not a comma-chained list.
  - Bad: "Open a terminal, run nmap against the target, and read the
    output."
  - Good: "Open a terminal. Run nmap against the target. Read the output."
- **Active voice. Imperative mood for instructions.** The reader is the
  one doing the thing — tell them to do it.
  - Bad: "The target should be scanned before an exploit is attempted."
  - Good: "Scan the target before you try an exploit."
- **Keep articles.** "The," "a," "an" stay. Dropping them to sound terse
  reads like a broken translation, not like Linus.
- **Simple tenses.** Past, present, future. Skip the perfect and
  progressive forms where a simple tense does the job.
  - Bad: "You will have been scanning the network for several minutes."
  - Good: "The scan takes a few minutes."
- **No noun clusters over three words.** "Remote code execution
  vulnerability scanner" is four nouns stacked — break it apart:
  "a scanner for remote code execution."
- **Paragraphs: 6 sentences, max.** If it runs longer, it's two ideas.
  Split it.
- **No slang, no idioms, no metaphors a non-native reader would miss.**
  "Dive into the deep end," "footgun," "rabbit hole" — cut them from
  procedural text. Say the plain thing instead.

### STE vs. club voice — precedence rule

`CLAUDE.md` wants Linus Torvalds: blunt, warm, encouraging, willing to use
an idiom to land a point. STE wants none of that in technical prose. Both
are right, for different parts of the page.

**STE governs technical and procedural prose** — anything that tells the
reader what a thing is or what to type. **The club voice governs framing,
encouragement, and section intros** — the paragraph that tells the reader
why they should care, before the steps start.

Don't blend them inside one sentence. Put the encouragement in its own
sentence, ahead of the instructions, and let the instructions be plain.

**Example 1**

- Before (voice bleeding into procedure): "Once you've got your feet wet
  with nmap, don't be afraid to dive into Metasploit — everybody screws up
  their first exploit."
- After: "Nmap is easy. Metasploit is not — everyone stumbles on it at
  first. That's normal. Scan the target with nmap. Pick the matching
  module in Metasploit. Set the target IP address. Run it."

**Example 2**

- Before (passive, hedged): "It is generally recommended that logs should
  perhaps be checked by the user prior to escalation attempts."
- After: "Logs bite people who skip them. Check the log before you try to
  escalate."

**Example 3**

- Before (idiom in an instruction): "Don't go down the rabbit hole of
  every CVE — triage first."
- After: "Don't chase every CVE. Triage first — that's the encouragement.
  Rank each finding by exploitability before you research it."

One line, framed by the club, then plain STE steps. That's the pattern for
the whole wiki.

---

## Part 3 — Site format

Know this before you write a file. Getting it wrong produces pages that build
but do not appear, or appear in the wrong place.

### Stack

Hugo static site, Relearn theme. No app code, no database, no build pipeline
beyond `hugo`. Content is Markdown with **TOML front matter** (`+++`
delimiters, not `---`).

### Layout

```
content/            every page. Directory structure == URL structure == nav.
  _index.md         home page (type = "home"); also holds the meeting schedule
  start/            Start Here
  learn/            the roadmap and its subsections
  compete/          CTF, CCDC, CyberPatriot, archive
  lab/              Club Lab
  projects/         member projects and guides
  toolbox/          links, cheat sheets, AI pages
  meta/             authoring guide, TODO — docs about the wiki itself
assets/css/         custom.css (structural) + theme-hacker.css (palette tokens)
assets/images/      logo.svg — sidebar logo AND favicon, one file
layouts/            template overrides: home page partials, shortcodes
themes/relearn/     git submodule — NEVER edit
public/             generated output — NEVER hand-edit
```

### File naming

- Section landing page: `_index.md`. Every other page: `<name>.md`.
- A directory only becomes a section if it contains `_index.md`.

### Required front matter

Every page:

```toml
+++
title = "Page Title"
weight = 3
description = "One sentence. Shown on section card grids."
+++
```

`weight` orders siblings, low first. `description` is not optional — the
`section-grid` shortcode prints it, and a missing one leaves a blank card.
Section landing pages may also set `icon` (a Font Awesome class) and
`homecard = false` to stay off the home page grid.

### Navigation is automatic

There is no menu file to update. The sidebar tree, the card grids, and the
home page sections all derive from the content directory and front matter. Add
a file in the right place with the right front matter and it appears.

### Shortcodes

`{{</* section-grid */>}}` lists a section's children as cards. Relearn's own
shortcodes (notice boxes, mermaid, tabs) are available — see
`content/meta/authoring/` for the full reference. Prefer a plain Markdown link
over `relref`; a bare `relref` in a link target emits a build warning.

### Styling

Palette tokens are `--wf-*`, defined in `assets/css/theme-hacker.css`.
Structural CSS goes in `assets/css/custom.css`, which loads last and wins.
**Never put a literal hex value in custom.css** — use a token. The one
exception is `assets/images/logo.svg`, which renders outside the page where CSS
variables do not exist, so its colors are hardcoded and must be kept in sync by
hand.

### The meeting schedule

Lives in `content/_index.md` front matter as `[[params.sessions]]` blocks with
`"YYYY-MM-DD"` string dates. Row state (done / TODAY / NEXT / upcoming) is
derived from the date at build time — do not add fields to track it. `status`
exists only to override (`cancelled`, `moved`, `done`). Full instructions:
`content/meta/authoring/`.

### Naming rule for AI content

This wiki is provider-agnostic. It was rewritten once to strip vendor names
because a page full of model names and benchmark scores was stale within
months. The rule now:

- **People: yes.** Name researchers, educators and authors, and link their
  work. Credit is owed and readers need to find the source.
- **FOSS tools: yes.** Name open-source projects, frameworks and locally
  runnable models. Anyone can install them, and the name is how you find them.
- **Proprietary products and vendors: no.** No company names, no hosted model
  or product names. Describe the capability, not the brand.
- **No benchmark numbers, leaderboard placements or competition results**
  unless you fetched the primary source and cite it inline. This is what got
  the previous AI pages deleted.

Write patterns so they survive the tool that currently implements them.

### Verify before you report

```bash
hugo --quiet     # must exit clean: zero errors, zero warnings
```

A page that builds is not a page that works. Confirm your new page actually
rendered under `public/` at the URL you expect, and that any link you wrote
resolves to a real built page.
