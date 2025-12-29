---
name: tasknotes
description: Manage tasks and pomodoro timer in Obsidian via TaskNotes plugin API. Use when user wants to create tasks, list tasks, query by status or project, update task status, delete tasks, start/stop pomodoro timer, or check what they need to do. Trigger phrases include create task, show tasks, my tasks, mark done, delete task, task list, kanban, what should I work on, start pomodoro, stop timer, pause timer.
---

# TaskNotes Skill

Manage Obsidian tasks via the TaskNotes plugin HTTP API.

## Setup Requirements

1. **TaskNotes plugin** installed in Obsidian with HTTP API enabled
2. **API token** in `.env` file (auto-discovered from vault root or ~/.config/tasknotes/):
   ```
   TASKNOTES_API_KEY=your_token_here
   ```
3. **API port** (default: 8080) - configurable via `TASKNOTES_API_PORT` env var

## Commands

```bash
# List all tasks
{baseDir}/tasknotes.py list

# List by status
{baseDir}/tasknotes.py list --status in-progress
{baseDir}/tasknotes.py list --status near-backlog

# List by project
{baseDir}/tasknotes.py list --project "[[Goal Name]]"

# Human-readable output (add --table)
{baseDir}/tasknotes.py list --table

# Create task
{baseDir}/tasknotes.py create "Task title" --project "Goal Name" --priority high --status near-backlog

# Create task with scheduled time
{baseDir}/tasknotes.py create "Task title" \
  --project "Goal Name" \
  --scheduled "2025-12-23T15:00:00" \
  --priority high

# Update task status
{baseDir}/tasknotes.py update "Notes/Tasks/task-file.md" --status done

# Add/update task description
{baseDir}/tasknotes.py update "Notes/Tasks/task-file.md" \
  --details "## Task\nUpdated context here."

# Delete task
{baseDir}/tasknotes.py delete "Notes/Tasks/task-file.md"

# Get stats
{baseDir}/tasknotes.py stats

# Get available options (projects, statuses, etc.)
{baseDir}/tasknotes.py options
```

## Pomodoro Statistics

```bash
# By project/goal (default)
{baseDir}/pomodoro_stats.py --by-project

# By task
{baseDir}/pomodoro_stats.py --by-task

# By date
{baseDir}/pomodoro_stats.py --by-date

# Last 7 days only
{baseDir}/pomodoro_stats.py --days 7 --by-project

# JSON output
{baseDir}/pomodoro_stats.py --json
```

## Task Properties

**Status values:**
- `none` - No status
- `far-backlog` - Future/someday
- `near-backlog` - Ready to work on
- `in-progress` - Currently working
- `done` - Completed

**Priority values:**
- `none`, `low`, `middle`, `high`, `urgent`

**Other fields:**
- `projects` - Array of goal/project links, e.g. `["[[Goal Name]]"]`
- `contexts` - Array like `["office", "energy-high"]`
- `due` - Due date (YYYY-MM-DD)
- `scheduled` - Scheduled date/time (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)
- `timeEstimate` - Minutes (number)
- `tags` - Array of tags
- `details` - Task description/body content (writes to markdown body)

## Pomodoro Timer API

Control the built-in pomodoro timer via API:

```bash
# Start timer
source .env && curl -s -X POST "http://localhost:${TASKNOTES_API_PORT:-8080}/api/pomodoro/start" \
  -H "Authorization: Bearer $TASKNOTES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"taskId": "Tasks/my-task.md"}'

# Stop/pause/resume
source .env && curl -s -X POST "http://localhost:${TASKNOTES_API_PORT:-8080}/api/pomodoro/stop" \
  -H "Authorization: Bearer $TASKNOTES_API_KEY"

# Get status
source .env && curl -s "http://localhost:${TASKNOTES_API_PORT:-8080}/api/pomodoro/status" \
  -H "Authorization: Bearer $TASKNOTES_API_KEY"
```

## When to Use

**Tasks:**
- "create a task for X" → create task with title X
- "show my tasks" → list all tasks
- "show in-progress tasks" → list --status in-progress
- "mark X as done" → update task status to done
- "delete task X" → delete task

**Pomodoro:**
- "start pomodoro" → start timer (ask which task)
- "stop pomodoro" → stop timer
- "pomodoro status" → check time remaining

## Example Workflows

### Morning: Check what to work on
```bash
{baseDir}/tasknotes.py list --status in-progress --table
{baseDir}/tasknotes.py list --status near-backlog --limit 5 --table
```

### Create task linked to goal
```bash
{baseDir}/tasknotes.py create "Finish landing page copy" \
  --project "Claude Code Lab - Launch January 2025" \
  --priority high \
  --status near-backlog
```

### Complete a task
```bash
{baseDir}/tasknotes.py update "Notes/Tasks/finish-landing-page.md" --status done
```
