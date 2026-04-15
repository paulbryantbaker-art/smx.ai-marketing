# Design Handoff — Read Me First

**Updated: 2026-04-15**

The smbx.ai website visual system was rebuilt in a series of commits on 2026-04-14.
Any LinkedIn document, carousel, post, or marketing asset generated from this point
forward must reflect the **current** design language — not the April 4 state captured
in the older `STYLE_GUIDE.md`.

## What to read (in order)

1. **`DESIGN_LANGUAGE.md`** — the authoritative visual system. Colors, type,
   spacing, motion, materials, editorial primitives, anti-slop rules, and a
   section on **translating site patterns to LinkedIn documents**. Start here.

2. **`STYLE_GUIDE.md`** — authoritative for logo asset rules, brand voice, and
   written copy patterns. These did not change.

3. **`.claude/skills/awesome-design-md/`** — vendored skill with 65+ brand
   DESIGN.md references (Apple, Linear, Stripe, Framer, Vercel, etc.). Invoke
   via the Skill tool when you need to translate a specific brand aesthetic
   into the smbx visual vocabulary. The smbx site itself is informed by:
   - `apple` — cinematic dark/light section rhythm, glass materials, ruthless
     reduction
   - `framer` — ring-accent CTAs (no blurred halos), confident compression
   - `x.ai` (Grok) — AI-chat restraint, whitespace confidence
   If building a derivative doc, reference these files directly — do not
   paraphrase from memory, the tokens matter.

## Key deltas from the 2026-04-04 STYLE_GUIDE.md

- Accent shifted from rose-gold to a single brand pink (`#D44A78` light,
  `#E8709A` dark). Rose-gold 3D logo variant is deprecated for docs — use the
  flat wordmark.
- Page background changed from cream `#F8F6F2` to `#F9F9FC` light / `#1A1C1E`
  dark. Immersive sections use `#0f1012`.
- Sora replaces the previous headline font (800–900 weight, tight tracking).
  Inter stays as body.
- Eyebrow system is now two-variant: **hook** (0.2em + dot, accent) opens a
  page; **section** (0.08em, no dot) opens a section. No longer a single
  repeating label style.
- Radial-gradient blur halos behind CTAs are out. Ring-accent pattern is in
  (1px accent border + inner hairline + soft drop shadow).
- Apple Glass material (backdrop-filter blur + saturate) replaces flat
  translucent overlays on mobile sticky chrome.
- Cinematic anchor pattern: each journey page now has one interactive
  wrapped in an immersive dark band, rendered as a "light card on dark stage"
  — same pattern works for LinkedIn carousel hero slides.
- Scroll-reveal motion is universal across primitives (section-level fade +
  y-translate, once-only, `-10%` viewport margin). Derivative docs should
  pace content with whitespace to mirror this rhythm.
- New trademarked-term affordance: `JargonTerm` tooltip (dashed underline +
  hover/focus definition) for first-time mentions of Baseline™, Blind Equity™,
  Rundown™. Document equivalent: italicize the term + footnote its definition
  the first time it appears.

## Output patterns for LinkedIn docs

See **`DESIGN_LANGUAGE.md` § 9** for concrete slide patterns (title, content,
stat, light-card-on-dark, quote, CTA) and **§ 7** for anti-slop rules.

The short version:
- Dark title slide + light content slide is the native rhythm.
- One accent per slide, never more.
- Sora 900 for headlines, Inter 400/500 for body, no third font.
- Eyebrow at top of each slide in the correct variant.
- Stats in tabular-nums (Sora 900, clamp sizes).
- Quotes use Sora 900, not italic Inter.
- CTAs are dark blocks with an accent ring border.

## If in doubt

The source of truth is the website code at github.com/paulbryantbaker-art/SMBx
(tokens at `client/src/components/content/tokens.ts`, primitives at
`storyBlocks.tsx`). This repo's `DESIGN_LANGUAGE.md` narrates that code — it
is not a separate design decision. When the site changes, update
`DESIGN_LANGUAGE.md` here and mention the commit.
