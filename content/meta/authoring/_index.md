+++
title = "Authoring"
weight = 2
+++

---

# So You Want to Help Write the Wiki?

This wiki is a community effort. Every page someone writes makes it more useful
for the next person who joins. You do not need to be a developer to contribute —
if you can write Markdown and use GitHub, you can add pages.

This guide covers two paths:

- **Just writing content** — the fast path. No local setup needed.
- **Full local setup** — for previewing changes before submitting, or making
  deeper edits to the site config and theme.

---

## Path 1 — Just Writing a Page

If you only want to add or edit content, you do not need Hugo installed. The
wiki is just Markdown files. You can write one, open a pull request, and someone
will review and merge it.

### 1. Fork and clone the repo

```bash
git clone https://github.com/dxcently/fau-cyber-security-club-wiki.git
cd fau-cyber-security-club-wiki
```

### 2. Create your file

All content lives under `content/`. The structure looks like this:

```
content/
├── _index.md                     # Home page
├── introduction/
│   ├── _index.md                 # Section landing page
│   └── getting-started/_index.md
├── resources/
│   └── _index.md
└── your-section/
    └── your-page.md              ← your file goes here
```

Create a `.md` file in the right section. Every page needs a front matter block
at the top:

```toml
+++
title = "Your Page Title"
weight = 2
+++
```

- `title` — shows up in the sidebar and as the page heading
- `weight` — controls order in the sidebar (lower number = higher up)
- Add `type = "chapter"` for section landing pages to get the big header style

Write your content in plain Markdown below the front matter. That is it.

### 3. Submit a pull request

```bash
git checkout -b my-new-page
git add content/
git commit -m "add page: your topic here"
git push origin my-new-page
```

Open a pull request on GitHub. Someone will review it and merge it in.

---

## Path 2 — Full Local Setup

Do this if you want to preview the site before submitting, or if you are making
changes beyond content — config, menus, theme, etc.

### Install Hugo

{{< tabs >}} {{% tab title="Linux" %}}

```bash
sudo snap install hugo
```

{{% /tab %}} {{% tab title="macOS" %}}

```bash
brew install hugo
```

{{% /tab %}} {{% tab title="Windows" %}}

```bash
winget install Hugo.Hugo.Extended
```

{{% /tab %}} {{< /tabs >}}

Verify:

```bash
hugo version
```

### Run the dev server

```bash
hugo server
```

Open [http://localhost:1313](http://localhost:1313). The page live-reloads on
every save. Use this to check that your page looks right before submitting.

### Build the site

```bash
hugo
```

Outputs the static site to `public/`. You normally do not need this unless you
are deploying.

---

## Shortcodes (Fancy Formatting)

Shortcodes are Hugo's way of doing things plain Markdown cannot. Use them
sparingly — plain text is usually enough and easier to maintain.

| Shortcode   | What It Does                                     |
| ----------- | ------------------------------------------------ |
| **Notice**  | Callout boxes (tip, warning, info, caution, etc) |
| **Tabs**    | Tabbed content for OS or environment differences |
| **Expand**  | Collapsible sections for optional content        |
| **Mermaid** | Diagrams and flowcharts rendered from text       |

---

### Notice (Callout Boxes)

Use when something needs to stand out — a warning, a tip, a gotcha. Two syntax
options; both work the same way.

Short form (simpler to write):

```
> [!tip] Pro Tip
> Your tip text goes here.
```

Shortcode form (more control over the title text):

```
{{%/* notice style="warning" title="Heads Up" */%}}
Something the reader should not skip.
{{%/* /notice */%}}
```

Swap `style=` for: `tip`, `warning`, `info`, `note`, `caution`, `important`

---

### Tabs

Use tabs when the same instructions differ by OS or environment and stacking
them vertically would be cluttered.

Wrap everything in `tabs`, then put each option in its own `tab` block. The
`title=` value is what appears on the clickable tab.

```
{{</* tabs */>}}
{{%/* tab title="Linux" */%}}
Your Linux instructions here.
{{%/* /tab */%}}
{{%/* tab title="Windows" */%}}
Your Windows instructions here.
{{%/* /tab */%}}
{{</* /tabs */>}}
```

Any normal Markdown works inside a tab block — code, lists, paragraphs.

---

### Expand (Collapsible Sections)

Use for content that is optional or would interrupt the flow — full command
output, a deeper explanation, a reference table. The section is collapsed by
default; the reader opens it if they want it.

The `title=` is the label shown while collapsed.

```
{{%/* expand title="Show the full output..." */%}}
Your hidden content here. Works with any Markdown inside.
{{%/* /expand */%}}
```

---

### Mermaid (Diagrams)

Renders diagrams from text. No image files, no external tools. Write the diagram
definition between the tags.

```
{{</* mermaid */>}}
flowchart TD
    A[Start] --> B[Do a thing]
    B --> C[Done]
{{</* /mermaid */>}}
```

Mermaid supports flowcharts, sequence diagrams, state machines, Gantt charts,
and more. The syntax differs per diagram type — check the
[Mermaid docs](https://mermaid.js.org/intro/) for what you need.

---

## Front Matter Reference

| Parameter           | Type    | Default | What It Does                                |
| ------------------- | ------- | ------- | ------------------------------------------- |
| **title**           | string  | —       | Page title                                  |
| **weight**          | int     | —       | Sidebar order (lower = higher up)           |
| **type**            | string  | —       | `"home"` or `"chapter"` for special layouts |
| **hidden**          | boolean | false   | Hides the page from the sidebar             |
| **disableToc**      | boolean | false   | Hides the table of contents                 |
| **disableNextPrev** | boolean | false   | Hides the Next / Previous nav buttons       |

---

## Deeper Edits — Hugo Config and Theme

This section is for changes beyond content: menus, sidebar links, colors,
config.

### Key files

| File                          | What it controls                                    |
| ----------------------------- | --------------------------------------------------- |
| `hugo.toml`                   | Site title, theme variant, sidebar menus, nav links |
| `i18n/en.toml`                | UI string overrides (e.g. sidebar section title)    |
| `assets/css/theme-hacker.css` | Color scheme — Base16 Greenscreen palette           |

### Adding sidebar shortcut links

Shortcut links (Discord, GitHub, etc.) live in `hugo.toml` under
`[[menus.shortcuts]]`. Add a new entry:

```toml
[[menus.shortcuts]]
  name = "<i class='fab fa-github'></i> GitHub"
  url = "https://github.com/your-repo"
  weight = 10
```

The sidebar section title ("Quick Links") is set in `i18n/en.toml`.

### Color scheme

The wiki uses a custom **Hacker Terminal** palette — green on black. All colors
are defined as CSS variables in `assets/css/theme-hacker.css`.

**Base palette**

| Hex       | Role                               |
| --------- | ---------------------------------- |
| `#001100` | Background (main + sidebar)        |
| `#002200` | Slightly lighter bg (code, boxes)  |
| `#005500` | Dark accent, borders, separators   |
| `#007700` | Muted text, visited links          |
| `#009900` | Secondary elements, H5/H6 headings |
| `#00BB00` | Main text, H3/H4 headings          |
| `#00FF00` | H1/H2 titles, highlights, hover    |
| `#00FF88` | Hyperlinks (cyan-green)            |
| `#00FFC8` | Hyperlink hover state              |

**Key CSS variables**

| Variable                    | Value     | What it controls      |
| --------------------------- | --------- | --------------------- |
| `--PRIMARY-color`           | `#00BB00` | Primary brand color   |
| `--PRIMARY-HOVER-color`     | `#00FF00` | Hover state           |
| `--MAIN-BG-color`           | `#001100` | Page background       |
| `--MAIN-TEXT-color`         | `#00BB00` | Body text             |
| `--MAIN-TITLES-TEXT-color`  | `#00FF00` | H1 / H2 headings      |
| `--MAIN-LINK-color`         | `#00FF88` | Hyperlinks            |
| `--CODE-BLOCK-BG-color`     | `#002200` | Code block background |
| `--CODE-BLOCK-BORDER-color` | `#005500` | Code block border     |
| `--CODE-INLINE-color`       | `#00FF00` | Inline code text      |
| `--MENU-SECTIONS-BG-color`  | `#001100` | Sidebar background    |
| `--MENU-VISITED-color`      | `#007700` | Visited sidebar links |

Edit `assets/css/theme-hacker.css` to change any of these. The theme variant is
wired up in `hugo.toml` via `themeVariant = 'hacker'`.

---

## Using AI to Write Pages

You do not have to write everything from scratch. Claude, ChatGPT, and similar
tools are good at drafting Markdown pages — as long as you give them enough
context and review what comes out.

### What to tell it

- The front matter format (TOML with `+++` delimiters)
- Which section the page belongs to
- What it should cover
- The tone: direct, practical, no filler

Example prompt:

```
Write a wiki page for a cybersecurity club. Front matter uses TOML with +++ delimiters.

+++
title = "Your Title"
weight = 2
+++

The page is about [topic]. Keep it direct and practical.
Cover: [list what you want].
```

### What to watch for

AI will confidently write things that are wrong. Read it before committing. If
the page covers a specific tool or command, test that it actually works.

Cut any paragraph that says nothing. Phrases like "it's important to note" or
"feel free to explore" are filler — delete them.

### Claude Code

If you have [Claude Code](https://claude.ai/code), run `claude` or `claude rc`
from the repo root. It reads the existing content and `CLAUDE.md`, matches the
site's style, and writes files directly. Just tell it what you need. I've also
prompted it to write like a less condescending Linus Torvalds lol.

---

## Questions?

Reach out on the [Discord](https://discord.gg/kHvmg3AFhN). No judgment — we were
all new to this once.
