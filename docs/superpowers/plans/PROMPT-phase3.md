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
