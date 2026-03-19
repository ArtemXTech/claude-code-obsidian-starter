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
