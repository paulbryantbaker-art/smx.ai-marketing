#!/usr/bin/env python3
"""
smbx.ai LinkedIn Carousel — Monday Week 1, Post 1
"CIM in 30 Minutes" — Brokers · M&A Network (283K) · Carousel (5)

Source: SMBX_90_DAY_PLAN.xlsx, Week 1 Monday, Row 1
Hook: "A CIM takes your team 40 hours. Yulia generates one in 30 minutes.
Same 30 pages. Institutional quality."
Deal size: $8M EBITDA · Pillar: P1 Yulia Does the Work · CTA: Talk to Yulia. smbx.ai

Built to the smbx.ai DESIGN_LANGUAGE.md canon (2026-04-15):
  - Field Note masthead (No. 11), two-variant eyebrows, Sora 800 + Inter
  - Light-dominant rhythm with dark cinematic anchor at S4
  - Fibonacci spacing, mobile-readable typography
  - CTA block = "Talk to Yulia" (not Baseline — this is Product-phase content)

Usage:
    python3 carousel-brokers-cim-30min.py
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
NOTE_NO   = "No. 11"
GROUP     = "M&A Network (283K)"   # appears in cover eyebrow trail and filename

TOKENS = {
    "light": {
        "bg":"#F9F9FC", "bg_alt":"#f4f4f7",
        "ink":"#0f1012", "body":"#3c3d40", "muted":"#6e6a63",
        "accent":"#D44A78", "tint":"rgba(212,74,120,0.08)",
        "border":"rgba(15,16,18,0.08)", "border_soft":"rgba(15,16,18,0.06)",
        "card_bg":"#ffffff",
        "logo_file":"G3L.png",
    },
    "dark": {
        "bg":"#1A1C1E", "bg_alt":"#151617",
        "ink":"#f9f9fc", "body":"rgba(218,218,220,0.85)", "muted":"rgba(218,218,220,0.55)",
        "accent":"#E8709A", "tint":"rgba(232,112,154,0.10)",
        "border":"rgba(255,255,255,0.08)", "border_soft":"rgba(255,255,255,0.06)",
        "card_bg":"#1a1c1e",
        "logo_file":"G3D.png",
    },
}
TOK = TOKENS[MODE]

IMM = {
    "bg":"#0f1012", "ink":"#f9f9fc",
    "muted":"rgba(255,255,255,0.55)", "body":"rgba(255,255,255,0.78)",
    "accent": TOK["accent"], "border":"rgba(255,255,255,0.10)",
}

def b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

LOGO_DARK_BG  = b64(REPO / "assets" / "logos" / "G3D.png")
LOGO_DECK     = b64(REPO / "assets" / "logos" / TOK["logo_file"])
HEADSHOT      = b64(REPO / "assets" / "portrait-square.jpeg")

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

.eyebrow-hook {
    display:flex; align-items:center; gap:13px;
    margin-top:55px;
    font-family:'Inter'; font-size:28px; font-weight:700;
    text-transform:uppercase; letter-spacing:0.2em; color:__accent__;
}
.eyebrow-hook .dot {
    width:14px; height:14px; border-radius:50%;
    background:__accent__; flex-shrink:0;
}

.eyebrow-section {
    font-family:'Inter'; font-size:28px; font-weight:600;
    text-transform:uppercase; letter-spacing:0.08em; color:__accent__;
}
.canvas.imm .eyebrow-section { color:__imm_accent__; }

h1.hook {
    font-family:'Sora'; font-weight:800; line-height:0.94; letter-spacing:-0.04em;
    color:__ink__; margin-top:21px;
}
.canvas.imm h1.hook { color:__imm_ink__; }

h1.section {
    font-family:'Sora'; font-weight:800; line-height:1.0; letter-spacing:-0.03em;
    color:__ink__; margin-top:21px;
}
.canvas.imm h1.section { color:__imm_ink__; }

p.sub {
    font-family:'Inter'; font-weight:400; font-size:34px; line-height:1.45;
    color:__body__; margin-top:34px; max-width:920px;
}
p.sub strong { color:__ink__; font-weight:600; }

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

.cover-byline {
    margin-top:55px; display:flex; align-items:center; gap:21px;
}
.cover-byline .portrait {
    width:89px; height:89px; border-radius:50%;
    object-fit:cover; object-position:center; border:2px solid __border__;
}
.cover-byline .who .name { font-family:'Sora'; font-weight:800; font-size:34px; letter-spacing:-0.02em; color:__ink__; }
.cover-byline .who .cred { font-family:'Inter'; font-size:24px; font-weight:500; color:__muted__; margin-top:8px; }

.cover-swipe {
    margin-top:auto;
    display:flex; align-items:center; justify-content:space-between;
    padding-top:21px; border-top:1px solid __border__;
}
.cover-swipe .group {
    font-family:'Inter'; font-size:22px; font-weight:500;
    color:__muted__;
}
.cover-swipe .hint {
    font-family:'Inter'; font-size:24px; font-weight:700;
    text-transform:uppercase; letter-spacing:0.2em; color:__accent__;
}

.foot {
    margin-top:auto;
    display:flex; align-items:center; justify-content:space-between;
    padding-top:21px; border-top:1px solid __border__;
    font-family:'Inter'; font-size:26px; font-weight:500; color:__muted__;
}
.foot .who { display:flex; align-items:center; gap:13px; }
.foot .portrait { width:48px; height:48px; border-radius:50%; object-fit:cover; object-position:center; border:1px solid __border__; }
.foot .name-ink { color:__ink__; font-weight:700; }

.attr-imm {
    margin-top:auto;
    display:flex; align-items:center; justify-content:space-between;
    padding-top:34px; opacity:0.55;
}
.attr-imm .mark { height:34px; object-fit:contain; }
.attr-imm .meta { font-family:'Inter'; font-size:22px; font-weight:500; color:rgba(255,255,255,0.7); }

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
.kv-card-dark .row .v { font-family:'Sora'; font-weight:800; font-size:34px; letter-spacing:-0.02em; color:#f9f9fc; }

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
.kv-card .row .v { font-family:'Sora'; font-weight:800; font-size:32px; letter-spacing:-0.02em; color:__ink__; }
.kv-card .row .v.accent { color:__accent__; }

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
.light-card .gap-row .v { font-family:'Sora'; font-weight:800; font-size:96px; letter-spacing:-0.045em; color:#D44A78; }
.light-card .caption { font-family:'Inter'; font-size:24px; font-weight:400; color:#6e6a63; margin-top:21px; line-height:1.4; }

.cta-ring {
    margin-top:55px;
    background:#0f1012;
    border:1px solid rgba(212,74,120,0.55);
    border-radius:21px;
    padding:55px 48px 48px 48px;
    box-shadow: inset 0 0 0 1px rgba(212,74,120,0.18), 0 34px 55px -34px rgba(15,16,18,0.45);
}
.cta-ring .cta-eyebrow { font-family:'Inter'; font-size:28px; font-weight:600; text-transform:uppercase; letter-spacing:0.08em; color:#E8709A; }
.cta-ring h2 { font-family:'Sora'; font-weight:800; font-size:55px; line-height:1.04; letter-spacing:-0.03em; color:#f9f9fc; margin-top:21px; }
.cta-ring .pill {
    display:inline-flex; align-items:center; gap:13px;
    margin-top:34px; padding:21px 34px;
    background:#E8709A; color:#0f1012; border-radius:999px;
    font-family:'Inter'; font-size:26px; font-weight:700; letter-spacing:0.02em;
}
.cta-ring .pill .arrow { font-family:'Sora'; font-weight:700; }
.cta-ring .reassure { font-family:'Inter'; font-size:24px; font-weight:400; color:rgba(255,255,255,0.55); margin-top:21px; }
"""

for k, v in TOK.items():
    CSS = CSS.replace(f"__{k}__", v)
for k, v in IMM.items():
    CSS = CSS.replace(f"__imm_{k}__", v)

def wrap(inner, surface="light"):
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<div class="canvas {surface}"><div class="content">{inner}</div></div>
</body></html>"""

def masthead():
    return f"""<div class="masthead">
      <img src="data:image/png;base64,{LOGO_DECK}" class="mark" alt="smbx.ai">
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
# S1 — COVER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
S1 = wrap(f"""
    {masthead()}

    <div class="eyebrow-hook">
      <span class="dot"></span>
      <span>Brokers &nbsp;·&nbsp; $8M EBITDA &nbsp;·&nbsp; CIM</span>
    </div>

    <h1 class="hook" style="font-size:104px;">
      40 hours.<br>30 minutes.<br>Same CIM.
    </h1>

    <div class="mega-compare">
      <div class="mega-row">
        <span class="label">Your analyst, tonight &amp; tomorrow</span>
        <span class="val muted num">40 hrs</span>
      </div>
      <div class="mega-row">
        <span class="label">Yulia, before your next call</span>
        <span class="val accent num">30 min</span>
      </div>
      <div class="mega-gap">
        <span class="label">Same 30 pages &nbsp;·&nbsp; institutional quality</span>
        <span class="val num">80&times;</span>
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
      <span class="group">For: {GROUP}</span>
      <span class="hint">Swipe &rsaquo;</span>
    </div>
""", surface="light")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# S2 — What goes in a CIM (dark KV card)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
S2 = wrap(f"""
    <div class="eyebrow-section">The CIM, unpacked</div>

    <h1 class="section" style="font-size:64px;">
      Every buyer expects these 6 sections.
    </h1>

    <div class="kv-card-dark">
      <div class="row">
        <span class="k">Executive summary</span>
        <span class="v num">2 pages</span>
      </div>
      <div class="row">
        <span class="k">Investment highlights</span>
        <span class="v num">3 pages</span>
      </div>
      <div class="row">
        <span class="k">Financials &amp; add-backs</span>
        <span class="v num">8 pages</span>
      </div>
      <div class="row">
        <span class="k">Market + competitive position</span>
        <span class="v num">6 pages</span>
      </div>
      <div class="row">
        <span class="k">Growth thesis</span>
        <span class="v num">6 pages</span>
      </div>
      <div class="row">
        <span class="k">Management &amp; operations</span>
        <span class="v num">5 pages</span>
      </div>
    </div>

    {footer()}
""", surface="light")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# S3 — Yulia generates each (bordered card, with timings)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
S3 = wrap(f"""
    <div class="eyebrow-section">What Yulia does</div>

    <h1 class="section" style="font-size:60px;">
      She writes each one while you&rsquo;re still brewing coffee.
    </h1>

    <div class="kv-card">
      <div class="row">
        <span class="k">Exec summary + highlights</span>
        <span class="v num">4 min</span>
      </div>
      <div class="row">
        <span class="k">Financials + normalized add-backs</span>
        <span class="v num">8 min</span>
      </div>
      <div class="row">
        <span class="k">Market + competitive</span>
        <span class="v num">6 min</span>
      </div>
      <div class="row">
        <span class="k">Growth thesis</span>
        <span class="v num">6 min</span>
      </div>
      <div class="row">
        <span class="k">Management &amp; ops</span>
        <span class="v num">6 min</span>
      </div>
      <div class="row">
        <span class="k">Total runtime</span>
        <span class="v num accent">30 min</span>
      </div>
    </div>

    {footer()}
""", surface="light")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# S4 — Cinematic anchor: the leverage moment
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
S4 = wrap(f"""
    <div class="eyebrow-section">What 39.5 hours back looks like</div>

    <h1 class="section" style="font-size:60px;">
      CIM delivered. Day unbooked.
    </h1>

    <div class="light-card">
      <div class="anchor-eyebrow">Per CIM · $8M EBITDA engagement</div>

      <div class="row-line">
        <span class="k">Analyst hours at $200/hr</span>
        <span class="v num">$8,000</span>
      </div>
      <div class="row-line">
        <span class="k">Yulia, same output</span>
        <span class="v num">included</span>
      </div>

      <div class="gap-row">
        <span class="k">Time leverage</span>
        <span class="v num">80&times;</span>
      </div>

      <div class="caption">
        Draft in 30 minutes. Broker review in 2. Same-day turnaround on new engagements.
      </div>
    </div>

    {attr_imm()}
""", surface="imm")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# S5 — Close · Talk to Yulia CTA
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
S5 = wrap(f"""
    <div class="eyebrow-section">See it live</div>

    <h1 class="section" style="font-size:72px;">
      Bring a real engagement. Watch Yulia write it.
    </h1>

    <p class="sub">
      Paste your financials. Yulia drafts the CIM in <strong>30 minutes</strong>.
      You review, edit, send. Same day.
    </p>

    <div class="cta-ring">
      <div class="cta-eyebrow">Free &middot; No account required</div>
      <h2>Talk to Yulia.</h2>
      <span class="pill">
        smbx.ai <span class="arrow">&rsaquo;</span>
      </span>
      <div class="reassure">
        30-page PDF in your inbox &nbsp;·&nbsp; Your data stays yours
      </div>
    </div>

    {footer()}
""", surface="light")

slides = [S1, S2, S3, S4, S5]

print(f"Rendering {len(slides)} slides ({MODE}) at {W}x{H} @ {DPR}x...")

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
        print(f"  Slide {i+1}/{len(slides)}")

    browser.close()

imgs = [Image.open(p).convert("RGB").resize((W, H), Image.LANCZOS) for p in pngs]
pdf_path = OUT_DIR / f"MON-1-brokers-cim-MANetwork-{MODE}.pdf"
imgs[0].save(str(pdf_path), "PDF", resolution=288.0, save_all=True, append_images=imgs[1:])

for p in pngs:
    os.unlink(p)

print(f"\nDone: {pdf_path}")
