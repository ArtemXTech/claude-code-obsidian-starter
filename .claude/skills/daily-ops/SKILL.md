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
