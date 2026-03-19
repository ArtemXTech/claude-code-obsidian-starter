# Ingestion Workflow

Pull data from all connected sources into workspace Inbox/ folders.

## Prerequisites

- M365 MCP connector must be available (for email + calendar)
- Slack MCP connector must be available (for Slack channels)
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

## Stage 2: Slack Ingestion

### 2a. Detect connected workspace

```
Tool: mcp__claude_ai_Slack__slack_search_channels
Parameters:
  query: "bizdev"
  channel_types: "public_channel,private_channel"
  limit: 5
```

Check if results contain known Avitia channels (`#bizdev`, `#product-development`). If yes: connected to avitiabio. If no known channels found: report "Unknown Slack workspace — skipping Slack ingestion."

### 2b. Read configured channels

For each channel in the avitiabio config (see Slack channel list in routing config above):

```
Tool: mcp__claude_ai_Slack__slack_read_channel
Parameters:
  channel_name: "{channel-name}"
  limit: 50
  oldest: "{scan_window_start_unix_timestamp}"
```

### 2c. Filter and classify messages

For each channel's messages:

- Skip bot messages, join/leave notifications, simple emoji reactions
- Look for: action items, decisions, questions, status updates, shared links with context
- Group threaded replies — treat the thread as one item, not individual messages
- Classify into category: `task | decision | blocker | fyi`

### 2d. Write inbox items

For each surviving item, run dedup (Stage 4), then write to `Avitia/Inbox/` using template.

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
    "slack_avitiabio": "{now or previous value if skipped}",
    "calendar": "{now or previous value if skipped}"
  }
}
```

## Stage 8: Summary

Report what was ingested:

```markdown
## Ingestion Complete — {date}

| Source | Items Found | Items Captured | Skipped (dedup) | Workspace |
|--------|------------|----------------|-----------------|-----------|
| Email | X | Y | Z | Amuse: A, Avitia: B, Unrouted: C |
| Slack (avitiabio) | X | Y | Z | Avitia |
| Calendar | X | Y | Z | Mixed |

Signals for existing tasks: N items matched open tasks (not captured)
Archived: N old items moved to archive/

{If any source had null timestamp: "First run for {source} — capped at 5 items. Run again to catch remaining."}
{If any source skipped: "Skipped: {source} — {reason}"}
```
