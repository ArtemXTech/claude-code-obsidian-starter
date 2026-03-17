# Morning Routine

Start the day with intention.

## Steps

### 1. Review Yesterday

Check if there's a note from yesterday:
```bash
cat "Daily/$(date -v-1d +%Y-%m-%d). Morning Check-in.md" 2>/dev/null
```

Briefly summarize what happened yesterday.

### 2. Workspace Status Triage

For each workspace (Amuse, Avitia), run a status triage that cross-references open tasks against email signals.

#### 2a. Collect open tasks

Gather tasks from both layers for the workspace:

**Planning layer** — open items from the workspace task board:
```bash
ws="Amuse"  # repeat for each workspace
[ -f "$ws/Tasks.md" ] && grep "^\- \[ \]" "$ws/Tasks.md"
```

**Execution layer** — task files whose `projects` field matches this workspace:
```bash
for f in Tasks/*.md; do
  [ -f "$f" ] && grep -l "projects:.*\[\[$ws\]\]" "$f"
done
```

For each matched task file, extract frontmatter:
```bash
grep "^title:\|^status:\|^priority:\|^due:\|^projects:" "$f"
```

Only include tasks with `status: open` or `status: in-progress`. Try the TaskNotes API first:
```bash
curl -s "http://127.0.0.1:8090/api/tasks?status=open&status=in-progress"
```
If API is unreachable, use the file-based fallback above.

#### 2b. Search for email signals

**Avitia (Outlook/M365):** Use the `outlook_email_search` MCP tool to search for sent emails since the last sync date that match each open task's title. This surfaces tasks that may have been completed via email but not yet marked done.

```
Tool: outlook_email_search
Query: task title keywords
Date filter: since last_synced date from previous morning check-in
```

If the MCP tool is unreachable or errors, skip email signals for Avitia and note it was skipped.

**Amuse (Gmail):** No MCP connector available. Present tasks without email signals and ask: "Any of these resolved via email since last check-in?"

#### 2c. Present triage table

For each workspace, present a triage table:

| Task | Due | Signal | Suggested Status |
|------|-----|--------|-----------------|
| Task title | 2026-03-15 ⚠️ | Email sent Mar 16 re: deliverable | Done? |
| Task title | 2026-03-18 | — | Open |

- Use ⚠️ for overdue tasks (due date < today)
- **Signal** column shows email evidence (Avitia) or "—" if none / manual workspace
- **Suggested Status** = "Done?" if email signal found, otherwise current status

#### 2d. Confirm completions

Ask: "Which of these are done? (list numbers, or 'none')"

Wait for user confirmation before making any changes.

#### 2e. Update on confirmation

For each task confirmed as done, update all three layers:

1. **Task file frontmatter** — set `status: done` and `dateCompleted: {today}`:
```bash
# In the task's Tasks/*.md file, update frontmatter
sed -i '' 's/^status: .*/status: done/' "Tasks/{task-file}.md"
# Add dateCompleted if not present
```

2. **Workspace Tasks.md** — move the item from Active/Up Next to the Done section

3. **Workspace Handoff.md** — if the task appears as an action item, check it off:
```bash
grep -n "task title" "$ws/Handoff.md"
# If found, change `- [ ]` to `- [x]`
```

4. **Bump last_synced** — record today's date as the last triage sync point in the morning check-in note for next session's email search window

### 3. Remaining Open Tasks

After triage confirmations are applied, show what's still open across all workspaces in a single consolidated view:

| Workspace | Task | Priority | Due | Status |
|-----------|------|----------|-----|--------|
| Amuse | Task title | high | 2026-03-18 | open |
| Avitia | Task title | medium | — | in-progress |

Sort by: overdue first (⚠️), then by priority (high > medium > low), then by due date.

Present: "After triage, you have X open tasks across Y workspaces. Here's what remains:"

### 4. Morning Check-in

Ask:
- How are you feeling? (mood, energy 1-10)
- How did you sleep?
- What's your main focus today?

### 5. Create Morning Note

Create `Daily/YYYY-MM-DD. Morning Check-in.md` using template:
`templates/morning-checkin.md`

Fill in their answers.

### 6. Plan the Day

Based on energy, workspace priorities, and due dates, suggest 1-3 tasks for today.

Ask: "Should I create these tasks?"

If yes, create via API or direct file:
```bash
curl -X POST "http://127.0.0.1:8090/api/tasks" \
  -H "Content-Type: application/json" \
  -d '{"title": "Task title", "status": "open", "priority": "high", "projects": ["[[Amuse]]"]}'
```

### 7. Wrap Up

> "Morning complete! Focus today: [main focus]"
> "Have a great day!"
