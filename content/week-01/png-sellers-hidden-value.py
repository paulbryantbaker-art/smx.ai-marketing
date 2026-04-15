#!/usr/bin/env python3
"""
smbx.ai LinkedIn Single Image — Monday Week 1, Post 4
"$2.6M Hidden Value" — Sellers · Business Owners & Investors Network (1.8M)

Source: SMBX_90_DAY_PLAN.xlsx, Week 1 Monday, Row 4
Hook: "Your broker hasn't found value you don't know about since the day
you hired them. Yulia finds it in the first conversation. $2.6M in
adjustments on a $7M EBITDA company — hiding in plain sight."
Deal size: $7M EBITDA · Pillar: P2 Real Math · CTA: Talk to Yulia. smbx.ai

Field Note No. 33. Canon per DESIGN_LANGUAGE.md.
"""

import os, sys, base64, tempfile
from pathlib import Path
from playwright.sync_api import sync_playwright

W, H = 1080, 1350; DPR = 2
REPO = Path(__file__).resolve().parent.parent.parent
OUT_DIR = REPO / "content" / "week-01"
MODE = sys.argv[1].lower() if len(sys.argv) > 1 else "light"; assert MODE in ("light", "dark")

NOTE_NO   = "No. 33"
YEAR_WEEK = "2026 · Week 01"
GROUP     = "Business Owners & Investors Network (1.8M)"

TOKENS = {
    "light": {"bg":"#F9F9FC","ink":"#0f1012","body":"#3c3d40","muted":"#6e6a63","accent":"#D44A78","border":"rgba(15,16,18,0.08)","border_soft":"rgba(15,16,18,0.06)","logo_file":"G3L.png"},
    "dark":  {"bg":"#1A1C1E","ink":"#f9f9fc","body":"rgba(218,218,220,0.85)","muted":"rgba(218,218,220,0.55)","accent":"#E8709A","border":"rgba(255,255,255,0.10)","border_soft":"rgba(255,255,255,0.06)","logo_file":"G3D.png"},
}
TOK = TOKENS[MODE]

def b64(p):
    with open(p, "rb") as f: return base64.b64encode(f.read()).decode()

LOGO     = b64(REPO / "assets" / "logos" / TOK["logo_file"])
HEADSHOT = b64(REPO / "assets" / "portrait-square.jpeg")

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap');
* { margin:0; padding:0; box-sizing:border-box; }
body { width:1080px; height:1350px; overflow:hidden; font-family:'Inter', system-ui, sans-serif; background:__bg__; color:__ink__; -webkit-font-smoothing:antialiased; }
.num { font-variant-numeric:tabular-nums; font-feature-settings:'tnum' 1; }
.canvas { width:1080px; height:1350px; position:relative; overflow:hidden; background:__bg__; }
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
.eyebrow-hook .dot { width:14px; height:14px; border-radius:50%; background:__accent__; flex-shrink:0; }

h1.hook {
    font-family:'Sora'; font-weight:800; font-size:84px;
    line-height:0.96; letter-spacing:-0.04em;
    color:__ink__; margin-top:21px;
}

/* Two-column $ compare */
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
    font-family:'Sora'; font-weight:800; font-size:88px;
    letter-spacing:-0.045em; color:__muted__; margin-top:13px; line-height:1.0;
}
.compare-side .big.accent { color:__accent__; }
.compare-side .note {
    font-family:'Inter'; font-size:22px; font-weight:500;
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

.punchline {
    margin-top:55px; padding-left:34px;
    border-left:8px solid __accent__;
    font-family:'Sora'; font-weight:800; font-size:38px;
    line-height:1.18; letter-spacing:-0.025em; color:__ink__;
}
.punchline .accent { color:__accent__; }

.byline {
    margin-top:auto;
    display:flex; align-items:center; justify-content:space-between;
    padding-top:21px; border-top:1px solid __border__;
}
.byline .who { display:flex; align-items:center; gap:21px; }
.byline .portrait {
    width:76px; height:76px; border-radius:50%;
    object-fit:cover; object-position:center; border:2px solid __border__;
}
.byline .who-text .name { font-family:'Sora'; font-weight:800; font-size:30px; letter-spacing:-0.02em; color:__ink__; }
.byline .who-text .cred { font-family:'Inter'; font-size:22px; font-weight:500; color:__muted__; margin-top:5px; }
.byline .right {
    text-align:right;
}
.byline .right .cta {
    font-family:'Inter'; font-size:24px; font-weight:700; color:__accent__;
    text-transform:uppercase; letter-spacing:0.15em;
}
.byline .right .meta {
    font-family:'Inter'; font-size:20px; font-weight:500; color:__muted__;
    margin-top:4px;
}
"""

for k, v in TOK.items(): CSS = CSS.replace(f"__{k}__", v)

HTML = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<div class="canvas"><div class="content">

  <div class="masthead">
    <img src="data:image/png;base64,{LOGO}" class="mark" alt="smbx.ai">
    <div class="meta">Field Note &nbsp;·&nbsp; <span class="num">{NOTE_NO}</span></div>
  </div>

  <div class="eyebrow-hook">
    <span class="dot"></span>
    <span>Sellers &nbsp;·&nbsp; $7M EBITDA &nbsp;·&nbsp; Hidden value</span>
  </div>

  <h1 class="hook">
    Hidden in<br>plain sight.
  </h1>

  <div class="compare-cols">
    <div class="compare-side">
      <div class="label">Your broker saw</div>
      <div class="big num">$7.0M</div>
      <div class="note">Reported EBITDA, as-is</div>
    </div>
    <div class="compare-side">
      <div class="label accent">Yulia found</div>
      <div class="big accent num">$9.6M</div>
      <div class="note">Documented adjustments</div>
    </div>
  </div>

  <div class="gap-row">
    <span class="label">New value</span>
    <span class="val num">+$2.6M</span>
  </div>

  <div class="punchline">
    Your broker hasn&rsquo;t found new value since the day you hired them.<br>
    Yulia finds it in the <span class="accent">first conversation</span>.
  </div>

  <div class="byline">
    <div class="who">
      <img src="data:image/jpeg;base64,{HEADSHOT}" class="portrait" alt="Paul Baker">
      <div class="who-text">
        <div class="name">Paul Baker</div>
        <div class="cred">Founder, smbx.ai &nbsp;·&nbsp; For: {GROUP}</div>
      </div>
    </div>
    <div class="right">
      <div class="cta">Talk to Yulia &rsaquo;</div>
      <div class="meta">smbx.ai &nbsp;·&nbsp; {YEAR_WEEK}</div>
    </div>
  </div>

</div></div>
</body></html>"""

print(f"Rendering MON-4 ({MODE}) at {W}x{H} @ {DPR}x...")
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=DPR)
    tmp = tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode="w"); tmp.write(HTML); tmp.close()
    page.goto(f"file://{tmp.name}"); page.wait_for_timeout(2000)
    out = OUT_DIR / f"MON-4-sellers-hidden-value-BOIN-{MODE}.png"
    page.screenshot(path=str(out))
    os.unlink(tmp.name); browser.close()
print(f"Done: {out}")
