---
type: runbook
workspace: "[[Amuse]]"
synced_from: RUNBOOK.md
last_synced: 2026-03-17
---

# Amuse Runbook

> Track workflows discovered during real work and decide whether they stay manual or get promoted into reusable automation.

## Status Legend

- **New** — just identified, not yet tested
- **Testing** — being tried in live work
- **Active** — promoted and running
- **Rejected** — tried, didn't fit
- **Retired** — replaced or no longer needed

## Promotion Ladder

1. Keep manual → 2. CLAUDE.md rule → 3. Slash command → 4. Skill → 5. Hook → 6. Scheduled task → 7. Plugin/MCP/CLI → 8. Agent/subagent

---

## Active Automations

### Session Start — Load Shared Context
- **Status:** Active | **Home:** Skill (`/gws-session-start`)
- **What:** Reads CLAUDE.md + agency-memory.md from AGENCY-OPS, optionally client files from Amuse drive
- **Owner:** @Kam

### Session End — Write Back to Drive
- **Status:** Active | **Home:** Skill (`/session-end`)
- **What:** Updates shared file on Drive (TASKS.md, DECISIONS.md, or client-memory.md), writes handoff note
- **Owner:** @Kam

### Memory Status Check
- **Status:** Active | **Home:** Hook (UserPromptSubmit)
- **What:** Confirms project-memory and claude-mem are reachable
- **Owner:** @Kam

### Privacy Guard
- **Status:** Active | **Home:** Hook (PostToolUse → Write/Edit)
- **What:** Scans for sensitive data (API keys, SSNs, financial data)
- **Owner:** @Kam

### Deliverable Tracker
- **Status:** Active | **Home:** Hook (Stop)
- **What:** Tracks deliverables produced during session
- **Owner:** @Kam

### Session Indexer
- **Status:** Active | **Home:** Hook (Stop)
- **What:** Indexes session to ~/.claude/hooks/index-sessions.log
- **Owner:** @Kam

### Write-Back Check
- **Status:** Active | **Home:** Hook (Stop)
- **What:** Reminds to sync local changes back to Drive before ending a session
- **Owner:** @Kam

### Drive Sync Check
- **Status:** Active | **Home:** Scheduled Task (daily cron)
- **What:** Compares local files against Drive, flags drift
- **Owner:** @Coon

### Session-Start Status Triage
- **Status:** Active | **Home:** Skill (`review` → morning workflow steps 2-3)
- **What:** Cross-references open tasks against email signals per workspace. Avitia uses Outlook MCP; Amuse uses manual confirmation. Updates task files, Tasks.md, and Handoff.md on user confirmation.
- **Owner:** @Kam

---

## Candidates

### New Client Scaffold
- **Status:** New
- **Summary:** Create numbered folder structure + core files on new client Shared Drive
- **Recommended home:** Skill or CLI script
- **Owner:** @Kam

### Meeting Recap → Drive
- **Status:** New
- **Summary:** Pull Granola transcript, extract decisions/action items, update client-memory.md and TASKS.md
- **Recommended home:** Skill (needs human review step)
- **Owner:** @Kam / @Jee

### Automation Classification on Prompt
- **Status:** New
- **Summary:** Check if task matches existing automation before starting manual work
- **Recommended home:** Hook (UserPromptSubmit)
- **Owner:** @Kam

### Write-Back Enforcement
- **Status:** New
- **Summary:** Verify at least one shared file was updated before session ends
- **Recommended home:** Hook (Stop)
- **Owner:** @Kam

---

## Review Schedule

- Weekly: scan candidates, promote what validated cleanly
- Monthly: audit active automations, retire what's unused
