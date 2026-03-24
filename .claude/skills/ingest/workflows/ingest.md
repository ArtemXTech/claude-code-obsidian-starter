# Ingestion Workflow

Pull data from all connected sources into workspace Inbox/ folders.

## Prerequisites

- M365 MCP connector must be available (for Outlook email + calendar)
- Slack MCP connector must be available (for Slack channels)
- Gmail reader script at `.claude/scripts/gmail-reader.py` with venv at `~/.config/google-tokens/venv/`
- OAuth tokens in `~/.config/google-tokens/` for each configured Gmail account
- If any source is unreachable, skip it gracefully and report

## Routing Configuration

```yaml
routing:
  slack:
    avitiabio: Avitia
    amuse: Amuse
  email:
    domain_map:
      "@avitia.bio": Avitia
      "@avitiabio.com": Avitia
      "@submersive.com": Amuse
      "@amuse.us": Amuse
    sender_map:
      "notifications@read.ai": Avitia
    keyword_fallback:
      - pattern: "ICHIP|liquid biopsy|ctDNA|BD-\\d+"
        workspace: Avitia
      - pattern: "Submersive|bathhouse|waitlist|Webflow"
        workspace: Amuse
  calendar:
    team_map:
      Avitia:
        - "@avitia.bio"
        - "@avitiabio.com"
        - "ruth"       # display name fallback (case-insensitive substring, only when no domain match)
        - "mauricio"
        - "anna"
        - "dmitri"
      Amuse:
        - "@submersive.com"
        - "@amuse.us"
        - "jee"
        - "chris"
        - "corvas"
    # Matching order: email domain first, then display name fallback
    cross_workspace: duplicate
  gmail:
    account_map:
      k-at-amuse-us: Amuse
      kkafimd-at-gmail-com: Medical
      vizucla-at-gmail-com: Personal
    sender_overrides:
      # Sender overrides take priority over account_map
      "noreply.business@bell.ca": Amuse
  fallback: Inbox/

slack:
  avitiabio:
    channels:
      - "#bizdev"
      - "#product-development"
      - "#software"
      - "#branding-marketing"
      - "#portal-redevelopment"
      - "#br-validation-team"
      - "#marketing"
    exclude:
      - "#random"
      - "#general"
      - "#careers"
  amuse:
    channels:
      - "#amusementpark"
    exclude:
      - "#random"
      - "#general"
```

## Stage 0: Determine scan window

Read state from `.claude/skills/ingest/state.json`.

- If a source's timestamp is `null` (first run for that source): use 48 hours ago. Apply 5-item cap for that source.
- Otherwise: use that source's timestamp as the scan window start.

Per-source tracking means if Slack fails but email succeeds, only Slack gets the first-run cap on retry.

## Stage 1: Email Ingestion

### 1a. Search inbox

```
Tool: mcp__claude_ai_Microsoft_365__outlook_email_search
Parameters:
  query: "*"
  folderName: "Inbox"
  afterDateTime: {scan_window_start}
  limit: 25
```

### 1b. Search sent items

```
Tool: mcp__claude_ai_Microsoft_365__outlook_email_search
Parameters:
  query: "*"
  folderName: "Sent Items"
  afterDateTime: {scan_window_start}
  limit: 25
```

### 1c. Route each email to workspace

For each email, determine workspace:

1. Check sender email against `domain_map` — if match, route to that workspace
2. Check sender against `sender_map` — if match, route (and flag Read.ai for Phase 1b parser)
3. Check subject + body against `keyword_fallback` patterns — if match, route
4. If no match: route to vault-root `Inbox/`

### 1d. Fetch full body for routed emails

For emails classified as potentially actionable (not newsletters, auto-replies, calendar RSVPs):

```
Tool: mcp__claude_ai_Microsoft_365__read_resource
Parameters:
  uri: "mail:///messages/{messageId}"
```

### 1e. Classify and write

Classify each email into category: `task | decision | blocker | fyi`

Skip entirely:
- Newsletters, marketing, automated notifications
- Calendar invites / RSVPs
- Purely social or greeting-only emails

For each surviving item, run dedup (Stage 4), then write using template.

**source_id format:** `email:{messageId}`

## Stage 1.5: Gmail Ingestion

### 1.5a. Invoke Gmail reader script

For each account in `gmail.account_map`, call the reader script:

```bash
~/.config/google-tokens/venv/bin/python3 .claude/scripts/gmail-reader.py \
  --account {account_slug} \
  --after {scan_window_for_this_account} \
  --limit 25
```

Use the scan window from `sources.gmail_{account_slug}` in state.json.
If the key is missing or `null`, use 48 hours ago and apply the 5-item cap.

If the script exits non-zero or returns an error JSON on stderr, log the failure
and skip this account. Continue to the next account. Do not abort the entire Gmail stage.

### 1.5b. Parse and route

Parse the JSON array output from stdout. For each message:
- Look up workspace from `gmail.account_map[account_slug]`
- Account identity is the routing signal — no domain_map/sender_map/keyword matching needed

### 1.5c. Classify and write

Same classification logic as Stage 1e (Outlook):
- Classify into: `task | decision | blocker | fyi`
- Skip newsletters, marketing, automated notifications, calendar RSVPs
- For each surviving item, run dedup (Stage 4), then write using template

**source_id format:** `gmail:{account_slug}:{messageId}`

This is intentionally distinct from Outlook's `email:{messageId}` to prevent cross-source ID collisions.

**source field:** `gmail` (extends the existing `slack|email|calendar|meeting` set)

### 1.5d. Graceful degradation

| Condition | Behavior |
|-----------|----------|
| Script not found | Skip all Gmail, report skipped |
| Token missing for one account | Skip that account, continue others |
| API error for one account | Skip that account, continue others |
| All accounts fail | Report all failures, continue to Stage 2 |

## Stage 2: Slack Ingestion

### 2a. Detect connected Slack workspaces

Run two probes to determine which Slack workspace(s) are reachable:

**Probe 1 (Avitia):**
```
Tool: mcp__claude_ai_Slack__slack_search_channels
Parameters:
  query: "bizdev"
  channel_types: "public_channel,private_channel"
  limit: 5
```

If results contain `#bizdev` or other known avitiabio channels → add `"avitiabio"` to `connected_slacks`.

**Probe 2 (Amuse):**
```
Tool: mcp__claude_ai_Slack__slack_search_channels
Parameters:
  query: "amusementpark"
  channel_types: "public_channel,private_channel"
  limit: 5
```

If results contain `#amusementpark` → add `"amuse"` to `connected_slacks`.

If `connected_slacks` is empty: report "No Slack workspace detected — skipping Slack ingestion." and proceed to Stage 3.

If both are detected (future multi-workspace MCP): ingest both.

### 2b. Read configured channels

For each workspace in `connected_slacks`, read the channel list from the matching config block above.

For each channel in that workspace's config:

```
Tool: mcp__claude_ai_Slack__slack_read_channel
Parameters:
  channel_name: "{channel-name}"
  limit: 50
  oldest: "{scan_window_start_unix_timestamp}"
```

Use the scan window from `sources.slack_{workspace_key}` in the state file. If the key is missing or `null`, use 48 hours ago and apply a 5-item cap.

### 2c. Filter and classify messages

For each channel's messages:

- Skip bot messages, join/leave notifications, simple emoji reactions
- Look for: action items, decisions, questions, status updates, shared links with context
- Group threaded replies — treat the thread as one item, not individual messages
- Classify into category: `task | decision | blocker | fyi`

### 2d. Write inbox items

For each surviving item, run dedup (Stage 4), then write to the workspace's `Inbox/` folder:

- Messages from avitiabio → `Avitia/Inbox/`
- Messages from amuse → `Amuse/Inbox/`

Routing is implicit from workspace detection — no keyword matching needed for Slack.

**source_id format:** `slack:{channelId}:{threadTs}` (or `messageTs` for non-threaded)

**source_id format reference:**

| Source | New format | Old format (backward compat) |
|--------|-----------|------------------------------|
| Email | `email:{messageId}` | `outlook:{messageId}` (from old inbox skill) |
| Slack | `slack:{channelId}:{threadTs}` | N/A |
| Calendar | `calendar:{eventId}` | N/A |

## Stage 3: Calendar Ingestion

### 3a. Search upcoming events

```
Tool: mcp__claude_ai_Microsoft_365__outlook_calendar_search
Parameters:
  query: "*"
  startDateTime: "{today}"
  endDateTime: "{today + 3 days}"
  limit: 20
```

### 3b. Route each event to workspace

For each event, check attendee emails:

1. Match attendee email domains against `calendar.team_map` domain entries (e.g., `@avitia.bio`)
2. If no domain match, check attendee display names against name entries (case-insensitive substring)
3. If attendees span both workspaces: create item in BOTH workspace Inboxes (`cross_workspace: duplicate`)
4. If still no match: route to vault-root `Inbox/`

### 3c. Write calendar items

Write each event as an inbox item with `category: meeting`, `source: calendar`.

Include in body: event time, attendees, description/agenda if present, location.

**source_id format:** `calendar:{eventId}`

## Stage 4: Deduplication

Before writing ANY item, check for duplicates:

**Check 1 — source_id match (new format):**
```bash
grep -rl "source_id: {source_id}" {workspace}/Inbox/ 2>/dev/null
```

**Check 2 — source_id match (old inbox format, Avitia only):**
```bash
grep -rl "source_id: outlook:{messageId}" Avitia/Inbox/ 2>/dev/null
```

**Check 2b — Gmail source_id match:**
```bash
grep -rl "source_id: gmail:{account_slug}:{messageId}" {workspace}/Inbox/ 2>/dev/null
```

If either check finds a match → skip silently.

**Check 3 — semantic match against existing open tasks:**
Collect open tasks:
```bash
grep "^\- \[ \]" {workspace}/Tasks.md 2>/dev/null
```

If the item substantially duplicates an existing task, skip and note as "signal for existing task" (reported in summary).

## Stage 5: Write items

For each item that passes dedup:

1. Generate filename: `{source}-{YYYY-MM-DD}-{short-slug}.md`
2. Fill template from `.claude/skills/ingest/templates/inbox-item.md`
3. Write to `{workspace}/Inbox/`

## Stage 5.5: Calendar Event Detection

After writing inbox items, scan all newly written items for calendar-worthy content.

### Detection criteria

An item is calendar-worthy if ANY of:
- `category: meeting` in frontmatter
- Body contains a specific date + time (not just a date)
- Keywords in subject/body: "meeting", "AGM", "assemblée", "appointment", "call", "webinar", "deadline" combined with a future datetime

### Extraction

For each detected item, extract:
- **title**: event summary (from subject or body)
- **start**: datetime (ISO 8601)
- **end**: datetime (default: start + 1 hour)
- **location**: physical address, Zoom/Teams link, or "Virtual"
- **description**: 1-2 sentence context

### Push to Apple Calendar

Use workspace-to-calendar mapping:

```yaml
calendar_push:
  Avitia: "kkafi@icdh.com"        # Outlook — work meetings
  Amuse: "canyou@amuse.us"        # Google — Amuse business
  Personal: "Kam's Fam Calendar"   # Family, friends, social events
  Medical: "Home"                  # Physician/community
```

```bash
python3 .claude/scripts/ical-writer.py \
  --calendar "{calendar_from_mapping}" \
  --title "{title}" \
  --start "{start}" \
  --end "{end}" \
  --location "{location}" \
  --notes "{description}"
```

On success, update the inbox item:
- Set `linked_task: "calendar:ical:{eventUID}"`
- Add `## 📅 Calendar Event` section with extracted details

### Graceful degradation

If ical-writer.py fails (Calendar.app not responding, calendar not found):
- Log the error
- Still write the `## 📅 Calendar Event` section with extracted details (manual fallback)
- Do NOT block the rest of the pipeline

## Stage 5.6: Auto-Task Promotion (High-Confidence Only)

After writing inbox items, check for HIGH-CONFIDENCE task items that can be auto-promoted without manual triage.

### Auto-promotion criteria (ALL must be high-confidence)

An item qualifies for auto-promotion if ANY of:
- Has an **explicit deadline** in the email body ("due by March 26", "deadline Thursday", "expires on")
- Is a **direct ask** to Kam ("please review", "action required", "your input needed", "complete the")
- Is `category: blocker`

Items that do NOT qualify (stay as `status: new` for manual triage):
- General FYIs, newsletters, meeting notes without action items
- Ambiguous asks ("let's discuss", "thoughts?", "FYI")
- Items without clear ownership or deadline

### Auto-promotion writes (3 layers)

1. **TaskNotes API** (execution layer):
```bash
curl -X POST "http://127.0.0.1:8090/api/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "{task title}",
    "status": "open",
    "priority": "normal",
    "projects": ["[[{Workspace}]]"],
    "due": "{due date if known}"
  }'
```
If API unreachable, create task file directly in `Tasks/`.

2. **Workspace Tasks.md** (planning layer):
```markdown
## Active
- [ ] {task title} — {one-line context} — @Kam | Due: {date} | Source: `Inbox/{filename}`
```

3. **Apple Reminders** (phone visibility — ONLY if has due date):
```bash
python3 .claude/scripts/reminder-writer.py \
  --list "{workspace}" \
  --title "{task title}" \
  --due "{YYYY-MM-DD}" \
  --notes "Source: {workspace}/Inbox/{filename}"
```

Workspace-to-list mapping:
```yaml
reminder_push:
  Avitia: "Avitia"
  Amuse: "Amuse"
  Personal: "Personal"
  Medical: "Medical"
  fallback: "Inbox"
```

4. Update inbox item: `status: triaged`, `linked_task: Tasks/{filename}.md`

### Graceful degradation

- TaskNotes API down → create file in Tasks/ directly
- Reminders.app unresponsive → skip, task still exists in Obsidian
- Do NOT block the rest of the pipeline for any single layer failure

## Stage 5.7: Reminders Reverse Sync

Read Apple Reminders to sync changes from iPhone back to Obsidian.

### 5.7a: Completed reminders → mark done in Obsidian

```bash
python3 .claude/scripts/reminder-reader.py --completed --since "{last_reminders_sync}"
```

For each completed reminder:
1. Match to Obsidian task:
   - **ID match**: `grep -rl "reminder_id: \"{reminder_id}\"" Tasks/ */Inbox/`
   - **Title match** (fallback): fuzzy match title against open tasks in `{list_name}/Tasks.md`
2. If matched:
   - TaskNotes: update `status: done` via API or sed
   - Tasks.md: move from `## Active` to `## Done (this week)` with completion date
   - Inbox item (if exists): set `status: acted-on`
3. If no match: log and skip (legacy reminder not from this system)

### 5.7b: New phone-captured reminders → create inbox items

```bash
python3 .claude/scripts/reminder-reader.py --open --list "Inbox"
```

For each open reminder in the "Inbox" list:
1. Check if already exists in Obsidian: `grep -rl "reminder_id: \"{id}\"" */Inbox/`
2. If new, create inbox item:
   - Route to vault-root `Inbox/` (workspace TBD during triage)
   - Set `source: reminders`, `category: task`, `reminder_id: "{id}"`
   - File: `reminders-{YYYY-MM-DD}-{short-slug}.md`
3. Present in next triage for workspace assignment

For open reminders in workspace lists (Avitia, Amuse, Personal, Medical):
1. Check if already in Obsidian by reminder_id
2. If new (created on phone, not by the system), create inbox item in `{Workspace}/Inbox/`

### 5.7c: Update sync state

Update `sources.reminders` in state.json. First run = look back 7 days.

### Graceful degradation

If Reminders.app is unresponsive or reminder-reader.py fails:
- Skip this stage entirely
- Do NOT block email/gmail/slack/calendar ingestion

## Stage 6: Archive cleanup

Move items with `status: acted-on` or (`status: triaged` AND `linked_task` is set) that are older than 14 days:

```bash
# For each workspace inbox
mkdir -p {workspace}/Inbox/archive
# Move qualifying files (check date: field in frontmatter, not filesystem mtime)
```

## Stage 7: Update state

Update `.claude/skills/ingest/state.json` — only update timestamps for sources that successfully ran:

```json
{
  "last_run": "{now ISO 8601}",
  "sources": {
    "email": "{now or previous value if skipped}",
    "gmail_k-at-amuse-us": "{now or previous value if skipped}",
    "gmail_vizucla-at-gmail-com": "{now or previous value if skipped}",
    "gmail_kkafimd-at-gmail-com": "{now or previous value if skipped}",
    "gmail_kam4sale-at-gmail-com": "{now or previous value if skipped}",
    "slack_avitiabio": "{now or previous value if skipped}",
    "slack_amuse": "{now or previous value if skipped}",
    "calendar": "{now or previous value if skipped}"
  }
}
```

If a source key is missing from the state file (e.g., `slack_amuse` on first run from a new account), treat it identically to `null` — use 48-hour lookback with 5-item cap.

## Stage 8: Summary

Report what was ingested:

```markdown
## Ingestion Complete — {date}

| Source | Items Found | Items Captured | Skipped (dedup) | Workspace |
|--------|------------|----------------|-----------------|-----------|
| Email (Outlook) | X | Y | Z | Amuse: A, Avitia: B, Unrouted: C |
| Gmail (k@amuse.us) | X | Y | Z | Amuse |
| Gmail (vizucla@gmail.com) | X | Y | Z | Inbox |
| Gmail (kkafimd@gmail.com) | X | Y | Z | Inbox |
| Gmail (kam4sale@gmail.com) | X | Y | Z | Inbox |
| Slack (avitiabio) | X | Y | Z | Avitia |
| Slack (amuse) | X | Y | Z | Amuse |
| Calendar | X | Y | Z | Mixed |

Only include Slack rows for workspaces that were actually detected and ingested. Omit rows for undetected workspaces.
Only include Gmail rows for accounts that were actually attempted. If an account's token is missing, note as skipped.

Signals for existing tasks: N items matched open tasks (not captured)
Archived: N old items moved to archive/

{If any source had null/missing timestamp: "First run for {source} — capped at 5 items. Run again to catch remaining."}
{If any source skipped: "Skipped: {source} — {reason}"}
```
