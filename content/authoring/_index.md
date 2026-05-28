+++
title = "Authoring"
weight = 999
+++

# Hugo Relearn Theme Reference

## Overview

The Hugo Relearn Theme is a documentation-focused theme with features like
shortcodes, customizable front matter, sidebar navigation, and search.

---

## Custom Hacker Terminal Theme

**File:** `assets/css/theme-hacker.css`

### Color Palette (Base16 Terminal Style)

| Color Name   | Hex Code  | RGB            | Usage                           |
| ------------ | --------- | -------------- | ------------------------------- |
| Background   | `#001100` | rgb(0, 17, 0)  | Main background, sidebar        |
| Foreground   | `#00BB00` | rgb(0, 187, 0) | Main text, links                |
| Bright White | `#00FF00` | rgb(0, 255, 0) | Titles, highlights, accents     |
| Bright Black | `#007700` | rgb(0, 119, 0) | Borders, separators, muted text |
| Blue/Cyan    | `#009900` | rgb(0, 153, 0) | Secondary elements              |
| Dark Accent  | `#005500` | rgb(0, 85, 0)  | Subtle accents, dark borders    |

### Original Terminal Color Mapping

```json
{
  "terminal.background": "#001100",
  "terminal.foreground": "#00BB00",
  "terminalCursor.background": "#00BB00",
  "terminalCursor.foreground": "#00BB00",
  "terminal.ansiBlack": "#001100",
  "terminal.ansiBlue": "#009900",
  "terminal.ansiBrightBlack": "#007700",
  "terminal.ansiBrightBlue": "#009900",
  "terminal.ansiBrightCyan": "#005500",
  "terminal.ansiBrightGreen": "#00BB00",
  "terminal.ansiBrightMagenta": "#00BB00",
  "terminal.ansiBrightRed": "#007700",
  "terminal.ansiBrightWhite": "#00FF00",
  "terminal.ansiBrightYellow": "#007700",
  "terminal.ansiCyan": "#005500",
  "terminal.ansiGreen": "#00BB00",
  "terminal.ansiMagenta": "#00BB00",
  "terminal.ansiRed": "#007700",
  "terminal.ansiWhite": "#00BB00",
  "terminal.ansiYellow": "#007700"
}
```

### Configuration

In `hugo.toml`:

```toml
[params]
  themeVariant = 'hacker'
```

---

## Sidebar Configuration

### Social Links (Discord & GitHub)

Added via Hugo menus in `hugo.toml`:

```toml
[menus]
  [[menus.shortcuts]]
    name = "<i class='fab fa-fw fa-discord'></i> Discord"
    identifier = "discord"
    url = "https://discord.gg/kHvmg3AFhN"
    weight = 10

  [[menus.shortcuts]]
    name = "<i class='fab fa-fw fa-github'></i> GitHub"
    identifier = "github"
    url = "https://github.com/dxcently/fau-cyber-security-club-wiki"
    weight = 20
```

### Sidebar Menus Configuration

```toml
[params]
  # Configure sidebar menus
  [[params.sidebarmenus]]
    type = 'page'
    identifier = 'home'
    main = true
    disableTitle = true
    pageRef = ''

  [[params.sidebarmenus]]
    type = 'menu'
    identifier = 'shortcuts'
    main = false
    disableTitle = false
```

### Custom Menu Title

In `i18n/en.toml`:

```toml
[shortcuts-menuTitle]
other = "Connect"
```

### Search

Search is **enabled by default** in Relearn theme. To disable:

```toml
[params]
  search.disable = true        # Disable all search
  search.index.disable = true  # Disable search popup only
  search.page.disable = true   # Disable dedicated search page only
```

---

## Available Shortcodes (17 total)

| Shortcode     | Purpose                                      |
| ------------- | -------------------------------------------- |
| **Badge**     | Marker badges to display in your text        |
| **Button**    | Clickable buttons                            |
| **Card**      | Show content in a card                       |
| **Cards**     | Show content in a set of cards               |
| **Children**  | List the child pages of a page               |
| **Expand**    | Expandable/collapsible sections of text      |
| **Highlight** | Render code with a syntax highlighter        |
| **Icon**      | Nice icons for your page                     |
| **Include**   | Displays content from other files            |
| **Math**      | Beautiful math and chemical formulae         |
| **Mermaid**   | Generate diagrams and flowcharts from text   |
| **Notice**    | Boxes to help you structure your page        |
| **OpenAPI**   | UI for your OpenAPI / Swagger specifications |
| **Resources** | List resources contained in a page bundle    |
| **SiteParam** | Get value of site params                     |
| **Tab**       | Show content in a single tab                 |
| **Tabs**      | Show content in tabbed views                 |
| **Tree**      | Display text as a tree                       |

---

## Notice Shortcode

### Parameters

| Parameter    | Position | Default         | Purpose                                        |
| ------------ | -------- | --------------- | ---------------------------------------------- |
| **style**    | 1        | `default`       | Determines appearance scheme                   |
| **title**    | 2        | Varies          | Box heading text                               |
| **icon**     | 3        | Varies          | Font Awesome icon name                         |
| **groupid**  | —        | Empty           | Groups expandable boxes to sync                |
| **color**    | —        | Style-dependent | CSS color value                                |
| **expanded** | —        | Empty           | Controls expandability: empty, `true`, `false` |

### Available Styles

- **By Severity:** caution, important, info, note, tip, warning
- **By Brand:** primary, secondary, accent
- **By Color:** blue, cyan, green, grey, magenta, orange, red
- **By Special Type:** default, transparent, code, link, action, inline

### Usage Examples

```markdown
> [!tip] My Title Box content here
```

```markdown
{{% notice style="tip" title="My Title" %}} Box content here {{% /notice %}}
```

---

## Tabs Shortcode

### Parameters

| Parameter   | Default | Purpose                           |
| ----------- | ------- | --------------------------------- |
| **groupid** | Random  | Group name for synchronized tabs  |
| **style**   | Empty   | Default styling for all tabs      |
| **color**   | Empty   | Default color for all tabs        |
| **title**   | Empty   | Display text in front of tab view |
| **icon**    | Empty   | Font Awesome icon                 |

### Usage

```markdown
{{< tabs >}} {{% tab title="Label" %}}Content here{{% /tab %}} {{% tab
title="Label 2" %}}More content{{% /tab %}} {{< /tabs >}}
```

---

## Front Matter Parameters Reference

| Parameter                 | Type    | Default | Description                                            |
| ------------------------- | ------- | ------- | ------------------------------------------------------ |
| **title**                 | string  | —       | Page title                                             |
| **weight**                | int     | —       | Controls menu order (lower = higher)                   |
| **type**                  | string  | —       | Page type: "home", "chapter", etc.                     |
| **hidden**                | boolean | false   | Hides page's menu entry                                |
| **alwaysopen**            | string  | empty   | Controls whether submenus expand or collapse           |
| **collapsibleMenu**       | boolean | false   | Shows expander for submenus                            |
| **disableBreadcrumb**     | boolean | false   | Hides breadcrumbs from topbar                          |
| **disableToc**            | boolean | false   | Hides table of contents button                         |
| **disableNextPrev**       | boolean | false   | Hides Next and Previous navigation                     |
| **headingPre**            | string  | empty   | HTML prefix for page heading                           |
| **headingPost**           | string  | empty   | HTML suffix for page heading                           |
| **menuPre**               | string  | empty   | HTML prefix for menu entry title                       |
| **menuPost**              | string  | empty   | HTML suffix for menu entry title                       |
| **linkTitle**             | string  | empty   | Menu-specific title for page                           |
| **ordersectionsby**       | string  | weight  | Ordering: weight, title, linktitle, modifieddate, etc. |
| **imageEffects.border**   | boolean | false   | Adds border to images                                  |
| **imageEffects.shadow**   | boolean | false   | Adds shadow effect to images                           |
| **imageEffects.lightbox** | boolean | true    | Enables lightbox for images                            |
| **highlightWrap**         | boolean | true    | Enables line wrapping in code blocks                   |

---

## Page Types

- **home** - For the main landing page
- **chapter** - For section index pages (creates chapter-style header)
- (default) - Regular content pages

---

## Mermaid Shortcode (Diagrams)

### Parameters

| Parameter | Default | Purpose                                  |
| --------- | ------- | ---------------------------------------- |
| **align** | center  | Vertical alignment (left, center, right) |
| **zoom**  | varies  | Enables pan/zoom functionality           |

### Supported Diagram Types

- Flowcharts and graphs
- Sequence and class diagrams
- State and entity relationship models
- GANTT charts, timelines, and user journeys
- Pie, quadrant, and radar charts
- C4 architecture diagrams
- Mindmaps, sankey flows, and block diagrams
- Git graphs, kanban boards, and treemaps

### Usage

```markdown
{{< mermaid align="center" zoom="true" >}} graph LR; If --> Then Then --> Else
{{< /mermaid >}}
```

---

## Expand Shortcode (Collapsible Content)

### Parameters

| Parameter    | Position | Default   | Purpose                  |
| ------------ | -------- | --------- | ------------------------ |
| **title**    | 1        | "Details" | Text next to expand icon |
| **expanded** | 2        | false     | Initial state            |

### Usage

```markdown
{{% expand title="Expand me..." %}} Hidden content here {{% /expand %}}
```

Or with Markdown callout:

```markdown
> [!default] Expand me... Hidden content here
```

---

## Content Organization

```
content/
├── _index.md              # Home page (type: home)
├── section1/
│   ├── _index.md          # Section page (type: chapter)
│   ├── page1.md           # Regular page
│   └── subsection/
│       └── _index.md      # Nested section
└── section2/
    └── _index.md
```

- Use `weight` in front matter to control menu order
- Chapters create visual separation in navigation
- Nested folders create hierarchical navigation
