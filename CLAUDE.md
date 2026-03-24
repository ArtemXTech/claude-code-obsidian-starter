# CLAUDE.md

## Project Structure

```
.
├── Amuse/          # Amuse workspace (clients, tasks, decisions, handoff, runbook)
├── Avitia/         # Avitia workspace (Kam is Acting CSO)
├── Tasks/          # TaskNotes plugin target
├── Daily/          # Daily notes (cross-workspace)
├── Meetings/       # Synced meetings from Granola
├── Claude-Sessions/# Cross-workspace session index
├── Bases/          # Obsidian Bases (structured data views)
├── Infrastructure/ # Claude Code system docs (MCP, hooks, troubleshooting)
├── Notes/          # Assets and references
├── guide/          # Documentation assets
└── .claude/skills/ # Claude Code skills
    ├── review/     # Morning, evening, weekly routines
    ├── client/     # Client follow-ups
    ├── query/      # Query vault data
    ├── granola/    # Sync meetings from Granola app
    └── tasknotes/  # Task management
```

## Workspaces

| Workspace | Vault Folder | Drive | Status |
|-----------|-------------|-------|--------|
| [[Amuse]] | Amuse/ | Shared drives/Amuse/ | Active |
| [[Avitia]] | Avitia/ | — | Active |

## Team

| Name | Email | Role | Tag |
|------|-------|------|-----|
| Kam | k@amuse.us | Tech + BD, co-founder | @Kam |
| Jee | jee@amuse.us | Strategy + creative, co-founder | @Jee |
| Coon | canyou@amuse.us | AI-COO | @Coon |

## Quick Start

- `/setup-memory` - Build your personalized CLAUDE.md
- `"morning routine"` - Start your day
- `"daily ops"` - Intelligent cross-source triage
- `"pull updates"` - Ingest from email, Slack, calendar
- `"what's emerging"` - Think across accumulated data
- `"get my projects"` - See all projects
- `"who needs follow-up?"` - Check clients
- `"sync my meetings"` - Sync Granola meetings to vault

## Output Preferences

When querying data, **present as markdown table**. Use grep to extract frontmatter - don't read full files.

## File Naming Convention

All authored files MUST follow: `{description}-{YYYY-MM-DD}-{author}.{ext}`

- **author**: lowercase first name (`kam`, `jee`, `coon`)
- **versioning**: append `-v2`, `-v3` before author tag for revisions
- **scope**: all files in client folders, reply drafts, deliverables, meetings
- **exempt**: system files (`TASKS.md`, `HANDOFF.md`, `DECISIONS.md`, `CLIENT.md`)

# About Me

Partner at Amuse. Acting CSO of Avitia (an Amuse client). I manage strategy development through to implementation.

## Communication Style

- Brief but detailed — get to the point with substance
- Markdown tables for data output

## How to Work With Me

- Be proactive — surface insights and suggestions
- **Always ask before changing files** — multiple workspace systems are in place per client
- Respect each client's workspace conventions
- Don't assume one client's structure applies to another
