#!/usr/bin/env python3
"""
smbx.ai LinkedIn Carousel — Monday Week 1, Post 2
"3 Valuations Before Lunch" — Brokers · Dealflow Network (152K)

Source: SMBX_90_DAY_PLAN.xlsx (per-slide content from xlsx columns).
Field Note No. 18. Canon per DESIGN_LANGUAGE.md.
"""

import os, sys, base64, tempfile
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image

W, H = 1080, 1350; DPR = 2
REPO = Path(__file__).resolve().parent.parent.parent
OUT_DIR = REPO / "content" / "week-01"
MODE = sys.argv[1].lower() if len(sys.argv) > 1 else "light"; assert MODE in ("light", "dark")

YEAR_WEEK = "2026 · Week 01"
NOTE_NO   = "No. 18"

TOKENS = {
    "light": {"bg":"#F9F9FC","ink":"#0f1012","body":"#3c3d40","muted":"#6e6a63","accent":"#D44A78","tint":"rgba(212,74,120,0.08)","border":"rgba(15,16,18,0.08)","border_soft":"rgba(15,16,18,0.06)","card_bg":"#ffffff","logo_file":"G3L.png"},
    "dark":  {"bg":"#1A1C1E","ink":"#f9f9fc","body":"rgba(218,218,220,0.85)","muted":"rgba(218,218,220,0.55)","accent":"#E8709A","tint":"rgba(232,112,154,0.10)","border":"rgba(255,255,255,0.08)","border_soft":"rgba(255,255,255,0.06)","card_bg":"#1a1c1e","logo_file":"G3D.png"},
}
TOK = TOKENS[MODE]
IMM = {"bg":"#0f1012","ink":"#f9f9fc","muted":"rgba(255,255,255,0.55)","body":"rgba(255,255,255,0.78)","accent":TOK["accent"],"border":"rgba(255,255,255,0.10)"}

def b64(p):
    with open(p, "rb") as f: return base64.b64encode(f.read()).decode()

LOGO_DARK_BG = b64(REPO / "assets" / "logos" / "G3D.png")
LOGO_DECK    = b64(REPO / "assets" / "logos" / TOK["logo_file"])
HEADSHOT     = b64(REPO / "assets" / "portrait-square.jpeg")

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&family=Inter:wght@400;500;600;700&display=swap');
* { margin:0; padding:0; box-sizing:border-box; }
body { width:1080px; height:1350px; overflow:hidden; font-family:'Inter', system-ui, sans-serif; -webkit-font-smoothing:antialiased; }
.num { font-variant-numeric:tabular-nums; font-feature-settings:'tnum' 1; }
.canvas { width:1080px; height:1350px; position:relative; overflow:hidden; }
.canvas.light { background:__bg__; color:__ink__; }
.canvas.imm   { background:__imm_bg__; color:__imm_ink__; }
.content { position:relative; z-index:2; height:100%; display:flex; flex-direction:column; padding:89px 76px 55px 76px; }

.masthead { display:flex; align-items:center; justify-content:space-between; padding-bottom:21px; border-bottom:1px solid __border__; }
.masthead .mark { height:55px; object-fit:contain; }
.masthead .meta { font-family:'Inter'; font-size:24px; font-weight:700; text-transform:uppercase; letter-spacing:0.2em; color:__muted__; }
.masthead .meta .num { color:__ink__; }

/* Eyebrow demoted to muted gray — accent reserved for one moment per slide */
.eyebrow-hook { display:flex; align-items:center; gap:13px; margin-top:55px; font-family:'Inter'; font-size:24px; font-weight:700; text-transform:uppercase; letter-spacing:0.2em; color:__muted__; }
.eyebrow-hook .dot { width:13px; height:13px; border-radius:50%; background:__accent__; flex-shrink:0; }
.eyebrow-section { font-family:'Inter'; font-size:24px; font-weight:700; text-transform:uppercase; letter-spacing:0.18em; color:__muted__; }
.canvas.imm .eyebrow-section { color:rgba(255,255,255,0.55); }

h1.hook { font-family:'Sora'; font-weight:800; line-height:0.98; letter-spacing:-0.04em; color:__ink__; margin-top:21px; }
h1.section { font-family:'Sora'; font-weight:800; line-height:1.0; letter-spacing:-0.03em; color:__ink__; margin-top:21px; }
.canvas.imm h1.section { color:__imm_ink__; }
p.sub { font-family:'Inter'; font-weight:400; font-size:30px; line-height:1.4; color:__body__; margin-top:34px; max-width:920px; }
p.sub strong { color:__ink__; font-weight:600; }

/* Cover compare-cols — side-by-side time block (different from MON-1's stat strip) */
.cover-compare { margin-top:34px; padding:21px 0; border-top:1px solid __border__; border-bottom:1px solid __border__; display:grid; grid-template-columns:1fr 1fr; gap:34px; }
.cover-compare .col { }
.cover-compare .col-label { font-family:'Inter'; font-size:18px; font-weight:700; text-transform:uppercase; letter-spacing:0.18em; color:__muted__; padding-bottom:13px; border-bottom:1px solid __border__; }
.cover-compare .col.accent .col-label { color:__accent__; }
.cover-compare .big { font-family:'Sora'; font-weight:800; font-size:72px; letter-spacing:-0.045em; color:__muted__; line-height:1.0; margin-top:13px; }
.cover-compare .col.accent .big { color:__accent__; }
.cover-compare .meta { font-family:'Inter'; font-size:18px; font-weight:500; color:__muted__; margin-top:8px; }

/* Signature close (S5) — magazine end-page, whisper-weight type */
.signature-page { display:flex; flex-direction:column; height:100%; padding:0; }
.sig-top { padding-bottom:21px; border-bottom:1px solid __border__; display:flex; justify-content:space-between; align-items:center; }
.sig-top .mark { height:42px; }
.sig-top .meta { font-family:'Inter'; font-size:21px; font-weight:600; color:__muted__; text-transform:uppercase; letter-spacing:0.18em; }
.sig-top .meta .end { color:__accent__; }
.sig-mid { flex:1; display:flex; flex-direction:column; justify-content:center; align-items:flex-start; }
.sig-quiet { font-family:'Sora'; font-weight:400; font-size:96px; color:__ink__; letter-spacing:-0.045em; line-height:1.0; }
.sig-link { margin-top:34px; font-family:'Inter'; font-size:34px; font-weight:600; color:__accent__; letter-spacing:0.04em; }
.sig-link .arrow { font-family:'Sora'; font-weight:600; }
.sig-aside { margin-top:21px; font-family:'Inter'; font-size:21px; font-weight:400; color:__muted__; }

.cover-byline { margin-top:34px; display:flex; align-items:center; gap:21px; }
.cover-byline .portrait { width:89px; height:89px; border-radius:50%; object-fit:cover; object-position:center; border:2px solid __border__; }
.cover-byline .who .name { font-family:'Sora'; font-weight:800; font-size:34px; letter-spacing:-0.02em; color:__ink__; }
.cover-byline .who .cred { font-family:'Inter'; font-size:24px; font-weight:500; color:__muted__; margin-top:8px; }

.cover-swipe { margin-top:auto; display:flex; align-items:center; justify-content:flex-end; padding-top:21px; border-top:1px solid __border__; }
.cover-swipe .hint { font-family:'Inter'; font-size:24px; font-weight:700; text-transform:uppercase; letter-spacing:0.2em; color:__accent__; }

.foot { margin-top:auto; display:flex; align-items:center; justify-content:space-between; padding-top:21px; border-top:1px solid __border__; font-family:'Inter'; font-size:26px; font-weight:500; color:__muted__; }
.foot .who { display:flex; align-items:center; gap:13px; }
.foot .portrait { width:48px; height:48px; border-radius:50%; object-fit:cover; object-position:center; border:1px solid __border__; }
.foot .name-ink { color:__ink__; font-weight:700; }

.attr-imm { margin-top:auto; display:flex; align-items:center; justify-content:space-between; padding-top:34px; opacity:0.55; }
.attr-imm .mark { height:34px; object-fit:contain; }
.attr-imm .meta { font-family:'Inter'; font-size:22px; font-weight:500; color:rgba(255,255,255,0.7); }

.list-card-dark { background:#0f1012; border-radius:14px; padding:13px 34px 8px 34px; margin-top:34px; box-shadow: 0 21px 55px -34px rgba(15,16,18,0.45); }
.list-card-dark .row { padding:21px 0; border-bottom:1px solid rgba(255,255,255,0.08); font-family:'Inter'; font-size:28px; font-weight:600; color:#f9f9fc; }
.list-card-dark .row:last-child { border-bottom:none; }

.role-card { background:__card_bg__; border:1px solid __border__; border-radius:14px; padding:21px 34px 13px 34px; margin-top:34px; }
.role-card .row { display:flex; align-items:baseline; gap:21px; padding:18px 0; border-bottom:1px solid __border_soft__; }
.role-card .row:last-child { border-bottom:none; }
.role-card .row .verb { font-family:'Sora'; font-weight:800; font-size:32px; color:__accent__; min-width:200px; text-transform:uppercase; letter-spacing:0.04em; }
.role-card .row .body { font-family:'Inter'; font-size:26px; font-weight:500; color:__ink__; line-height:1.35; }

.caption-quote { margin-top:34px; padding-left:21px; border-left:3px solid __accent__; font-family:'Inter'; font-size:24px; font-weight:500; line-height:1.45; color:__body__; font-style:italic; }
.caption-line { margin-top:21px; font-family:'Inter'; font-size:24px; font-weight:500; color:__muted__; line-height:1.4; }

/* Before / After cinematic comparison */
.ba-card { margin-top:34px; background:#ffffff; border:1px solid rgba(15,16,18,0.08); border-radius:21px; padding:42px 42px 34px 42px; box-shadow: 0 34px 89px -34px rgba(0,0,0,0.55); color:#0f1012; }
.ba-card .anchor-eyebrow { font-family:'Inter'; font-size:24px; font-weight:600; text-transform:uppercase; letter-spacing:0.08em; color:#D44A78; }
.ba-grid { display:grid; grid-template-columns:1fr 1fr; gap:34px; margin-top:21px; }
.ba-col { }
.ba-col-label { font-family:'Inter'; font-size:18px; font-weight:700; text-transform:uppercase; letter-spacing:0.18em; color:#6e6a63; padding-bottom:13px; border-bottom:1px solid rgba(15,16,18,0.08); }
.ba-col.accent .ba-col-label { color:#D44A78; }
.ba-step { display:flex; justify-content:space-between; align-items:baseline; padding:13px 0; }
.ba-step .step { font-family:'Inter'; font-size:20px; font-weight:500; color:#6e6a63; }
.ba-step .time { font-family:'Sora'; font-weight:800; font-size:22px; color:#3c3d40; letter-spacing:-0.02em; }
.ba-col.accent .ba-step .time { color:#D44A78; }
.ba-total { display:flex; justify-content:space-between; align-items:baseline; padding-top:13px; margin-top:8px; border-top:2px solid rgba(15,16,18,0.15); }
.ba-total .label { font-family:'Inter'; font-size:14px; font-weight:700; text-transform:uppercase; letter-spacing:0.18em; color:#6e6a63; }
.ba-total .total-val { font-family:'Sora'; font-weight:800; font-size:34px; color:#3c3d40; letter-spacing:-0.025em; }
.ba-col.accent .ba-total { border-top-color:#D44A78; }
.ba-col.accent .ba-total .total-val { color:#D44A78; }
.ba-card .punchline { margin-top:21px; padding-top:21px; border-top:1px solid rgba(15,16,18,0.08); font-family:'Sora'; font-weight:800; font-size:30px; color:#0f1012; letter-spacing:-0.02em; }
.ba-card .punchline em { color:#D44A78; font-style:normal; }

.anchor-caption { margin-top:21px; font-family:'Inter'; font-size:24px; font-weight:500; color:rgba(255,255,255,0.7); line-height:1.4; padding-left:21px; border-left:2px solid __imm_accent__; }

.cta-ring { margin-top:34px; background:#0f1012; border:1px solid rgba(212,74,120,0.55); border-radius:21px; padding:48px 48px 42px 48px; box-shadow: inset 0 0 0 1px rgba(212,74,120,0.18), 0 34px 55px -34px rgba(15,16,18,0.45); }
.cta-ring .cta-eyebrow { font-family:'Inter'; font-size:24px; font-weight:600; text-transform:uppercase; letter-spacing:0.08em; color:#E8709A; }
.cta-ring h2 { font-family:'Sora'; font-weight:800; font-size:44px; line-height:1.04; letter-spacing:-0.03em; color:#f9f9fc; margin-top:13px; }
.cta-ring .pill { display:inline-flex; align-items:center; gap:13px; margin-top:34px; padding:18px 34px; background:#E8709A; color:#0f1012; border-radius:999px; font-family:'Inter'; font-size:26px; font-weight:700; letter-spacing:0.02em; }
.cta-ring .pill .arrow { font-family:'Sora'; font-weight:700; }
.cta-ring .reassure { font-family:'Inter'; font-size:22px; font-weight:400; color:rgba(255,255,255,0.55); margin-top:21px; }
"""

for k, v in TOK.items(): CSS = CSS.replace(f"__{k}__", v)
for k, v in IMM.items(): CSS = CSS.replace(f"__imm_{k}__", v)

def wrap(inner, surface="light"):
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="canvas {surface}"><div class="content">{inner}</div></div></body></html>"""

def masthead():
    return f"""<div class="masthead"><img src="data:image/png;base64,{LOGO_DECK}" class="mark"><div class="meta">Field Note &nbsp;·&nbsp; <span class="num">{NOTE_NO}</span></div></div>"""

def footer():
    return f"""<div class="foot"><div class="who"><img src="data:image/jpeg;base64,{HEADSHOT}" class="portrait"><span><span class="name-ink">Paul Baker</span> &nbsp;·&nbsp; smbx.ai</span></div><div class="num">{YEAR_WEEK}</div></div>"""

def attr_imm():
    return f"""<div class="attr-imm"><img src="data:image/png;base64,{LOGO_DARK_BG}" class="mark"><div class="meta">Paul Baker &nbsp;·&nbsp; <span class="num">{YEAR_WEEK}</span></div></div>"""

# S1 — Cover
S1 = wrap(f"""
    {masthead()}

    <div class="eyebrow-hook">
      <span class="dot"></span>
      <span>Brokers &nbsp;·&nbsp; $5M&ndash;$15M EBITDA &nbsp;·&nbsp; Valuations</span>
    </div>

    <h1 class="hook" style="font-size:72px;">
      3 valuations. Before lunch.
    </h1>

    <p class="sub">
      <strong>Multi-methodology.</strong> Documented add-backs.
      Defensible math.
    </p>

    <div class="cover-compare">
      <div class="col">
        <div class="col-label">Traditional</div>
        <div class="big num">11 days</div>
        <div class="meta">per valuation</div>
      </div>
      <div class="col accent">
        <div class="col-label">With Yulia</div>
        <div class="big num">1 hour</div>
        <div class="meta">per valuation</div>
      </div>
    </div>

    <div class="cover-byline">
      <img src="data:image/jpeg;base64,{HEADSHOT}" class="portrait">
      <div class="who">
        <div class="name">Paul Baker</div>
        <div class="cred">Founder, smbx.ai &nbsp;·&nbsp; <span class="num">20+</span> years in M&amp;A</div>
      </div>
    </div>

    <div class="cover-swipe">
      <span class="hint">Swipe &rsaquo;</span>
    </div>
""", surface="light")

# S2 — What each valuation includes (light, list card)
S2 = wrap(f"""
    <div class="eyebrow-section">What each valuation includes</div>

    <h1 class="section" style="font-size:56px;">
      Seven things in every report.
    </h1>

    <div class="list-card-dark">
      <div class="row">SDE multiples, industry-matched comps</div>
      <div class="row">Comparable transactions, closed deals</div>
      <div class="row">Asset-based floor</div>
      <div class="row">Add-back schedule, line by line</div>
      <div class="row">Seven-factor quality score</div>
      <div class="row">SBA financing feasibility</div>
      <div class="row">Sensitivity analysis</div>
    </div>

    <div class="caption-quote">
      &ldquo;Not a calculator. A full valuation report.&rdquo;
    </div>

    {footer()}
""", surface="light")

# S3 — 22 deterministic formulas
S3 = wrap(f"""
    <div class="eyebrow-section"><span class="num">22</span> deterministic formulas</div>

    <h1 class="section" style="font-size:60px;">
      Not AI estimates. Not rules of thumb.
    </h1>

    <div class="role-card">
      <div class="row">
        <span class="verb">Auditable</span>
        <span class="body">every line traceable to source.</span>
      </div>
      <div class="row">
        <span class="verb">Reproducible</span>
        <span class="body">same inputs, same outputs, every time.</span>
      </div>
      <div class="row">
        <span class="verb">Defensible</span>
        <span class="body">survives a buyer&rsquo;s diligence team.</span>
      </div>
    </div>

    <div class="caption-quote">
      &ldquo;Your client&rsquo;s attorney can challenge any line. It holds up.&rdquo;
    </div>

    {footer()}
""", surface="light")

# S4 — Before vs After cinematic anchor
S4 = wrap(f"""
    <div class="eyebrow-section">Before vs after</div>

    <h1 class="section" style="font-size:60px;">
      <span class="num">11</span> days. <span class="num">1</span> hour.
    </h1>

    <div class="ba-card">
      <div class="anchor-eyebrow">Per valuation, traditional vs Yulia</div>

      <div class="ba-grid">
        <div class="ba-col">
          <div class="ba-col-label">Before</div>
          <div class="ba-step"><span class="step">Research</span><span class="time num">3 days</span></div>
          <div class="ba-step"><span class="step">Normalize</span><span class="time num">2 days</span></div>
          <div class="ba-step"><span class="step">Model</span><span class="time num">3 days</span></div>
          <div class="ba-step"><span class="step">Write</span><span class="time num">2 days</span></div>
          <div class="ba-step"><span class="step">Format</span><span class="time num">1 day</span></div>
          <div class="ba-total">
            <span class="label">Total</span>
            <span class="total-val num">11 days</span>
          </div>
        </div>

        <div class="ba-col accent">
          <div class="ba-col-label">After</div>
          <div class="ba-step"><span class="step">Intake</span><span class="time num">15 min</span></div>
          <div class="ba-step"><span class="step">Review</span><span class="time num">30 min</span></div>
          <div class="ba-step"><span class="step">Send</span><span class="time num">15 min</span></div>
          <div class="ba-total">
            <span class="label">Total</span>
            <span class="total-val num">1 hour</span>
          </div>
        </div>
      </div>

      <div class="punchline">
        Same quality. <em>99% less time.</em>
      </div>
    </div>

    {attr_imm()}
""", surface="imm")

# S5 — Minimal signature close (magazine end-page)
S5 = wrap(f"""
    <div class="signature-page">
      <div class="sig-top">
        <img src="data:image/png;base64,{LOGO_DECK}" class="mark" alt="smbx.ai">
        <div class="meta">Field Note &nbsp;·&nbsp; <span class="num">{NOTE_NO}</span> &nbsp;·&nbsp; <span class="end">End</span></div>
      </div>

      <div class="sig-mid">
        <div class="sig-quiet">Talk to Yulia.</div>
        <div class="sig-link">smbx.ai &nbsp;<span class="arrow">&rsaquo;</span></div>
        <div class="sig-aside">$149/month &middot; Unlimited valuations.</div>
      </div>

      {footer()}
    </div>
""", surface="light")

slides = [S1, S2, S3, S4, S5]
print(f"Rendering {len(slides)} slides ({MODE}) at {W}x{H} @ {DPR}x...")

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=DPR)
    pngs = []
    for i, html in enumerate(slides):
        tmp = tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode="w"); tmp.write(html); tmp.close()
        page.goto(f"file://{tmp.name}"); page.wait_for_timeout(2000)
        png_path = tempfile.NamedTemporaryFile(suffix=".png", delete=False); png_path.close()
        page.screenshot(path=png_path.name); pngs.append(png_path.name)
        os.unlink(tmp.name); print(f"  Slide {i+1}/{len(slides)}")
    browser.close()

imgs = [Image.open(p).convert("RGB").resize((W, H), Image.LANCZOS) for p in pngs]
pdf_path = OUT_DIR / f"MON-2-brokers-valuations-Dealflow-{MODE}.pdf"
imgs[0].save(str(pdf_path), "PDF", resolution=288.0, save_all=True, append_images=imgs[1:])
for p in pngs: os.unlink(p)
print(f"\nDone: {pdf_path}")
