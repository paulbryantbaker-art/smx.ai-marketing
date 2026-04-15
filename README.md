# smbx.ai Marketing Command Center

90-day LinkedIn execution for smbx.ai — the AI deal intelligence platform for M&A. This repo is the single source of truth for marketing strategy, content, brand assets, and execution tracking.

---

## Quick Start

**Start here:** Read [SMBX_90_DAY_EXECUTION_PLAN.md](SMBX_90_DAY_EXECUTION_PLAN.md) — the definitive strategy. Five personas, 13-week calendar across five phases (Seed → Soft Open → Founding Push → Launch → Flywheel), content formula, stats arsenal, operations cadence, and metrics.

**Then:** Read [.impeccable.md](.impeccable.md) for the taste layer that governs every visual asset (three-word brand personality, format DNA, anti-references, design principles).

---

## File Map

| File / Folder | What It Does |
|---|---|
| `SMBX_90_DAY_EXECUTION_PLAN.md` | **The single source of truth.** 90-day plan with five personas, 13-week calendar, content formula, stats arsenal, operations cadence. Supersedes all prior strategy docs. |
| `STYLE_GUIDE.md` | Universal brand and UI style guide — color tokens, typography, logo usage, components, document PDF branding. Reference for any visual asset production. |
| `.impeccable.md` | The taste layer. Three-word brand personality (Veteran. Warm. Precise.), format DNA (institutional research + boutique VC memo), anti-references, design principles. |
| `GEMINI_LINKEDIN_PROFILE_BRIEF.md` | Brief for LinkedIn profile modernization. Paste into a dedicated Gemini chat to generate headline, about, featured section, and experience copy. Do before Week 1. |
| `.agents/product-marketing-context.md` | Product/audience/voice context for marketing skills. Read by every content skill before producing output. |
| `.agents/skills/linkedin-image-post/` | Skill for 1080×1080 single image posts. Flat/document aesthetic, Fibonacci spacing, light/dark modes. |
| `.agents/skills/linkedin-carousel/` | Skill for 1080×1350 multi-slide carousels. Same vocabulary, scaled up, with slide type templates and deck cohesion rules. |
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
