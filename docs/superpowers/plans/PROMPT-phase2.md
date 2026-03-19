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
