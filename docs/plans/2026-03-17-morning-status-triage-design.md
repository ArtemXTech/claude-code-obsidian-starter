# Morning Status Triage — Design

**Date:** 2026-03-17
**Author:** Kam
**Status:** Approved

## Problem

Open tasks go stale between sessions. Work gets done (emails sent, calls completed, deliverables shipped) but task status isn't updated until someone manually triages. This creates false urgency and wastes the first minutes of every session reconciling what's actually open.

## Solution

Enhance morning routine steps 2-3 with a workspace-aware status triage that cross-references open tasks against available signals, presents findings, and updates everything on confirmation.

## Design

### Trigger

Runs as part of the existing morning routine (`review` skill → `workflows/morning.md`, steps 2-3). Not a standalone skill.

### Flow per workspace

```
For each active workspace (Amuse, Avitia):
  1. Collect open tasks (TaskNotes files + workspace Tasks.md)
  2. Gather signals:
     - Avitia: Search Outlook (outlook_email_search) for sent emails
       since workspace last_synced date, match against open task titles
     - Amuse: No email MCP available — skip to manual
  3. Present triage table:
     | Task | Due | Signal | Suggested Status |
     - Highlight overdue tasks
     - Show email matches for Avitia
     - Show "no signal" for Amuse tasks
  4. Ask user: "Any of these done? Confirm or adjust."
  5. On confirmation:
     - Update task file frontmatter (status: done, dateCompleted)
     - Move items in workspace Tasks.md (Active → Done)
     - Update Handoff.md if task appears there
     - Bump last_synced date on workspace docs
```

### Guard rails

- **Never auto-close** — always present matches and wait for confirmation
- **Outlook fallback** — if MCP unreachable, fall back to manual triage (same as Amuse)
- **Workspace scoping** — only triage tasks where `projects` matches current workspace
- **Idempotent** — re-running triage on already-done tasks is a no-op

### Email platform mapping

| Workspace | Email | MCP | Triage Method |
|-----------|-------|-----|---------------|
| Amuse | Gmail | None | Manual (present + ask) |
| Avitia | Outlook/M365 | `outlook_email_search` | Signal-assisted (search + confirm) |

### Files modified

- `.claude/skills/review/workflows/morning.md` — steps 2-3 enhanced with triage sub-steps

### Files read (not modified)

- `Tasks/*.md` — TaskNotes execution layer
- `{Workspace}/Tasks.md` — planning layer
- `{Workspace}/Handoff.md` — handoff doc (updated if tasks appear there)

## What's NOT in scope

- Gmail MCP integration (blocked — no connector available)
- Auto-closing tasks without confirmation
- Standalone triage skill (extract later if needed)
- Changes to steps 1, 4-7 of morning routine

## Verification

1. Run `morning routine` trigger
2. Confirm steps 2-3 present triage table for each workspace
3. Confirm Avitia triage includes Outlook email matches (when MCP is reachable)
4. Confirm Amuse triage presents open tasks for manual confirmation
5. Confirm marking tasks done updates: TaskNotes file, Tasks.md, Handoff.md
6. Confirm `last_synced` date bumps on workspace docs
