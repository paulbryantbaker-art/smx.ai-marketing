#!/usr/bin/env python3
"""
smbx.ai LinkedIn Carousel — Monday Post 1: Sellers
"7.2× vs 3.1× HVAC" — Small Business Network (314K)

Built to the smbx.ai DESIGN_LANGUAGE.md (2026-04-15 redesign), with
LinkedIn-mobile typography compensation and Fibonacci spacing
(8/13/21/34/55/89/144) throughout.

Deck rhythm — light is the dominant mode, dark is contrast:
  S1 cover    LIGHT  Field Note masthead, portrait byline, data hook
  S2 3.1×     LIGHT  dark KV card on light page
  S3 7.2×     LIGHT  bordered KV card + accent proof badges
  S4 gap      DARK   cinematic anchor — light card on dark stage
  S5 close    LIGHT  Sora prompt + dark ring-CTA block on light page

Usage:
    python3 carousel-sellers-hvac.py            # light deck (default)
    python3 carousel-sellers-hvac.py dark
"""

import os, sys, base64, tempfile
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image

W, H = 1080, 1350
DPR = 2
REPO = Path(__file__).resolve().parent.parent.parent
OUT_DIR = REPO / "content" / "week-01"

MODE = sys.argv[1].lower() if len(sys.argv) > 1 else "light"
assert MODE in ("light", "dark")

YEAR_WEEK = "2026 · Week 01"
NOTE_NO   = "No. 17"

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
        "accent":"#E8709A", "accent_hover":"#B03860",
        "tint":"rgba(232,112,154,0.10)",
        "border":"rgba(255,255,255,0.08)", "border_soft":"rgba(255,255,255,0.06)",
        "card_bg":"#1a1c1e",
        "logo_file":"G3D.png",
    },
}
TOK = TOKENS[MODE]

# Immersive dark stage — used by the cinematic anchor slide only.
IMM = {
    "bg":"#0f1012",
    "ink":"#f9f9fc",
    "muted":"rgba(255,255,255,0.55)",
    "body":"rgba(255,255,255,0.78)",
    "accent": TOK["accent"],
    "border":"rgba(255,255,255,0.10)",
}

def b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

LOGO_LIGHT_BG = b64(REPO / "assets" / "logos" / "G3L.png")  # black wordmark for light pages
LOGO_DARK_BG  = b64(REPO / "assets" / "logos" / "G3D.png")  # white wordmark for dark surfaces
LOGO_DECK     = b64(REPO / "assets" / "logos" / TOK["logo_file"])
HEADSHOT      = b64(REPO / "assets" / "portrait-square.jpeg")

# ── CSS ────────────────────────────────────────────────────────────────
# Sizes calibrated for 1080 canvas → 360px mobile thumbnail (÷3).
# Spacing uses Fibonacci scale {8, 13, 21, 34, 55, 89, 144} throughout.
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap');
* { margin:0; padding:0; box-sizing:border-box; }
body { width:1080px; height:1350px; overflow:hidden; font-family:'Inter', system-ui, sans-serif; -webkit-font-smoothing:antialiased; }
.num { font-variant-numeric:tabular-nums; font-feature-settings:'tnum' 1; }
.canvas { width:1080px; height:1350px; position:relative; overflow:hidden; }

.canvas.light { background:__bg__; color:__ink__; }
.canvas.imm   { background:__imm_bg__; color:__imm_ink__; }

.content {
    position:relative; z-index:2; height:100%;
    display:flex; flex-direction:column;
    padding:89px 76px 55px 76px;
}

/* ── Masthead — Field Note signature ────────────────────────────────── */
.masthead {
    display:flex; align-items:center; justify-content:space-between;
    padding-bottom:21px; border-bottom:1px solid __border__;
}
.masthead .mark { height:55px; object-fit:contain; }
.masthead .meta {
    font-family:'Inter'; font-size:24px; font-weight:700;
    text-transform:uppercase; letter-spacing:0.2em;
    color:__muted__;
}
.masthead .meta .num { color:__ink__; }
.canvas.imm .masthead { border-bottom-color:rgba(255,255,255,0.10); }
.canvas.imm .masthead .meta { color:rgba(255,255,255,0.55); }
.canvas.imm .masthead .meta .num { color:#f9f9fc; }

/* ── HookEyebrow — opens deck, accent + dot, 0.2em ──────────────────── */
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

/* ── SectionEyebrow — per-section, 0.08em, no dot ───────────────────── */
.eyebrow-section {
    font-family:'Inter'; font-size:28px; font-weight:600;
    text-transform:uppercase; letter-spacing:0.08em;
    color:__accent__;
}
.canvas.imm .eyebrow-section { color:__imm_accent__; }

/* ── Display headlines ──────────────────────────────────────────────── */
h1.hook {
    font-family:'Sora'; font-weight:800;
    line-height:0.94; letter-spacing:-0.04em;
    color:__ink__; margin-top:21px;
}
.canvas.imm h1.hook { color:__imm_ink__; }

h1.section {
    font-family:'Sora'; font-weight:800;
    line-height:1.0; letter-spacing:-0.03em;
    color:__ink__; margin-top:21px;
}
.canvas.imm h1.section { color:__imm_ink__; }

p.sub {
    font-family:'Inter'; font-weight:400;
    font-size:34px; line-height:1.45;
    color:__body__; margin-top:34px; max-width:920px;
}
.canvas.imm p.sub { color:__imm_body__; }
p.sub strong { color:__ink__; font-weight:600; }
.canvas.imm p.sub strong { color:__imm_ink__; }

/* ── Mega-compare (cover data hook) ─────────────────────────────────── */
.mega-compare {
    margin-top:55px;
    border-top:1px solid __border__;
    border-bottom:1px solid __border__;
    padding:21px 0;
}
.mega-row {
    display:flex; justify-content:space-between; align-items:baseline;
    padding:13px 0;
}
.mega-row .label {
    font-family:'Inter'; font-size:30px; font-weight:500; color:__muted__;
}
.mega-row .val {
    font-family:'Sora'; font-weight:800; font-size:64px;
    letter-spacing:-0.04em; color:__ink__;
}
.mega-row .val.muted { color:__muted__; font-size:55px; }
.mega-row .val.accent { color:__accent__; }

.mega-gap {
    display:flex; justify-content:space-between; align-items:baseline;
    margin-top:13px; padding:21px 0 0 0;
    border-top:3px solid __accent__;
}
.mega-gap .label {
    font-family:'Inter'; font-size:24px; font-weight:700;
    text-transform:uppercase; letter-spacing:0.18em; color:__accent__;
}
.mega-gap .val {
    font-family:'Sora'; font-weight:800; font-size:89px;
    letter-spacing:-0.045em; color:__accent__;
}

/* ── Cover byline (portrait + name + credentials) ───────────────────── */
.cover-byline {
    margin-top:55px;
    display:flex; align-items:center; gap:21px;
}
.cover-byline .portrait {
    width:89px; height:89px; border-radius:50%;
    object-fit:cover; object-position:center;
    border:2px solid __border__;
}
.cover-byline .who .name {
    font-family:'Sora'; font-weight:800; font-size:34px;
    letter-spacing:-0.02em; color:__ink__;
}
.cover-byline .who .cred {
    font-family:'Inter'; font-size:24px; font-weight:500;
    color:__muted__; margin-top:8px;
}

/* ── Cover swipe hint (bottom strip) ────────────────────────────────── */
.cover-swipe {
    margin-top:auto;
    display:flex; align-items:center; justify-content:flex-end;
    padding-top:21px; border-top:1px solid __border__;
}
.cover-swipe .hint {
    font-family:'Inter'; font-size:24px; font-weight:700;
    text-transform:uppercase; letter-spacing:0.2em; color:__accent__;
}

/* ── Footer (light surfaces) ────────────────────────────────────────── */
.foot {
    margin-top:auto;
    display:flex; align-items:center; justify-content:space-between;
    padding-top:21px; border-top:1px solid __border__;
    font-family:'Inter'; font-size:26px; font-weight:500;
    color:__muted__;
}
.foot .who { display:flex; align-items:center; gap:13px; }
.foot .portrait {
    width:48px; height:48px; border-radius:50%;
    object-fit:cover; object-position:center;
    border:1px solid __border__;
}
.foot .name-ink { color:__ink__; font-weight:700; }

/* ── Discrete attribution for cinematic-anchor slides ───────────────── */
.attr-imm {
    margin-top:auto;
    display:flex; align-items:center; justify-content:space-between;
    padding-top:34px;
    opacity:0.55;
}
.attr-imm .mark { height:34px; object-fit:contain; }
.attr-imm .meta {
    font-family:'Inter'; font-size:22px; font-weight:500;
    color:rgba(255,255,255,0.7);
}

/* ── Dark KV card on light page ─────────────────────────────────────── */
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
.kv-card-dark .row .v {
    font-family:'Sora'; font-weight:800; font-size:38px;
    letter-spacing:-0.02em; color:#f9f9fc;
}

/* ── Bordered KV card ───────────────────────────────────────────────── */
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
.kv-card .row .v {
    font-family:'Sora'; font-weight:800; font-size:38px;
    letter-spacing:-0.02em; color:__ink__;
}

/* ── Proof badge row ────────────────────────────────────────────────── */
.proof-row {
    display:flex; align-items:center; gap:13px; flex-wrap:wrap;
    padding:21px 34px; background:__tint__; border-radius:13px; margin-top:34px;
}
.proof-row .label { font-family:'Inter'; font-size:28px; font-weight:700; color:__ink__; }
.proof-row .badge {
    display:inline-flex; align-items:center; padding:8px 21px;
    border:1.5px solid __accent__; border-radius:999px;
}
.proof-row .badge .n {
    font-family:'Sora'; font-weight:800; font-size:32px;
    color:__accent__; letter-spacing:-0.02em;
}

/* ── Light card on dark stage (cinematic anchor) ────────────────────── */
.light-card {
    margin-top:55px;
    background:#ffffff;
    border:1px solid rgba(15,16,18,0.08);
    border-radius:21px;
    padding:55px 55px 34px 55px;
    box-shadow: 0 34px 89px -34px rgba(0,0,0,0.55);
    color:#0f1012;
}
.light-card .anchor-eyebrow {
    font-family:'Inter'; font-size:28px; font-weight:600;
    text-transform:uppercase; letter-spacing:0.08em;
    color:#D44A78;
}
.light-card .row-line {
    display:flex; justify-content:space-between; align-items:baseline;
    padding:13px 0; border-bottom:1px solid rgba(15,16,18,0.06);
}
.light-card .row-line:first-of-type { margin-top:21px; }
.light-card .row-line .k {
    font-family:'Inter'; font-size:28px; font-weight:500; color:#6e6a63;
}
.light-card .row-line .v {
    font-family:'Sora'; font-weight:800; font-size:55px;
    letter-spacing:-0.03em; color:#3c3d40;
}
.light-card .gap-row {
    display:flex; justify-content:space-between; align-items:baseline;
    padding-top:34px; margin-top:21px;
    border-top:3px solid #D44A78;
}
.light-card .gap-row .k {
    font-family:'Inter'; font-size:28px; font-weight:700;
    text-transform:uppercase; letter-spacing:0.08em; color:#D44A78;
}
.light-card .gap-row .v {
    font-family:'Sora'; font-weight:800; font-size:108px;
    letter-spacing:-0.045em; color:#D44A78;
}
.light-card .caption {
    font-family:'Inter'; font-size:24px; font-weight:400;
    color:#6e6a63; margin-top:21px; line-height:1.4;
}

/* ── Ring-accent CTA block (sits on light page on close slide) ──────── */
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
.cta-ring .cta-eyebrow {
    font-family:'Inter'; font-size:28px; font-weight:600;
    text-transform:uppercase; letter-spacing:0.08em;
    color:#E8709A;
}
.cta-ring h2 {
    font-family:'Sora'; font-weight:800; font-size:55px;
    line-height:1.04; letter-spacing:-0.03em;
    color:#f9f9fc; margin-top:21px;
}
.cta-ring .pill {
    display:inline-flex; align-items:center; gap:13px;
    margin-top:34px; padding:21px 34px;
    background:#E8709A; color:#0f1012;
    border-radius:999px;
    font-family:'Inter'; font-size:26px; font-weight:700;
    letter-spacing:0.02em;
}
.cta-ring .pill .arrow { font-family:'Sora'; font-weight:700; }
.cta-ring .reassure {
    font-family:'Inter'; font-size:24px; font-weight:400;
    color:rgba(255,255,255,0.55); margin-top:21px;
}
"""

for k, v in TOK.items():
    CSS = CSS.replace(f"__{k}__", v)
for k, v in IMM.items():
    CSS = CSS.replace(f"__imm_{k}__", v)

def wrap(inner, surface="light"):
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<div class="canvas {surface}"><div class="content">{inner}</div></div>
</body></html>"""

def masthead(deck_logo=LOGO_DECK):
    """Field Note signature — logo top-left + 'FIELD NOTE · No. 01' top-right."""
    return f"""<div class="masthead">
      <img src="data:image/png;base64,{deck_logo}" class="mark" alt="smbx.ai">
      <div class="meta">Field Note &nbsp;·&nbsp; <span class="num">{NOTE_NO}</span></div>
    </div>"""

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

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SLIDE 1 — COVER (light page, full Field Note signature)
# Masthead → HookEyebrow → Sora hook → mega-compare data → byline → swipe
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
S1 = wrap(f"""
    {masthead()}

    <div class="eyebrow-hook">
      <span class="dot"></span>
      <span>HVAC &nbsp;·&nbsp; $3M&ndash;$5M EBITDA &nbsp;·&nbsp; Sell-side</span>
    </div>

    <h1 class="hook" style="font-size:89px;">
      Same metro.<br>Same revenue.<br>Same year.
    </h1>

    <div class="mega-compare">
      <div class="mega-row">
        <span class="label">Seller A &nbsp;·&nbsp; tax returns &amp; a tired handshake</span>
        <span class="val muted num">3.1&times;</span>
      </div>
      <div class="mega-row">
        <span class="label">Seller B &nbsp;·&nbsp; data room &amp; 18 months of prep</span>
        <span class="val accent num">7.2&times;</span>
      </div>
      <div class="mega-gap">
        <span class="label">Gap on $4M EBITDA</span>
        <span class="val num">$16.4M</span>
      </div>
    </div>

    <div class="cover-byline">
      <img src="data:image/jpeg;base64,{HEADSHOT}" class="portrait" alt="Paul Baker">
      <div class="who">
        <div class="name">Paul Baker</div>
        <div class="cred">Founder, smbx.ai &nbsp;·&nbsp; <span class="num">20+</span> years in M&amp;A</div>
      </div>
    </div>

    <div class="cover-swipe">
      <span class="hint">Swipe &rsaquo;</span>
    </div>
""", surface="light")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SLIDE 2 — THE 3.1× SELLER (light, dark KV card)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
S2 = wrap(f"""
    <div class="eyebrow-section">The 3.1&times; seller</div>

    <h1 class="section" style="font-size:64px;">
      He brought tax returns and a tired handshake.
    </h1>

    <div class="kv-card-dark">
      <div class="row">
        <span class="k">Concentration</span>
        <span class="v num">40% in 2 contracts</span>
      </div>
      <div class="row">
        <span class="k">Management</span>
        <span class="v">Founder runs every bid</span>
      </div>
      <div class="row">
        <span class="k">Financials</span>
        <span class="v">Tax-basis, no QofE</span>
      </div>
      <div class="row">
        <span class="k">PE interest</span>
        <span class="v num">3 firms. All passed.</span>
      </div>
      <div class="row">
        <span class="k">Outcome</span>
        <span class="v">Strategic low-ball, accepted</span>
      </div>
    </div>

    {footer()}
""", surface="light")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SLIDE 3 — THE 7.2× SELLER (light, bordered card)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
S3 = wrap(f"""
    <div class="eyebrow-section">The 7.2&times; seller</div>

    <h1 class="section" style="font-size:64px;">
      He brought a data room and 18 months of preparation.
    </h1>

    <div class="kv-card">
      <div class="row">
        <span class="k">Concentration</span>
        <span class="v num">35% &rarr; 12%</span>
      </div>
      <div class="row">
        <span class="k">Management</span>
        <span class="v">VP Ops, Sales Dir, Svc Mgr</span>
      </div>
      <div class="row">
        <span class="k">Owner role</span>
        <span class="v num">9 months out of meetings</span>
      </div>
      <div class="row">
        <span class="k">Sell-side QofE</span>
        <span class="v num">$1.2M documented add-backs</span>
      </div>
    </div>

    <div class="proof-row">
      <span class="label">Result:</span>
      <span class="badge"><span class="n num">7.2&times;</span></span>
      <span class="badge"><span class="n num">$28.8M close</span></span>
    </div>

    {footer()}
""", surface="light")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SLIDE 4 — THE GAP (cinematic anchor: light card on dark stage)
# Only dark slide in the deck — the contrast moment.
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
S4 = wrap(f"""
    <div class="eyebrow-section">Same earnings. Different outcome.</div>

    <h1 class="section" style="font-size:60px;">
      $4M EBITDA, two prices.
    </h1>

    <div class="light-card">
      <div class="anchor-eyebrow">Sale price on $4M EBITDA</div>

      <div class="row-line">
        <span class="k">Seller A &nbsp;·&nbsp; <span class="num">3.1&times;</span></span>
        <span class="v num">$12.4M</span>
      </div>
      <div class="row-line">
        <span class="k">Seller B &nbsp;·&nbsp; <span class="num">7.2&times;</span></span>
        <span class="v num">$28.8M</span>
      </div>

      <div class="gap-row">
        <span class="k">Gap</span>
        <span class="v num">$16.4M</span>
      </div>

      <div class="caption">
        Same industry. Same metro. Same year. One ran a process; one took an offer.
      </div>
    </div>

    {attr_imm()}
""", surface="imm")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SLIDE 5 — CLOSE (light page, dark ring-CTA block — site PageCTA pattern)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
S5 = wrap(f"""
    <div class="eyebrow-section">Run a Baseline</div>

    <h1 class="section" style="font-size:76px;">
      Find what a buyer would flag&thinsp;&mdash;&thinsp;before they do.
    </h1>

    <p class="sub">
      Eighteen months of prep is what separates 3&times; from 7&times;. The
      first step is knowing what&rsquo;s in your data room before the buyer
      asks for it.
    </p>

    <div class="cta-ring">
      <div class="cta-eyebrow">Free &middot; 12 minutes</div>
      <h2>Run a Baseline&trade; on your business.</h2>
      <span class="pill">
        Start at smbx.ai <span class="arrow">&rsaquo;</span>
      </span>
      <div class="reassure">
        No account required &nbsp;·&nbsp; Your data stays yours
      </div>
    </div>

    {footer()}
""", surface="light")

# ── Render ──────────────────────────────────────
slides = [S1, S2, S3, S4, S5]

print(f"Rendering {len(slides)} slides ({MODE} mode) at {W}x{H} @ {DPR}x...")

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=DPR)

    pngs = []
    for i, html in enumerate(slides):
        tmp = tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode="w")
        tmp.write(html)
        tmp.close()
        page.goto(f"file://{tmp.name}")
        page.wait_for_timeout(2000)
        png_path = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        png_path.close()
        page.screenshot(path=png_path.name)
        pngs.append(png_path.name)
        os.unlink(tmp.name)
        print(f"  Slide {i+1}/{len(slides)}")

    browser.close()

imgs = [Image.open(p).convert("RGB").resize((W, H), Image.LANCZOS) for p in pngs]
pdf_path = OUT_DIR / f"MON-1-sellers-hvac-{MODE}.pdf"
imgs[0].save(str(pdf_path), "PDF", resolution=288.0, save_all=True, append_images=imgs[1:])

for p in pngs:
    os.unlink(p)

print(f"\nDone: {pdf_path}")
