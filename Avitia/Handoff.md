---
type: handoff
workspace: "[[Avitia]]"
last_updated: 2026-03-12
prepared_for: "BD Team, Ruth (R&D), Mauricio (Software)"
prepared_by: "@Kam"
---

# Avitia — Project Handoff

**Status:** Infrastructure audit complete — now executing gap remediation (MCP connectors, CS Jira, tag enforcement)

## What This Is

Avitia is a molecular diagnostics company focused on liquid biopsy (ctDNA) cancer detection. Kam serves as Acting CSO, leading BD strategy, AI infrastructure, and go-to-market coordination. The workspace covers business development across 4 regions (Thailand, MENA, Quebec, China/Burning Rock), R&D grant work (Medteq), software (ICHIP portal), and cross-functional operations.

## Reading Order

| # | File | What It Gives You | Time |
|---|------|-------------------|------|
| 1 | `.claude.md` | Entity definitions, brand architecture, hard constraints, context selection | 5 min |
| 2 | `bd-team-claude.md` | Platform map, search patterns, reference database, tags, output conventions | 5 min |
| 3 | `AVITIA_CLAUDE_WORKSPACE_MASTER.md` | Full workspace reference (10 parts) — teams, platforms, workflows, implementation tracking | 15 min |
| 4 | `deliverables/claude-first-audit.html` | Infrastructure audit — test results, gaps, roadmap, project setup guide | 10 min |

## The Situation

The Claude-first infrastructure audit was completed March 12, 2026. It tested 11 MCP integrations against live Atlassian and Microsoft 365 platforms (10 pass, 1 amber), identified 8 gaps with owners, and produced a 3-phase roadmap for full team adoption.

The audit was reframed from Claude Code to Claude Chat — BD team will use Claude Projects with custom instructions and MCP connectors, not slash commands or terminal tools.

## Key People

| Who | Role | Focus |
|-----|------|-------|
| Kam | Acting CSO | BD, strategy, AI infrastructure |
| Ruth | R&D Lead | Clinical validation, Medteq grant, lab ops |
| Mauricio | Software Lead | ICHIP portal, integrations |
| Anna | CEO | Executive oversight |
| Dmitri | IT / Ops | SharePoint, infrastructure |

## What's Resolved (Audit Results)

1. **Atlassian + M365 MCP connectivity** — 10/11 tests pass, CQL and JQL patterns confirmed
2. **Platform routing** — Confluence (narrative), SharePoint (files), Jira (tasks)
3. **Tag taxonomy** — 24 standard tags across domain, region, content type
4. **BD search patterns** — JQL and CQL shortcuts documented and tested
5. **Input template structure** — 10 templates across BD, R&D, Software
6. **Claude Projects setup** — 6 recommended Projects with context upload specs

## What's Open (8 Gaps)

| # | Gap | Owner | Priority |
|---|-----|-------|----------|
| 1 | CS Jira project doesn't exist | Kam | High — blocks chatbot routing |
| 2 | RD project lacks Epic issue type | Ruth | Medium |
| 3 | Ancestor ID 70844417 returns 404 on direct GET | — | Amber — CQL workaround works |
| 4 | No unified search layer | Kam | Medium |
| 5 | reflib at Phase 1 (10 papers) | Kam | Medium |
| 6 | Tag taxonomy not enforced | Kam | Medium |
| 7 | No R&D or Software input templates | Kam + Ruth + Mauricio | Medium |
| 8 | MCP connectors not configured for BD Chat | Kam | High — blocks self-service |

## Immediate Next Actions

- [ ] Configure MCP connectors for BD team Claude accounts — @Kam
- [ ] Create CS Jira project — @Kam
- [ ] Set up 6 Claude Projects (Thailand, MENA, Medteq, ICHIP, Competitive, BD Weekly) — @Kam
- [ ] Add Epic issue type to RD project — @Ruth
- [ ] Begin tag taxonomy enforcement — @Kam
- [ ] Build R&D and Software input templates — @Kam + @Ruth + @Mauricio
