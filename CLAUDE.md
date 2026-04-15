# CLAUDE.md — smbx.ai Marketing

**Read this before any work in this repo.** Then `DESIGN_HANDOFF.md` → `DESIGN_LANGUAGE.md` → relevant skill.

## Source of truth

| What | Where |
|---|---|
| 90-day strategy | `SMBX_90_DAY_PLAN.xlsx` — use Python + openpyxl to read. Never fabricate from memory. |
| Visual system | `DESIGN_LANGUAGE.md` (authoritative) + `DESIGN_HANDOFF.md` (orientation) |
| Brand voice | `STYLE_GUIDE.md` |
| Carousel production | `.claude/skills/linkedin-carousel/SKILL.md` |
| Single-image posts | `.agents/skills/linkedin-image-post/SKILL.md` |

## Non-negotiables (the things Paul has already corrected once)

### Typography

- **Never use `<br>` in any H1 or punchline. Ever.** Not for mid-sentence breaks, not for "fragment cadence" between multiple sentences — every time I've tried the "fragment cadence allowed" exception, Paul has flagged it as AI-generated. Fix: (a) reduce font-size until the whole line fits, or (b) if you have two distinct statements that must be on separate lines, wrap each in its own block element (`<div>` / `<p>`). **`<br>` is an AI-slop tell and belongs in no asset.**
- **Mobile typography floor:** LinkedIn is 95%+ mobile. 1080 canvas shrinks ÷3 to ~360px thumbnail. Floors: eyebrow 28px, body 34px, KV key 28px, KV value 34–38px, footer 26px.
- **Sora 800 + Inter.** No third font. Avoid weight 700.

### Layout

- **Fibonacci spacing only** — all margins/padding from {8, 13, 21, 34, 55, 89, 144}. Never 20/24/32/40/48/56/60/72/80/96 for layout spacing.
- **Content top-aligned, bottom breathes.** `margin-top:auto` on footer/attribution is the only layout mechanism. No `justify-content:center` or `space-between` on `.content`.

### Deck rhythm (carousels)

- **LIGHT is dominant. DARK is contrast.** 5-slide rhythm: LIGHT cover → LIGHT data → LIGHT data → DARK cinematic anchor (S4) → LIGHT close with dark ring-CTA block inside. One dark moment per deck.
- **Field Note masthead** — logo top-left + `FIELD NOTE · NO. XX` top-right. Pick non-sequential numbers (17, 23, 31, 38) — never "No. 01".
- **Two-variant eyebrows** — HookEyebrow (dot + 0.2em) on cover only, once per deck. SectionEyebrow (0.08em, no dot) on every other slide.
- **Cover must have portrait byline** — face on LinkedIn is non-negotiable.

### Content

- **Group info goes in the filename, not on the slide.** Example: `MON-1-brokers-cim-MANetwork-light.pdf`. Do not add a "For: {Group}" tag to the slide itself — Paul's already corrected this.
- **CTAs match the xlsx.** Product-phase content uses "Talk to Yulia. smbx.ai" (not "Run a Baseline" or "Learn More"). Check the xlsx `CTA` column for each post.

## Working cadence

- **One day at a time.** Paul reviews each day's assets before moving to the next. Don't speculatively build Tue/Wed before Mon is approved.
- **Filename convention:** `MON-{N}-{topic}-{GroupShort}-light.{pdf|png}`. GroupShort is a 1-2 word abbreviation of the group name (MANetwork, Dealflow, SuperCFO, BOIN).
- **After building, always render and visually QA before shipping.** Extract PDF slides with `pdftoppm -png -r 144 ...` and Read each PNG. Verify typography, no AI-slop tells, no orphaned words, mobile-readable sizes.

## Reference implementations (Monday Week 1)

- `content/week-01/carousel-brokers-cim-30min.py` — canonical carousel structure, Field Note No. 11
- `content/week-01/png-sellers-hidden-value.py` — canonical single-image structure, Field Note No. 33

Clone one of these when starting a new asset. Every rule above is encoded in them.
