# Morning Status Triage Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Enhance morning routine steps 2-3 to triage stale tasks against email signals before presenting the daily plan.

**Architecture:** Replace the current "list and display" steps 2-3 in `morning.md` with a workspace-aware triage loop that gathers signals (Outlook for Avitia, manual for Amuse), presents a triage table, confirms with the user, and batch-updates all affected files.

**Tech Stack:** Obsidian vault markdown, TaskNotes API, Outlook MCP (`outlook_email_search`)

---

### Task 1: Rewrite steps 2-3 in morning.md

**Files:**
- Modify: `.claude/skills/review/workflows/morning.md:17-47`

**Step 1: Replace step 2 (Check Workspaces) with workspace triage**

Replace lines 17-31 with the new step 2 that includes triage. The new step 2 should:

```markdown
### 2. Workspace Status Triage

For each active workspace, collect open tasks and check for completion signals.

**Workspace email mapping:**
| Workspace | Email MCP | Method |
|-----------|-----------|--------|
| Amuse | None (Gmail) | Manual triage |
| Avitia | `outlook_email_search` | Signal-assisted |

**For each workspace (Amuse, Avitia):**

#### 2a. Collect open tasks

Read planning-layer tasks:
```bash
echo "=== $ws ==="
[ -f "$ws/$ws.md" ] && grep "^status:" "$ws/$ws.md"
echo "--- Open Tasks ---"
[ -f "$ws/Tasks.md" ] && grep "^\- \[ \]" "$ws/Tasks.md"
```

Read execution-layer tasks scoped to this workspace:
```bash
for f in Tasks/*.md; do
  if [ -f "$f" ] && grep -q "projects:" "$f" && grep -q "$ws" "$f" && grep -q "status: open" "$f"; then
    echo "$(basename "$f" .md): $(grep "^due:" "$f" 2>/dev/null || echo 'no due date')"
  fi
done
```

#### 2b. Gather signals (Avitia only)

For Avitia, get `last_synced` date from `Avitia/Tasks.md` frontmatter, then search Outlook:

```
Use outlook_email_search MCP tool:
- Query: sent emails from Kam since last_synced date
- Match subject lines against open task titles
- If MCP unreachable, skip to manual triage
```

#### 2c. Present triage table

Present to user:

```
**[Workspace] Task Triage:**
| Task | Due | Signal | Suggested |
|------|-----|--------|-----------|
| Finalize ROM | Mar 14 ⚠️ | Sent email match | Done? |
| Review ticketing | — | No signal | Still open? |
```

- ⚠️ = overdue
- Signal column: "Email match: [subject]" for Avitia, "No email MCP" for Amuse

#### 2d. Confirm with user

Ask: "Which of these are done? (list numbers, 'all', or 'none')"

#### 2e. Update on confirmation

For each confirmed-done task:

1. **Update TaskNotes file** — set `status: done` and `dateCompleted: YYYY-MM-DD` in frontmatter
   ```bash
   # Via API if running:
   curl -X PUT "http://127.0.0.1:8090/api/tasks/Tasks%2F{task}.md" \
     -H "Content-Type: application/json" \
     -d '{"status": "done"}'
   # Or edit file directly if API is down
   ```

2. **Update workspace Tasks.md** — move `- [ ] Task...` from Active/Up Next to Done section with completion date

3. **Update Handoff.md** — if the task appears in the handoff's action items, check it off

4. **Bump last_synced** — update `last_synced` in workspace Tasks.md and Handoff.md frontmatter to today
```

**Step 2: Replace step 3 (Check Execution Tasks) with remaining-tasks summary**

Replace lines 33-47 with a simplified step 3 that shows what's left after triage:

```markdown
### 3. Remaining Open Tasks

After triage, show what's still open across all workspaces:

```bash
echo "=== Still Open ==="
for f in Tasks/*.md; do
  if [ -f "$f" ] && grep -q "status: open" "$f"; then
    title=$(grep "^title:" "$f" | sed 's/title: //')
    due=$(grep "^due:" "$f" | sed 's/due: //')
    project=$(grep -A1 "^projects:" "$f" | tail -1 | sed 's/.*"\[\[//' | sed 's/\]\]".*//')
    echo "- $title | $project | due: ${due:-none}"
  fi
done
```

Present: "After triage, you have X open tasks across Y workspaces."
```

**Step 3: Verify the full morning.md reads correctly**

Read the file end-to-end to confirm steps 1-7 flow naturally with the new triage integrated.

**Step 4: Commit**

```bash
git add .claude/skills/review/workflows/morning.md
git commit -m "feat: add status triage to morning routine steps 2-3

Cross-references open tasks against Outlook emails (Avitia) or
manual confirmation (Amuse) before presenting the daily plan.
Updates TaskNotes files, workspace Tasks.md, and Handoff.md on
confirmation."
```

---

### Task 2: Add triage candidate to runbook

**Files:**
- Modify: `Amuse/Runbook.md`

**Step 1: Move "Session-Start Status Triage" from Candidates to Active**

Add to the Active Automations section:

```markdown
### Session-Start Status Triage
- **Status:** Active | **Home:** Skill (`review` → morning workflow steps 2-3)
- **What:** Cross-references open tasks against email signals per workspace. Avitia uses Outlook MCP; Amuse uses manual confirmation. Updates task files, Tasks.md, and Handoff.md on user confirmation.
- **Owner:** @Kam
```

**Step 2: Commit**

```bash
git add Amuse/Runbook.md
git commit -m "docs: add session-start status triage to active automations in runbook"
```

---

## Verification

1. Trigger `morning routine` and confirm steps 2-3 present a triage table per workspace
2. Confirm Avitia workspace attempts Outlook email search (or falls back gracefully)
3. Confirm Amuse workspace presents tasks for manual confirmation
4. Mark a task done and verify: TaskNotes file updated, Tasks.md updated, Handoff.md updated
5. Confirm `last_synced` dates bumped
