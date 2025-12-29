# Claude Code Obsidian Starter Kit

This is a pre-configured Obsidian vault with Claude Code skills for task management and data querying.

## Quick Commands

Try these commands:
- "Create a task: [your task]" - Creates a new task in Obsidian
- "Show my tasks" - Lists all your tasks
- "Show my in-progress tasks" - Filter by status
- "Start my morning" - Get a daily overview

## Project Structure

```
.
├── Daily/          # Daily notes
├── Tasks/          # Task files (managed by TaskNotes)
├── Goals/          # Goal tracking
├── Templates/      # Note templates
│   └── Bases/      # Obsidian Bases (structured data views)
└── .claude/skills/ # Claude Code skills
    ├── tasknotes/  # Task management
    ├── obases/     # Query Obsidian Bases
    └── morning-routine/  # Daily routine
```

## Skills Available

### TaskNotes
Create and manage tasks via the TaskNotes Obsidian plugin.
- Status: none, far-backlog, near-backlog, in-progress, done
- Priority: none, low, middle, high, urgent

### Obsidian Bases (obases)
Query structured data in Obsidian Bases (like databases).
- Requires: Obsidian running with headless-bases plugin

### Morning Routine
Start your day with an overview of tasks and schedule.

## Setup Requirements

1. **Obsidian** with these plugins enabled:
   - TaskNotes (included)
   - Dataview (included)
   - headless-bases (included)

2. **TaskNotes API**:
   - Enable HTTP API in TaskNotes settings
   - Copy API token to `.env` file

3. **Environment**:
   ```
   TASKNOTES_API_KEY=your_token_here
   ```

## Conventions

- Tasks go in `Tasks/` folder
- Daily notes go in `Daily/` folder with format `YYYY-MM-DD.md`
- Goals go in `Goals/` folder
