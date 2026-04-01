#!/usr/bin/env python3
"""
smbx.ai LinkedIn Carousel — "Revenue Multiples Are The Most Dangerous Metric"
Week 1, Monday post for PE/M&A/VC Group.

Playwright-rendered HTML/CSS at 2x DPR (288 DPI).
Outputs individual PNGs + combined PDF.

Usage:
    python3 content/week-01/carousel-revenue-multiples.py

Requirements:
    pip3 install playwright Pillow
    python3 -m playwright install chromium
"""

import os
import sys
import base64
import tempfile
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image

# ── Config ────────────────────────────────────────────────────────────────
W, H = 1080, 1350
DPR = 2
REPO = Path(__file__).resolve().parent.parent.parent
OUT_DIR = REPO / "content" / "week-01"

# ── Assets ────────────────────────────────────────────────────────────────
def b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

LOGO = b64(REPO / "assets" / "logos" / "logo_transparent.png")
BG_DARK = b64(REPO / "assets" / "GD.jpeg")
BG_LIGHT = b64(REPO / "assets" / "rose gold bg.jpeg")
HEADSHOT = b64(REPO / "assets" / "portrait-square.jpeg")

# ── Shared CSS ────────────────────────────────────────────────────────────
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap');
* { margin:0; padding:0; box-sizing:border-box; }
:root {
    --primary: #D44A78;
    --accent-dk: #E8709A;
    --bg-light: #F9F9FC;
    --bg-dark: #1A1C1E;
    --bg-cream: #FAF8F4;
    --card-light: #FFFFFF;
    --card-dark: #2F3133;
    --card-border: #EEEEF0;
    --text: #1A1A18;
    --text-light: #F0F0F2;
    --text-sec: #44403C;
    --text-muted: #6E6A63;
    --text-dim: #A9A49C;
    --green: #34A853;
    --red: #EA4335;
}
body {
    width: 1080px; height: 1350px; overflow: hidden;
    font-family: 'Inter', system-ui, sans-serif;
    -webkit-font-smoothing: antialiased;
}
.slide {
    width: 1080px; height: 1350px;
    position: relative; overflow: hidden;
}
.content {
    position: relative; z-index: 1; height: 100%;
    display: flex; flex-direction: column; padding: 0 72px;
}
.logo {
    object-fit: contain;
    filter: drop-shadow(0 4px 16px rgba(160,48,80,0.3));
}
.logo-on-dark {
    filter: drop-shadow(0 4px 16px rgba(160,48,80,0.3));
}
.logo-on-light {
    filter: drop-shadow(0 2px 8px rgba(0,0,0,0.08));
}
.section-label {
    font-family: Inter; font-weight: 600; font-size: 15px;
    letter-spacing: 0.12em; color: var(--primary);
    text-transform: uppercase; padding-bottom: 10px;
    border-bottom: 3px solid var(--primary); display: inline-block;
}
h1, h2, h3 { font-family: 'Sora', sans-serif; }
.dark-card {
    background: var(--card-dark);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 24px; padding: 32px;
}
.dark-card.accent-border { border: 2px solid var(--primary); }
.light-card {
    background: var(--card-light);
    border: 1px solid var(--card-border);
    border-radius: 20px; padding: 28px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}
.light-card.accent-border { border: 2px solid var(--primary); }
.circuit-dark {
    position: absolute; inset: 0;
    background: url('data:image/jpeg;base64,""" + BG_DARK + """') center/cover;
    opacity: 0.35;
}
.circuit-dark::after {
    content: ''; position: absolute; inset: 0;
    background: radial-gradient(ellipse 75% 65% at center, var(--bg-dark) 0%, transparent 100%);
}
.circuit-light {
    position: absolute; inset: 0;
    background: url('data:image/jpeg;base64,""" + BG_LIGHT + """') center/cover;
    opacity: 0.10;
}
.circuit-light::after {
    content: ''; position: absolute; inset: 0;
    background: radial-gradient(ellipse 75% 60% at center, var(--bg-light) 0%, transparent 100%);
}
.bottom-stripe {
    position: absolute; bottom: 0; left: 0; right: 0;
    height: 5px; background: var(--primary);
}
.page-num {
    position: absolute; bottom: 16px; right: 72px;
    font-family: Inter; font-weight: 500; font-size: 16px;
}
.headshot {
    border-radius: 50%; object-fit: cover;
    object-position: center;
    border: 4px solid var(--accent-dk);
}
.accent-left {
    border-left: 4px solid var(--accent-dk); padding-left: 16px;
}
.metric-row {
    display: flex; flex-direction: column; gap: 2px;
    padding: 10px 0;
    border-bottom: 1px solid rgba(255,255,255,0.06);
}
.metric-label { font-size: 15px; color: #9A9A9E; }
.metric-value {
    font-family: Sora; font-weight: 600; font-size: 25px;
    color: var(--text-light);
}
"""

TOTAL = 7

def slide(body, bg="bg-light", layers="", page_color="var(--text-dim)"):
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<div class="slide" style="background:var(--{bg});">{layers}
<div class="content">{body}</div>
<div class="bottom-stripe"></div>
<div class="page-num" style="color:{page_color};">{{PN}}</div>
</div></body></html>"""


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 1: COVER — Paul + Logo + Headline
# ══════════════════════════════════════════════════════════════════════════
S1 = slide(f"""
<div style="display:flex;justify-content:center;padding-top:48px;">
    <img src="data:image/png;base64,{LOGO}" class="logo logo-on-dark" style="height:100px;">
</div>

<div style="display:flex;flex-direction:column;align-items:center;margin-top:32px;">
    <img src="data:image/jpeg;base64,{HEADSHOT}" class="headshot" style="width:240px;height:240px;">
    <div style="font-family:Sora;font-weight:800;font-size:38px;color:var(--text-light);margin-top:18px;">Paul Baker</div>
    <div style="font-size:28px;color:#9A9A9E;margin-top:6px;">Founder, smbx.ai &bull; 20+ Years in M&amp;A</div>
</div>

<div style="margin-top:auto;margin-bottom:0;flex:1;display:flex;flex-direction:column;justify-content:center;">
    <div style="width:80px;height:4px;background:var(--primary);margin-bottom:24px;"></div>
    <h1 style="font-weight:800;font-size:76px;line-height:1.08;letter-spacing:-0.02em;color:var(--text-light);">
        Revenue Multiples Are The <span style="color:var(--accent-dk);">Most Dangerous</span> Metric in M&amp;A
    </h1>
</div>

<div style="margin-bottom:48px;">
    <div class="dark-card accent-border" style="display:flex;justify-content:space-between;align-items:center;padding:28px 36px;">
        <div>
            <div style="font-weight:700;font-size:30px;color:var(--accent-dk);letter-spacing:0.06em;">SWIPE TO SEE WHY &rsaquo;</div>
            <div style="font-size:32px;color:var(--text-light);margin-top:8px;">Same revenue. One worth $450K. The other $1.6M.</div>
        </div>
    </div>
</div>
""", bg="bg-dark", layers='<div class="circuit-dark"></div>', page_color="#6E6A63")


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 2: THE QUOTE — Dark card dominates
# ══════════════════════════════════════════════════════════════════════════
S2 = slide(f"""
<div style="display:flex;justify-content:flex-start;padding-top:48px;">
    <img src="data:image/png;base64,{LOGO}" class="logo logo-on-light" style="height:56px;">
</div>
<div class="section-label" style="margin-top:20px;font-size:24px;">The Seller's Logic</div>

<div class="dark-card" style="margin-top:24px;flex:1;display:flex;flex-direction:column;margin-bottom:48px;padding:44px;">
    <div style="font-family:Sora;font-weight:800;font-size:72px;color:var(--accent-dk);line-height:1;">&ldquo;</div>
    <p style="font-family:Sora;font-weight:600;font-size:48px;color:var(--text-light);line-height:1.3;margin-top:8px;">
        My business does $2M in revenue. Companies like mine sell for 1x.
    </p>
    <p style="font-family:Sora;font-weight:800;font-size:58px;color:var(--accent-dk);margin-top:32px;">
        So it's worth $2M.
    </p>

    <div style="width:100%;height:2px;background:rgba(255,255,255,0.08);margin:36px 0;"></div>

    <h2 style="font-weight:800;font-size:56px;line-height:1.1;color:var(--text-light);">
        That math killed every one of those deals.
    </h2>
    <p style="font-size:36px;color:#9A9A9E;margin-top:24px;line-height:1.45;">
        $600K owner comp + one client at 35% is a different asset than 22% margins and 400 clients.
    </p>

    <div style="margin-top:auto;padding-top:28px;border-top:2px solid rgba(255,255,255,0.06);">
        <div style="display:flex;align-items:center;gap:14px;">
            <div style="width:14px;height:14px;border-radius:50%;background:var(--accent-dk);"></div>
            <span style="font-family:Sora;font-weight:700;font-size:32px;color:var(--accent-dk);">Here's the proof &rsaquo;</span>
        </div>
    </div>
</div>
""", bg="bg-light", layers='<div class="circuit-light"></div>')


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 3: COMPARISON — Two dark cards side by side
# ══════════════════════════════════════════════════════════════════════════
S3 = slide(f"""
<div style="display:flex;justify-content:flex-start;padding-top:40px;">
    <img src="data:image/png;base64,{LOGO}" class="logo logo-on-light" style="height:48px;">
</div>
<div class="section-label" style="margin-top:16px;font-size:22px;">Same Revenue. Different Reality.</div>
<h2 style="font-weight:800;font-size:44px;color:var(--text);margin-top:12px;">Both companies: $2M revenue</h2>

<div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:20px;flex:1;margin-bottom:16px;">
    <div class="dark-card" style="display:flex;flex-direction:column;padding:28px 24px;">
        <div style="font-size:20px;font-weight:600;letter-spacing:0.12em;color:#9A9A9E;">BUSINESS A</div>
        <div style="font-family:Sora;font-weight:700;font-size:28px;color:var(--red);margin-top:6px;">&ldquo;The Trap&rdquo;</div>
        <div style="margin-top:16px;display:flex;flex-direction:column;flex:1;">
            <div class="metric-row" style="padding:12px 0;"><span class="metric-label" style="font-size:26px;">Owner Comp</span><span class="metric-value" style="font-size:42px;">$600K</span></div>
            <div class="metric-row" style="padding:12px 0;"><span class="metric-label" style="font-size:26px;">Margins</span><span class="metric-value" style="font-size:42px;">8%</span></div>
            <div class="metric-row" style="padding:12px 0;"><span class="metric-label" style="font-size:26px;">Top Client</span><span class="metric-value" style="font-size:42px;">35%</span></div>
            <div class="metric-row" style="padding:12px 0;"><span class="metric-label" style="font-size:26px;">Clients</span><span class="metric-value" style="font-size:42px;">~12</span></div>
            <div class="metric-row" style="padding:12px 0;border-bottom:none;"><span class="metric-label" style="font-size:26px;">Trend</span><span class="metric-value" style="font-size:42px;">Flat</span></div>
        </div>
        <div style="padding-top:16px;border-top:2px solid rgba(255,255,255,0.08);margin-top:auto;">
            <div style="font-size:18px;font-weight:700;letter-spacing:0.1em;color:var(--red);">VALUE</div>
            <div style="font-family:Sora;font-weight:800;font-size:60px;color:var(--red);">$450K</div>
        </div>
    </div>
    <div class="dark-card accent-border" style="display:flex;flex-direction:column;padding:28px 24px;">
        <div style="font-size:20px;font-weight:600;letter-spacing:0.12em;color:#9A9A9E;">BUSINESS B</div>
        <div style="font-family:Sora;font-weight:700;font-size:28px;color:var(--green);margin-top:6px;">&ldquo;The Asset&rdquo;</div>
        <div style="margin-top:16px;display:flex;flex-direction:column;flex:1;">
            <div class="metric-row" style="padding:12px 0;"><span class="metric-label" style="font-size:26px;">Owner Comp</span><span class="metric-value" style="font-size:42px;">$200K</span></div>
            <div class="metric-row" style="padding:12px 0;"><span class="metric-label" style="font-size:26px;">Margins</span><span class="metric-value" style="font-size:42px;">22%</span></div>
            <div class="metric-row" style="padding:12px 0;"><span class="metric-label" style="font-size:26px;">Top Client</span><span class="metric-value" style="font-size:42px;">4%</span></div>
            <div class="metric-row" style="padding:12px 0;"><span class="metric-label" style="font-size:26px;">Clients</span><span class="metric-value" style="font-size:42px;">~400</span></div>
            <div class="metric-row" style="padding:12px 0;border-bottom:none;"><span class="metric-label" style="font-size:26px;">Trend</span><span class="metric-value" style="font-size:42px;">+15%</span></div>
        </div>
        <div style="padding-top:16px;border-top:2px solid rgba(255,255,255,0.08);margin-top:auto;">
            <div style="font-size:18px;font-weight:700;letter-spacing:0.1em;color:var(--green);">VALUE</div>
            <div style="font-family:Sora;font-weight:800;font-size:60px;color:var(--green);">$1.6M</div>
        </div>
    </div>
</div>

<div style="text-align:center;padding:12px 0 40px;">
    <span style="font-family:Sora;font-weight:700;font-size:38px;color:var(--primary);">Same revenue. 3.5x difference in value.</span>
</div>
""", bg="bg-light")


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 4: THE 3 DRIVERS
# ══════════════════════════════════════════════════════════════════════════
S4 = slide(f"""
<div style="display:flex;justify-content:flex-start;padding-top:48px;">
    <img src="data:image/png;base64,{LOGO}" class="logo logo-on-light" style="height:56px;">
</div>
<div class="section-label" style="margin-top:20px;font-size:24px;">What Matters</div>

<h2 style="font-weight:800;font-size:60px;color:var(--text);margin-top:20px;line-height:1.12;">
    The 3 Things That<br>Actually Drive Value
</h2>
<div style="width:80px;height:4px;background:var(--primary);margin:24px 0;"></div>

<div style="display:flex;flex-direction:column;gap:20px;flex:1;margin-bottom:48px;">
    <div class="dark-card" style="flex:1;display:flex;align-items:center;gap:28px;padding:36px 40px;">
        <div style="font-family:Sora;font-weight:800;font-size:80px;color:rgba(255,255,255,0.25);line-height:1;">01</div>
        <div>
            <div style="font-family:Sora;font-weight:700;font-size:42px;color:var(--text-light);">Adjusted SDE</div>
            <div style="font-size:30px;color:#9A9A9E;margin-top:10px;line-height:1.4;">Every add-back identified from actual returns. Not estimated.</div>
        </div>
    </div>
    <div class="dark-card" style="flex:1;display:flex;align-items:center;gap:28px;padding:36px 40px;">
        <div style="font-family:Sora;font-weight:800;font-size:80px;color:rgba(255,255,255,0.25);line-height:1;">02</div>
        <div>
            <div style="font-family:Sora;font-weight:700;font-size:42px;color:var(--text-light);">Quality of Earnings</div>
            <div style="font-size:30px;color:#9A9A9E;margin-top:10px;line-height:1.4;">Concentration, dependency, margin trend, sustainability.</div>
        </div>
    </div>
    <div class="dark-card accent-border" style="flex:1;display:flex;align-items:center;gap:28px;padding:36px 40px;">
        <div style="font-family:Sora;font-weight:800;font-size:80px;color:rgba(212,74,120,0.4);line-height:1;">03</div>
        <div>
            <div style="font-family:Sora;font-weight:700;font-size:42px;color:var(--text-light);">Buyer Landscape</div>
            <div style="font-size:30px;color:#9A9A9E;margin-top:10px;line-height:1.4;">Who's buying in your sector right now &mdash; and what they're paying.</div>
        </div>
    </div>
</div>
""", bg="bg-cream", layers='<div class="circuit-light"></div>')


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 5: DEEP DIVE — SDE + Blind Equity
# ══════════════════════════════════════════════════════════════════════════
S5 = slide(f"""
<div style="display:flex;justify-content:flex-start;padding-top:40px;">
    <img src="data:image/png;base64,{LOGO}" class="logo logo-on-light" style="height:48px;">
</div>
<div class="section-label" style="margin-top:16px;font-size:22px;">Deep Dive: #1</div>

<h2 style="font-weight:800;font-size:56px;color:var(--text);margin-top:16px;">Adjusted SDE</h2>
<div style="width:80px;height:4px;background:var(--primary);margin:16px 0;"></div>

<div class="dark-card" style="flex:1;display:flex;flex-direction:column;margin-bottom:48px;padding:36px;">
    <div style="background:rgba(212,74,120,0.08);border-radius:16px;padding:28px;border-left:5px solid var(--accent-dk);">
        <div style="font-family:Sora;font-weight:700;font-size:38px;color:var(--accent-dk);">Blind Equity&trade;</div>
        <p style="font-size:30px;color:#9A9A9E;margin-top:8px;line-height:1.4;">
            The hidden value in your books you didn't know was there.
        </p>
    </div>

    <div style="margin-top:28px;font-size:30px;color:#9A9A9E;">
        <div style="font-family:Sora;font-weight:700;font-size:32px;color:var(--text-light);margin-bottom:16px;">Real example &mdash; cleaning company:</div>
        <div style="display:flex;justify-content:space-between;padding:14px 0;border-bottom:1px solid rgba(255,255,255,0.06);">
            <span>Personal vehicles</span><span style="color:var(--text-light);font-weight:700;font-size:34px;">$48K</span>
        </div>
        <div style="display:flex;justify-content:space-between;padding:14px 0;border-bottom:1px solid rgba(255,255,255,0.06);">
            <span>Spouse on payroll</span><span style="color:var(--text-light);font-weight:700;font-size:34px;">$24K</span>
        </div>
        <div style="display:flex;justify-content:space-between;padding:14px 0;border-bottom:1px solid rgba(255,255,255,0.06);">
            <span>Above-market rent</span><span style="color:var(--text-light);font-weight:700;font-size:34px;">$31K</span>
        </div>
        <div style="display:flex;justify-content:space-between;padding:14px 0;border-bottom:1px solid rgba(255,255,255,0.06);">
            <span>One-time equipment</span><span style="color:var(--text-light);font-weight:700;font-size:34px;">$18K</span>
        </div>
        <div style="display:flex;justify-content:space-between;padding:14px 0;border-bottom:1px solid rgba(255,255,255,0.06);">
            <span>Cell &amp; internet</span><span style="color:var(--text-light);font-weight:700;font-size:34px;">$3K</span>
        </div>
        <div style="display:flex;justify-content:space-between;padding:18px 0 0;margin-top:8px;">
            <span style="font-family:Sora;font-weight:700;font-size:36px;color:var(--accent-dk);">Total Blind Equity</span>
            <span style="font-family:Sora;font-weight:800;font-size:42px;color:var(--accent-dk);">$124K</span>
        </div>
    </div>

    <div style="margin-top:auto;padding-top:24px;border-top:2px solid rgba(255,255,255,0.06);">
        <p style="font-family:Sora;font-weight:700;font-size:40px;color:var(--text-light);line-height:1.3;">
            At 3.2x, that's <span style="color:var(--accent-dk);">$400K</span> in hidden value.
        </p>
    </div>
</div>
""", bg="bg-light", layers='<div class="circuit-light"></div>')


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 6: QUALITY + BUYER LANDSCAPE (consolidated)
# ══════════════════════════════════════════════════════════════════════════
S6 = slide(f"""
<div style="display:flex;justify-content:flex-start;padding-top:40px;">
    <img src="data:image/png;base64,{LOGO}" class="logo logo-on-light" style="height:48px;">
</div>
<div class="section-label" style="margin-top:16px;font-size:22px;">Deep Dive: #2 &amp; #3</div>

<h2 style="font-weight:800;font-size:56px;color:var(--text);margin-top:16px;">Quality of Earnings</h2>

<div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:20px;">
    <div class="light-card" style="padding:28px;">
        <div style="display:flex;align-items:center;gap:12px;">
            <div style="width:14px;height:14px;border-radius:50%;background:var(--primary);flex-shrink:0;"></div>
            <span style="font-family:Sora;font-weight:700;font-size:34px;color:var(--text);">Concentration</span>
        </div>
        <p style="font-size:28px;color:var(--text-muted);margin-top:10px;line-height:1.4;">One client holds the keys?</p>
    </div>
    <div class="light-card" style="padding:28px;">
        <div style="display:flex;align-items:center;gap:12px;">
            <div style="width:14px;height:14px;border-radius:50%;background:var(--primary);flex-shrink:0;"></div>
            <span style="font-family:Sora;font-weight:700;font-size:34px;color:var(--text);">Dependency</span>
        </div>
        <p style="font-size:28px;color:var(--text-muted);margin-top:10px;line-height:1.4;">Runs without you?</p>
    </div>
    <div class="light-card" style="padding:28px;">
        <div style="display:flex;align-items:center;gap:12px;">
            <div style="width:14px;height:14px;border-radius:50%;background:var(--primary);flex-shrink:0;"></div>
            <span style="font-family:Sora;font-weight:700;font-size:34px;color:var(--text);">Margins</span>
        </div>
        <p style="font-size:28px;color:var(--text-muted);margin-top:10px;line-height:1.4;">Creeping or compressing?</p>
    </div>
    <div class="light-card" style="padding:28px;">
        <div style="display:flex;align-items:center;gap:12px;">
            <div style="width:14px;height:14px;border-radius:50%;background:var(--primary);flex-shrink:0;"></div>
            <span style="font-family:Sora;font-weight:700;font-size:34px;color:var(--text);">Recurring?</span>
        </div>
        <p style="font-size:28px;color:var(--text-muted);margin-top:10px;line-height:1.4;">Recurring earns the premium.</p>
    </div>
</div>

<div style="width:100%;height:2px;background:var(--card-border);margin:24px 0;"></div>

<h2 style="font-weight:800;font-size:56px;color:var(--text);">Buyer Landscape</h2>

<div class="dark-card" style="margin-top:20px;flex:1;display:flex;flex-direction:column;margin-bottom:48px;padding:40px;">
    <p style="font-size:38px;color:var(--text-light);line-height:1.4;">
        Who is actively acquiring in your sector &mdash; and what are they paying.
    </p>
    <div class="accent-left" style="margin-top:auto;padding-top:28px;border-left-width:5px;">
        <p style="font-family:Sora;font-weight:700;font-size:40px;color:var(--text-light);">Value isn't what a spreadsheet says.</p>
        <p style="font-weight:700;font-size:36px;color:var(--accent-dk);margin-top:12px;">It's what the market clears.</p>
    </div>
</div>
""", bg="bg-cream")


# ══════════════════════════════════════════════════════════════════════════
# SLIDE 7: CTA — Paul again, engagement hook
# ══════════════════════════════════════════════════════════════════════════
S7 = slide(f"""
<div style="display:flex;justify-content:center;padding-top:44px;">
    <img src="data:image/png;base64,{LOGO}" class="logo logo-on-dark" style="height:90px;">
</div>

<div style="text-align:center;margin-top:28px;">
    <h2 style="font-weight:800;font-size:60px;color:var(--text-light);line-height:1.12;">
        Revenue tells you the size.
    </h2>
    <h2 style="font-weight:800;font-size:60px;color:var(--accent-dk);line-height:1.12;margin-top:8px;">
        It tells you almost nothing about the value.
    </h2>
</div>

<div class="light-card accent-border" style="margin-top:28px;display:flex;flex-direction:column;align-items:center;text-align:center;padding:40px;flex:1;margin-bottom:48px;">
    <img src="data:image/jpeg;base64,{HEADSHOT}" class="headshot" style="width:220px;height:220px;">
    <div style="font-family:Sora;font-weight:800;font-size:42px;color:var(--text);margin-top:20px;">Paul Baker</div>
    <div style="font-size:30px;color:var(--text-muted);margin-top:6px;">Founder, smbx.ai &bull; 20+ Years in M&amp;A</div>

    <div style="width:70px;height:3px;background:var(--primary);margin:24px 0;"></div>

    <h2 style="font-weight:800;font-size:64px;color:var(--primary);">Am I wrong?</h2>
    <p style="font-size:38px;color:var(--text);line-height:1.45;margin-top:16px;">
        <strong>Where does it break<br>down for you?</strong>
    </p>

    <div style="margin-top:auto;padding-top:24px;">
        <p style="font-weight:700;font-size:34px;color:var(--primary);">Follow for more M&amp;A intelligence</p>
        <p style="font-family:Sora;font-weight:700;font-size:32px;color:var(--text-muted);margin-top:10px;">smbx.ai</p>
    </div>
</div>
""", bg="bg-dark", layers='<div class="circuit-dark"></div>', page_color="#6E6A63")


# ══════════════════════════════════════════════════════════════════════════
# RENDER
# ══════════════════════════════════════════════════════════════════════════
slides = [S1, S2, S3, S4, S5, S6, S7]

print(f"Rendering {len(slides)} slides at {W}x{H} @ {DPR}x...")

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(
        viewport={"width": W, "height": H},
        device_scale_factor=DPR
    )

    pngs = []
    for i, html in enumerate(slides):
        html = html.replace("{PN}", f"{i+1} / {len(slides)}")
        tmp = tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode="w")
        tmp.write(html)
        tmp.close()
        page.goto(f"file://{tmp.name}")
        page.wait_for_timeout(2000)  # Wait for fonts to load
        png_path = OUT_DIR / f"slide_{i+1}.png"
        page.screenshot(path=str(png_path))
        pngs.append(str(png_path))
        os.unlink(tmp.name)
        print(f"  Slide {i+1}/{len(slides)} -> {png_path.name}")

    browser.close()

# Combine into PDF
imgs = [
    Image.open(p).convert("RGB").resize((W, H), Image.LANCZOS)
    for p in pngs
]
pdf_path = OUT_DIR / "revenue-multiples-carousel.pdf"
imgs[0].save(
    str(pdf_path), "PDF",
    resolution=288.0,
    save_all=True,
    append_images=imgs[1:]
)

print(f"\nDone: {pdf_path}")
print(f"  {len(slides)} slides, {W}x{H} @ {DPR}x ({W*DPR}x{H*DPR} actual)")
print(f"  PDF ready for LinkedIn upload")
