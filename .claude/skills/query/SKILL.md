---
name: query
description: Query Obsidian notes using dataview. Use to show goals, recent notes, or create goals. For TASKS, use the tasknotes skill instead.
---

# Obsidian Query

Query notes in Obsidian using dataview (via headless-bases plugin).

## Prerequisites

- Obsidian must be running with headless-bases plugin
- Server at http://127.0.0.1:27124

## Quick Examples

```bash
# Check connection
{baseDir}/query.py status

# Query goals
{baseDir}/query.py goals

# Query with filter
{baseDir}/query.py goals --where "Priority=High"

# Recent files
{baseDir}/query.py recent 5

# Create a goal
{baseDir}/query.py create goals "Learn Rust" --fields "Status=In progress,Priority=High"
```

## Commands

### Status
```bash
{baseDir}/query.py status
```

### Query Collections
```bash
{baseDir}/query.py goals                           # All active goals
{baseDir}/query.py goals --where "Priority=High"   # Filter
{baseDir}/query.py goals --view all                # Different view
{baseDir}/query.py goals --json                    # JSON output
```

### Recent Files
```bash
{baseDir}/query.py recent [count]
{baseDir}/query.py recent 10
```

### Create Goal
```bash
{baseDir}/query.py create goals "Goal Title" --fields "Status=In progress,Priority=High"
```

## Note

For **tasks**, use the `tasknotes` skill instead - it has full task management (create, update, delete, list).
