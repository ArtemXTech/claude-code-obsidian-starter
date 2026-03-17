---
type: decisions
workspace: "[[Avitia]]"
last_updated: 2026-03-12
---

# Avitia Decisions

> Key architectural and strategy decisions. Newest first.

---

### 2026-03-12 — Claude Chat-First (Not Code) for BD Team

- **Decision:** Infrastructure audit reframed from Claude Code to Claude Chat. BD team will use Claude Projects with custom instructions and uploaded source docs, plus MCP connectors for live platform queries. No slash commands, no terminal.
- **Rationale:** BD team doesn't have access to Claude Code. Chat with Projects provides the same structured context loading pattern in a browser-native interface.
- **Decided by:** @Kam
- **Follow-up:** Configure MCP connectors (Atlassian + M365) for BD accounts. Set up 6 recommended Claude Projects.
- **Reference:** `deliverables/claude-first-audit.html`, project-memory note #32

---

### 2026-03-12 — 6 Claude Projects Recommended for BD Team

- **Decision:** Six domain-specific Claude Projects recommended: Thailand Partnership, MENA Expansion, Medteq Grant, ICHIP Portal, Competitive Intelligence, BD Weekly Sync.
- **Rationale:** Each Project gets preloaded with relevant source docs and custom instructions, replacing the /recall pattern from Code. Keeps context focused and token-efficient.
- **Decided by:** @Kam
- **Reference:** Section 6 of `deliverables/claude-first-audit.html`

---

### 2026-03-12 — Unified Tag Taxonomy Adopted

- **Decision:** Standardized tag taxonomy across all platforms: 9 domain tags (liquid-biopsy, ctDNA, find-it, etc.), 6 region tags (thailand, mena, quebec, china, etc.), 9 content type tags (deliverable, competitor, grant, etc.).
- **Rationale:** Consistent tagging enables cross-platform search and project-memory filtering. Currently advisory; enforcement planned for Phase 2.
- **Decided by:** @Kam
- **Reference:** `bd-team-claude.md` standard tags section, audit Section 6

---

### 2026-03-12 — Platform Routing Confirmed

- **Decision:** Three-platform routing: Confluence for narrative/context (meeting notes, partnership docs), SharePoint for files/deliverables (decks, grants, contracts), Jira for tasks/tracking (by project key: BD, RD, CS, MKT, SW, SUP).
- **Rationale:** Each platform has a natural strength. Cross-referencing via MCP connectors eliminates the need to duplicate content.
- **Decided by:** @Kam
- **Reference:** `AVITIA_CLAUDE_WORKSPACE_MASTER.md`, audit Section 1

---

### 2026-03-04 — ICHIP Portal Ontology: Four-Layer Architecture

- **Decision:** Portal documentation structured as 4-layer ontology: Entity Registry (nouns), Feature Taxonomy (capabilities), Workflow Catalog (processes), Relationship Graph (connections).
- **Rationale:** Supports portal redesign by providing a complete domain model that can be referenced across UX, engineering, and QC workstreams.
- **Decided by:** @Kam
- **Reference:** `documents/ichip-portal-ontology.md`, project-memory notes #119-125
