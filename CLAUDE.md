# CLAUDE.md

## Project Structure

```
.
├── Projects/       # Active projects
├── Clients/        # Client profiles
├── Tasks/          # Task files (managed by TaskNotes)
├── Meetings/       # Synced meetings from Granola
├── Daily/          # Daily notes
├── Bases/          # Obsidian Bases (structured data views)
└── .claude/skills/ # Claude Code skills
    ├── review/     # Morning, evening, weekly routines
    ├── client/     # Client follow-ups
    ├── query/      # Query vault data
    ├── granola/    # Sync meetings from Granola app
    └── tasknotes/  # Task management
```

## Quick Start

- `/setup-memory` - Build your personalized CLAUDE.md
- `"morning routine"` - Start your day
- `"get my projects"` - See all projects
- `"who needs follow-up?"` - Check clients
- `"sync my meetings"` - Sync Granola meetings to vault

## Output Preferences

When querying data, **present as markdown table**. Use grep to extract frontmatter - don't read full files.
