# Morning Routine

Start the day with intention.

## Steps

### 1. Review Yesterday

Check if there's a note from yesterday:
```bash
cat "Daily/$(date -v-1d +%Y-%m-%d). Morning Check-in.md" 2>/dev/null
```

Briefly summarize what happened yesterday.

### 2. Daily Ops Triage

Run the daily-ops skill for cross-source intelligent triage:

→ Follow: `.claude/skills/daily-ops/workflows/triage.md`

This handles:
- Ingestion from all sources (email, Slack, calendar)
- Cross-referencing against open tasks, calendar, meetings, decisions
- Intelligence briefing with conflicts, stale items, connections
- Interactive triage with task promotion (dual-layer: TaskNotes + Tasks.md)

After daily-ops completes, continue to Step 3.

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
