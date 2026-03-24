# Daily Ops Triage Workflow

Intelligent daily triage that cross-references all sources and produces a synthesized briefing.

## Step 1: Run Ingestion

Call the ingest skill workflow:

→ Follow: `.claude/skills/ingest/workflows/ingest.md`

If ingestion reports all sources skipped, continue anyway — there may be existing `status: new` items from previous runs.

## Step 2: Collect New Items

Grep for all `status: new` inbox items across all locations:

```bash
grep -rl "status: new" Amuse/Inbox/ Avitia/Inbox/ Inbox/ 2>/dev/null
```

For each found file, extract frontmatter:
```bash
grep "^type:\|^source:\|^workspace:\|^category:\|^date:\|^from:\|^subject:\|^status:" "{file}"
```

## Step 3: Load Context

### 3a. Open tasks (both layers)

**Execution layer (TaskNotes API):**
```bash
curl -s "http://127.0.0.1:8090/api/tasks?status=open&status=in-progress" 2>/dev/null
```

If API unreachable, fall back to file-based:
```bash
for f in Tasks/*.md; do
  [ -f "$f" ] && grep -l "status: open\|status: in-progress" "$f"
done
```

**Planning layer:**
```bash
grep "^\- \[ \]" Amuse/Tasks.md Avitia/Tasks.md 2>/dev/null
```

### 3b. Today's calendar

Check for calendar items ingested in Step 1, or from previous runs:
```bash
grep -rl "source: calendar" Amuse/Inbox/ Avitia/Inbox/ Inbox/ 2>/dev/null | while read f; do
  grep "date: $(date +%Y-%m-%d)" "$f" && echo "$f"
done
```

### 3c. Recent meetings

**Granola meetings (last 3 days):**
```bash
ls -1 Meetings/*.md 2>/dev/null | tail -5
```

**Read.ai meeting items in Inbox (last 3 days):**
```bash
grep -rl "category: meeting" Avitia/Inbox/ 2>/dev/null
```

### 3d. Recent decisions

```bash
head -30 Amuse/Decisions.md
head -30 Avitia/Decisions.md
```

## Step 4: Cross-Reference and Synthesize

With all context loaded, analyze for:

### Conflicts & Alerts
- Meeting today about topic X, but related task is overdue or has no prep
- Email contradicts an existing task or decision
- Two tasks that are implicitly dependent but not linked

### Stale Items
- Tasks with due dates in the past
- Commitments from meetings (last 7 days) with no corresponding task
- Inbox items that have been `status: new` for more than 3 days

### Connections
- Slack thread that relates to an open Jira ticket or task
- Email that echoes a recent meeting discussion
- Same person appearing across multiple sources on same topic

### Today's Priorities
Synthesize — don't just list. Consider:
- What's due today or overdue
- What meetings are coming and what prep is needed
- What's been stale the longest
- Energy allocation across workspaces

Present using the briefing template at `.claude/skills/daily-ops/templates/briefing.md`.

## Step 5: Interactive Triage

For each `status: new` item, present a recommendation:

| # | Source | Summary | Workspace | Recommendation |
|---|--------|---------|-----------|----------------|

Then ask: **"How should I triage these? (e.g., '1,2 → Task, 3 → FYI, 4-5 → Dismiss', or 'all FYI')"**

Wait for user confirmation before making any changes.

### Triage Actions

**→ Task** (task promotion — tri-layer write):

1. Create TaskNotes execution task:
```bash
curl -X POST "http://127.0.0.1:8090/api/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "{task title}",
    "status": "open",
    "priority": "normal",
    "projects": ["[[{Workspace}]]"],
    "due": "{YYYY-MM-DD if known}"
  }'
```
If API unreachable, create task file directly in `Tasks/`.

2. Append to `{Workspace}/Tasks.md` under `## Active`:
```markdown
- [ ] {task title} — {one-line context} — @Kam | Due: {date} | Source: `Inbox/{filename}`
```

3. **Push to Apple Reminders** (only if task has a due date or explicit urgency):
```bash
python3 .claude/scripts/reminder-writer.py \
  --list "{Workspace}" \
  --title "{task title}" \
  --due "{YYYY-MM-DD}" \
  --notes "Source: {Workspace}/Inbox/{filename}"
```
Workspace-to-list: Avitia→"Avitia", Amuse→"Amuse", Personal→"Personal", Medical→"Medical"

4. Update inbox item: set `status: triaged`, `linked_task: Tasks/{task-filename}.md`

5. Check `{Workspace}/Handoff.md` — if the task appears as an action item, check it off:
```bash
grep -n "{task title keywords}" {Workspace}/Handoff.md
# If found as "- [ ]", change to "- [x]"
```

**→ Decision:**

1. Append to `{Workspace}/Decisions.md`:
```markdown
### {today's date} — {decision title}

- **Decision:** {what was decided}
- **Rationale:** {why, if stated}
- **Decided by:** {who}
- **Reference:** `{Workspace}/Inbox/{filename}`
```

2. Update inbox item: set `status: triaged`

**→ FYI:**
Update inbox item: set `status: triaged`

**→ Calendar:**

1. Extract date, time, location, and key details from the inbox item body
2. Present calendar event summary for user confirmation:
   - What, When, Where, Action needed
3. Determine target calendar from workspace mapping:
   - Avitia → `kkafi@icdh.com`, Amuse → `canyou@amuse.us`
   - Personal → `Kam's Fam Calendar`, Medical → `Home`
4. On user confirmation, push to Apple Calendar:
```bash
python3 .claude/scripts/ical-writer.py \
  --calendar "{target_calendar}" \
  --title "{title}" --start "{start}" --end "{end}" \
  --location "{location}" --notes "{description}"
```
5. Update inbox item: add `## 📅 Calendar Event` section, set `linked_task: "calendar:ical:{eventUID}"`
6. Set `status: triaged`
7. If ical-writer fails, fall back to manual — extract details in inbox item for user to add

**→ Dismiss:**
Update inbox item: set `status: acted-on`

**→ Relate:**
Add wikilink to `related:` field in inbox item frontmatter. Keep `status: new`.

### Financial tagging

When triaging items that are bills, insurance notices, pay stubs, receipts, or tax-relevant documents, set the `financial_type` field:

```yaml
financial_type: "utility|insurance|payroll|tax|expense|receipt"
```

This enables retrieval via `grep -rl "financial_type:"` for tax season and financing applications.

### Cross-workspace rerouting

If an item landed in the wrong workspace (e.g., Bell Business bill via vizucla → Personal, but it's an Amuse expense):
1. Move the file to the correct `{Workspace}/Inbox/`
2. Update `workspace:` in frontmatter
3. Add the sender to `sender_overrides` in ingest routing config to prevent recurrence

## Step 6: Summary

```markdown
Triage complete:
- {N} items → Task (created in TaskNotes + {Workspace}/Tasks.md)
- {N} items → Decision (appended to Decisions.md)
- {N} items → Calendar (details extracted)
- {N} items → FYI
- {N} items → Dismissed
- {N} items → Related (still pending)
- {N} items remaining as new
- {N} items rerouted to different workspace
```
