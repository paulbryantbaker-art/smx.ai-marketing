# smbx.ai Marketing Command Center

90-day LinkedIn execution for smbx.ai — the AI deal intelligence platform for M&A. This repo is the single source of truth for marketing strategy, content, brand assets, and execution tracking.

---

## Quick Start

**Start here:** Open [SMBX_90_DAY_PLAN.xlsx](SMBX_90_DAY_PLAN.xlsx) — the definitive strategy. Five personas, 13-week calendar across five phases (Seed → Soft Open → Founding Push → Launch → Flywheel), content formula, stats arsenal, operations cadence, and metrics.

**Then:** Read [DESIGN_HANDOFF.md](DESIGN_HANDOFF.md) and [DESIGN_LANGUAGE.md](DESIGN_LANGUAGE.md) for the visual system every carousel and single-image post must match.

---

## File Map

| File / Folder | What It Does |
|---|---|
| `SMBX_90_DAY_PLAN.xlsx` | **The single source of truth.** 90-day plan with five personas, 13-week calendar, content formula, stats arsenal, operations cadence. Paul's working surface — edit here, not in markdown. |
| `DESIGN_HANDOFF.md` | Short orientation on the 2026-04-15 visual system. Key deltas from the deprecated cream/rose-gold doc. Read before DESIGN_LANGUAGE.md. |
| `DESIGN_LANGUAGE.md` | Full authoritative visual system — palette, type, spacing, motion, editorial primitives, anti-slop rules, and § 9 "Translating to LinkedIn documents" as the direct output spec. |
| `STYLE_GUIDE.md` | Brand voice and copy patterns. Unchanged from 2026-04-04. Authoritative for logo asset rules. |
| `.impeccable.md` | The taste layer. Three-word brand personality (Veteran. Warm. Precise.), format DNA (institutional research + boutique VC memo), anti-references, design principles. |
| `.agents/product-marketing-context.md` | Product/audience/voice context for marketing skills. Read by every content skill before producing output. |
| `.agents/skills/linkedin-image-post/` | Skill for 1080×1350 single-image Field Note posts. |
| `.agents/skills/linkedin-carousel/` | Skill for 1080×1350 multi-slide carousels. Locked to the 2026-04-15 canon (Field Note masthead, two-variant eyebrows, Sora 800 + Inter, Fibonacci spacing, light-dominant rhythm with dark cinematic anchor). |
| `assets/logos/` | Active logo assets: `G3L.png` (light wordmark), `G3D.png` (dark wordmark), `X.png` (icon mark), `LI BG.png` (LinkedIn banner background). |
| `assets/portrait-square.jpeg` | Paul's pre-cropped square headshot. Used in masthead/footer of every asset. |
| `content/week-01/` through `content/week-13/` | Weekly content production folders. Python render scripts + PDF/PNG outputs per post. |
| `tracking/content-tracker.md` | Per-post tracking: status, impressions, comments, DMs, Yulia conversations started (the north star metric). |

---

## Three Rules That Govern Everything

1. **Identity, not information.** Content that educates gets scrolled past. Content that mirrors back the persona's deepest unspoken fear makes them stop.
2. **The post gives 80%. Yulia gives 100%.** Every post deliberately leaves the HOW unresolved. The open loop is the conversion mechanism.
3. **Be the content LinkedIn wants to serve.** Algorithm rewards dwell time, comment depth, and "see more" clicks. Emotional resonance on-platform → specific usefulness off-platform.

## North Star Metric

**Yulia conversations started per post.** Not impressions. Not likes. Not profile views. Someone left LinkedIn, typed into Yulia's chat, and got real analysis.

## Branded Terms

Three open-loop terms used across every phase:

- **The Baseline™** — Relief + validation. What the business actually earns. (Reluctant Seller)
- **Blind Equity™** — Urgency + discovery. Hidden add-backs in the books. (Future Seller)
- **The Rundown™** — Confidence + speed. 7-dimension deal intelligence. (Buyer / Searcher)

## The Five Personas

1. **The Reluctant Seller** — 50–65, service business, 1–3 years of thinking about selling, has done nothing
2. **The Future Seller** — Same demos, 2–5 years from exit, paralyzed by complexity
3. **The First-Time Buyer** — 28–45, leaving corporate, terrified of a $1.5M personal guarantee
4. **The Search Fund Operator** — Has capital, active search, investors getting impatient
5. **The Broker** — 5–15 deals/year, sub-$10M, tech stack held together with duct tape

---

## Creative Tools

| Tool | Cost | Purpose |
|---|---|---|
| Playwright (Python) | Free | Production render pipeline for all visual assets (single posts + carousels) at 2× DPR |
| HeyGen Creator | $29/mo | AI avatar videos (Paul's digital twin + voice clone) |
| Canva | $0–13/mo | Backup/exploration for non-pipeline assets |
| Buffer | Free | Post scheduling |

---

## Key References

- **Founder:** Paul Baker — 20+ year M&A veteran, practitioner-turned-builder
- **AI:** Yulia — the AI deal analyst (not a chatbot, not an advisor)
- **Strategy:** Group-first LinkedIn (240K+ member groups), building from ~300 to 1,000+ connections over 90 days
- **Voice:** Direct, specific, human. Never corporate. Brokers are customers, not competitors.
