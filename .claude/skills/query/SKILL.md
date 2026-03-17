---
name: query
description: Query data from this vault. USE WHEN user asks about projects, clients, tasks, daily notes. Use grep to extract frontmatter - do NOT read full files.
---

# Query Skill

## IMPORTANT

**Use `grep` to extract frontmatter. Do NOT read full files.**

## Workspaces (Projects)

Workspaces live at root level: `Amuse/Amuse.md`, `Avitia/Avitia.md`.

```bash
for f in Amuse/Amuse.md Avitia/Avitia.md; do
  [ -f "$f" ] && echo "=== $(basename "$(dirname "$f")") ===" && grep "^status:\|^type:\|^drive:\|^repo:" "$f"
done
```

**Present as table:**
| Workspace | Status | Drive | Repo |
|-----------|--------|-------|------|

## Clients

Clients are workspace-scoped: `{Workspace}/Clients/*.md`.

```bash
for dir in Amuse/Clients Avitia/Clients; do
  [ -d "$dir" ] && for f in "$dir"/*.md; do
    [ -f "$f" ] && echo "=== $(basename "$f" .md) [$(basename "$(dirname "$(dirname "$f")")")] ===" && grep "^name:\|^stage:\|^company:\|^next_action:" "$f"
  done
done
```

**Present as table:**
| Client | Company | Stage | Workspace | Next Action |
|--------|---------|-------|-----------|-------------|

## Tasks

### Execution tasks (TaskNotes API — daily/scheduled work)
```bash
curl -s "http://127.0.0.1:8090/api/tasks"
```

### Planning tasks (workspace-level — high-level status, blockers)
```bash
for f in Amuse/Tasks.md Avitia/Tasks.md; do
  [ -f "$f" ] && echo "=== $(basename "$(dirname "$f")") ===" && grep "^\- \[" "$f"
done
```

## Daily Notes

```bash
ls -t Daily/*.md | head -5 | while read f; do
  echo "=== $(basename "$f" .md) ==="
  grep "^mood:\|^energy:\|^sleep_quality:" "$f"
done
```

## Output

Always present results as markdown table.
