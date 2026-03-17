---
type: handoff
workspace: "[[Amuse]]"
synced_from: HANDOFF.md
last_synced: 2026-03-17
prepared_for: "COO, Amuse Marketing (canyou@amuse.us)"
prepared_by: "@Kam, @Jee"
---

# Submersive x Amuse — Project Handoff

**Status:** Active client engagement — ROM delivered, call with Corvas completed. Tech sprint unblocked. (Updated 2026-03-17)

## What This Is

Amuse's first major client engagement of 2026. [[Submersive]] is a premium immersive bathhouse opening at 901 Barton Springs, Austin TX in early 2027. We've been engaged to lead the full go-to-market — from waitlist infrastructure through founding membership presale through grand opening.

## Reading Order

| # | File | What It Gives You | Time |
|---|------|-------------------|------|
| 1 | `CLAUDE.md` | People, terms, project index | 5 min |
| 2 | `TASKS.md` | What's active, blocked, and done | 3 min |
| 3 | `DATA_ARCHITECTURE.md` | How the info system is organized | 10 min |
| 4 | `memory/projects/submersive.md` | Full project KB | 10 min |

## The Situation

[[Submersive]] is a novel category — part thermal bathhouse, part immersive art experience, part neuroaesthetic wellness destination. The founder is Corvas Brinkerhoff (co-founded Meow Wolf). The COO is Chris Mora. The venue is a 25,000 sq ft buildout in Austin; soft open is March 2027.

Amuse delivered our proposal on March 4. **Option A (Integrated Launch Partner) was confirmed March 6** — all six scoping call decisions resolved. What remains is formalizing the budget numbers into a ROM supplement for Chris by EOW March 14.

The GTM Spine: **BUILD → SEED → SELL → OPEN → AMPLIFY**. We are in BUILD. Waitlist launches March 30. Presale starts May 2026 with a 3-drop graduated discount model (May → July → Sept), targeting $1.725M in pre-opening revenue. Tech sprint confirmed but paused pending ROM delivery.

## Key People

| Who | Role | Contact |
|-----|------|---------|
| @Jee | Amuse strategy lead | jee@amuse.us |
| @Kam | Amuse tech + BD | k@amuse.us |
| Chris Mora | [[Submersive]] COO — primary contact | chris@submersive.com |
| Corvas Brinkerhoff | [[Submersive]] Founder/CEO | corvas@submersive.com |
| Eoghan / Nikolai | [[Submersive]] designers | |
| Didi | Former Meow Wolf CMO — PR advisor | |
| Fever | GA marketing partner — separate from our scope | |

## Business Model

**Pre-Opening Revenue — 3-Drop Presale Model (confirmed March 12):**

| Drop | Timing | Price | Deposit | Cap | Revenue |
|------|--------|-------|---------|-----|---------|
| Drop 1 | May 2026 | $299/yr | $100 | 1,000 | $77K |
| Drop 2 | July 2026 | $349/yr | $125 | 1,000 | $95K |
| Drop 3 | Sept 2026 | $399/yr | $150 | 1,000 | $140K |
| Q1 2027 Pre-sale | Q1 2027 | $449/yr | — | 500 new | $781K |
| Soft Launch | Q1 2027 | $88/day | — | 141/day × 20d | $187K |
| Grand Opening | Q1 2027 | $120/day | — | 707/day × 7d | $445K |
| **Total** | | | | | **$1.725M** |

Full price post-launch: $499/yr. 10-year membership model projects $1.4M–$3.5M annual revenue at base case (5% penetration, 55% retention).

**Unit Economics:**
- Break-even: 11% capacity (27K guests, $3.9M revenue)
- Conservative case: 45% capacity → $13.7M, 56% EBITDA
- Target CAC: $11 | Marketing budget: $550K

## Tech Stack (Kam's Sprint: March 9-23)

| Tool | Purpose |
|------|---------|
| Webflow | Landing page + waitlist capture |
| Klaviyo | CRM + email automation |
| Beehiiv | Waitlist newsletter |
| Stripe + Memberful | Founding membership purchases |
| GA4 + Segment | Analytics + attribution |
| Geneva | Founding member community |
| Tock | Pre-opening ticketing |

## What's Resolved (Scoping Call March 5-6)

1. Engagement structure — Option A confirmed
2. Membership tiers + pricing — confirmed by Corvas
3. Visual brand system access — resolved
4. Meow Wolf positioning — resolved
5. March 30 waitlist date — confirmed
6. Presale date — May 2026 Drop 1 confirmed (3-drop graduated model)

## What's Open

Four variables need Chris's answers before the ROM is final:

1. **Tech in-house post-BUILD?** — Does Submersive bring tech ops in-house?
2. **Content volume in SELL?** — Frequency and channel mix target
3. **Ad spend budget?** — Monthly paid media range
4. **Budget ceiling?** — Hard cap to design around?

Additionally:

5. **Ticketing / reservation platform** — Chris wants Amuse input. Fever is preparing a proposal; other options available (Tock, etc.). Needs evaluation before presale infrastructure decisions.

## DevOps Review (March 12, 2026)

Full infrastructure audit — 11 issues identified, 10 resolved. Interactive dashboard on Drive.

- Added: write-back-check hook (Stop), drive-sync-check scheduled task (daily cron)
- Removed: context-selector hook (redundant)
- Dashboard: `Shared drives/Amuse/06-reporting/devops-review/devops-review-2026-03-10.html`
- Git: Switched from KamKamBaham to Kam-amuse account. HTTPS works via `gh` credential helper.

## Completed Actions (March 12–17)

- [x] Finalize ROM supplement — @Kam — sent
- [x] Get Chris's answers on 4 open variables — @Kam — answered 2026-03-12
- [x] Draft AI one-pager — @Kam — sent
- [x] Respond to Chris re: presale targets + ticketing platform experience — @Kam — sent
- [x] Send finalized package to Chris (ROM + AI one-pager + call ask) — @Kam — sent
- [x] Schedule call with Chris + Corvas — @Kam — completed

## Current Next Actions

- [ ] Review ticketing/reservation platform options (Fever proposal + alternatives) — @Kam
- [ ] Resume tech sprint: Webflow LP, Klaviyo CRM, GA4+Segment, Beehiiv — @Kam
