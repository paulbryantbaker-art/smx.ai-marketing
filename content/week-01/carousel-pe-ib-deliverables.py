#!/usr/bin/env python3
"""
smbx.ai LinkedIn Carousel — Monday Week 1, Post 3
"IB Deliverable List" — PE / Funds · SuperCFO Group (262K)

Source: SMBX_90_DAY_PLAN.xlsx (per-slide content from xlsx columns).
Field Note No. 24. Canon per DESIGN_LANGUAGE.md.
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
NOTE_NO   = "No. 24"

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

/* Cover hero stat — single massive number (different from MON-1 strip / MON-2 compare-cols) */
.hero-stat { margin-top:34px; padding:34px 0 21px 0; border-top:1px solid __border__; border-bottom:1px solid __border__; }
.hero-stat .label { font-family:'Inter'; font-size:18px; font-weight:700; color:__muted__; text-transform:uppercase; letter-spacing:0.18em; }
.hero-stat .number { font-family:'Sora'; font-weight:800; font-size:200px; letter-spacing:-0.06em; color:__accent__; line-height:1.0; margin-top:13px; }
.hero-stat .caption { font-family:'Inter'; font-size:24px; font-weight:500; color:__ink__; margin-top:13px; line-height:1.35; }
.hero-stat .caption strong { font-weight:700; }

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

/* Deliverable list (dark KV with role tag on right) */
.kv-card-dark { background:#0f1012; border-radius:14px; padding:18px 34px 8px 34px; margin-top:34px; box-shadow: 0 21px 55px -34px rgba(15,16,18,0.45); }
.kv-card-dark .row { display:flex; justify-content:space-between; align-items:baseline; padding:13px 0; border-bottom:1px solid rgba(255,255,255,0.08); }
.kv-card-dark .row:last-child { border-bottom:none; }
.kv-card-dark .row.divider { border-top:1.5px solid rgba(232,112,154,0.5); margin-top:8px; padding-top:18px; }
.kv-card-dark .row .k { font-family:'Inter'; font-size:24px; font-weight:600; color:#f9f9fc; }
.kv-card-dark .row .v { font-family:'Inter'; font-size:18px; font-weight:700; letter-spacing:0.18em; text-transform:uppercase; }
.kv-card-dark .row .v.yulia { color:__accent__; }
.kv-card-dark .row .v.you { color:#f9f9fc; }

/* Production / Judgment role card (S3) */
.role-card-2 { background:__card_bg__; border:1px solid __border__; border-radius:14px; padding:34px 38px 28px 38px; margin-top:34px; }
.role-card-2 .roles { display:grid; grid-template-columns:1fr 1fr; gap:34px; }
.role-card-2 .role-block { }
.role-card-2 .role-label { font-family:'Inter'; font-size:18px; font-weight:700; text-transform:uppercase; letter-spacing:0.18em; color:__muted__; padding-bottom:13px; border-bottom:1px solid __border__; }
.role-card-2 .role-block.you .role-label { color:__accent__; }
.role-card-2 .role-who { font-family:'Sora'; font-weight:800; font-size:28px; color:__ink__; margin-top:21px; line-height:1.2; letter-spacing:-0.02em; }
.role-card-2 .role-eq { font-family:'Inter'; font-size:22px; font-weight:500; color:__muted__; margin-top:8px; line-height:1.35; }
.role-card-2 .role-eq strong { color:__ink__; font-weight:600; }
.role-card-2 .role-block.you .role-eq strong { color:__accent__; }

.caption-quote { margin-top:34px; padding-left:21px; border-left:3px solid __accent__; font-family:'Inter'; font-size:24px; font-weight:500; line-height:1.4; color:__body__; font-style:italic; }

/* Cost comparison cinematic anchor */
.cost-card { margin-top:34px; background:#ffffff; border:1px solid rgba(15,16,18,0.08); border-radius:21px; padding:48px 48px 42px 48px; box-shadow: 0 34px 89px -34px rgba(0,0,0,0.55); color:#0f1012; }
.cost-card .anchor-eyebrow { font-family:'Inter'; font-size:24px; font-weight:600; text-transform:uppercase; letter-spacing:0.08em; color:#D44A78; }
.cost-card .cost-row { display:flex; justify-content:space-between; align-items:baseline; padding:21px 0; border-bottom:1px solid rgba(15,16,18,0.06); }
.cost-card .cost-row:first-of-type { margin-top:21px; }
.cost-card .cost-row.last { border-bottom:none; padding-bottom:0; }
.cost-card .cost-row .label { }
.cost-card .cost-row .label .name { font-family:'Sora'; font-weight:800; font-size:24px; color:#0f1012; letter-spacing:-0.02em; }
.cost-card .cost-row .label .calc { font-family:'Inter'; font-size:18px; font-weight:500; color:#6e6a63; margin-top:8px; }
.cost-card .cost-row .price { font-family:'Sora'; font-weight:800; font-size:48px; letter-spacing:-0.03em; color:#3c3d40; }
.cost-card .cost-row.accent .price { color:#D44A78; font-size:64px; }
.cost-card .punchline { margin-top:21px; padding-top:21px; border-top:3px solid #D44A78; font-family:'Sora'; font-weight:800; font-size:32px; line-height:1.18; letter-spacing:-0.02em; color:#0f1012; }
.cost-card .punchline em { color:#D44A78; font-style:normal; }

.anchor-caption { margin-top:21px; font-family:'Inter'; font-size:22px; font-weight:500; color:rgba(255,255,255,0.7); line-height:1.4; padding-left:21px; border-left:2px solid __imm_accent__; font-style:italic; }

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
      <span>PE / Funds &nbsp;·&nbsp; $30M sell-side &nbsp;·&nbsp; IB stack</span>
    </div>

    <h1 class="hook" style="font-size:68px;">
      Yulia produces all of it.
    </h1>

    <p class="sub">
      Every deliverable a boutique IB ships on a $30M sell-side.
      <strong>The 10% she doesn&rsquo;t?</strong> You pick up the phone.
    </p>

    <div class="hero-stat">
      <div class="label">Cost comparison &middot; per $30M engagement</div>
      <div class="number num">756&times;</div>
      <div class="caption">Cheaper than a boutique IB. <strong>Same deliverables.</strong></div>
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

# S2 — The deliverable list (dark KV card with role tag)
S2 = wrap(f"""
    <div class="eyebrow-section">The deliverable list</div>

    <h1 class="section" style="font-size:48px;">
      Eleven by Yulia. Three by you.
    </h1>

    <div class="kv-card-dark">
      <div class="row"><span class="k">Valuation report</span><span class="v yulia">Yulia</span></div>
      <div class="row"><span class="k">CIM, 25&ndash;40 pages</span><span class="v yulia">Yulia</span></div>
      <div class="row"><span class="k">Financial model + sensitivity</span><span class="v yulia">Yulia</span></div>
      <div class="row"><span class="k">Blind teaser</span><span class="v yulia">Yulia</span></div>
      <div class="row"><span class="k">Buyer universe + outreach</span><span class="v yulia">Yulia</span></div>
      <div class="row"><span class="k">NDA + IOI/LOI management</span><span class="v yulia">Yulia</span></div>
      <div class="row"><span class="k">DD checklist + working capital</span><span class="v yulia">Yulia</span></div>
      <div class="row"><span class="k">Closing checklist</span><span class="v yulia">Yulia</span></div>
      <div class="row divider"><span class="k">Negotiate</span><span class="v you">You</span></div>
      <div class="row"><span class="k">Relationships</span><span class="v you">You</span></div>
      <div class="row"><span class="k">Judgment</span><span class="v you">You</span></div>
    </div>

    {footer()}
""", surface="light")

# S3 — IB = production + judgment
S3 = wrap(f"""
    <div class="eyebrow-section">An IB is production + judgment</div>

    <h1 class="section" style="font-size:56px;">
      Yulia replaces the production team.
    </h1>

    <div class="role-card-2">
      <div class="roles">
        <div class="role-block">
          <div class="role-label">Production</div>
          <div class="role-who">Analysts, Associates, VPs</div>
          <div class="role-eq">Yulia <strong>replaces</strong> this.</div>
        </div>
        <div class="role-block you">
          <div class="role-label">Judgment</div>
          <div class="role-who">Managing Director</div>
          <div class="role-eq">Your judgment is <strong>irreplaceable</strong>.</div>
        </div>
      </div>
    </div>

    <div class="caption-quote">
      &ldquo;Your analyst&rsquo;s hours are not. Your judgment is.&rdquo;
    </div>

    {footer()}
""", surface="light")

# S4 — Cost comparison cinematic anchor
S4 = wrap(f"""
    <div class="eyebrow-section">Cost comparison &middot; $30M deal</div>

    <h1 class="section" style="font-size:60px;">
      Same deliverables. <span class="num">756&times;</span> the price.
    </h1>

    <div class="cost-card">
      <div class="anchor-eyebrow">All-in fees per engagement</div>

      <div class="cost-row">
        <div class="label">
          <div class="name">Boutique IB</div>
          <div class="calc">$150K retainer + 4% success fee on $30M</div>
        </div>
        <div class="price num">$1.35M</div>
      </div>

      <div class="cost-row accent last">
        <div class="label">
          <div class="name">Yulia</div>
          <div class="calc">$149/mo &times; 12 months</div>
        </div>
        <div class="price num">$1,788</div>
      </div>

      <div class="punchline">
        Same quality. <em>Subscription pricing.</em>
      </div>
    </div>

    <div class="anchor-caption">
      &ldquo;Not a toy. Institutional quality at subscription pricing.&rdquo;
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
        <div class="sig-aside">$149/month &middot; For the production. Your expertise for the judgment.</div>
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
pdf_path = OUT_DIR / f"MON-3-pe-ib-deliverables-SuperCFO-{MODE}.pdf"
imgs[0].save(str(pdf_path), "PDF", resolution=288.0, save_all=True, append_images=imgs[1:])
for p in pngs: os.unlink(p)
print(f"\nDone: {pdf_path}")
