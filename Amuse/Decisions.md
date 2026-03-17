---
type: decisions
workspace: "[[Amuse]]"
synced_from: DECISIONS.md
last_synced: 2026-03-12
---

# Amuse Decisions

> Synced from workspace `DECISIONS.md`. Newest first.

---

### 2026-03-12 — Revenue Model Received: 3-Drop Presale + 10-Year Membership Projections

- **Decision:** Received and incorporated Chris's updated revenue model into all workspace files. Key changes from original assumptions:
  - Old: 2-tier Founding Membership ($399/$1,499), $349K presale target, mid-April launch
  - New: 3-drop graduated presale ($299→$349→$399→$449), $1.725M pre-opening revenue target, May 2026 first drop
  - 10-year membership model added (base case: 5% penetration, 55% retention, $1.4M→$3.5M annual)
- **Rationale:** Revenue model fundamentally changes presale infrastructure scope, timeline, and budget assumptions. ROM supplement must reflect these numbers.
- **Decided by:** Chris Mora (shared model), @Kam (incorporated)
- **Follow-up:** Ticketing/reservation platform evaluation added as new workstream (Fever preparing proposal). Respond to Chris with ROM + platform input.
- **Reference:** `[EXT] Member Revenue Model (updated 3.2.26 w pre sale forecast).xlsx`

---

### 2026-03-12 — DevOps Review: Hook Cleanup and Automation Changes

- **Decision:** Removed `context-selector` hook (UserPromptSubmit). Added `write-back-check` hook (Stop event). Created `drive-sync-check` scheduled task (daily cron).
- **Rationale:** context-selector was redundant — hooks can't read prompt text, and workspace rules are already loaded via `.claude.md`. Write-back hook enforces Drive-as-source-of-truth. Scheduled sync catches drift.
- **Decided by:** @Kam
- **Follow-up:** Monitor write-back hook for false positives. Legacy `.gdoc` on AGENCY-OPS is cosmetic.
- **Reference:** `devops-review-2026-03-10.html`, `Shared drives/Amuse/06-reporting/devops-review/`

---

### 2026-03-10 — Rate Structure Confirmed for [[Submersive]] Engagement

- **Decision:** Confirmed Amuse billing model:
  - **Jee base:** $5K/month = marketing strategy + execution plan with 3 launched tasks/week
  - **Kam standard rate:** $500/hr | Startup rate: $250/hr | Monthly minimum: $5K/20hrs retainer
  - **Ad management:** Separate line item. 15-20% of monthly ad spend, floor ~$1K/mo
  - **Deal structure:** Amuse works within client budget. Delta bridged by equity or rev-share.
- **Decided by:** @Kam
- **Follow-up:** Plug into budget tool, finalize ROM, include in Chris reply by EOW

---

### 2026-03-10 — Option A vs B Reframed

- **Decision:** Option A (Integrated Launch Partner) confirmed March 6. ROM supplement is the deliverable, not a re-pitch. Option B stays as reference.
- **Decided by:** @Kam

---

### 2026-03-10 — Option A: Kam Role Clarified

- **Decision:** In Option A, Kam builds AI infrastructure FOR [[Submersive]] (client-owned asset). In Option B, AI stays agency-internal.
- **Rationale:** Option A = Submersive gets an asset; Option B = Submersive gets the output.
- **Decided by:** @Kam

---

### 2026-03-06 — Option A Retainer Confirmed

- **Decision:** [[Submersive]] confirmed Option A (Integrated Launch Partner — monthly retainer through grand opening). All six scoping call decisions resolved.
- **Decided by:** Chris Mora + Corvas Brinkerhoff
- **Follow-up:** Begin tech sprint March 9. ROM supplement pending.

---

### 2026-03-04 — Founding Membership Tiers + Pricing Confirmed

- **Decision:** Founding Member: 500 spots, $399/yr or $699/2yr. Founding Circle: 100 spots (nomination-only), $1,499/yr or $3,500 lifetime.
- **Decided by:** Corvas Brinkerhoff
