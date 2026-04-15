---
name: awesome-design-md
description: Reference brand-inspired design systems (Apple, Linear, Stripe, Vercel, Notion, etc.) before building UI. Use when the user asks to build, redesign, or style something "like <brand>", "in the style of <brand>", "inspired by <brand>", or references a specific well-known product's aesthetic. Library covers 65+ brands — consumer tech, SaaS, automotive, fintech, media.
source: https://github.com/VoltAgent/awesome-design-md · distributed via `npx getdesign@latest`
license: See upstream repo. Brand references are provided as design-pattern documentation, not as claims of affiliation.
---

# awesome-design-md

A library of DESIGN.md files that encode the visual system of popular brands — typography, color roles, spatial rhythm, component patterns, motion principles, and voice. Use these as **reference** before generating UI in a brand's style.

## When to use

Invoke when the user:
- Asks to build or redesign something "like `<brand>`", "in the style of `<brand>`", "inspired by `<brand>`"
- References a well-known product's aesthetic as a target (e.g., "make it feel like Linear", "Stripe-style docs", "Apple product page")
- Wants to match a brand's conventions for typography, color, spacing, or motion

Do **not** invoke when the user references a brand in a non-design context (e.g., discussing competitors' pricing, API integrations, or business strategy).

## How to use

1. **Identify the brand.** Match the user's reference to one of the files listed below. If the exact brand isn't in the library, pick the closest aesthetic sibling and say so (e.g., "using Linear as the nearest reference since Height.app isn't in the library").
2. **Read the brand file.** Use the Read tool on `brands/<brand>.md` (relative to this skill directory). Don't paraphrase from memory — the files contain specific tokens (hex codes, type scales, radii) that matter.
3. **Extract only what's load-bearing.** Brand files are 200–400 lines. Pull out: color roles, type stack + scale, spacing/radius tokens, signature component patterns, motion principles, voice. Skip sections that don't apply to the current task.
4. **Adapt, don't copy.** The user's product has its own identity — apply the brand's *approach* (the pattern, the rhythm, the restraint), not a pixel-for-pixel clone. If project has an existing design system, reconcile: respect tokens the user already chose; only import from the brand where the user has no opinion yet.
5. **Cite the file you used.** In your response, reference the brand file path so the user can review the same source material.

## Available brands

**Consumer tech / devices**: `apple`, `nvidia`, `meta`, `playstation`, `bmw`, `bugatti`, `ferrari`, `lamborghini`, `renault`, `tesla`, `spacex`, `nike`

**AI / developer tools**: `claude`, `anthropic` (via `claude`), `cursor`, `vercel`, `framer`, `linear.app`, `raycast`, `warp`, `opencode.ai`, `voltagent`, `lovable`, `replicate`, `runwayml`, `elevenlabs`, `cohere`, `minimax`, `mistral.ai`, `together.ai`, `ollama`, `hashicorp`, `supabase`, `mongodb`, `clickhouse`, `posthog`, `sentry`, `expo`, `sanity`, `mintlify`, `resend`, `composio`, `x.ai`, `clay`, `webflow`

**SaaS / productivity**: `notion`, `figma`, `miro`, `airtable`, `cal`, `superhuman`, `intercom`, `zapier`, `ibm`, `shopify`

**Fintech / crypto**: `stripe`, `coinbase`, `binance`, `kraken`, `revolut`, `wise`

**Media / content**: `spotify`, `pinterest`, `airbnb`, `uber`, `theverge`, `wired`

## File layout

```
awesome-design-md/
├── SKILL.md                  ← this file
└── brands/
    ├── apple.md
    ├── linear.app.md
    ├── stripe.md
    ├── …
    └── manifest.json         ← index with URLs and one-line descriptors
```

## Attribution

Files sourced from the `getdesign` npm package v0.6.2 (`npx getdesign@latest`), which is the distribution channel for the VoltAgent awesome-design-md repository. Brand names are trademarks of their respective owners — files document public design patterns for reference purposes.
