---
name: obases
description: Query and create items in Obsidian Bases (structured data views). Use to explore user's goals, tasks, experiments, and create new items programmatically.
---

# Obsidian Bases CLI

Query and create structured data in Obsidian Bases. Bases are like databases/spreadsheets in Obsidian that organize notes with properties, filters, and views.

## Prerequisites

- Obsidian must be running with the `headless-bases` plugin active
- Server runs at `http://127.0.0.1:27124`
- **Base must be open in Obsidian main view to query data**

## Quick Start

```bash
# Check connection
{baseDir}/obases.py status

# List all bases
{baseDir}/obases.py bases

# Open base first (required before view queries work)
{baseDir}/obases.py open "Templates/Bases/Goals.base"

# Query a view
{baseDir}/obases.py view "Templates/Bases/Goals.base" "Current"

# Get schema (fields, example)
{baseDir}/obases.py schema "Templates/Bases/Goals.base"

# Create new item
{baseDir}/obases.py create "Templates/Bases/Goals.base" "My New Goal" --json '{"Status": "In progress", "Priority": "High"}'
```

## Commands

### Status
```bash
{baseDir}/obases.py status
```

### List Bases
```bash
{baseDir}/obases.py bases
```

### Get Schema (for discovery)
```bash
{baseDir}/obases.py schema "Templates/Bases/Goals.base"
```

Returns:
- `sourceFolder`: Where items are stored
- `fields`: Available fields with types
- `example`: One real example to learn from
- `availableViews`: List of views

### Query a View
```bash
{baseDir}/obases.py view "<base-path>" "<view-name>"
{baseDir}/obases.py view "<base-path>" "<view-name>" -o table    # Force table format
{baseDir}/obases.py view "<base-path>" "<view-name>" -o json     # Force JSON
```

Output format auto-detects: table for terminal, JSON for pipes.

### Open a Base
```bash
{baseDir}/obases.py open "<base-path>"             # Opens in main view
{baseDir}/obases.py open "<base-path>" --sidebar   # Opens in sidebar
```

### Create Item
```bash
{baseDir}/obases.py create "<base-path>" "<title>" --json '{"field": "value", ...}'
{baseDir}/obases.py create "<base-path>" "<title>" -j '{"field": "value"}' -b "Body content"
```

**Workflow:**
1. First run `schema` to see available fields and example
2. Then create with appropriate fields

**Example:**
```bash
# 1. Check schema
{baseDir}/obases.py schema "Templates/Bases/Goals.base"

# 2. Create goal (using example as guide)
{baseDir}/obases.py create "Templates/Bases/Goals.base" "Learn Rust" --json '{
  "Status": "In progress",
  "Priority": "High",
  "Area": "Career",
  "categories": ["[[Goals]]"]
}'
```

## Key Bases in This Vault

| Base | Purpose | Common Views |
|------|---------|--------------|
| `Templates/Bases/Goals.base` | Active goals | Current, Every morning, Every week |
| `Templates/Bases/Experiments.base` | Experiments | Current, All Experiments |
| `Templates/Bases/People.base` | Contacts | All Contacts, Reconnect |
| `Templates/Bases/Content.base` | Video ideas | Content, Active Content |
| `Templates/Bases/Journals.base` | Check-ins | All Entries, Last 7 Days |

## Agent Workflow

### Reading Goals
```bash
{baseDir}/obases.py view "Templates/Bases/Goals.base" "Current" -o json | jq '.rows[] | {name: .file, status: .Status, priority: .Priority}'
```

### Creating a Goal
```bash
# 1. Get schema
{baseDir}/obases.py schema "Templates/Bases/Goals.base"

# 2. Create (include categories to make it appear in base)
{baseDir}/obases.py create "Templates/Bases/Goals.base" "New Goal Title" --json '{
  "Status": "In progress",
  "Priority": "High",
  "Area": "Career",
  "Frequency": "Every morning",
  "categories": ["[[Goals]]"]
}'

# 3. Verify
{baseDir}/obases.py view "Templates/Bases/Goals.base" "Current" -o json | jq '.rows | last'
```

## Filtering with jq

```bash
# Get just goal names
{baseDir}/obases.py view "Templates/Bases/Goals.base" "Current" -o json | jq -r '.rows[].file'

# Filter by priority
{baseDir}/obases.py view "Templates/Bases/Goals.base" "Current" -o json | jq '.rows | map(select(.Priority == "High"))'

# Count items
{baseDir}/obases.py view "Templates/Bases/Goals.base" "Current" -o json | jq '.rows | length'
```

## Error Handling

- Exit code 0: Success
- Exit code 1: Error (prints message to stderr)
- **"No data in view"**: Base not open in Obsidian → run `open <path>` first
- **"View not found"**: Check available views with `schema <path>`

## Notes

- Items are markdown files with YAML frontmatter
- Creating an item = creating a markdown file with frontmatter
- The `categories` field often determines which base an item appears in
- Views are filtered by Obsidian's formulas
