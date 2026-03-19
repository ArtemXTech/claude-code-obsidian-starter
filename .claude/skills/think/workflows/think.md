# Think Workflow

Surface emergent patterns from accumulated vault data.

## Step 0: Determine scope

**Default:** Last 7 days across all workspaces.

**User overrides:**
- "think about Avitia only" → filter to Avitia sources
- "think about the last month" → extend window to 30 days
- "think about Amuse only" → filter to Amuse sources

Parse the user's trigger phrase for scope modifiers before proceeding.

## Step 1: Collect Data

Scan all sources within the temporal window. Count items as you go (for `sources_scanned` in output).

### 1a. Inbox items (all statuses — new, triaged, acted-on)

```bash
# Find all inbox items within time window (exclude archive/)
for dir in Amuse/Inbox Avitia/Inbox Inbox; do
  [ -d "$dir" ] && find "$dir" -name "*.md" -not -path "*/archive/*"
done
```

Read frontmatter + body of each qualifying file. Filter by `date:` field against the temporal window.

### 1b. Tasks (both layers)

**Planning layer:**
```bash
cat Amuse/Tasks.md Avitia/Tasks.md 2>/dev/null
```

**Execution layer:**
```bash
curl -s "http://127.0.0.1:8090/api/tasks" 2>/dev/null
```

If API unreachable, read from `Tasks/*.md` files directly.

### 1c. Decisions

```bash
cat Amuse/Decisions.md Avitia/Decisions.md 2>/dev/null
```

Focus on entries within the temporal window.

### 1d. Project context (Handoffs)

```bash
cat Amuse/Handoff.md Avitia/Handoff.md 2>/dev/null
```

These provide the "stated priorities" baseline for drift detection.

### 1e. Meetings

```bash
# Granola meetings within window
ls -1 Meetings/*.md 2>/dev/null
```

Read notes and transcript summaries for meetings in the window.

### 1f. Daily notes and past thinking outputs

```bash
ls -1 Daily/*.md 2>/dev/null
```

Read recent daily notes. If past thinking outputs exist, note what patterns were already surfaced (avoid repeating stale observations).

### 1g. Sessions

```bash
ls -1 Amuse/Sessions/*.md 2>/dev/null
```

## Step 2: Pattern Analysis

With all data loaded, systematically look for each pattern type:

### Cross-workspace echoes
Same topic, person, or entity appearing in BOTH Amuse and Avitia data within the window. These are significant because the user manages both workspaces and may not realize when themes overlap.

### Recurring themes
A person, topic, or keyword surfacing 3+ times across DIFFERENT sources (not just the same Slack channel). Frequency across source types is more significant than frequency within one source.

### Unanswered questions
Scan meeting notes and emails for question marks, "need to decide", "TBD", "open question" — then check if a corresponding task or decision entry exists. If not, it's unanswered.

### Strategic tensions
Look for workstreams whose goals or resource demands conflict. Example: two tasks due the same week that both require Kam's full attention.

### Stale commitments
Action items from meetings (look for "will do", "I'll", "action:", "- [ ]" in meeting notes) that have no matching task in Tasks.md or TaskNotes.

### Emerging opportunities
Connections between contacts, capabilities, or needs across workspaces that haven't been explicitly linked. Look for: same person mentioned in different contexts, complementary needs/offers, timing coincidences.

### Drift detection
Compare current activity (recent tasks, inbox items, meetings) against the priorities stated in Handoff.md. Flag significant divergence — activity that doesn't serve any stated priority, or stated priorities with zero recent activity.

## Step 3: Write Output

Create `Daily/{YYYY-MM-DD}. Thinking.md` using the template at `.claude/skills/think/templates/thinking.md`.

**Quality bar for patterns:**
- Each pattern must reference specific items (file names, task titles, meeting names)
- "So what" must be actionable — a question to answer, a decision to make, or a connection to explore
- Provocations should be genuinely non-obvious, not restatements of existing tasks

**Quality bar for Provocations (examples of good provocations):**
- "Ruth mentioned Burning Rock benchmarking in Monday's BD call, and Mauricio's #software thread about CGP panel integration references the same dataset. Neither workstream knows about the other — is there a shared dependency here?"
- "You've had 3 meetings about Thailand expansion in the past 2 weeks but no new tasks were created. Is this stalled, or is the work happening off-platform?"
- "The Submersive waitlist launch is 11 days out and the tech sprint has been 'unblocked' for 5 days with no commits. What's the blocker behind the blocker?"

If fewer than 2 patterns are found (e.g., not enough data has accumulated), report: "Not enough accumulated data for meaningful pattern detection. Run daily ingestion for a few more days, then try again."

## Step 4: Present to User

After writing the file, present the key findings conversationally. Don't just dump the file — highlight the 1-2 most important patterns and ask: "Any of these worth digging into?"
