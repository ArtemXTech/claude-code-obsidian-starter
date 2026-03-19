# Obsidian Custom Commands Implementation Plan

> **For agentic workers:** This plan is designed for Ralph Loop execution — one loop per phase. Each phase has a self-contained PROMPT.md and completion promise. Run phases sequentially (Phase 2 depends on Phase 1).

**Goal:** Build three Claude Code skills (ingest, daily-ops, think) that capture multi-source data into the vault and provide intelligent triage and emergent pattern recognition.

**Architecture:** Ingestion pipeline writes structured markdown to workspace Inbox/ folders. Daily Ops orchestrates ingestion + cross-reference + interactive triage. Think reads accumulated vault data offline for pattern synthesis.

**Tech Stack:** Claude Code skills (markdown workflows), M365 MCP (email/calendar), Slack MCP (channels), TaskNotes HTTP API (port 8090), Granola local cache.

**Spec:** `docs/superpowers/specs/2026-03-19-obsidian-commands-design.md`

---

## File Map

### New files to create:

```
.claude/skills/ingest/
├── SKILL.md                    # Skill definition, triggers, overview
├── state.json                  # Last-run timestamps per source
├── templates/inbox-item.md     # Frontmatter template for ingested items
└── workflows/ingest.md         # Full ingestion workflow with routing config

.claude/skills/daily-ops/
├── SKILL.md                    # Skill definition, triggers
├── templates/briefing.md       # Intelligence briefing output template
└── workflows/triage.md         # Full triage workflow

.claude/skills/think/
├── SKILL.md                    # Skill definition, triggers
├── templates/thinking.md       # Output template
└── workflows/think.md          # Analysis workflow

docs/superpowers/plans/PROMPT-phase1a.md  # Ralph Loop prompt for Phase 1a
docs/superpowers/plans/PROMPT-phase2.md   # Ralph Loop prompt for Phase 2
docs/superpowers/plans/PROMPT-phase3.md   # Ralph Loop prompt for Phase 3

Amuse/Inbox/.gitkeep            # New folder
Inbox/.gitkeep                  # New vault-root fallback folder
```

### Files to modify:

```
.claude/skills/review/workflows/morning.md    # Replace steps 2a-2e + 2b-ext with daily-ops call
CLAUDE.md                                      # Add new skills to quick start
```

### Files to deprecate (after Phase 1 verified):

```
.claude/skills/inbox/ → .claude/skills/inbox-deprecated/
```

---

## Phase 1a: Core Ingestion Skill

### Ralph Loop Prompt

```markdown
# PROMPT.md — Phase 1a: Ingest Skill

You are building the `ingest` Claude Code skill for an Obsidian vault.

## Spec
Read: `docs/superpowers/specs/2026-03-19-obsidian-commands-design.md` (Layer 1 section)

## What to build
Create the ingest skill that pulls data from Outlook email, Slack (Avitia workspace), and calendar into workspace-specific Inbox/ folders.

## Tasks (in order)
Follow the task list in `docs/superpowers/plans/2026-03-19-obsidian-commands.md` — Phase 1a tasks only.

## Completion criteria
All skill files exist. Routing config is defined. Templates match spec schema. Dedup logic documented. Graceful degradation specified. State tracking works.

When all Phase 1a tasks are complete:
<promise>INGEST SKILL COMPLETE</promise>
```

**Ralph Loop command:**
```bash
/ralph-loop "$(cat docs/superpowers/plans/PROMPT-phase1a.md)" --completion-promise "INGEST SKILL COMPLETE" --max-iterations 15
```

---

### Task 1: Create folder structure

**Files:**
- Create: `.claude/skills/ingest/SKILL.md`
- Create: `Amuse/Inbox/.gitkeep`
- Create: `Inbox/.gitkeep`

- [ ] **Step 1: Create Amuse/Inbox/ and vault-root Inbox/**

```bash
mkdir -p Amuse/Inbox && touch Amuse/Inbox/.gitkeep
mkdir -p Inbox && touch Inbox/.gitkeep
```

- [ ] **Step 2: Verify Avitia/Inbox/ exists**

```bash
ls -la Avitia/Inbox/
```
Expected: directory exists (already created)

- [ ] **Step 3: Create SKILL.md**

Create `.claude/skills/ingest/SKILL.md`:

```markdown
---
name: ingest
description: Pull data from Outlook email, Slack, and calendar into workspace Inbox/ folders as structured markdown. Use when user says "ingest", "pull updates", "sync sources", or during daily-ops.
---

# Ingest Skill

Multi-source ingestion pipeline. Pulls email, Slack, and calendar data into workspace-specific Inbox/ folders.

## How It Works

Queries M365 MCP (email, calendar) and Slack MCP (channels) for new items since last run. Classifies each item by workspace using routing rules, writes structured markdown to the appropriate Inbox/ folder.

## Triggers

- "ingest", "pull updates", "sync sources"
- Called automatically by daily-ops skill as step 1

## Workflow

→ Follow: `.claude/skills/ingest/workflows/ingest.md`

## Output

Items written to `{Workspace}/Inbox/` as markdown files:

- **File naming:** `{source}-{YYYY-MM-DD}-{short-slug}.md`
- **Categories:** `task`, `decision`, `blocker`, `fyi`, `meeting`
- **Frontmatter:** See `templates/inbox-item.md` for schema

## Sources

| Source | Method | Phase |
|--------|--------|-------|
| Outlook email | M365 MCP `outlook_email_search` | 1a |
| Slack (Avitia) | Slack MCP `slack_read_channel` | 1a |
| Calendar | M365 MCP `outlook_calendar_search` | 1a |
| Read.ai digests | M365 MCP (email, special parser) | 1b |
| Slack (Amuse) | Slack MCP | Future |

## Integration Points

| System | How |
|--------|-----|
| Daily Ops | Calls ingest as step 1 |
| Morning routine | Via daily-ops |
| TaskNotes | Task/blocker items can be promoted via daily-ops triage |
| Existing inbox skill | Superseded — see migration notes in spec |

## Graceful Degradation

| Source | If unavailable | Behavior |
|--------|---------------|----------|
| M365 MCP | Unreachable | Skip email + calendar, report skipped |
| Slack MCP | Unreachable | Skip Slack, report skipped |

## MCP Tools Used

| Tool | Purpose |
|------|---------|
| `outlook_email_search` | Search inbox/sent by date |
| `read_resource` | Fetch full email body |
| `outlook_calendar_search` | Get upcoming events |
| `slack_search_channels` | Detect connected workspace |
| `slack_read_channel` | Read channel messages |
```

- [ ] **Step 4: Commit**

```bash
git add .claude/skills/ingest/SKILL.md Amuse/Inbox/.gitkeep Inbox/.gitkeep
git commit -m "feat: scaffold ingest skill structure and inbox folders"
```

---

### Task 2: Create inbox item template

**Files:**
- Create: `.claude/skills/ingest/templates/inbox-item.md`

- [ ] **Step 1: Create template**

Create `.claude/skills/ingest/templates/inbox-item.md`:

```markdown
---
type: inbox-item
source: {slack|email|calendar|meeting}
workspace: {Amuse|Avitia}
source_id: "{source}:{id}"
channel: "{#channel-name}"
category: {task|decision|blocker|fyi|meeting}
date: {YYYY-MM-DD}
from: "{sender/author name}"
subject: "{subject or thread topic}"
status: new
linked_task: ""
related: []
---

# {Summary title}

## Extracted

{The specific action item, decision, or insight — 1-3 sentences}

## Source Context

> {Relevant quote from email body, Slack message, or calendar description}
```

- [ ] **Step 2: Commit**

```bash
git add .claude/skills/ingest/templates/inbox-item.md
git commit -m "feat: add inbox item template for ingest skill"
```

---

### Task 3: Create state tracking

**Files:**
- Create: `.claude/skills/ingest/state.json`

- [ ] **Step 1: Create initial state file**

Create `.claude/skills/ingest/state.json`:

```json
{
  "last_run": null,
  "sources": {
    "email": null,
    "slack_avitiabio": null,
    "calendar": null
  }
}
```

- [ ] **Step 2: Add to .gitignore or document**

State file tracks per-user run history. A source with `null` timestamp is treated as first-run (48h window, 5-item cap). Per-source tracking means if Slack fails but email succeeds, only Slack gets the first-run cap on retry. Resets are safe (just pulls a larger window).

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/ingest/state.json
git commit -m "feat: add ingestion state tracking"
```

---

### Task 4: Write the ingestion workflow

**Files:**
- Create: `.claude/skills/ingest/workflows/ingest.md`

This is the main workflow file. It contains the routing config (as YAML code blocks), all source-specific ingestion stages, dedup logic, and the archive cleanup step.

- [ ] **Step 1: Create the workflow**

Create `.claude/skills/ingest/workflows/ingest.md` with the following content:

```markdown
# Ingestion Workflow

Pull data from all connected sources into workspace Inbox/ folders.

## Prerequisites

- M365 MCP connector must be available (for email + calendar)
- Slack MCP connector must be available (for Slack channels)
- If any source is unreachable, skip it gracefully and report

## Routing Configuration

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
      "notifications@read.ai": Avitia
    keyword_fallback:
      - pattern: "ICHIP|liquid biopsy|ctDNA|BD-\\d+"
        workspace: Avitia
      - pattern: "Submersive|bathhouse|waitlist|Webflow"
        workspace: Amuse
  calendar:
    team_map:
      Avitia:
        - "@avitia.bio"
        - "@avitiabio.com"
        - "ruth"       # display name fallback (case-insensitive substring, only when no domain match)
        - "mauricio"
        - "anna"
        - "dmitri"
      Amuse:
        - "@submersive.com"
        - "@amuse.us"
        - "jee"
        - "chris"
        - "corvas"
    # Matching order: email domain first, then display name fallback
    cross_workspace: duplicate
  fallback: Inbox/

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
` ` `

## Stage 0: Determine scan window

Read state from `.claude/skills/ingest/state.json`.

- If `last_run` is null (first run): use 48 hours ago. Set `first_run_complete: false`.
- Otherwise: use `last_run` timestamp.

First-run cap: max 5 items per source/channel. Show summary of total found vs. captured.

## Stage 1: Email Ingestion

### 1a. Search inbox

` ` `
Tool: mcp__claude_ai_Microsoft_365__outlook_email_search
Parameters:
  query: "*"
  folderName: "Inbox"
  afterDateTime: {scan_window_start}
  limit: 25
` ` `

### 1b. Search sent items

` ` `
Tool: mcp__claude_ai_Microsoft_365__outlook_email_search
Parameters:
  query: "*"
  folderName: "Sent Items"
  afterDateTime: {scan_window_start}
  limit: 25
` ` `

### 1c. Route each email to workspace

For each email, determine workspace:

1. Check sender email against `domain_map` — if match, route to that workspace
2. Check sender against `sender_map` — if match, route (and flag Read.ai for Phase 1b parser)
3. Check subject + body against `keyword_fallback` patterns — if match, route
4. If no match: route to vault-root `Inbox/`

### 1d. Fetch full body for routed emails

For emails classified as potentially actionable (not newsletters, auto-replies, calendar RSVPs):

` ` `
Tool: mcp__claude_ai_Microsoft_365__read_resource
Parameters:
  uri: "mail:///messages/{messageId}"
` ` `

### 1e. Classify and write

Classify each email into category: `task | decision | blocker | fyi`

Skip entirely:
- Newsletters, marketing, automated notifications
- Calendar invites / RSVPs
- Purely social or greeting-only emails

For each surviving item, run dedup (Stage 4), then write using template.

## Stage 2: Slack Ingestion

### 2a. Detect connected workspace

` ` `
Tool: mcp__claude_ai_Slack__slack_search_channels
Parameters:
  query: "bizdev"
  channel_types: "public_channel,private_channel"
  limit: 5
` ` `

Check if results contain known Avitia channels (`#bizdev`, `#product-development`). If yes: connected to avitiabio. If no known channels found: report "Unknown Slack workspace — skipping Slack ingestion."

### 2b. Read configured channels

For each channel in the avitiabio config:

` ` `
Tool: mcp__claude_ai_Slack__slack_read_channel
Parameters:
  channel_name: "{channel-name}"
  limit: 50
  oldest: "{scan_window_start_unix_timestamp}"
` ` `

### 2c. Filter and classify messages

For each channel's messages:

- Skip bot messages, join/leave notifications, simple emoji reactions
- Look for: action items, decisions, questions, status updates, shared links with context
- Group threaded replies — treat the thread as one item, not individual messages
- Classify into category: `task | decision | blocker | fyi`

### 2d. Write inbox items

For each surviving item, run dedup (Stage 4), then write to `Avitia/Inbox/` using template.

Set `source_id: "slack:{channelId}:{threadTs}"` (or `messageTs` for non-threaded).

**source_id format by source:**

| Source | New format | Old format (backward compat) |
|--------|-----------|------------------------------|
| Email | `email:{messageId}` | `outlook:{messageId}` (from old inbox skill) |
| Slack | `slack:{channelId}:{threadTs}` | N/A |
| Calendar | `calendar:{eventId}` | N/A |

## Stage 3: Calendar Ingestion

### 3a. Search upcoming events

` ` `
Tool: mcp__claude_ai_Microsoft_365__outlook_calendar_search
Parameters:
  query: "*"
  startDateTime: "{today}"
  endDateTime: "{today + 3 days}"
  limit: 20
` ` `

### 3b. Route each event to workspace

For each event, check attendee emails:

1. Match attendee email domains against `calendar.team_map`
2. If attendees span both workspaces: create item in BOTH workspace Inboxes (cross_workspace: duplicate)
3. If no domain match: check attendee display names as fallback (case-insensitive substring)
4. If still no match: route to vault-root `Inbox/`

### 3c. Write calendar items

Write each event as an inbox item with `category: meeting`, `source: calendar`.

Include in body: event time, attendees, description/agenda if present, location.

Set `source_id: "calendar:{eventId}"`.

## Stage 4: Deduplication

Before writing ANY item, check for duplicates:

**Check 1 — source_id match (new format):**
` ` `bash
grep -rl "source_id: {source_id}" {workspace}/Inbox/ 2>/dev/null
` ` `

**Check 2 — source_id match (old inbox format, Avitia only):**
` ` `bash
grep -rl "source_id: outlook:{messageId}" Avitia/Inbox/ 2>/dev/null
` ` `

If either check finds a match → skip silently.

**Check 3 — semantic match against existing open tasks:**
Collect open tasks:
` ` `bash
grep "^\- \[ \]" {workspace}/Tasks.md 2>/dev/null
` ` `

If the item substantially duplicates an existing task, skip and note as "signal for existing task" (reported in summary).

## Stage 5: Write items

For each item that passes dedup:

1. Generate filename: `{source}-{YYYY-MM-DD}-{short-slug}.md`
2. Fill template from `.claude/skills/ingest/templates/inbox-item.md`
3. Write to `{workspace}/Inbox/`

## Stage 6: Archive cleanup

Move items with `status: acted-on` or (`status: triaged` AND `linked_task` is set) that are older than 14 days:

` ` `bash
# For each workspace inbox
mkdir -p {workspace}/Inbox/archive
# Move qualifying files
` ` `

Check file date from frontmatter `date:` field, not filesystem mtime.

## Stage 7: Update state

Update `.claude/skills/ingest/state.json`:

` ` `json
{
  "last_run": "{now ISO 8601}",
  "sources": {
    "email": "{now}",
    "slack_avitiabio": "{now}",
    "calendar": "{now}"
  },
  "first_run_complete": true
}
` ` `

## Stage 8: Summary

Report what was ingested:

` ` `markdown
## Ingestion Complete — {date}

| Source | Items Found | Items Captured | Skipped (dedup) | Workspace |
|--------|------------|----------------|-----------------|-----------|
| Email | X | Y | Z | Amuse: A, Avitia: B, Unrouted: C |
| Slack (avitiabio) | X | Y | Z | Avitia |
| Calendar | X | Y | Z | Mixed |

Signals for existing tasks: N items matched open tasks (not captured)
Archived: N old items moved to archive/

{If first run: "First run — capped at 5 items per source. Run again to catch remaining."}
{If any source skipped: "Skipped: {source} — {reason}"}
` ` `
```

**Note:** The triple backticks inside the workflow file should use the actual markdown fence syntax. The spaces shown above (`` ` ` ` ``) are to avoid escaping issues in this plan — the actual file uses standard fences.

- [ ] **Step 2: Verify workflow references correct MCP tool names**

```bash
grep -n "mcp__" .claude/skills/ingest/workflows/ingest.md
```

Expected: tool names match the MCP tools available in the system.

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/ingest/workflows/ingest.md
git commit -m "feat: add complete ingestion workflow with routing, dedup, and archive"
```

---

### Task 5: Verify ingest skill is complete

- [ ] **Step 1: Verify all files exist**

```bash
ls -la .claude/skills/ingest/SKILL.md
ls -la .claude/skills/ingest/state.json
ls -la .claude/skills/ingest/templates/inbox-item.md
ls -la .claude/skills/ingest/workflows/ingest.md
ls -la Amuse/Inbox/.gitkeep
ls -la Inbox/.gitkeep
```

All should exist.

- [ ] **Step 2: Verify SKILL.md references workflow correctly**

```bash
grep "workflows/ingest.md" .claude/skills/ingest/SKILL.md
```

Expected: path reference found.

- [ ] **Step 3: Verify template has all required frontmatter fields**

```bash
grep -c "type:\|source:\|workspace:\|source_id:\|channel:\|category:\|date:\|from:\|subject:\|status:\|linked_task:\|related:" .claude/skills/ingest/templates/inbox-item.md
```

Expected: 12 fields.

---

## Phase 2: Daily Ops Skill

### Ralph Loop Prompt

```markdown
# PROMPT.md — Phase 2: Daily Ops Skill

You are building the `daily-ops` Claude Code skill for an Obsidian vault.

## Spec
Read: `docs/superpowers/specs/2026-03-19-obsidian-commands-design.md` (Layer 2 section)

## Dependencies
The `ingest` skill must already exist at `.claude/skills/ingest/`. Read its SKILL.md and workflow to understand how to call it.

## What to build
Create the daily-ops skill that:
1. Calls ingest as step 1
2. Collects all status:new items from workspace Inboxes
3. Loads context (tasks from BOTH layers, calendar, meetings, decisions)
4. Cross-references to produce an intelligence briefing
5. Presents interactive triage with task promotion (dual-layer: TaskNotes API + Tasks.md)

## Tasks
Follow the task list in `docs/superpowers/plans/2026-03-19-obsidian-commands.md` — Phase 2 tasks only.

## Key references
- TaskNotes API: `.claude/skills/tasknotes/SKILL.md`
- Existing morning routine: `.claude/skills/review/workflows/morning.md`
- Ingest skill: `.claude/skills/ingest/SKILL.md`

## Completion criteria
All skill files exist. Workflow covers all 5 execution steps. Task promotion writes to both layers. Briefing output matches spec format.

When all Phase 2 tasks are complete:
<promise>DAILY OPS COMPLETE</promise>
```

**Ralph Loop command:**
```bash
/ralph-loop "$(cat docs/superpowers/plans/PROMPT-phase2.md)" --completion-promise "DAILY OPS COMPLETE" --max-iterations 15
```

---

### Task 6: Create daily-ops SKILL.md

**Files:**
- Create: `.claude/skills/daily-ops/SKILL.md`

- [ ] **Step 1: Create SKILL.md**

Create `.claude/skills/daily-ops/SKILL.md`:

```markdown
---
name: daily-ops
description: Intelligent daily triage across all sources. Runs ingestion, cross-references calendar/tasks/meetings/email, produces synthesized briefing, and guides interactive triage. Use when user says "daily ops", "what's going on", "briefing", "triage my day".
---

# Daily Ops Skill

Single command for your daily operational awareness. Pulls fresh data, cross-references everything, surfaces conflicts and connections, then triages new items.

## How It Works

1. Calls `ingest` skill to pull fresh data from all sources
2. Collects all `status: new` items across workspace Inboxes
3. Loads context from both task layers, calendar, meetings, decisions
4. Cross-references to produce an intelligence briefing
5. Presents interactive triage for new items

## Triggers

- "daily ops", "what's going on", "briefing", "triage my day"
- Replaces steps 2a-2e and 2b-ext of the morning routine

## Workflow

→ Follow: `.claude/skills/daily-ops/workflows/triage.md`

## Output

Structured intelligence briefing with:
- Conflicts & Alerts
- Stale Items
- Connections across sources
- Synthesized priorities
- Interactive triage table

## Integration Points

| System | How |
|--------|-----|
| Ingest skill | Called as step 1 |
| Morning routine | Replaces workspace triage block |
| TaskNotes | Promotes items to tasks (dual-layer) |
| Decisions.md | Promotes decision items |
```

- [ ] **Step 2: Commit**

```bash
git add .claude/skills/daily-ops/SKILL.md
git commit -m "feat: create daily-ops skill definition"
```

---

### Task 7: Create daily-ops briefing template

**Files:**
- Create: `.claude/skills/daily-ops/templates/briefing.md`

- [ ] **Step 1: Create template**

Create `.claude/skills/daily-ops/templates/briefing.md`:

```markdown
## Daily Ops — {date}

### Conflicts & Alerts
{conflicts_or_none}

### Stale Items
{stale_items_or_none}

### Connections
{connections_or_none}

### Today's Priorities
{synthesized_priorities}

### New Items for Triage ({count} items)

| # | Source | Summary | Workspace | Recommendation |
|---|--------|---------|-----------|----------------|
{triage_rows}
```

- [ ] **Step 2: Commit**

```bash
git add .claude/skills/daily-ops/templates/briefing.md
git commit -m "feat: add daily-ops briefing template"
```

---

### Task 8: Write the daily-ops triage workflow

**Files:**
- Create: `.claude/skills/daily-ops/workflows/triage.md`

- [ ] **Step 1: Create the workflow**

Create `.claude/skills/daily-ops/workflows/triage.md`:

```markdown
# Daily Ops Triage Workflow

Intelligent daily triage that cross-references all sources and produces a synthesized briefing.

## Step 1: Run Ingestion

Call the ingest skill workflow:

→ Follow: `.claude/skills/ingest/workflows/ingest.md`

If ingestion reports all sources skipped, continue anyway — there may be existing `status: new` items from previous runs.

## Step 2: Collect New Items

Grep for all `status: new` inbox items across all locations:

` ` `bash
grep -rl "status: new" Amuse/Inbox/ Avitia/Inbox/ Inbox/ 2>/dev/null
` ` `

For each found file, extract frontmatter:
` ` `bash
grep "^type:\|^source:\|^workspace:\|^category:\|^date:\|^from:\|^subject:\|^status:" "{file}"
` ` `

## Step 3: Load Context

### 3a. Open tasks (both layers)

**Execution layer (TaskNotes API):**
` ` `bash
curl -s "http://127.0.0.1:8090/api/tasks?status=open&status=in-progress" 2>/dev/null
` ` `

If API unreachable, fall back to file-based:
` ` `bash
for f in Tasks/*.md; do
  [ -f "$f" ] && grep -l "status: open\|status: in-progress" "$f"
done
` ` `

**Planning layer:**
` ` `bash
grep "^\- \[ \]" Amuse/Tasks.md Avitia/Tasks.md 2>/dev/null
` ` `

### 3b. Today's calendar

Check for calendar items ingested in Step 1, or from previous runs:
` ` `bash
grep -rl "source: calendar" Amuse/Inbox/ Avitia/Inbox/ Inbox/ 2>/dev/null | while read f; do
  grep "date: $(date +%Y-%m-%d)" "$f" && echo "$f"
done
` ` `

### 3c. Recent meetings

**Granola meetings (last 3 days):**
` ` `bash
ls -1 Meetings/*.md 2>/dev/null | tail -5
` ` `

**Read.ai meeting items in Inbox (last 3 days):**
` ` `bash
grep -rl "category: meeting" Avitia/Inbox/ 2>/dev/null
` ` `

### 3d. Recent decisions

` ` `bash
head -30 Amuse/Decisions.md
head -30 Avitia/Decisions.md
` ` `

## Step 4: Cross-Reference and Synthesize

With all context loaded, analyze for:

### Conflicts & Alerts
- Meeting today about topic X, but related task is overdue or has no prep
- Email contradicts an existing task or decision
- Two tasks that are implicitly dependent but not linked

### Stale Items
- Tasks with due dates in the past
- Commitments from meetings (last 7 days) with no corresponding task
- Inbox items that have been `status: new` for more than 3 days

### Connections
- Slack thread that relates to an open Jira ticket or task
- Email that echoes a recent meeting discussion
- Same person appearing across multiple sources on same topic

### Today's Priorities
Synthesize — don't just list. Consider:
- What's due today or overdue
- What meetings are coming and what prep is needed
- What's been stale the longest
- Energy allocation across workspaces

Present using the briefing template at `.claude/skills/daily-ops/templates/briefing.md`.

## Step 5: Interactive Triage

For each `status: new` item, present a recommendation:

| # | Source | Summary | Workspace | Recommendation |
|---|--------|---------|-----------|----------------|

Then ask: **"How should I triage these? (e.g., '1,2 → Task, 3 → FYI, 4-5 → Dismiss', or 'all FYI')"**

Wait for user confirmation before making any changes.

### Triage Actions

**→ Task** (task promotion — dual-layer write):

1. Create TaskNotes execution task:
` ` `bash
curl -X POST "http://127.0.0.1:8090/api/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "{task title}",
    "status": "open",
    "priority": "normal",
    "projects": ["[[{Workspace}]]"]
  }'
` ` `
If API unreachable, create task file directly in `Tasks/`.

2. Append to `{Workspace}/Tasks.md` under `## Active`:
` ` `markdown
- [ ] {task title} — {one-line context} — @Kam | Source: `Inbox/{filename}`
` ` `

3. Update inbox item: set `status: triaged`, `linked_task: Tasks/{task-filename}.md`

4. Check `{Workspace}/Handoff.md` — if the task appears as an action item, check it off:
` ` `bash
grep -n "{task title keywords}" {Workspace}/Handoff.md
# If found as "- [ ]", change to "- [x]"
` ` `

**→ Decision:**

1. Append to `{Workspace}/Decisions.md`:
` ` `markdown
### {today's date} — {decision title}

- **Decision:** {what was decided}
- **Rationale:** {why, if stated}
- **Decided by:** {who}
- **Reference:** `{Workspace}/Inbox/{filename}`
` ` `

2. Update inbox item: set `status: triaged`

**→ FYI:**
Update inbox item: set `status: triaged`

**→ Dismiss:**
Update inbox item: set `status: acted-on`

**→ Relate:**
Add wikilink to `related:` field in inbox item frontmatter. Keep `status: new`.

## Step 6: Summary

` ` `markdown
Triage complete:
- {N} items → Task (created in TaskNotes + {Workspace}/Tasks.md)
- {N} items → Decision (appended to Decisions.md)
- {N} items → FYI
- {N} items → Dismissed
- {N} items → Related (still pending)
- {N} items remaining as new
` ` `
```

- [ ] **Step 2: Commit**

```bash
git add .claude/skills/daily-ops/workflows/triage.md
git commit -m "feat: add daily-ops triage workflow with cross-reference and task promotion"
```

---

### Task 9: Update morning routine to use daily-ops

**Files:**
- Modify: `.claude/skills/review/workflows/morning.md`

- [ ] **Step 1: Read current morning routine**

```bash
cat .claude/skills/review/workflows/morning.md
```

- [ ] **Step 2: Replace steps 2a through 2e and 2b-ext**

Replace the entire "### 2. Workspace Status Triage" section (steps 2a through 2e, including 2b-ext) with:

```markdown
### 2. Daily Ops Triage

Run the daily-ops skill for cross-source intelligent triage:

→ Follow: `.claude/skills/daily-ops/workflows/triage.md`

This handles:
- Ingestion from all sources (email, Slack, calendar)
- Cross-referencing against open tasks, calendar, meetings, decisions
- Intelligence briefing with conflicts, stale items, connections
- Interactive triage with task promotion

After daily-ops completes, continue to Step 3.
```

Keep steps 1 (Review Yesterday), 3+ (Remaining Open Tasks, Morning Check-in, Create Morning Note, Plan the Day, Wrap Up) unchanged.

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/review/workflows/morning.md
git commit -m "feat: integrate daily-ops into morning routine, replacing manual triage steps"
```

---

### Task 10: Verify daily-ops skill is complete

- [ ] **Step 1: Verify all files exist**

```bash
ls -la .claude/skills/daily-ops/SKILL.md
ls -la .claude/skills/daily-ops/templates/briefing.md
ls -la .claude/skills/daily-ops/workflows/triage.md
```

- [ ] **Step 2: Verify workflow references ingest correctly**

```bash
grep "ingest" .claude/skills/daily-ops/workflows/triage.md
```

Expected: references to ingest workflow.

- [ ] **Step 3: Verify morning routine references daily-ops**

```bash
grep "daily-ops" .claude/skills/review/workflows/morning.md
```

Expected: reference found.

---

## Phase 3: Think Skill

### Ralph Loop Prompt

```markdown
# PROMPT.md — Phase 3: Think Skill

You are building the `think` Claude Code skill for an Obsidian vault.

## Spec
Read: `docs/superpowers/specs/2026-03-19-obsidian-commands-design.md` (Layer 3 section)

## What to build
Create the think skill that reads accumulated vault data and surfaces emergent patterns, connections, and questions the user hasn't explicitly named.

## Key design points
- Works OFFLINE from vault data only — no live API calls
- Reads from: workspace Inboxes, Tasks.md, Decisions.md, Handoff.md, Meetings/, Daily/, Sessions/
- Also queries TaskNotes API for execution-layer tasks
- Default temporal window: 7 days, overridable
- Output written to Daily/YYYY-MM-DD. Thinking.md

## Tasks
Follow the task list in `docs/superpowers/plans/2026-03-19-obsidian-commands.md` — Phase 3 tasks only.

## Completion criteria
All skill files exist. Workflow covers data collection, pattern analysis, and output writing. Template matches spec format including Provocations section.

When all Phase 3 tasks are complete:
<promise>THINK SKILL COMPLETE</promise>
```

**Ralph Loop command:**
```bash
/ralph-loop "$(cat docs/superpowers/plans/PROMPT-phase3.md)" --completion-promise "THINK SKILL COMPLETE" --max-iterations 10
```

---

### Task 11: Create think SKILL.md

**Files:**
- Create: `.claude/skills/think/SKILL.md`

- [ ] **Step 1: Create SKILL.md**

Create `.claude/skills/think/SKILL.md`:

```markdown
---
name: think
description: Surface emergent patterns, connections, and unanswered questions from accumulated vault data. Use when user says "think", "what's emerging", "connect the dots", "what am I missing".
---

# Think Skill

Emergent idea synthesis from accumulated vault data. Finds patterns you haven't named.

## How It Works

Scans recent vault data (Inboxes, tasks, decisions, meetings, sessions) and looks for:
- Cross-workspace echoes
- Recurring themes (3+ appearances across sources)
- Unanswered questions from meetings
- Strategic tensions between workstreams
- Stale commitments
- Emerging opportunities
- Drift from stated priorities

## Triggers

- "think", "what's emerging", "connect the dots", "what am I missing"
- Optional scope: "think about Avitia only", "think about the last month"

## Workflow

→ Follow: `.claude/skills/think/workflows/think.md`

## Output

Written to `Daily/YYYY-MM-DD. Thinking.md` with patterns, unanswered questions, and provocations.

## Data Sources (vault-only, no live APIs except TaskNotes)

| Source | Location |
|--------|----------|
| Inbox items | `Amuse/Inbox/`, `Avitia/Inbox/`, `Inbox/` |
| Planning tasks | `Amuse/Tasks.md`, `Avitia/Tasks.md` |
| Execution tasks | TaskNotes API (port 8090) |
| Decisions | `Amuse/Decisions.md`, `Avitia/Decisions.md` |
| Project context | `Amuse/Handoff.md`, `Avitia/Handoff.md` |
| Meetings | `Meetings/` (Granola) |
| Daily notes | `Daily/` |
| Sessions | `Amuse/Sessions/` |
```

- [ ] **Step 2: Commit**

```bash
git add .claude/skills/think/SKILL.md
git commit -m "feat: create think skill definition"
```

---

### Task 12: Create thinking output template

**Files:**
- Create: `.claude/skills/think/templates/thinking.md`

- [ ] **Step 1: Create template**

Create `.claude/skills/think/templates/thinking.md`:

```markdown
---
type: thinking
date: {YYYY-MM-DD}
sources_scanned: {count}
time_window: {N}d
---

# What's Emerging — {date}

## Patterns

### {Pattern Title}
{Description with specific references to source items}

**So what:** {Why this matters — implication or question it raises}

## Unanswered Questions
- {Question from meeting/email with no task or resolution}

## Provocations
- {Non-obvious connection or "what if" synthesized from the data}
```

- [ ] **Step 2: Commit**

```bash
git add .claude/skills/think/templates/thinking.md
git commit -m "feat: add thinking output template"
```

---

### Task 13: Write the think workflow

**Files:**
- Create: `.claude/skills/think/workflows/think.md`

- [ ] **Step 1: Create the workflow**

Create `.claude/skills/think/workflows/think.md`:

```markdown
# Think Workflow

Surface emergent patterns from accumulated vault data.

## Step 0: Determine scope

**Default:** Last 7 days across all workspaces.

**User overrides:**
- "think about Avitia only" → filter to Avitia sources
- "think about the last month" → extend window to 30 days
- "think about Amuse only" → filter to Amuse sources

Parse the user's trigger phrase for scope modifiers before proceeding.

## Step 1: Collect Data

Scan all sources within the temporal window. Count items as you go (for `sources_scanned` in output).

### 1a. Inbox items (all statuses — new, triaged, acted-on)

` ` `bash
# Find all inbox items within time window
for dir in Amuse/Inbox Avitia/Inbox Inbox; do
  [ -d "$dir" ] && find "$dir" -name "*.md" -not -path "*/archive/*" | while read f; do
    date=$(grep "^date:" "$f" | head -1 | awk '{print $2}')
    # Include if date is within window
  done
done
` ` `

Read frontmatter + body of each qualifying file.

### 1b. Tasks (both layers)

**Planning layer:**
` ` `bash
cat Amuse/Tasks.md Avitia/Tasks.md 2>/dev/null
` ` `

**Execution layer:**
` ` `bash
curl -s "http://127.0.0.1:8090/api/tasks" 2>/dev/null
` ` `

If API unreachable, read from `Tasks/*.md` files directly.

### 1c. Decisions

` ` `bash
cat Amuse/Decisions.md Avitia/Decisions.md 2>/dev/null
` ` `

Focus on entries within the temporal window.

### 1d. Project context (Handoffs)

` ` `bash
cat Amuse/Handoff.md Avitia/Handoff.md 2>/dev/null
` ` `

These provide the "stated priorities" baseline for drift detection.

### 1e. Meetings

` ` `bash
# Granola meetings within window
ls -1 Meetings/*.md 2>/dev/null
` ` `

Read notes and transcript summaries for meetings in the window.

### 1f. Daily notes and past thinking outputs

` ` `bash
ls -1 Daily/*.md 2>/dev/null
` ` `

Read recent daily notes. If past thinking outputs exist, note what patterns were already surfaced (avoid repeating stale observations).

### 1g. Sessions

` ` `bash
ls -1 Amuse/Sessions/*.md 2>/dev/null
` ` `

## Step 2: Pattern Analysis

With all data loaded, systematically look for each pattern type:

### Cross-workspace echoes
Same topic, person, or entity appearing in BOTH Amuse and Avitia data within the window. These are significant because the user manages both workspaces and may not realize when themes overlap.

### Recurring themes
A person, topic, or keyword surfacing 3+ times across DIFFERENT sources (not just the same Slack channel). Frequency across source types is more significant than frequency within one source.

### Unanswered questions
Scan meeting notes and emails for question marks, "need to decide", "TBD", "open question" — then check if a corresponding task or decision entry exists. If not, it's unanswered.

### Strategic tensions
Look for workstreams whose goals or resource demands conflict. Example: two tasks due the same week that both require Kam's full attention.

### Stale commitments
Action items from meetings (look for "will do", "I'll", "action:", "- [ ]" in meeting notes) that have no matching task in Tasks.md or TaskNotes.

### Emerging opportunities
Connections between contacts, capabilities, or needs across workspaces that haven't been explicitly linked. Look for: same person mentioned in different contexts, complementary needs/offers, timing coincidences.

### Drift detection
Compare current activity (recent tasks, inbox items, meetings) against the priorities stated in Handoff.md. Flag significant divergence — activity that doesn't serve any stated priority, or stated priorities with zero recent activity.

## Step 3: Write Output

Create `Daily/{YYYY-MM-DD}. Thinking.md` using the template at `.claude/skills/think/templates/thinking.md`.

**Quality bar for patterns:**
- Each pattern must reference specific items (file names, task titles, meeting names)
- "So what" must be actionable — a question to answer, a decision to make, or a connection to explore
- Provocations should be genuinely non-obvious, not restatements of existing tasks

**Quality bar for Provocations (examples of good provocations):**
- "Ruth mentioned Burning Rock benchmarking in Monday's BD call, and Mauricio's #software thread about CGP panel integration references the same dataset. Neither workstream knows about the other — is there a shared dependency here?"
- "You've had 3 meetings about Thailand expansion in the past 2 weeks but no new tasks were created. Is this stalled, or is the work happening off-platform?"
- "The Submersive waitlist launch is 11 days out and the tech sprint has been 'unblocked' for 5 days with no commits. What's the blocker behind the blocker?"

If fewer than 2 patterns are found (e.g., not enough data has accumulated), report: "Not enough accumulated data for meaningful pattern detection. Run daily ingestion for {N} more days, then try again."

## Step 4: Present to User

After writing the file, present the key findings conversationally. Don't just dump the file — highlight the 1-2 most important patterns and ask: "Any of these worth digging into?"
```

- [ ] **Step 2: Commit**

```bash
git add .claude/skills/think/workflows/think.md
git commit -m "feat: add think workflow with pattern analysis and quality criteria"
```

---

### Task 14: Update CLAUDE.md with new skills

**Files:**
- Modify: `CLAUDE.md`

- [ ] **Step 1: Add new skills to Quick Start section**

In `CLAUDE.md`, add to the Quick Start section:

```markdown
- `"daily ops"` - Intelligent cross-source triage
- `"pull updates"` - Ingest from email, Slack, calendar
- `"what's emerging"` - Think across accumulated data
```

- [ ] **Step 2: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: add ingest, daily-ops, and think skills to CLAUDE.md quick start"
```

---

### Task 15: Verify think skill is complete

- [ ] **Step 1: Verify all files exist**

```bash
ls -la .claude/skills/think/SKILL.md
ls -la .claude/skills/think/templates/thinking.md
ls -la .claude/skills/think/workflows/think.md
```

- [ ] **Step 2: Verify full skill chain**

```bash
# Ingest exists and is referenced by daily-ops
grep "ingest" .claude/skills/daily-ops/workflows/triage.md

# Daily-ops exists and is referenced by morning routine
grep "daily-ops" .claude/skills/review/workflows/morning.md

# Think exists independently
grep "think" .claude/skills/think/SKILL.md

# CLAUDE.md has all three
grep -c "daily ops\|pull updates\|what's emerging" CLAUDE.md
```

Expected: all references found, CLAUDE.md count = 3.

---

### Task 16: Create standalone Ralph Loop PROMPT files

**Files:**
- Create: `docs/superpowers/plans/PROMPT-phase1a.md`
- Create: `docs/superpowers/plans/PROMPT-phase2.md`
- Create: `docs/superpowers/plans/PROMPT-phase3.md`

- [ ] **Step 1: Extract the three Ralph Loop prompts from this plan into standalone files**

Copy the content from each phase's "Ralph Loop Prompt" code block into its corresponding file. These are the prompts that get fed to `/ralph-loop`.

- [ ] **Step 2: Commit**

```bash
git add docs/superpowers/plans/PROMPT-phase1a.md docs/superpowers/plans/PROMPT-phase2.md docs/superpowers/plans/PROMPT-phase3.md
git commit -m "feat: create standalone Ralph Loop prompt files for each phase"
```

---

## Phase 1b: Read.ai Integration (Post-Launch)

**Not a Ralph Loop** — requires human judgment on email format.

### Task 17: Analyze Read.ai email format

- [ ] **Step 1: Search for Read.ai emails**

```
Tool: mcp__claude_ai_Microsoft_365__outlook_email_search
Parameters:
  query: "from:read.ai OR from:notifications@read.ai"
  limit: 5
```

- [ ] **Step 2: Fetch 2-3 full email bodies and document structure**

For each email found:
```
Tool: mcp__claude_ai_Microsoft_365__read_resource
Parameters:
  uri: "mail:///messages/{messageId}"
```

- [ ] **Step 3: Document the parsing approach**

Note: HTML structure, where action items live, attendee format, meeting title extraction. Save findings to `.claude/skills/ingest/docs/readai-format.md`.

- [ ] **Step 4: Add Read.ai parser to ingest workflow**

Update `.claude/skills/ingest/workflows/ingest.md` — add a Read.ai-specific stage between Stage 1 (email) and Stage 2 (Slack) that:
1. Filters emails matching `sender_map` for Read.ai
2. Parses using the documented format
3. Writes with `category: meeting` and `source: meeting`

---

## Ralph Loop Execution Summary

| Phase | Prompt File | Promise | Max Iterations | Dependencies |
|-------|------------|---------|----------------|--------------|
| 1a | `PROMPT-phase1a.md` | `INGEST SKILL COMPLETE` | 15 | None |
| 2 | `PROMPT-phase2.md` | `DAILY OPS COMPLETE` | 15 | Phase 1a |
| 3 | `PROMPT-phase3.md` | `THINK SKILL COMPLETE` | 10 | Phase 1a (data exists) + Phase 2 (triage statuses enriched) |
| 1b | Manual | N/A | N/A | Phase 1a + human review |

**Run order:** 1a → 2 → 3 → 1b

After each Ralph Loop completes, verify the phase's output before starting the next loop.
