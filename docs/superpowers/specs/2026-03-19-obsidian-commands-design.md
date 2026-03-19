# Obsidian Custom Commands — Design Spec

**Date:** 2026-03-19
**Author:** Kam
**Status:** Approved (Rev 2.1)

---

## Overview

Three-layer system that captures data from email, Slack (single-workspace, extensible), calendar, and meetings into the Obsidian vault, then provides two commands on top: intelligent daily triage and emergent idea synthesis.

**Build order:** Layer 1 (Ingest) → Layer 2 (Daily Ops) → Layer 3 (Think)

## Constraints

- Read-only ingestion — no auto-responding, no Slack posting, no Jira auto-updates
- Data routes into existing workspace folders (Amuse/, Avitia/), not a separate silo
- Injoy Slack workspace is out of scope for now
- Avitia uses Read.ai meeting digests via email; Amuse uses Granola local sync
- All skills are Claude Code skills (natural language triggers), not Obsidian plugins
- Slack MCP is connected to one workspace at a time (currently Avitia/avitiabio)

## Migration: Existing `inbox` Skill

The existing `inbox` skill (`.claude/skills/inbox/`) handles Avitia-only email scanning with its own schema. The new `ingest` skill **supersedes** it.

### What changes:

| Aspect | Old (`inbox`) | New (`ingest`) |
|--------|--------------|----------------|
| Scope | Avitia email only | Email + Slack + Calendar, multi-workspace |
| File naming | `{category}-{description}-{YYYY-MM-DD}-kam.md` | `{source}-{YYYY-MM-DD}-{short-slug}.md` |
| Category field | `category: task \| decision \| blocker \| fyi` | `category: task \| decision \| blocker \| fyi \| meeting` (same field name, +meeting) |
| Note type | (none) | `type: inbox-item` (note-level classification) |
| Status values | `status: raw \| actioned \| dismissed` | `status: new \| triaged \| acted-on` |
| Dedup key | `source_id: outlook:{messageId}` | `source_id: {source}:{id}` (same pattern, extended) |
| Task link | `linked_task: path` | `linked_task: path` (preserved) |

### Migration steps:

1. Existing files in `Avitia/Inbox/` keep their current schema — no bulk rewrite
2. New `ingest` skill reads both old and new schemas during dedup (checks both `source_id` and `hash`)
3. Old `inbox` skill folder is renamed to `inbox-deprecated/` after `ingest` is verified working
4. Morning routine workflow updated to call `ingest` instead of `inbox` at step 2b-ext

---

## Layer 1: Ingestion Pipeline

### New Skill: `ingest`

**Trigger phrases:** "ingest", "pull updates", "sync sources"

**Purpose:** Pull data from all connected sources into workspace Inbox/ folders as structured markdown notes.

### Sources and Methods

| Source | Method | Destination | Phase | Notes |
|--------|--------|-------------|-------|-------|
| Outlook email | M365 MCP `outlook_email_search` | `{workspace}/Inbox/` | 1a | Sender domain + keyword routing |
| Slack (Avitia) | Slack MCP `slack_read_channel` | `Avitia/Inbox/` | 1a | avitiabio — currently connected |
| Calendar | M365 MCP `outlook_calendar_search` | `{workspace}/Inbox/` | 1a | Attendee email routing |
| Read.ai digests | M365 MCP (email) | `Avitia/Inbox/` | 1b | Requires format analysis first |
| Slack (Amuse) | Slack MCP `slack_read_channel` | `Amuse/Inbox/` | Future | Requires workspace switch or second connection |

### Slack MCP: Single-Workspace Design

The Slack MCP connector authenticates to one workspace. The skill **detects which workspace** it's connected to by calling `slack_search_channels` and matching known channel names against the config.

- **Current state:** Connected to avitiabio. Ingest runs Slack for Avitia only.
- **Amuse Slack:** Marked as `# FUTURE — requires second Slack MCP connection or manual workspace switch`. Not included in Phase 1.
- **Per-run behavior:** Skill reports which Slack workspace was ingested and which was skipped.

### Workspace Routing Rules

Configurable in skill workflow (markdown with YAML code blocks, consistent with skill ecosystem):

```yaml
routing:
  slack:
    avitiabio: Avitia
    # amuse: Amuse  # FUTURE — requires second Slack MCP connection
  email:
    domain_map:
      "@avitia.bio": Avitia
      "@avitiabio.com": Avitia
      "@submersive.com": Amuse
      "@amuse.us": Amuse
    sender_map:
      "notifications@read.ai": Avitia  # Read.ai digests — Phase 1b
    keyword_fallback:
      - pattern: "ICHIP|liquid biopsy|ctDNA|BD-\\d+"
        workspace: Avitia
      - pattern: "Submersive|bathhouse|waitlist|Webflow"
        workspace: Amuse
  calendar:
    # Route by attendee email domain/address overlap
    team_map:
      Avitia:
        - "@avitia.bio"
        - "@avitiabio.com"
        - "ruth"       # fallback partial match on display name
        - "mauricio"
        - "anna"
        - "dmitri"
      Amuse:
        - "@submersive.com"
        - "@amuse.us"
        - "jee"
        - "chris"
        - "corvas"
    # When attendees span both workspaces: route to BOTH workspace Inboxes
    cross_workspace: duplicate
  fallback: Inbox/  # vault-root for ambiguous items
```

### Inbox Item Schema

Each ingested item creates one `.md` file:

**Filename:** `{source}-{YYYY-MM-DD}-{short-slug}.md`
Example: `slack-2026-03-19-bizdev-burning-rock-update.md`

**Frontmatter:**

```yaml
---
type: inbox-item                    # note-level classification (consistent across vault)
source: slack | email | calendar | meeting
workspace: Amuse | Avitia
channel: "#bizdev"                  # slack only
from: "Ruth Miller"
date: 2026-03-19
category: task | decision | blocker | fyi | meeting  # action classification
status: new | triaged | acted-on
source_id: "slack:C0AFNCK4HJ9:1710864000"  # dedup key: source:channel/thread:timestamp
linked_task: ""                     # path to TaskNotes file, set during triage
related: []                         # wikilinks added during triage
---
```

**Body:** Brief summary. Key quotes or details. For Read.ai digests: extracted action items, key topics, attendees.

### Deduplication

Uses `source_id` field (same pattern as existing inbox skill, extended to all sources):

| Source | source_id format |
|--------|-----------------|
| Email | `outlook:{messageId}` |
| Slack | `slack:{channelId}:{threadTs}` |
| Calendar | `calendar:{eventId}` |

Before writing, grep target Inbox/ for matching `source_id`. Skip if found. Also checks old-format `source_id` from existing inbox items for backward compatibility.

### Slack Channel Selection

Not all channels are worth ingesting. Config specifies which channels per workspace:

```yaml
slack:
  avitiabio:
    channels:
      - "#bizdev"
      - "#product-development"
      - "#software"
      - "#branding-marketing"
      - "#portal-redevelopment"
      - "#br-validation-team"
      - "#marketing"
    exclude:
      - "#random"
      - "#general"
      - "#careers"
  # amuse:
  #   channels: []  # FUTURE — TBD when connected
```

### Ingestion Scope

Each run pulls data since last successful run (tracked in `ingest/state.json`):

```json
{
  "last_run": "2026-03-19T12:00:00Z",
  "sources": {
    "slack_avitiabio": "2026-03-19T12:00:00Z",
    "email": "2026-03-19T12:00:00Z",
    "calendar": "2026-03-19T12:00:00Z"
  }
}
```

**First run:** Pulls last 48 hours with a cap of 5 items per source/channel. Produces a summary of what was found vs. what was captured, so the user can adjust channel selection before the next full run.

### Read.ai Ingestion (Phase 1b)

Read.ai meeting digests arrive as emails. Before implementing the parser:

1. Examine 2-3 actual Read.ai digest emails via `outlook_email_search` + `read_resource`
2. Document the email structure (HTML vs. plain text, where action items live, attendee format)
3. Build parser based on observed structure

Deferred to Phase 1b to avoid blocking core ingestion on format assumptions.

### Graceful Degradation

| Source | If unavailable | Behavior |
|--------|---------------|----------|
| M365 MCP | Unreachable | Skip email + calendar, report: "M365 unreachable — email/calendar skipped" |
| Slack MCP | Unreachable | Skip Slack, report: "Slack unreachable — skipped" |
| TaskNotes API | Port 8090 down | Skip task creation, write inbox file only |
| Granola | No new meetings | Silent — existing sync handles this |

---

## Layer 2: Daily Ops (Intelligent Triage)

### New Skill: `daily-ops`

**Trigger phrases:** "daily ops", "what's going on", "briefing", "triage my day"

### Execution Steps

1. **Run ingestion** — calls ingest skill to pull fresh data from all sources
2. **Collect all `status: new` items** — grep across `Amuse/Inbox/`, `Avitia/Inbox/`, and vault-root `Inbox/`
3. **Load context:**
   - Today's calendar events (from ingested calendar items)
   - Open tasks from BOTH layers:
     - Planning layer: `Amuse/Tasks.md` and `Avitia/Tasks.md`
     - Execution layer: TaskNotes API (`curl http://127.0.0.1:8090/api/tasks?status=open&status=in-progress`)
   - Recent meeting notes (Granola `Meetings/` + Read.ai items in Inbox)
   - Recent `Decisions.md` entries from both workspaces
4. **Cross-reference and synthesize** — produce intelligence briefing (see output format)
5. **Interactive triage** — present each `new` item with a recommendation, user confirms

### Intelligence Briefing Output

Presented as a structured markdown output (not written to a file unless user requests):

```markdown
## Daily Ops — 2026-03-19

### Conflicts & Alerts
- [description of conflict: e.g., meeting about X but task Y is overdue]

### Stale Items
- [promised deliverable with no progress, overdue tasks]

### Connections
- [Slack thread relates to Jira ticket, email echoes meeting discussion]

### Today's Priorities
1. [synthesized priority — not just a list, but reasoned ordering]
2. ...

### New Items for Triage (7 items)

| # | Source | Summary | Workspace | Recommendation |
|---|--------|---------|-----------|----------------|
| 1 | Slack #bizdev | Ruth shared Burning Rock update | Avitia | → Task (update BD-25) |
| 2 | Email | Chris re: ticketing platform | Amuse | → Task (evaluate Fever) |
| 3 | Read.ai | Product dev weekly summary | Avitia | → FYI (no action items for Kam) |
```

### Triage Actions

For each item, user can:

| Action | Effect |
|--------|--------|
| **→ Task** | See "Task Promotion" below |
| **→ Decision** | Appends to workspace `Decisions.md`, marks item `triaged` |
| **→ FYI** | Marks item `triaged`, no further action |
| **→ Dismiss** | Marks item `acted-on`, effectively archived |
| **→ Relate** | Adds wikilink to `related:` field, keeps as `new` for further triage |

### Task Promotion (→ Task action)

When an inbox item is promoted to a task, two things happen:

**1. TaskNotes execution task** (via API):
```bash
curl -X POST "http://127.0.0.1:8090/api/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "{extracted task title}",
    "status": "open",
    "priority": "normal",
    "projects": ["[[{Workspace}]]"],
    "due": "{due date if mentioned, otherwise omit}"
  }'
```

**2. Planning layer entry** — append to `{Workspace}/Tasks.md` under `## Active`:
```markdown
- [ ] {task title} — {one-line context from source} — @Kam | Source: `Inbox/{filename}`
```

**3. Update inbox item** — set `status: triaged` and `linked_task: Tasks/{task-filename}.md`

If TaskNotes API is unreachable, create task file directly in `Tasks/` and still update `Tasks.md`.

### Relationship to Existing Morning Routine

Daily Ops **replaces the Workspace Status Triage block** (steps 2a-2e in the morning routine) and **the inbox scan** (step 2b-ext). The existing morning routine skill calls daily-ops for these steps, then continues with its remaining steps (weekly review check, etc.).

---

## Layer 3: Thinking (Emergent Ideas)

### New Skill: `think`

**Trigger phrases:** "think", "what's emerging", "connect the dots", "what am I missing"

### Purpose

Surface implicit patterns, connections, and questions from accumulated vault data that the user hasn't explicitly named.

### Data Sources

Reads from (does NOT call live APIs — works from what's already in the vault):

- `Amuse/Inbox/` and `Avitia/Inbox/` — recent ingested items (all statuses)
- `Amuse/Tasks.md` and `Avitia/Tasks.md` — open and recent completed tasks
- `Amuse/Decisions.md` and `Avitia/Decisions.md` — recent decisions
- `Amuse/Handoff.md` and `Avitia/Handoff.md` — project context
- `Meetings/` — Granola meeting notes
- `Daily/` — daily notes and past thinking outputs
- `Amuse/Sessions/` — session notes
- TaskNotes API — open/in-progress tasks from execution layer

### Analysis Patterns

The skill looks for:

| Pattern | Example |
|---------|---------|
| **Cross-workspace echoes** | Same topic appearing in both Amuse and Avitia contexts |
| **Recurring themes** | A person/topic surfacing 3+ times across different sources in the past week |
| **Unanswered questions** | Questions raised in meetings/emails with no corresponding task or decision |
| **Strategic tensions** | Two active workstreams pulling in different directions |
| **Stale commitments** | Action items from meetings that never became tasks |
| **Emerging opportunities** | Connections between contacts, capabilities, or needs that haven't been explicitly linked |
| **Drift detection** | Current activity diverging from stated priorities in Handoff.md |

### Example Provocations

To illustrate the expected depth and tone:

- "Ruth mentioned Burning Rock benchmarking in Monday's BD call, and Mauricio's #software thread about CGP panel integration references the same dataset. Neither workstream knows about the other — is there a shared dependency here?"
- "You've had 3 meetings about Thailand expansion in the past 2 weeks but no new tasks were created. Is this stalled, or is the work happening off-platform?"
- "The Submersive waitlist launch is 11 days out and the tech sprint has been 'unblocked' for 5 days with no commits. What's the blocker behind the blocker?"

### Output

Written to `Daily/YYYY-MM-DD. Thinking.md` (matching existing daily note naming convention):

```markdown
---
type: thinking
date: 2026-03-19
sources_scanned: 47
time_window: 7d
---

# What's Emerging — 2026-03-19

## Patterns

### [Pattern Title]
[Description of what was noticed, with specific references to source items]

**So what:** [Why this matters — the implication or question it raises]

### [Pattern Title]
...

## Unanswered Questions
- [Question from meeting X that has no task or resolution]

## Provocations
- [A non-obvious connection or "what if" synthesized from the data]
```

### Temporal Window

Default: scans last 7 days of vault data. Can be overridden: "think about the last month" or "think about Avitia only".

### Dependency on Layer 1

The Thinking command improves as more data accumulates in the vault. In the first few days it will have limited material. After 1-2 weeks of daily ingestion, it becomes genuinely useful.

---

## Vault Structure Changes

### New folders:

```
Amuse/Inbox/          # NEW — ingested items for Amuse
Avitia/Inbox/         # EXISTS (empty) — will be populated
Inbox/                # NEW (vault root) — ambiguous items
```

### Retention policy:

Items with `status: acted-on` or `status: triaged` (with a `linked_task` set) older than 14 days are moved to `{workspace}/Inbox/archive/` by a cleanup step that runs at the end of each ingestion. Items with `status: triaged` but no `linked_task` are kept until acted on. This prevents Inbox folders from growing unbounded.

### `linked_task` convention:

The `linked_task` field always points to the TaskNotes execution file (e.g., `Tasks/Send updated deck to Anna.md`), not the planning layer entry in `{Workspace}/Tasks.md`. This gives each inbox item a navigable link to its resulting task.

### New skill folders:

```
.claude/skills/ingest/
├── SKILL.md           # Skill definition and trigger phrases
├── state.json         # Last-run timestamps per source
├── templates/
│   └── inbox-item.md  # Template for ingested items
└── workflows/
    └── ingest.md      # Ingestion workflow steps + routing config (YAML blocks)

.claude/skills/daily-ops/
├── SKILL.md
├── workflows/
│   └── triage.md      # Triage workflow steps
└── templates/
    └── briefing.md    # Briefing output template

.claude/skills/think/
├── SKILL.md
├── workflows/
│   └── think.md       # Analysis workflow steps
└── templates/
    └── thinking.md    # Output template
```

### Modified files:

- `.claude/skills/review/workflows/morning.md` — replace inbox call with daily-ops as step 1
- `.claude/skills/inbox/` — renamed to `inbox-deprecated/` after ingest is verified
- `CLAUDE.md` — add ingest, daily-ops, think to quick start section

---

## Implementation Order

### Phase 1a: Core Ingestion
1. Create `ingest` skill structure (SKILL.md, workflow, template)
2. Implement email ingestion (M365 MCP) with workspace routing
3. Implement Slack ingestion (Avitia workspace — detect connected workspace first)
4. Implement calendar ingestion (attendee email routing, cross-workspace duplication)
5. Add deduplication logic (source_id, backward-compatible with old inbox items)
6. Create vault-root `Inbox/` and `Amuse/Inbox/` folders
7. Add retention/archive cleanup step

### Phase 1b: Read.ai Integration
1. Examine 2-3 actual Read.ai digest emails, document structure
2. Build Read.ai-specific parser
3. Add to ingestion pipeline as meeting-type items

### Phase 2: Daily Ops
1. Create `daily-ops` skill structure
2. Implement ingestion trigger (calls ingest skill)
3. Implement context loading (both task layers: Tasks.md + TaskNotes API)
4. Implement cross-reference engine (calendar vs tasks vs inbox)
5. Build intelligence briefing output
6. Implement interactive triage with task promotion (dual-layer write)
7. Integrate into existing morning routine (replace steps 1 + 2b-ext)

### Phase 3: Thinking
1. Create `think` skill structure
2. Implement vault scanning (all sources including TaskNotes API)
3. Build pattern detection prompts
4. Implement output writing to `Daily/`
5. Add temporal window configuration

---

## Open Questions

1. **Slack workspace switching:** The Slack MCP connector is locked to one workspace. Amuse Slack ingestion requires either a second connection or manual switching. Deferred to future phase.
2. **Amuse Slack channels:** Channel list TBD once connected to Amuse workspace.
3. **Volume management:** If Slack channels are high-volume, may need message-level filtering (e.g., only threads with 3+ replies, or messages mentioning Kam). Monitor after first week of ingestion.
4. **TaskNotes API compatibility:** Confirm task creation via HTTP API (port 8090) works for promoting inbox items to tasks. Existing inbox skill uses this successfully.
