---
type: prd
workspace: "[[Amuse]]"
owner: "@Kam"
status: draft
created: 2026-03-12
---

# AI-COO (Coon) — Product Requirements Document

> Phased roadmap to operationalize Coon as Amuse's AI Chief Operating Officer.

## 1. Overview

**What:** Coon (`canyou@amuse.us`) is Amuse's AI-COO — an autonomous operations agent that monitors workspace health, triages incoming work, onboards new clients, and reports status to the team.

**Mission:** Keep Amuse's operational infrastructure running cleanly so Kam and Jee can focus on strategy and client delivery.

**Scope:** Amuse workspace only. Does not operate in client workspaces (Avitia, Submersive) or external systems beyond Amuse's Slack and Drive.

**Principles:**
- Triage + suggest, never act without human approval on anything irreversible
- Surface problems early, don't wait for someone to ask
- Respect the promotion ladder — earn autonomy through demonstrated reliability

---

## 2. Current State

### What Coon owns today

| Function | Home | Level | Status |
|----------|------|-------|--------|
| Drive Sync Check | Scheduled task (daily cron) | 6 | Active |

### What Coon inherits (framework)

| Asset | Location | Purpose |
|-------|----------|---------|
| Runbook | `Amuse/Runbook.md` | Automation tracking + promotion ladder |
| Handoff | `Amuse/Handoff.md` | Context document prepared for Coon |
| Tasks | `Amuse/Tasks.md` | Task board with @owner tags |
| Decisions | `Amuse/Decisions.md` | Decision log |

### Candidate automations ready for promotion

| Candidate | Current status | Recommended owner |
|-----------|---------------|-------------------|
| New Client Scaffold | New | @Coon |
| Meeting Recap → Drive | New | @Coon (with human review) |
| Automation Classification | New | @Coon |
| Write-Back Enforcement | New | @Coon |

### Promotion Ladder (from Runbook)

```
1. Manual → 2. CLAUDE.md rule → 3. Slash command → 4. Skill
→ 5. Hook → 6. Scheduled task → 7. Plugin/MCP/CLI → 8. Agent/subagent
                                  ↑ Coon is here     ↑ Phase 1    ↑ Phase 2
```

---

## 3. Phased Roadmap

### Phase 1: Level 6 → 7 (Persistent Services)

**Goal:** Coon becomes always-on — a Slack bot that monitors team channels, triages work, and reports ops status.

**Timeline:** 2 weeks to build, 1 week to stabilize

#### 3.1.1 Slack Gateway

**What:** Coon as a Slack bot in the Amuse workspace that monitors channels and responds to DMs.

**Setup requirements:**
- Create Slack workspace for Amuse (or use existing — currently connected workspace is Avitia)
- Create Coon as a Slack bot/app with bot token scopes: `channels:history`, `channels:read`, `chat:write`, `im:history`, `im:read`, `im:write`, `users:read`
- Connect via Slack MCP or direct Bolt/API integration
- Deploy as persistent service (scheduled task polling or Socket Mode for real-time)

**Channels monitored:**

| Channel | What Coon watches for |
|---------|----------------------|
| #ops | Task mentions, deadline references, decision signals, blockers |
| #general | Team coordination, meeting follow-ups, action items |

**DM capabilities (when someone DMs Coon):**

| Command | Response |
|---------|----------|
| "status" | Current task board summary, blockers, upcoming deadlines |
| "sync" | Trigger Drive sync check, report results |
| "tasks" | List active tasks by owner |
| "onboard [client]" | Start client scaffold workflow (Phase 2) |

**Triage logic:**

```
1. Message arrives in monitored channel
2. Classify: actionable? (yes/no)
   - Action items → extract, match to existing task or flag as new
   - Decisions → log to Decisions.md (draft, human approves)
   - Deadlines → check against task board, flag conflicts
   - Blockers → escalate immediately to @Kam or @Jee
3. If actionable:
   - Draft suggested action (task creation, status update, follow-up reminder)
   - Post in thread: "Suggested action: [X]. React ✅ to confirm or 🚫 to skip."
4. If confirmed → execute (create task, update file, send reminder)
5. If skipped → log as declined, learn pattern
```

**Response format:**
- Always reply in thread (never flood the channel)
- Use structured blocks: context → suggestion → action buttons
- Tag relevant @owner

#### 3.1.2 Ops Monitoring (Enhanced)

**What:** Expand beyond Drive sync to full operational health monitoring.

| Check | Frequency | Alert threshold |
|-------|-----------|----------------|
| Drive sync (existing) | Daily | Any file STALE > 24h |
| Hook health | Daily | Any hook failed in last run |
| Scheduled task health | Daily | Any task missed its cron window |
| Session indexing | On session end | QMD index not updated within 5 min |
| Vault integrity | Weekly | Broken wikilinks, orphan files, missing frontmatter |

**Alert routing:**
- Low severity (info) → Daily digest in #ops
- Medium severity (drift/stale) → Immediate Slack message to #ops
- High severity (broken automation) → DM to @Kam

#### 3.1.3 Phase 1 Graduation Criteria

| Criterion | Measure |
|-----------|---------|
| Uptime | Coon runs 7 consecutive days without manual restart |
| Triage accuracy | 80%+ of suggestions accepted (not skipped) over 2 weeks |
| False positive rate | <20% of alerts are noise |
| Response time | Slack triage posted within 5 minutes of trigger message |
| Zero data loss | No accidental overwrites or deletions |

---

### Phase 2: Level 7 → 8 (Autonomous Agent)

**Goal:** Coon graduates from suggesting to acting — handles routine operations autonomously with human override.

**Timeline:** 2 weeks after Phase 1 graduation

#### 3.2.1 Client Onboarding Scaffold

**What:** When Amuse signs a new client, Coon creates the full workspace infrastructure.

**Trigger:** DM to Coon: "onboard [client name]" or task created with tag `#onboard`

**Scaffold template:**

```
Shared drives/Amuse/[Client Name]/
├── 01-strategy/
│   └── proposal.md
├── 02-creative/
├── 03-tech/
├── 04-content/
├── 05-analytics/
├── 06-reporting/
├── TASKS.md
├── DECISIONS.md
├── HANDOFF.md
└── client-memory.md
```

**Vault mirror:**
```
Amuse/Clients/[Client Name].md  — frontmatter client card
```

**Workflow:**
1. Coon creates Drive folder structure from template
2. Coon creates vault client card with frontmatter
3. Coon adds client to Runbook monitoring (drive-sync-check pairs)
4. Coon posts confirmation to #ops: "New client [X] scaffolded. [links]"
5. Human reviews and adjusts

#### 3.2.2 Reporting & Alerts

**Daily Digest** (posted to #ops at 9:00 AM ET):

```
📊 Amuse Daily — March 12, 2026

TASKS
  Active: 2 | Up Next: 4 | Blocked: 2
  Due today: Finalize ROM supplement (@Kam)

OPS
  Drive sync: ✅ All current
  Hooks: ✅ All healthy
  Last session: 2026-03-12 10:39 AM

ATTENTION
  ⚠️ Chris's 4 open variables still unresolved (3 days)
  ⚠️ Founding membership pricing awaiting Corvas (5 days overdue)
```

**Weekly Summary** (posted Fridays at 5:00 PM ET):

```
📋 Amuse Weekly — Week of March 9

COMPLETED: 7 tasks
  - DevOps review (11 issues, 10 resolved)
  - Budget tool built
  - Rate structure confirmed
  ...

CARRIED OVER: 2 tasks
  - ROM supplement (due Mar 14)
  - AI one-pager

DECISIONS MADE: 3
BLOCKERS: 2 (unchanged from last week)

HEALTH: All automations green
```

**Escalation rules:**

| Condition | Action |
|-----------|--------|
| Task overdue > 2 days | DM owner with reminder |
| Blocker unchanged > 5 days | DM @Kam with escalation |
| Client follow-up overdue > 3 days | DM @Kam + @Jee |
| Automation failure | Immediate DM to @Kam |

#### 3.2.3 Autonomy Boundaries

| Action | Coon can do alone | Requires human approval |
|--------|-------------------|------------------------|
| Create tasks from Slack triage | ✅ (after Phase 1 graduation) | — |
| Update task status | ✅ | — |
| Post daily/weekly digest | ✅ | — |
| Create client scaffold | — | ✅ Must confirm before executing |
| Modify TASKS.md on Drive | — | ✅ Draft + approve |
| Modify DECISIONS.md on Drive | — | ✅ Always human-authored |
| Send messages to clients | — | ✅ Never autonomous |
| Delete files | — | ✅ Never autonomous |
| Change permissions/sharing | — | ❌ Prohibited |

#### 3.2.4 Phase 2 Graduation Criteria

| Criterion | Measure |
|-----------|---------|
| Client onboards | 3 successful scaffolds without manual fixes |
| Daily digests | 14 consecutive days posted accurately |
| Weekly summaries | 2 consecutive weeks with zero factual errors |
| Escalation accuracy | 90%+ of escalations were warranted |
| Autonomy discipline | Zero unauthorized actions over 2 weeks |

---

## 4. Technical Architecture

### Infrastructure

### Deployment: Two-Machine Architecture

Coon runs on a **dedicated always-on Mac** (`canyou@amuse.us`). Kam's machine is the authoring environment.

```
┌─── Coon's Mac (always-on) ──────────────────┐
│                                              │
│  ┌──────────┐  ┌──────────┐  ┌───────────┐  │
│  │  Slack   │  │   Ops    │  │ Reporting │  │
│  │ Gateway  │  │ Monitor  │  │  Engine   │  │
│  └────┬─────┘  └────┬─────┘  └─────┬─────┘  │
│       │              │              │        │
│  ┌────┴──────────────┴──────────────┴────┐   │
│  │         Core: Triage + Suggest        │   │
│  └────┬──────────────┬──────────────┬────┘   │
│       │              │              │        │
│  ┌────▼─────┐  ┌─────▼────┐  ┌─────▼────┐   │
│  │  Slack   │  │  Google  │  │ Obsidian │   │
│  │  API/MCP │  │  Drive   │  │  Vault   │   │
│  └──────────┘  └──────────┘  └──────────┘   │
│                                              │
│  Local services:                             │
│  • Claude Code (agent runtime)               │
│  • QMD index (SQLite FTS5 + embeddings)      │
│  • TaskNotes API (localhost:8090)             │
│  • Scheduled tasks (cron)                    │
│  • Google Drive mount                        │
│                                              │
└──────────────────────────────────────────────┘
         ▲                    ▲
         │ Slack messages     │ Drive sync
         │ Triage suggestions │ File updates
         ▼                    ▼
┌─── Kam's Mac (authoring) ───────────────────┐
│  • Strategy, decisions, client work          │
│  • Reviews/approves Coon's suggestions       │
│  • Obsidian vault (same Drive-synced copy)   │
│  • Claude Code (interactive sessions)        │
└──────────────────────────────────────────────┘
```

### What runs on Coon's Mac

| Component | Implementation | Why on Coon's machine |
|-----------|---------------|----------------------|
| Slack bot | Slack Bolt app or MCP Slack connector | Always-on, persistent polling/Socket Mode |
| Triage engine | Claude Code scheduled task or agent | Needs continuous channel monitoring |
| Ops monitor | Scheduled tasks (cron) | Needs local Drive mount for file comparison |
| Reporting | Scheduled tasks (cron) | Daily 9 AM, weekly Fridays 5 PM — must run unattended |
| QMD search | Local SQLite + FTS5 | Local processing, no external API dependency |
| Session extraction | Python scripts | Reads JSONL logs, writes to vault |
| Task management | TaskNotes API (`localhost:8090`) | Local Obsidian plugin |
| Drive access | Google Drive filesystem mount (`~/Library/CloudStorage/GoogleDrive-canyou@amuse.us/`) | Direct file access for sync checks and scaffold |
| Vault | Obsidian vault (synced) | Source of truth for Coon's reads/writes |

### What stays on Kam's Mac

| Component | Purpose |
|-----------|---------|
| Obsidian vault | Authoring — strategy docs, decisions, client work |
| Claude Code | Interactive sessions — Kam's work |
| Slack (human) | Reviews Coon's triage suggestions, approves actions |

### Slack Workspace

Coon operates in the **Amuse Slack workspace**. The MCP Slack connector on Coon's machine must connect to the Amuse workspace.

**Setup:**
1. Create Amuse Slack workspace (if not already existing)
2. Create Coon as a Slack bot app in the Amuse workspace
3. Connect Slack MCP on Coon's Mac to Amuse workspace
4. Create channels: `#ops`, `#general`
5. Invite Kam and Jee to the Amuse workspace

---

## 5. Permissions & Boundaries

### Read Access (always allowed)

- All Amuse vault files
- All Amuse Drive files
- Slack channel history (team channels only)
- Task board via API
- Session logs and QMD index

### Write Access (with constraints)

| Target | Constraint |
|--------|-----------|
| Slack messages | Only in #ops, #general, and DMs |
| Task creation | Allowed after Phase 1 graduation |
| Task status updates | Allowed after Phase 1 graduation |
| Drive files | Draft only — human approves before commit |
| Vault files | Only `Amuse/Tasks.md` updates and daily notes |

### Prohibited (never)

- Client-facing communications
- Financial data entry
- Permission/sharing changes
- File deletion
- Cross-workspace operations
- Direct responses to clients (Chris, Corvas, etc.)

### Escalation Chain

```
Coon → @Kam (default) → @Jee (if Kam unavailable > 4 hours)
```

---

## 6. QC Checklist

### Phase 1 Acceptance Tests

| # | Test | Pass criteria |
|---|------|---------------|
| 1.1 | Slack bot responds to DM "status" | Returns current task summary within 30s |
| 1.2 | Channel monitoring detects action item | Triage posted in thread within 5 min |
| 1.3 | Drive sync alert fires | Stale file detected and reported to #ops |
| 1.4 | Hook health check | All hooks verified, failures reported |
| 1.5 | Triage accuracy | Test with 10 sample messages, 8+ correctly classified |
| 1.6 | No false actions | Bot suggests only, never executes without ✅ |
| 1.7 | 7-day stability | No crashes, missed polls, or silent failures |

### Phase 2 Acceptance Tests

| # | Test | Pass criteria |
|---|------|---------------|
| 2.1 | Client scaffold | Trigger "onboard TestClient" → correct folder + files created |
| 2.2 | Daily digest | Posted at 9 AM ET, all sections accurate |
| 2.3 | Weekly summary | Posted Friday 5 PM, completed/carried tasks correct |
| 2.4 | Escalation | Overdue task triggers DM to correct owner |
| 2.5 | Autonomy boundary | Attempt prohibited action → blocked and logged |
| 2.6 | 3 client onboards | Scaffold 3 test clients, all clean |
| 2.7 | 14-day reporting | No missed digests, no factual errors |

### Rollback Plan

| Scenario | Action |
|----------|--------|
| Slack bot posts incorrect triage | Disable bot, revert to manual monitoring |
| Drive file corruption | Restore from Drive version history |
| Task duplication | Deduplicate via TaskNotes API, add guard |
| Runaway alerts | Kill scheduled task, investigate threshold tuning |
| Phase 2 autonomy failure | Demote to Phase 1 (suggest-only), investigate |

---

## 7. Implementation Order

| Step | What | Runs on | Depends on | Est. effort |
|------|------|---------|------------|-------------|
| 0 | Provision Coon's Mac — Claude Code, QMD, Obsidian, Drive mount, TaskNotes | Coon's Mac | Machine access | 2 hours |
| 1 | Set up Amuse Slack workspace + #ops and #general channels | Slack (web) | Slack admin | 30 min |
| 2 | Create Coon Slack bot app + connect Slack MCP on Coon's Mac | Coon's Mac | Slack workspace | 1 hour |
| 3 | Build triage engine (scheduled task) | Coon's Mac | Bot token | 1 day |
| 4 | Expand ops monitoring checks | Coon's Mac | Drive mount | 2 hours |
| 5 | Build DM command handler | Coon's Mac | Bot + triage | 4 hours |
| 6 | Daily digest scheduled task | Coon's Mac | Ops monitor + task API | 4 hours |
| 7 | Phase 1 QC testing | Both | Steps 1-6 | 2 days |
| 8 | Phase 1 stabilization (7-day run) | Coon's Mac | QC pass | 7 days |
| 9 | Client scaffold skill | Coon's Mac | Phase 1 graduated | 4 hours |
| 10 | Weekly summary | Coon's Mac | Daily digest working | 2 hours |
| 11 | Escalation rules | Coon's Mac | Reporting + task board | 2 hours |
| 12 | Phase 2 QC testing | Both | Steps 9-11 | 2 days |
| 13 | Phase 2 stabilization (14-day run) | Coon's Mac | QC pass | 14 days |

---

*Prepared by @Kam — 2026-03-12 | Status: Draft — pending team review*
