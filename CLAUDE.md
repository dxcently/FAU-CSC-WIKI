# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with
code in this repository.

## Commands

```bash
hugo server    # local dev server with live reload
hugo           # build site to public/
```

## Architecture

This is a Hugo static site for the **FAU Cyber Security Club**, using the
**Relearn theme** (`themes/relearn/`) with a custom terminal-green color scheme.

### Content

All pages live under `content/` as Markdown files named `_index.md` (for
sections) or `<name>.md` (for leaf pages). Front matter uses TOML delimiters
(`+++`).

- `content/_index.md` — home page (`type = "home"`)
- `content/<Section>/_index.md` — section/chapter pages (`type = "chapter"`,
  `weight` controls order)
- `content/<Section>/<Page>.md` — regular content pages
- `content/authoring/_index.md` — **author reference**: full shortcode docs,
  front matter options, theme config. Read this before adding new content or
  shortcodes.

### Key config files

| File                          | Purpose                                                         |
| ----------------------------- | --------------------------------------------------------------- |
| `hugo.toml`                   | Site config, theme variant, sidebar menus, social links         |
| `i18n/en.toml`                | UI string overrides (e.g., sidebar section title "Quick Links") |
| `assets/css/theme-hacker.css` | Custom terminal green-on-black theme (`#00BB00` on `#001100`)   |

### Sidebar menus (hugo.toml)

Two sidebar menus are configured: a `page` menu (main nav tree) and a `menu`
menu (shortcuts: Discord, GitHub, Owl Central). Adding social links means adding
a new `[[menus.shortcuts]]` entry.

### Planned content structure (from `content/authoring/todo/`)

The wiki is in early stages. Planned sections: CTF (blue/red teaming),
Infrastructure (VMs, networking), Club Server, and expanded Resources.
