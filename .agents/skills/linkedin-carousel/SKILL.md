---
name: linkedin-carousel
description: "When the user wants to create, iterate, or render LinkedIn carousel slides using the Playwright pipeline. Use when the user mentions 'carousel,' 'LinkedIn slides,' 'PDF carousel,' 'render slides,' 'new carousel,' or references the carousel-revenue-multiples.py script. This skill encodes all lessons learned from design iteration — font sizes, spacing, layout patterns, and asset handling for mobile-first LinkedIn carousel production."
metadata:
  version: 1.0.0
---

# LinkedIn Carousel Production

You are an expert LinkedIn carousel designer for smbx.ai. You produce carousels using a Playwright-rendered HTML/CSS pipeline at 2x DPR (288 DPI), output as individual PNGs + combined PDF for LinkedIn upload.

## Before Starting

Read `.agents/product-marketing-context.md` for brand voice, branded terms, forbidden words, and visual identity tokens.

## The Pipeline

Carousels are built as Python scripts using Playwright + Pillow:
- HTML/CSS slides rendered in Chromium at 1080x1350 @ 2x device pixel ratio
- Individual PNGs per slide + combined PDF at 288 DPI
- Google Fonts loaded via @import (Sora + Inter)
- Assets embedded as base64 (logo, portrait, backgrounds)

Reference implementation: `content/week-01/carousel-revenue-multiples.py`

## CRITICAL: Mobile-First Font Sizing

LinkedIn carousels render at ~350px on mobile phones. A 1080px canvas shrinks ~3x. **All text must be readable by someone on a phone without zooming.**

### Minimum Font Sizes (at 1080px canvas width)

These are MINIMUMS. Go larger when space allows.

| Element | Min Size | Font | Weight | Notes |
|---------|----------|------|--------|-------|
| H1 / Hero headline | 72-80px | Sora | 800 | The scroll-stopper. Must dominate. |
| H2 / Slide headline | 56-64px | Sora | 800 | Primary message per slide |
| Subheadline | 42-50px | Sora | 600-700 | Supporting the main point |
| Body text | 36-40px | Inter | 400-500 | Explanations, descriptions |
| Card title | 38-44px | Sora | 700 | Inside dark/light cards |
| Card body | 30-36px | Inter | 400 | Card descriptions |
| Data values / KPI numbers | 42-60px | Sora | 700-800 | Must pop — these are the proof |
| Data labels | 26-30px | Inter | 400-500 | Above or beside data values |
| Section labels | 24-28px | Inter | 600-700 | Uppercase, letter-spacing 0.1em |
| CTA text | 30-36px | Sora/Inter | 600-700 | "Swipe," "Follow," engagement hooks |
| Page numbers | 24px | Inter | 500 | Bottom corner, subtle |
| Fine print / attribution | 26-30px | Inter | 400 | Founder name, credentials |

### Ghost/Decorative Numbers
- Size: 80px+ with opacity 0.25+ (NOT 0.08-0.10 — those are invisible on mobile)
- For accent-colored ghost numbers: opacity 0.4+

### The Test
If you squint at the slide thumbnail and can't read it, it's too small. Every piece of text should be legible at 350px wide.

## Color System

| Token | Hex | Usage |
|-------|-----|-------|
| Primary accent | #D44A78 | Functional only — highlights, key numbers, labels, borders |
| Dark mode accent | #E8709A | Same uses on dark backgrounds |
| Light background | #F9F9FC | Light slide base |
| Dark background | #1A1C1E | Dark slide base |
| Cream background | #FAF8F4 | Alternate light slides, callout cards |
| Card dark | #2F3133 | Dark card backgrounds |
| Card light | #FFFFFF | Light card backgrounds |
| Card border | #EEEEF0 | Light card borders |
| Text primary (light) | #1A1A18 | Dark text on light backgrounds |
| Text primary (dark) | #F0F0F2 | Light text on dark backgrounds |
| Text secondary | #44403C | Subheadings on light bg |
| Text muted | #6E6A63 | Captions on light bg |
| Text muted (dark) | #9A9A9E | Captions on dark bg |
| Green (positive) | #34A853 | Good metrics, "The Asset" |
| Red (negative) | #EA4335 | Bad metrics, "The Trap" |

## Layout Patterns

### Slide Structure
- Canvas: 1080x1350px (4:5 portrait, LinkedIn optimal)
- Content padding: 0 72px (sides)
- Top padding: 40-48px
- Bottom: 5px #D44A78 accent stripe (absolute, full width)
- Page number: bottom-right, 24px Inter 500

### Logo Placement
- Use `logo_transparent.png` (white background stripped) — NEVER the JPEG
- Dark slides: `filter: drop-shadow(0 4px 16px rgba(160,48,80,0.3))`
- Light slides: `filter: drop-shadow(0 2px 8px rgba(0,0,0,0.08))`
- Cover/CTA slides: centered, 90-100px height
- Content slides: top-left, 48-56px height

### Portrait/Headshot
- Use `portrait-square.jpeg` (pre-cropped to square with dark side padding)
- NEVER use the raw `portrait.jpeg` — it's tall (0.62 aspect ratio) and will crop the head
- CSS: `border-radius:50%; object-fit:cover; object-position:center;`
- Border: 4px solid #E8709A
- Cover slide: 240px diameter
- CTA slide: 220px diameter

### Circuit Board Backgrounds
- Light: `rose gold bg.jpeg` at 10% opacity with radial gradient center fade
- Dark: `GD.jpeg` at 35% opacity with radial gradient center fade
- Radial fade: `radial-gradient(ellipse 75% 65% at center, base-color 0%, transparent 100%)`
- Use on: cover, closing, selected content slides for texture
- Skip on: data-heavy slides (comparison cards) where it competes

### Dark Cards (#2F3133)
- Border-radius: 24px
- Padding: 36-44px
- Border: 1px solid rgba(255,255,255,0.06)
- Accent variant: 2px solid #D44A78
- Use `flex:1` to fill available space ONLY when content can distribute evenly
- If content doesn't fill, remove `flex:1` and let it size naturally

### Light Cards (#FFFFFF)
- Border-radius: 20px
- Padding: 28-32px
- Border: 1px solid #EEEEF0
- Shadow: 0 1px 4px rgba(0,0,0,0.05)

## Spacing Rules

- NEVER leave dead space — if a flex container stretches but content doesn't fill, either add content or remove flex:1
- Use `margin-top:auto` to push footer elements to the bottom of flex containers
- Divider lines: 2px solid rgba(255,255,255,0.06) inside dark cards, 2px solid #EEEEF0 on light backgrounds
- Accent bars: 80px wide, 4px tall, #D44A78 — used below headlines as visual anchors

## Slide Type Templates

### Cover Slide (Dark)
- Background: dark + circuit overlay at 35%
- Logo: centered, 100px
- Headshot: centered, 240px circle
- Name + credentials: centered below headshot
- Headline: left-aligned, 72-80px
- Bottom teaser card: "SWIPE TO SEE WHY" with hook

### Quote/Statement Slide (Light bg, dark card)
- Logo: top-left, 56px
- Section label: uppercase, #D44A78
- Dark card fills remaining space
- Large quotation mark, quote text, divider, punchline, body
- Bottom CTA inside card with dot + arrow

### Side-by-Side Comparison (Light bg)
- Two dark cards in CSS grid (1fr 1fr)
- Each card: label, nickname, metric rows, bottom value
- Use red (#EA4335) for bad, green (#34A853) for good
- Bottom tagline centered below cards

### Numbered List Slide (Cream bg)
- Three stacked dark cards with flex:1
- Ghost numbers (80px, 0.25 opacity) left-aligned in each card
- Title + description right of ghost number
- Third card gets accent border

### Data Table Slide (Light bg, dark card)
- Dark card with line items (flex row, space-between)
- Labels left, values right
- Rows separated by 1px dividers
- Total row in accent color, larger font
- Bottom punchline with accent-colored key number

### CTA/Closing Slide (Dark)
- Background: dark + circuit overlay at 35%
- Logo: centered, 90px
- Punchline headline: centered, 60px, white + accent
- White card with accent border containing:
  - Headshot: 220px
  - Name + credentials
  - Engagement hook ("Am I wrong?") in 64px accent
  - Follow CTA

## Content Guidelines

- Lead with the most provocative statement
- One idea per slide — don't cram
- Use real numbers, never vague claims
- Branded terms (The Baseline, Blind Equity, The Rundown) appear naturally without definition in Weeks 1-4
- Questions on closing slide to drive comments
- Never use forbidden words (see product-marketing-context.md)

## Asset Paths (Relative to Repo Root)

| Asset | Path |
|-------|------|
| Logo (transparent PNG) | `assets/logos/logo_transparent.png` |
| Portrait (square, pre-cropped) | `assets/portrait-square.jpeg` |
| Dark circuit background | `assets/GD.jpeg` |
| Light circuit background | `assets/rose gold bg.jpeg` |

## Rendering

```python
# Standard render config
W, H = 1080, 1350
DPR = 2  # 2x for 288 DPI output

# Font loading wait
page.wait_for_timeout(2000)  # Google Fonts need time

# PDF assembly
imgs[0].save(path, "PDF", resolution=288.0, save_all=True, append_images=imgs[1:])
```

## Related Skills

- **social-content**: For post text that accompanies the carousel
- **copywriting**: For headline and CTA writing
- **copy-editing**: Run the Seven Sweeps on slide text before rendering
- **marketing-psychology**: For hook and engagement patterns
