---
name: linkedin-image-post
description: "When the user wants to create a single image post for LinkedIn — a standalone 1080×1350 portrait graphic for the feed. Use when the user mentions 'single image post,' 'LinkedIn image,' 'feed image,' 'single slide,' 'graphic post,' 'png post,' 'Field Note single,' or references any png-*.py scripts. This skill encodes the 2026-04-15 smbx.ai design canon: one self-contained published Field Note page with masthead, HookEyebrow, Sora hook, data/visual, punchline, portrait byline."
metadata:
  version: 4.0.0
---

# LinkedIn Single Image Post

You produce single 1080×1350 portrait images for LinkedIn feed using Playwright at 2× DPR. Output is a single PNG. The post reads as **one self-contained Field Note page** — the whole story in one frame, no swipe context needed.

## ⚠️ READ THIS FIRST

**Authoritative design docs** — read before building anything:

1. `DESIGN_HANDOFF.md` (repo root) — key deltas from the deprecated cream/rose-gold system
2. `DESIGN_LANGUAGE.md` (repo root) — full visual system, authoritative as of 2026-04-15
3. `STYLE_GUIDE.md` (repo root) — brand voice

**Reference implementations:**

- `content/week-01/png-sellers-gap.py` (MON-1B, Field Note No. 17) — two-column `$` compare + gap row + accent punchline + byline
- `content/week-01/png-buyers-screen.py` (MON-2B, No. 23) — dark KV card with 4 kill-threshold rows + accent punchline + byline

**Companion skill:** `linkedin-carousel`. The image post shares its component library — see that SKILL.md for the full component catalog. This skill documents only the single-page composition.

### Forbidden patterns

Same as `linkedin-carousel`, plus:

| Pattern | Why |
|---|---|
| Dark page background | Single images are LIGHT. Use a dark card inside a light page if you need contrast. |
| CTA ring block | Single images don't close on a CTA — they land on a punchline + byline. The CTA happens in the LinkedIn post text, not the image. |
| Swipe hint | There's no swipe. No `cover-swipe` element. |
| Multiple eyebrows | One HookEyebrow at the top. No SectionEyebrow elsewhere. |

## Format

| Attribute | Value |
|---|---|
| Canvas | 1080 × 1350 px (4:5 portrait) |
| DPR | 2× (renders at 2160 × 2700) |
| Output | Single PNG |
| Fonts | Sora 600/700/800 + Inter 400/500/600/700 |
| Assets | Base64-embedded (logo, portrait) |
| Font load wait | `page.wait_for_timeout(2000)` |
| Script name | `png-{topic}.py` |
| Output PNG name | `MON-{N}B-{topic}-single-{mode}.png` |

## Structure — one cohesive page

Top-to-bottom:

| Section | Content | Purpose |
|---|---|---|
| Masthead | Logo + "Field Note · No. XX" | Brand signature |
| HookEyebrow | `● CATEGORY · SUBJECT · ANGLE` (accent, dot, 0.2em) | Positioning |
| Sora hook | 72–84px display headline (1–2 lines) | The question/promise |
| Primary visual | `kv-card-dark` OR `compare-cols` + `gap-row` OR similar | The data |
| Punchline | `punchline` accent-bordered block | The insight |
| Byline | Portrait + name + credentials + date | Attribution |

Six elements total. Everything fits on one page, top-aligned, footer pinned with `margin-top:auto` on the byline.

## Scaffolding

Copy from `png-sellers-gap.py` (MON-1B) or `png-buyers-screen.py` (MON-2B).

### TOKENS + NOTE_NO

```python
NOTE_NO   = "No. 17"   # non-sequential, matches companion carousel if paired
YEAR_WEEK = "2026 · Week 01"

TOKENS = {
    "light": {
        "bg":"#F9F9FC",
        "ink":"#0f1012", "body":"#3c3d40", "muted":"#6e6a63",
        "accent":"#D44A78",
        "border":"rgba(15,16,18,0.08)", "border_soft":"rgba(15,16,18,0.06)",
        "logo_file":"G3L.png",
    },
    "dark": {
        "bg":"#1A1C1E",
        "ink":"#f9f9fc", "body":"rgba(218,218,220,0.85)", "muted":"rgba(218,218,220,0.55)",
        "accent":"#E8709A",
        "border":"rgba(255,255,255,0.10)", "border_soft":"rgba(255,255,255,0.06)",
        "logo_file":"G3D.png",
    },
}
```

If the image is a companion to a carousel (e.g. MON-1B pairs with MON-1), use the same `NOTE_NO` as the parent. If standalone, pick a new random-feeling number.

### Content container

Identical to the carousel:

```css
.content {
    position:relative; z-index:2; height:100%;
    display:flex; flex-direction:column;
    padding:89px 76px 55px 76px;
}
```

### Masthead + HookEyebrow + Sora hook

Same CSS as the carousel (see `linkedin-carousel/SKILL.md`).

```html
<div class="masthead">
  <img src="..." class="mark" alt="smbx.ai">
  <div class="meta">Field Note &nbsp;·&nbsp; <span class="num">No. 17</span></div>
</div>

<div class="eyebrow-hook">
  <span class="dot"></span>
  <span>HVAC &nbsp;·&nbsp; $4M EBITDA &nbsp;·&nbsp; Same metro</span>
</div>

<h1 class="hook">
  Same earnings.<br>Different preparation.
</h1>
```

```css
h1.hook {
    font-family:'Sora'; font-weight:800; font-size:84px;
    line-height:0.96; letter-spacing:-0.04em;
    color:__ink__; margin-top:21px;
}
```

`<br>` acceptable for deliberate two-line editorial cadence. Size per content: 72–84px for most hooks.

### Visual options

Pick one of these patterns for the middle of the page:

**A — Two-column `$` compare** (MON-1B)

```css
.compare-cols {
    margin-top:55px;
    display:grid; grid-template-columns:1fr 1fr; gap:55px;
    padding-bottom:21px; border-bottom:1px solid __border__;
}
.compare-side .label {
    font-family:'Inter'; font-size:24px; font-weight:600;
    text-transform:uppercase; letter-spacing:0.08em; color:__muted__;
}
.compare-side .label.accent { color:__accent__; }
.compare-side .big {
    font-family:'Sora'; font-weight:800; font-size:96px;
    letter-spacing:-0.045em; color:__muted__; margin-top:13px; line-height:1.0;
}
.compare-side .big.accent { color:__accent__; }
.compare-side .mult {
    font-family:'Inter'; font-size:24px; font-weight:500;
    color:__muted__; margin-top:8px;
}

.gap-row {
    margin-top:21px; padding-top:21px;
    border-top:3px solid __accent__;
    display:flex; justify-content:space-between; align-items:baseline;
}
.gap-row .label {
    font-family:'Inter'; font-size:26px; font-weight:700;
    text-transform:uppercase; letter-spacing:0.18em; color:__accent__;
}
.gap-row .val {
    font-family:'Sora'; font-weight:800; font-size:108px;
    letter-spacing:-0.045em; color:__accent__;
}
```

Left column muted, right column accent. Gap row below with the hero number at 108px.

**B — Dark KV card with verdict column** (MON-2B)

Same `kv-card-dark` component as the carousel. Each row has a key and a verdict value. Use when showing N discrete items that all resolve to the same action:

```html
<div class="kv-card-dark">
  <div class="row">
    <span class="k">Concentration</span>
    <span class="v"><span class="num">&gt;25%</span> &nbsp; <span class="verdict">kill</span></span>
  </div>
  <!-- ... -->
</div>
```

```css
.kv-card-dark .row .v .verdict {
    color:__accent__; text-transform:uppercase; letter-spacing:0.04em;
}
```

**C — Single big number** (for stat-hero images)

Same `.light-card > .gap-row` pattern as the carousel S4 anchor — single accent number at 108px as the page's hero.

### Punchline accent block

```css
.punchline {
    margin-top:55px; padding-left:34px;
    border-left:8px solid __accent__;
    font-family:'Sora'; font-weight:800; font-size:38px;
    line-height:1.18; letter-spacing:-0.025em; color:__ink__;
}
.punchline .accent { color:__accent__; }
```

One sentence. 2 lines maximum. The accent word is the point of the whole image.

### Byline — portrait + credentials + date

```css
.byline {
    margin-top:auto;
    display:flex; align-items:center; justify-content:space-between;
    padding-top:21px; border-top:1px solid __border__;
}
.byline .who { display:flex; align-items:center; gap:21px; }
.byline .portrait {
    width:76px; height:76px; border-radius:50%;
    object-fit:cover; object-position:center;
    border:2px solid __border__;
}
.byline .who-text .name {
    font-family:'Sora'; font-weight:800; font-size:30px;
    letter-spacing:-0.02em; color:__ink__;
}
.byline .who-text .cred {
    font-family:'Inter'; font-size:22px; font-weight:500;
    color:__muted__; margin-top:5px;
}
.byline .meta {
    font-family:'Inter'; font-size:24px; font-weight:500;
    color:__muted__;
}
```

Face-on-LinkedIn is non-negotiable. 76px portrait (carousel uses 89px on cover; here 76px since the single page is denser).

## Mobile typography floor

Same as carousel — 1080 canvas → 360px mobile thumbnail (÷3). Canvas-px minimums:

- Eyebrow: 28
- Hook headline: 72–84
- KV card key: 28
- KV card value: 34
- Compare-col big number: 96+
- Gap-row val: 108
- Punchline: 38
- Byline name: 30
- Byline cred: 22

## Fibonacci spacing

Same as carousel — `{8, 13, 21, 34, 55, 89, 144}`. No 20/24/32/40/48/56/60/72/80/96 for layout spacing.

## Render pipeline

```python
HTML = f"""..."""  # single HTML string with the full page

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=DPR)
    tmp = tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode="w")
    tmp.write(HTML); tmp.close()
    page.goto(f"file://{tmp.name}")
    page.wait_for_timeout(2000)
    out = OUT_DIR / f"MON-{N}B-{topic}-single-{MODE}.png"
    page.screenshot(path=str(out))
    os.unlink(tmp.name); browser.close()
```

No PDF assembly — single screenshot PNG.

## Pre-flight checklist

- [ ] Output filename matches `MON-{N}B-{topic}-single-light.png`
- [ ] NOTE_NO matches parent carousel if paired, or random-feeling if standalone
- [ ] LIGHT page background
- [ ] Masthead at top with "Field Note · No. XX"
- [ ] Exactly ONE HookEyebrow (with dot)
- [ ] NO SectionEyebrow anywhere
- [ ] NO cover-swipe hint
- [ ] NO cta-ring block
- [ ] Portrait visible in byline at bottom
- [ ] Punchline has accent left-border rule and ≤ 2 lines
- [ ] Hero number (if present) is at 96–108px Sora 800 accent
- [ ] All type sizes meet mobile floor
- [ ] All spacing from Fibonacci scale
- [ ] `.num` class on every element with digits
- [ ] Em-dashes, typographic quotes, `&times;`, `&ndash;` used correctly
- [ ] `margin-top:auto` on the byline to pin it to the bottom

## Verifying output

```bash
# Just Read the PNG directly — no pdftoppm needed
```

Read the rendered PNG and verify:
1. Masthead with correct No.
2. HookEyebrow visible
3. Sora hook fills the upper third
4. Visual (compare / KV card / big stat) in the middle
5. Punchline above the byline
6. Portrait visible in byline, date on right
7. Bottom 5–10% is breathing room before the byline divider

## Related

- **linkedin-carousel** — 5-slide PDF version with the same component vocabulary
- **copy-editing** — Seven Sweeps on the image text before rendering
- **DESIGN_LANGUAGE.md** — the authoritative visual system this skill implements
