+++
title = "Logo & Brand"
weight = 3
description = "The club owl mark in both forms, with downloads, colours, and rules for using it."
icon = "fa-solid fa-palette"
+++

The club mark is an owl — Florida Atlantic's bird — drawn as a low-polygon
wireframe. It exists in three forms. All are SVG, so they scale to any size
without going fuzzy.

All three come in a **dark-ground** and a **light-ground** version. They are the same drawing: only the palette differs, because a mark
tuned for a black screen washes out on paper. The previews below already show
whichever one matches the theme you are reading in — flip the theme in the
topbar and watch them swap.

---

## Shield

The full lockup: the owl inside a layered shield frame. Use this when the mark
stands alone and needs a container — an avatar, a sticker, a slide corner.

{{< mark-preview dark="/images/logo.svg" light="/images/shield-light.svg" width="200" alt="Club owl mark inside a shield" >}}

Downloads: **[for dark backgrounds](/images/logo.svg)** ·
**[for light backgrounds](/images/shield-light.svg)**

The shield is the only form that carries its own base, so either version
survives on either background — the light one just sits better on paper.

## Bare head

The face on its own, no frame. Use this when it sits on an existing panel or
next to text, where a second border would just add clutter.

{{< mark-preview dark="/images/owl-mark.svg" light="/images/owl-mark-light.svg" width="260" alt="Club owl head without the shield" >}}

Downloads: **[for dark backgrounds](/images/owl-mark.svg)** ·
**[for light backgrounds](/images/owl-mark-light.svg)**

## Full owl

The whole bird — head, folded wings, breast and talons. This is the version on
the home page. Use it where there is vertical room and the mark is the subject:
a poster, a slide, a shirt back, a Discord banner.

{{< mark-preview dark="/images/owl-full.svg" light="/images/owl-full-light.svg" width="220" alt="The full club owl with wings and talons" >}}

Downloads: **[for dark backgrounds](/images/owl-full.svg)** ·
**[for light backgrounds](/images/owl-full-light.svg)**

---

## Colours

Same drawing, two palettes. Every colour was measured against its own ground —
the dark set fails on paper and the light set disappears on black, which is
the whole reason both files exist.

| Role | Dark ground | Light ground | Where it goes |
| ---- | ----------- | ------------ | ------------- |
| Ground | `#030A08` | *(none — transparent)* | The shield only; the frameless marks sit on yours |
| Chrome | `#1E90FF` | `#0B5FC4` | Structure — linework, plates, the frame |
| Red | `#FF4D4D` | `#CC0000` | The brows. FAU's red, and the only red in the mark |
| Highlight | `#E8F4FF` | `#0847A0` | Eyes, beak ridge, chin |
| Green | `#00BB00` | `#0A6B2C` | Terminal green. Used across the site, **not** in the mark |

The highlight row is the one that surprises people: it does not stay white.
On a dark screen those shapes are light catching an edge, so on paper they
have to invert. But **not all the way to black** — an earlier pass took them
to ink and the eyes read as holes punched through the face, because pure
black was then the only colour in the drawing that was not part of the
palette. Deep blue keeps them in the family and still reads as pupils.

The mark is blue, red and white — FAU's colours. The site's terminal green
lives everywhere else: code blocks, headings, the roadmap's shared core.

---

## Using it

- **Pick the version that matches your background.** The frameless marks
  have no ground of their own — that is the point, they sit on yours. Use the
  dark-ground file on dark, the light-ground file on light. The shield brings
  its own base, so it works anywhere.
- **Do not recolour it.** The palette is the identity.
- **Do not stretch it.** Scale both dimensions together.
- **Do not add effects.** No drop shadows, no outlines, no gradients over it.
- **Keep clear space** around it — roughly the height of one brow.
- The bare head stops being readable below about 32 px, and the full owl below
  about 64 px. Use the shield form at small sizes; it was built for it.

> [!warning] FAU marks are not ours to use
> This owl is the **club's** mark. It is not Florida Atlantic University's
> logo, and it does not carry the university's marks. FAU restricts how
> registered student organisations use the university name and logos — see
> `AGENTS.md` in the repo root, and clear anything official with the club's
> advisor before publishing it outside the club.

---

## Where the files live

| File | What it is |
| ---- | ---------- |
| `assets/images/logo.svg` | Shield, dark ground. Also the sidebar logo. |
| `assets/images/shield-light.svg` | Shield, light ground. |
| `assets/images/owl-mark.svg` | Bare head, dark ground. |
| `assets/images/owl-mark-light.svg` | Bare head, light ground. |
| `assets/images/owl-full.svg` | Full owl — head, wings, breast, talons. |
| `assets/images/owl-full-light.svg` | Full owl, light ground. |
| `layouts/partials/home/owl-wireframe.html` | The large animated-scale hero version on the home page. This is the master geometry. |

These files repeat the same geometry because they render in different
places — the hero uses the site's CSS colour tokens, while the two SVGs are
standalone files that render outside the page where those tokens do not exist,
so their colours are written in directly. **If you change the mark, change
every file in the table,** or they drift apart.
