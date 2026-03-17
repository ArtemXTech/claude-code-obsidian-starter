---
name: tasknotes
description: Create, update, delete, and list tasks via HTTP API. USE WHEN user wants to create tasks, mark done, update status, or manage tasks.
---

# TaskNotes Skill

CRUD operations on tasks via TaskNotes plugin HTTP API.

## Hybrid Model

This vault uses a **hybrid task system**:

- **`Tasks/`** (TaskNotes) = **execution layer** — daily work, scheduling, Kanban, time tracking
- **`{Workspace}/Tasks.md`** (Amuse/Tasks.md, Avitia/Tasks.md) = **planning layer** — high-level status, blockers, team assignments

**Rules:**
1. Always set `projects` to the workspace wikilink: `["[[Amuse]]"]` or `["[[Avitia]]"]`
2. Only create execution-ready tasks in TaskNotes (not blocked tasks)
3. Blocked tasks stay in workspace `Tasks.md` until unblocked
4. When a task is completed in TaskNotes, also update the workspace `Tasks.md` if it appears there

## API Endpoint

```
http://127.0.0.1:8090/api
```

**Note:** Requires Obsidian to be open with TaskNotes plugin active.

## List Tasks

```bash
curl -s "http://127.0.0.1:8090/api/tasks"
curl -s "http://127.0.0.1:8090/api/tasks?status=in-progress"
```

## Create Task

```bash
curl -X POST "http://127.0.0.1:8090/api/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Task title",
    "status": "open",
    "priority": "high",
    "projects": ["[[Amuse]]"],
    "due": "2026-01-15",
    "scheduled": "2026-01-10"
  }'
```

**Fields:**

| Field | Values |
|-------|--------|
| title | Task name (required) |
| status | `open`, `in-progress`, `done` |
| priority | `none`, `low`, `normal`, `high` |
| projects | `["[[Amuse]]"]` or `["[[Avitia]]"]` - always scope to workspace |
| due | `YYYY-MM-DD` |
| scheduled | `YYYY-MM-DD` or `YYYY-MM-DDTHH:MM:SS` |

## Update Task

```bash
curl -X PUT "http://127.0.0.1:8090/api/tasks/Tasks%2Fmy-task.md" \
  -H "Content-Type: application/json" \
  -d '{"status": "done"}'
```

**Note:** Path must be URL-encoded (`/` → `%2F`, space → `%20`)

## Delete Task

```bash
curl -X DELETE "http://127.0.0.1:8090/api/tasks/Tasks%2Fmy-task.md"
```

## Get Options

```bash
curl -s "http://127.0.0.1:8090/api/options"
```

Returns available statuses, priorities, and projects.

## Fallback: Direct File Creation

If the API is not running (Obsidian closed), create task files directly in `Tasks/`:

```yaml
---
title: Task title
status: open
priority: high
projects:
  - "[[Amuse]]"
due: 2026-03-20
tags:
  - task
dateCreated: 2026-03-17
---

Task description here.
```

## Example Workflow

```bash
# Create
curl -X POST "http://127.0.0.1:8090/api/tasks" \
  -H "Content-Type: application/json" \
  -d '{"title": "Review proposal", "status": "open", "projects": ["[[Amuse]]"]}'

# Start working
curl -X PUT "http://127.0.0.1:8090/api/tasks/Tasks%2FReview%20proposal.md" \
  -H "Content-Type: application/json" \
  -d '{"status": "in-progress"}'

# Complete
curl -X PUT "http://127.0.0.1:8090/api/tasks/Tasks%2FReview%20proposal.md" \
  -H "Content-Type: application/json" \
  -d '{"status": "done"}'
```
