---
name: query
description: Query Obsidian notes using dataview. Use to show goals, tasks by folder, recent notes, etc.
---

# Obsidian Query

Query notes in Obsidian using the headless-bases plugin (runs dataview queries).

## Prerequisites

- Obsidian must be running with headless-bases plugin
- Server at http://127.0.0.1:27124

## Quick Examples

```bash
# Check connection
{baseDir}/query.py status

# Query goals
{baseDir}/query.py folder Goals

# Query tasks
{baseDir}/query.py folder Tasks

# Query with filter
{baseDir}/query.py folder Goals --where "Status=In progress"

# Recent files
{baseDir}/query.py recent 5
```

## Commands

### Status
```bash
{baseDir}/query.py status
```

### Query Folder
```bash
{baseDir}/query.py folder <folder-name>
{baseDir}/query.py folder Goals
{baseDir}/query.py folder Tasks --where "Priority=High"
```

### Recent Files
```bash
{baseDir}/query.py recent [count]
{baseDir}/query.py recent 10
```

### Query Base View
```bash
{baseDir}/query.py base "Templates/Bases/Goals.base" "Current"
```

## Output

Returns JSON with file paths and frontmatter properties.
