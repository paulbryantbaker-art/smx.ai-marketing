---
name: linkedin-carousel
description: "When the user wants to create, iterate, or render multi-slide LinkedIn carousels as PDFs using the Playwright pipeline. Use when the user mentions 'carousel,' 'LinkedIn slides,' 'PDF carousel,' 'render slides,' 'new carousel,' 'Field Note,' or references any *-carousel-*.py scripts. This skill encodes the 2026-04-15 smbx.ai design canon: Field Note masthead, two-variant eyebrows, Sora 800 + Inter, brand pink accent, Fibonacci spacing, light-dominant deck rhythm with one cinematic dark anchor at S4, ring-CTA close on light page, mobile-compensated typography."
metadata:
  version: 4.0.0
---

# LinkedIn Carousel Production

You produce multi-slide LinkedIn carousels at 1080×1350 portrait using a Playwright-rendered HTML/CSS pipeline at 2× DPR. Output is a multi-page PDF.

## ⚠️ READ THIS FIRST

**Authoritative design docs** — read before building anything:

1. `DESIGN_HANDOFF.md` (repo root) — key deltas from the deprecated cream/rose-gold system
2. `DESIGN_LANGUAGE.md` (repo root) — full visual system, authoritative as of 2026-04-15
3. `STYLE_GUIDE.md` (repo root) — brand voice and copy patterns (unchanged)

**Reference implementations** — the four shipped decks encode the proven pattern:

- `content/week-01/carousel-sellers-hvac.py` (MON-1, Field Note No. 17)
- `content/week-01/carousel-buyers-pe-screen.py` (MON-2, No. 23)
- `content/week-01/carousel-executives-exit.py` (MON-3, No. 31)
- `content/week-01/carousel-dealpros-closed3.py` (MON-4, No. 38)

If your output looks different from these rendered PDFs, you are wrong. Copy their CSS + TOKENS + `wrap()` / `masthead()` / `footer()` / `attr_imm()` functions exactly.

### Forbidden patterns

| Pattern | Why |
|---|---|
| Cream `#F8F6F2` backgrounds | Deprecated 2026-04-04 system. Use `#F9F9FC` (light). |
| Sora weight 900 keyword | Sora's heaviest Google Fonts weight is 800 — use 800. |
| Dark backgrounds across the whole deck | Dark is CONTRAST, used once per deck on the cinematic anchor (S4). Cover + content + close are all LIGHT. |
| "Field Note · No. 01" sequential numbering | Field Note numbers should feel like an established series — pick non-sequential numbers (e.g. 17, 23, 31, 38). |
| HookEyebrow on more than one slide | HookEyebrow (dot + 0.2em tracking) is once per deck, on the cover only. Content and close slides use SectionEyebrow. |
| Missing byline / portrait on cover | Cover must have portrait + name + credentials. Face-on-LinkedIn is non-negotiable. |
| Radial-gradient blur halos behind CTAs | AI-slop tell. Use ring-accent pattern (1px accent border + inner hairline + soft drop shadow). |
| Glassmorphism on content cards | Reserved for site mobile chrome. Carousels use flat hairlines. |
| Gradient text headlines (`background-clip: text`) | AI-slop tell. Solid ink or solid white only. |
| Accent color filling backgrounds | Pink is surgical punctuation, never wallpaper. |
| Multiple accent elements per slide | One non-structural accent per slide. Eyebrow and data-anchor accents are structural. |
| Body/eyebrow type smaller than canvas-mobile floor | 1080 canvas → 360px mobile thumbnail. Eyebrow floor 28px, body floor 26px, footer floor 26px. |
| Non-Fibonacci spacing | All margins/padding from {8, 13, 21, 34, 55, 89, 144}. |

## Format

| Attribute | Value |
|---|---|
| Canvas per slide | 1080 × 1350 px (4:5 portrait) |
| Slide count | 5 slides — cover, data, data, cinematic anchor, close |
| DPR | 2× (renders at 2160 × 2700) |
| Output | Multi-page PDF via Pillow at 288 DPI |
| Fonts | Sora 600/700/800 + Inter 400/500/600/700 via Google Fonts `@import` |
| Assets | Base64-embedded (logo, portrait) — never external paths |
| Font load wait | `page.wait_for_timeout(2000)` per slide |
| Script name | `carousel-{topic}.py` |
| Output PDF name | `MON-{N}-{topic}-{mode}.pdf` or whatever day prefix is in use |

## The 5-slide rhythm

LIGHT is the dominant mode. DARK appears once, on the cinematic anchor (S4).

| Slide | Surface | Purpose | Structure |
|---|---|---|---|
| S1 Cover | LIGHT | Who's writing, what's the hook, what data justifies swiping | Masthead (logo + "Field Note · No. XX") → HookEyebrow → Sora hook → mega-compare → portrait byline → swipe |
| S2 Data | LIGHT | First protagonist / first data point | SectionEyebrow → Sora headline → dark KV card → footer |
| S3 Data | LIGHT | Second protagonist / second data point (card type alternates from S2) | SectionEyebrow → Sora headline → bordered KV card (+ optional proof badges) → footer |
| S4 Anchor | DARK (`#0f1012`) | The money moment — hero data or quote lands here | SectionEyebrow → small headline → **light card on dark stage** → discrete bottom attribution |
| S5 Close | LIGHT | Prompt + CTA | SectionEyebrow → Sora prompt → sub paragraph → **dark ring-CTA block** → footer |

This rhythm mirrors the smbx.ai site's journey pages: light hero → light sections → one immersive dark cinematic-anchor band → light close with dark PageCTA block.

## Required scaffolding — copy from MON-1 (`carousel-sellers-hvac.py`)

### 1. TOKENS dict (light + dark deck modes + immersive stage tokens)

```python
TOKENS = {
    "light": {
        "bg":"#F9F9FC", "bg_alt":"#f4f4f7",
        "ink":"#0f1012", "body":"#3c3d40", "muted":"#6e6a63",
        "accent":"#D44A78", "accent_hover":"#B03860",
        "tint":"rgba(212,74,120,0.08)",
        "border":"rgba(15,16,18,0.08)", "border_soft":"rgba(15,16,18,0.06)",
        "card_bg":"#ffffff",
        "logo_file":"G3L.png",
    },
    "dark": {
        "bg":"#1A1C1E", "bg_alt":"#151617",
        "ink":"#f9f9fc", "body":"rgba(218,218,220,0.85)", "muted":"rgba(218,218,220,0.55)",
        "accent":"#E8709A",
        "tint":"rgba(232,112,154,0.10)",
        "border":"rgba(255,255,255,0.08)", "border_soft":"rgba(255,255,255,0.06)",
        "card_bg":"#1a1c1e",
        "logo_file":"G3D.png",
    },
}

# Immersive dark stage — used by S4 cinematic anchor regardless of deck mode.
IMM = {
    "bg":"#0f1012",
    "ink":"#f9f9fc",
    "muted":"rgba(255,255,255,0.55)",
    "body":"rgba(255,255,255,0.78)",
    "accent": TOK["accent"],
    "border":"rgba(255,255,255,0.10)",
}
```

Light mode is production default. Dark mode is a full-deck invert (rare).

### 2. NOTE_NO — pick a random-feeling number

```python
NOTE_NO = "No. 17"   # or 23, 31, 38 — non-sequential, feels like an established series
```

Never "No. 01" for first post. Field Note No. 17+ signals "this is post N of an ongoing series", which reads stronger than "this is our first".

### 3. Content container

```css
.content {
    position:relative; z-index:2; height:100%;
    display:flex; flex-direction:column;
    padding:89px 76px 55px 76px;     /* Fibonacci: 89/76/55 */
}
```

`flex-direction:column` + `margin-top:auto` on the footer element is the ONLY layout mechanism. Top-aligned content, bottom breathes, footer pinned.

### 4. Masthead — Field Note signature (cover)

```python
def masthead():
    return f"""<div class="masthead">
      <img src="data:image/png;base64,{LOGO_DECK}" class="mark" alt="smbx.ai">
      <div class="meta">Field Note &nbsp;·&nbsp; <span class="num">{NOTE_NO}</span></div>
    </div>"""
```

```css
.masthead {
    display:flex; align-items:center; justify-content:space-between;
    padding-bottom:21px; border-bottom:1px solid __border__;
}
.masthead .mark { height:55px; object-fit:contain; }
.masthead .meta {
    font-family:'Inter'; font-size:24px; font-weight:700;
    text-transform:uppercase; letter-spacing:0.2em; color:__muted__;
}
.masthead .meta .num { color:__ink__; }
```

Logo top-left (55px), "FIELD NOTE · NO. XX" top-right (24px uppercase tracked). Hairline divider below. Cover uses masthead AND HookEyebrow below. Content slides (S2–S5) open directly with SectionEyebrow — no masthead repeat, keeps content breathing.

### 5. HookEyebrow vs SectionEyebrow

```css
/* HookEyebrow — opens the deck, once per piece, on cover only */
.eyebrow-hook {
    display:flex; align-items:center; gap:13px;
    margin-top:55px;
    font-family:'Inter'; font-size:28px; font-weight:700;
    text-transform:uppercase; letter-spacing:0.2em;
    color:__accent__;
}
.eyebrow-hook .dot {
    width:14px; height:14px; border-radius:50%;
    background:__accent__; flex-shrink:0;
}

/* SectionEyebrow — per-slide opener, no dot */
.eyebrow-section {
    font-family:'Inter'; font-size:28px; font-weight:600;
    text-transform:uppercase; letter-spacing:0.08em;
    color:__accent__;
}
```

This two-variant system is the signature detail that makes the deck read as a document instead of a repeating slogan.

### 6. Display headlines

```css
h1.hook {
    font-family:'Sora'; font-weight:800;
    line-height:0.94; letter-spacing:-0.04em;
    color:__ink__; margin-top:21px;
}
h1.section {
    font-family:'Sora'; font-weight:800;
    line-height:1.0; letter-spacing:-0.03em;
    color:__ink__; margin-top:21px;
}
```

Always inline `style="font-size:Xpx"`. Per-slide sizing:
- Hook on cover (short fragments): 84–108px
- Hook on close (statement): 72–84px
- Section headlines: 60–72px

`<br>` is acceptable **only** for multi-fragment cadence where each fragment is a complete thought ("Same metro.<br>Same revenue.<br>Same year." / "40 hours.<br>30 minutes.<br>Same CIM."). **Never use `<br>` inside a single sentence.** If a single-sentence hook doesn't fit on one line at your chosen H1 size, reduce the font size until it does, or let CSS word-wrap pick the break point. Force-breaking "Hidden in<br>plain sight." (splitting a prepositional phrase) is the AI-slop tell.

### 7. Footer + attr_imm

```python
def footer():
    return f"""<div class="foot">
      <div class="who">
        <img src="data:image/jpeg;base64,{HEADSHOT}" class="portrait" alt="Paul Baker">
        <span><span class="name-ink">Paul Baker</span> &nbsp;·&nbsp; smbx.ai</span>
      </div>
      <div class="num">{YEAR_WEEK}</div>
    </div>"""

def attr_imm():
    return f"""<div class="attr-imm">
      <img src="data:image/png;base64,{LOGO_DARK_BG}" class="mark" alt="smbx.ai">
      <div class="meta">Paul Baker &nbsp;·&nbsp; <span class="num">{YEAR_WEEK}</span></div>
    </div>"""
```

```css
.foot {
    margin-top:auto;
    display:flex; align-items:center; justify-content:space-between;
    padding-top:21px; border-top:1px solid __border__;
    font-family:'Inter'; font-size:26px; font-weight:500; color:__muted__;
}
.foot .who { display:flex; align-items:center; gap:13px; }
.foot .portrait {
    width:48px; height:48px; border-radius:50%;
    object-fit:cover; object-position:center; border:1px solid __border__;
}
.foot .name-ink { color:__ink__; font-weight:700; }

.attr-imm {
    margin-top:auto;
    display:flex; align-items:center; justify-content:space-between;
    padding-top:34px; opacity:0.55;
}
.attr-imm .mark { height:34px; object-fit:contain; }
.attr-imm .meta { font-family:'Inter'; font-size:22px; font-weight:500; color:rgba(255,255,255,0.7); }
```

`foot` is the standard per-slide attribution on light slides. `attr_imm` is the quieter (55% opacity) version for the S4 cinematic anchor where the full footer would break the immersive effect.

## Component library

All sizes calibrated for 1080 canvas → 360px mobile thumbnail (÷3). Values below are canvas px.

### Cover-only components

**Mega-compare** — the data hook on the cover. Two muted rows + one accent gap row.

```css
.mega-compare {
    margin-top:55px;
    border-top:1px solid __border__; border-bottom:1px solid __border__;
    padding:21px 0;
}
.mega-row { display:flex; justify-content:space-between; align-items:baseline; padding:13px 0; }
.mega-row .label { font-family:'Inter'; font-size:30px; font-weight:500; color:__muted__; }
.mega-row .val { font-family:'Sora'; font-weight:800; font-size:64px; letter-spacing:-0.04em; color:__ink__; }
.mega-row .val.muted { color:__muted__; font-size:55px; }
.mega-row .val.accent { color:__accent__; }

.mega-gap {
    display:flex; justify-content:space-between; align-items:baseline;
    margin-top:13px; padding:21px 0 0 0; border-top:3px solid __accent__;
}
.mega-gap .label { font-family:'Inter'; font-size:24px; font-weight:700; text-transform:uppercase; letter-spacing:0.18em; color:__accent__; }
.mega-gap .val { font-family:'Sora'; font-weight:800; font-size:89px; letter-spacing:-0.045em; color:__accent__; }
```

Keep gap-row value to ≤6 characters. If longer (e.g. "$12K / $85K"), restructure to a punchier single value like "7× cheaper".

**Cover byline** — portrait + name + credentials. Face on LinkedIn.

```css
.cover-byline {
    margin-top:55px;
    display:flex; align-items:center; gap:21px;
}
.cover-byline .portrait {
    width:89px; height:89px; border-radius:50%;
    object-fit:cover; object-position:center; border:2px solid __border__;
}
.cover-byline .who .name {
    font-family:'Sora'; font-weight:800; font-size:34px;
    letter-spacing:-0.02em; color:__ink__;
}
.cover-byline .who .cred {
    font-family:'Inter'; font-size:24px; font-weight:500;
    color:__muted__; margin-top:8px;
}
```

**Cover swipe hint** — bottom-anchored `Swipe ›`.

```css
.cover-swipe {
    margin-top:auto;
    display:flex; align-items:center; justify-content:flex-end;
    padding-top:21px; border-top:1px solid __border__;
}
.cover-swipe .hint {
    font-family:'Inter'; font-size:24px; font-weight:700;
    text-transform:uppercase; letter-spacing:0.2em; color:__accent__;
}
```

### Content-slide components

**Dark KV card** (S2 typical): flat dark card on the light page.

```css
.kv-card-dark {
    background:#0f1012; border-radius:14px;
    padding:21px 34px 13px 34px; margin-top:55px;
    box-shadow: 0 21px 55px -34px rgba(15,16,18,0.45);
}
.kv-card-dark .row {
    display:flex; justify-content:space-between; align-items:baseline;
    padding:21px 0; border-bottom:1px solid rgba(255,255,255,0.08);
}
.kv-card-dark .row:last-child { border-bottom:none; }
.kv-card-dark .row .k { font-family:'Inter'; font-size:28px; font-weight:600; color:rgba(255,255,255,0.55); }
.kv-card-dark .row .v { font-family:'Sora'; font-weight:800; font-size:38px; letter-spacing:-0.02em; color:#f9f9fc; }
.kv-card-dark .row .v.accent { color:__accent__; }
```

4–5 rows is the sweet spot. Last row can carry `.v.accent` to highlight the outcome.

**Bordered KV card** (S3 typical): hairline on the light page — lighter weight than the dark card, used to alternate.

```css
.kv-card {
    background:__card_bg__; border:1px solid __border__; border-radius:14px;
    padding:21px 34px 13px 34px; margin-top:55px;
}
.kv-card .row {
    display:flex; justify-content:space-between; align-items:baseline;
    padding:21px 0; border-bottom:1px solid __border_soft__;
}
.kv-card .row:last-child { border-bottom:none; }
.kv-card .row .k { font-family:'Inter'; font-size:28px; font-weight:600; color:__muted__; }
.kv-card .row .v { font-family:'Sora'; font-weight:800; font-size:34px; letter-spacing:-0.02em; color:__ink__; }
.kv-card .row .v.accent { color:__accent__; }
.kv-card .row.divider { border-top:2px solid __border__; padding-top:28px; margin-top:8px; }
```

`.row.divider` optionally separates paired groups (e.g. "Screens 2 + 3").

**Proof badge row** (optional accent on S3):

```css
.proof-row {
    display:flex; align-items:center; gap:13px; flex-wrap:wrap;
    padding:21px 34px; background:__tint__; border-radius:13px; margin-top:34px;
}
.proof-row .label { font-family:'Inter'; font-size:28px; font-weight:700; color:__ink__; }
.proof-row .badge {
    display:inline-flex; align-items:center; padding:8px 21px;
    border:1.5px solid __accent__; border-radius:999px;
}
.proof-row .badge .n { font-family:'Sora'; font-weight:800; font-size:32px; color:__accent__; letter-spacing:-0.02em; }
```

### S4 cinematic anchor — light card on dark stage

The signature move. Full-bleed dark `#0f1012`, centered white card with hairline + soft drop shadow. Hero data or a quote lives inside.

```css
.light-card {
    margin-top:55px;
    background:#ffffff;
    border:1px solid rgba(15,16,18,0.08); border-radius:21px;
    padding:55px 55px 34px 55px;
    box-shadow: 0 34px 89px -34px rgba(0,0,0,0.55);
    color:#0f1012;
}
.light-card .anchor-eyebrow {
    font-family:'Inter'; font-size:28px; font-weight:600;
    text-transform:uppercase; letter-spacing:0.08em; color:#D44A78;
}

/* Data variant — row-lines + gap-row + caption */
.light-card .row-line {
    display:flex; justify-content:space-between; align-items:baseline;
    padding:13px 0; border-bottom:1px solid rgba(15,16,18,0.06);
}
.light-card .row-line:first-of-type { margin-top:21px; }
.light-card .row-line .k { font-family:'Inter'; font-size:28px; font-weight:500; color:#6e6a63; }
.light-card .row-line .v { font-family:'Sora'; font-weight:800; font-size:55px; letter-spacing:-0.03em; color:#3c3d40; }
.light-card .gap-row {
    display:flex; justify-content:space-between; align-items:baseline;
    padding-top:34px; margin-top:21px; border-top:3px solid #D44A78;
}
.light-card .gap-row .k { font-family:'Inter'; font-size:28px; font-weight:700; text-transform:uppercase; letter-spacing:0.08em; color:#D44A78; }
.light-card .gap-row .v { font-family:'Sora'; font-weight:800; font-size:108px; letter-spacing:-0.045em; color:#D44A78; }
.light-card .caption { font-family:'Inter'; font-size:24px; font-weight:400; color:#6e6a63; margin-top:21px; line-height:1.4; }

/* Quote variant — replace row-lines with quote + attribution */
.light-card .quote {
    font-family:'Sora'; font-weight:800; font-size:48px;
    line-height:1.18; letter-spacing:-0.025em; color:#0f1012; margin-top:21px;
}
.light-card .quote .accent { color:#D44A78; }
.light-card .attribution {
    font-family:'Inter'; font-size:22px; font-weight:500;
    color:#6e6a63; margin-top:21px; padding-left:13px;
    border-left:3px solid #D44A78;
}
```

Two S4 flavors in the reference decks:
- **Data variant** (MON-1, MON-3): two data rows + accent gap row with the hero number at 108px. See `carousel-sellers-hvac.py` S4.
- **Quote variant** (MON-4): pulled quote + attribution + optional small data row. See `carousel-dealpros-closed3.py` S4.

MON-2 uses a hybrid (kill-rows with verdicts + prose punchline). All three patterns are valid — pick what the content wants.

### S5 close — dark ring-CTA block on light page

Mirrors the site's PageCTA pattern. The dark block is the punch; the page around it stays light.

```css
.cta-ring {
    margin-top:55px;
    background:#0f1012;
    border:1px solid rgba(212,74,120,0.55);
    border-radius:21px;
    padding:55px 48px 48px 48px;
    box-shadow:
        inset 0 0 0 1px rgba(212,74,120,0.18),
        0 34px 55px -34px rgba(15,16,18,0.45);
}
.cta-ring .cta-eyebrow { font-family:'Inter'; font-size:28px; font-weight:600; text-transform:uppercase; letter-spacing:0.08em; color:#E8709A; }
.cta-ring h2 { font-family:'Sora'; font-weight:800; font-size:55px; line-height:1.04; letter-spacing:-0.03em; color:#f9f9fc; margin-top:21px; }
.cta-ring .pill {
    display:inline-flex; align-items:center; gap:13px;
    margin-top:34px; padding:21px 34px;
    background:#E8709A; color:#0f1012;
    border-radius:999px;
    font-family:'Inter'; font-size:26px; font-weight:700; letter-spacing:0.02em;
}
.cta-ring .pill .arrow { font-family:'Sora'; font-weight:700; }
.cta-ring .reassure { font-family:'Inter'; font-size:24px; font-weight:400; color:rgba(255,255,255,0.55); margin-top:21px; }
```

Block structure:
```html
<div class="cta-ring">
  <div class="cta-eyebrow">Free · 12 minutes</div>
  <h2>Run a Baseline™ on your business.</h2>
  <span class="pill">Start at smbx.ai <span class="arrow">›</span></span>
  <div class="reassure">No account required · Your data stays yours</div>
</div>
```

The pill text is an action verb + specific output ("Start at smbx.ai", "Run a Baseline"). Trademark terms (Baseline™, Blind Equity™, Rundown™) use `&trade;`.

## Mobile typography floor (non-negotiable)

LinkedIn is 95%+ mobile. 1080 canvas → ~360px thumbnail (÷3). Minimum canvas sizes:

| Element | Canvas px | Mobile px |
|---|---|---|
| Eyebrow (both variants) | 28 | 9.3 |
| Body paragraph | 34 | 11.3 |
| KV card key | 28 | 9.3 |
| KV card value (Sora 800) | 34–38 | 11.3–12.7 |
| Footer | 26 | 8.7 |
| Caption on cinematic anchor | 24 | 8.0 |
| Hero headline on cover | 84–108 | 28–36 |

Never go below 24px on canvas for any readable text. The site's web type scale (17–19px body) is for 1280px+ screens, not the carousel — do not copy it here.

## Fibonacci spacing

All margins and padding come from {8, 13, 21, 34, 55, 89, 144}. Typical cadence:

- Section padding top: **89**
- Section padding bottom: **55**
- Card vertical padding: **21–34**
- Headline → sub gap: **34**
- Sub → card gap: **55**
- Card → footer gap: **auto** (pushed by flex)
- Eyebrow → headline: **21**
- Masthead bottom border padding: **21**
- Row-line internal padding: **13–21**

Paul explicitly called this out. Do not use non-Fibonacci values (20, 24, 32, 40, 48, 56, 60, 72, 80, 96) for layout spacing.

## Voice (from STYLE_GUIDE.md + DESIGN_LANGUAGE.md § 8)

Brief, declarative, confident. No hedging. No "we believe". No "empowering". No "revolutionary".

**Hook pattern** — fragmented money question or sharp promise:
- "Same metro. Same revenue. Same year."
- "Kill 15 deals before lunch."
- "He closed 3. His cohort closed 0."

**Section headline pattern** — declarative claim with one number, verb, or proper noun:
- "He brought tax returns and a tired handshake."
- "One customer above 25% — kill."
- "An IT services company added $15.6M with one sentence."

**Body pattern** — named protagonists, real numbers, specific outcomes.

**CTA pattern** — action verb + specific output. "Run a Baseline", "Pre-screen any deal", "Map your exit". Never "Learn More".

**Trademark terms** (Baseline™, Blind Equity™, Rundown™) use the `&trade;` glyph.

## Render pipeline (copy verbatim from any reference impl)

```python
slides = [S1, S2, S3, S4, S5]

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=DPR)

    pngs = []
    for i, html in enumerate(slides):
        tmp = tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode="w")
        tmp.write(html); tmp.close()
        page.goto(f"file://{tmp.name}")
        page.wait_for_timeout(2000)
        png_path = tempfile.NamedTemporaryFile(suffix=".png", delete=False); png_path.close()
        page.screenshot(path=png_path.name)
        pngs.append(png_path.name)
        os.unlink(tmp.name)

    browser.close()

imgs = [Image.open(p).convert("RGB").resize((W, H), Image.LANCZOS) for p in pngs]
pdf_path = OUT_DIR / f"MON-{N}-{topic}-{MODE}.pdf"
imgs[0].save(str(pdf_path), "PDF", resolution=288.0, save_all=True, append_images=imgs[1:])

for p in pngs:
    os.unlink(p)
```

## Slide composition rules

1. **Maximum 2–3 content elements per slide** (eyebrow + headline + one card, or eyebrow + headline + sub + CTA ring on S5).
2. **Card alternation** across S2 → S3: if S2 has a dark KV card, S3 uses a bordered KV card (+ optional proof badges).
3. **One non-structural accent per slide.** Eyebrow color and accent gap rows are structural (don't count). Body accents cap at one.
4. **Content top-aligned, bottom breathes.** `margin-top:auto` on the footer/attribution is the only layout mechanism.
5. **Tabular numbers everywhere.** Apply `class="num"` to every element containing digits.
6. **Typography details:**
   - Em-dash: `&mdash;` with `&thinsp;` around it for tight dash rhythm
   - Typographic quotes: `&ldquo;` `&rdquo;` / `&lsquo;` `&rsquo;`
   - `&times;` for multiples (3.2×)
   - `&ndash;` for ranges (5.5–6.0×)
   - `&nbsp;·&nbsp;` as separator in metadata
   - `&rsaquo;` for swipe/arrow glyphs

## Pre-flight checklist

- [ ] Output filename matches `MON-{N}-{topic}-light.pdf`
- [ ] NOTE_NO is random-feeling (17, 23, 31, 38, etc.), not "No. 01"
- [ ] Cover has masthead + HookEyebrow + Sora hook + mega-compare + portrait byline + swipe
- [ ] S2/S3 alternate card types (dark KV vs bordered KV)
- [ ] S4 is the ONLY dark slide, uses light-card-on-dark pattern with `attr_imm()` attribution
- [ ] S5 is LIGHT with a dark `cta-ring` block inside it (not a full dark page)
- [ ] HookEyebrow appears exactly once (on the cover)
- [ ] SectionEyebrow on every other slide
- [ ] All type sizes meet the mobile floor (eyebrow ≥28, body ≥26, KV-k ≥28, KV-v ≥34, footer ≥26)
- [ ] All spacing values from Fibonacci scale
- [ ] Every slide has exactly ONE non-structural accent in the body
- [ ] Content padding is `89px 76px 55px 76px`
- [ ] `margin-top:auto` on footer/`attr_imm`/`cover-swipe` and ONLY those elements
- [ ] Em-dashes, typographic quotes, `&times;`, `&ndash;` used correctly
- [ ] `.num` class on every element containing digits
- [ ] All slides fit within 1350px height (footer visible, no clipping)

## Verifying output

Extract slides and Read each PNG before declaring done:

```bash
pdftoppm -png -r 144 content/week-01/MON-{N}-{topic}-light.pdf /tmp/check
```

Per-slide checks:
1. Cover has portrait visible in byline
2. Content sits in top 55–65% on light slides
3. S4 cinematic has the light card centered, discrete attribution at bottom
4. S5 dark CTA block sits inside the light page, not a full dark background
5. Headlines fill ≥75% of line width — no orphans
6. All text is legibly sized for mobile (re-check against the floor table)

If any slide fails: fix the script and re-render.

## Related

- **linkedin-image-post** (`.agents/skills/linkedin-image-post/`) — single 1080×1350 standalone Field Note image using the same component library
- **copy-editing** — Seven Sweeps on slide text before rendering
- **copywriting** — for hook and headline drafting
- **DESIGN_LANGUAGE.md** — the authoritative visual system this skill implements
