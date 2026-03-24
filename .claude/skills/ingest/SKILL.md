---
name: ingest
description: Pull data from Outlook email, Gmail, Slack, and calendar into workspace Inbox/ folders as structured markdown. Use when user says "ingest", "pull updates", "sync sources", or during daily-ops.
---

# Ingest Skill

Multi-source ingestion pipeline. Pulls Outlook email, Gmail (3 accounts), Slack, and calendar data into workspace-specific Inbox/ folders.

## How It Works

Queries M365 MCP (Outlook email, calendar), Gmail API (3 accounts via local script), and Slack MCP (channels) for new items since last run. Classifies each item by workspace using routing rules, writes structured markdown to the appropriate Inbox/ folder.

## Triggers

- "ingest", "pull updates", "sync sources"
- Called automatically by daily-ops skill as step 1

## Workflow

→ Follow: `.claude/skills/ingest/workflows/ingest.md`

## Output

Items written to `{Workspace}/Inbox/` as markdown files:

- **File naming:** `{source}-{YYYY-MM-DD}-{short-slug}.md`
- **Categories:** `task`, `decision`, `blocker`, `fyi`, `meeting`
- **Frontmatter:** See `templates/inbox-item.md` for schema

## Sources

| Source | Method | Phase | Target |
|--------|--------|-------|--------|
| Outlook email | M365 MCP `outlook_email_search` | 1 | Avitia/Inbox/ (via routing) |
| Gmail (k@amuse.us) | Local script `gmail-reader.py` via Bash | 1.5 | Amuse/Inbox/ |
| Gmail (kkafimd@gmail.com) | Local script `gmail-reader.py` via Bash | 1.5 | Medical/Inbox/ |
| Gmail (vizucla@gmail.com) | Local script `gmail-reader.py` via Bash | 1.5 | Personal/Inbox/ |
| Slack (Avitia) | Slack MCP `slack_read_channel` | 2 | Avitia/Inbox/ |
| Slack (Amuse) | Slack MCP `slack_read_channel` | 2 | Amuse/Inbox/ |
| Calendar | M365 MCP `outlook_calendar_search` | 3 | (via routing) |
| Read.ai digests | M365 MCP (email, special parser) | 1b | Avitia/Inbox/ |

## Integration Points

| System | How |
|--------|-----|
| Daily Ops | Calls ingest as step 1 |
| Morning routine | Via daily-ops |
| TaskNotes | Task/blocker items can be promoted via daily-ops triage |
| Existing inbox skill | Superseded — see migration notes in spec |

## Graceful Degradation

| Source | If unavailable | Behavior |
|--------|---------------|----------|
| M365 MCP | Unreachable | Skip Outlook email + calendar, report skipped |
| Gmail script | Missing/broken | Skip all Gmail accounts, report skipped |
| Gmail token | Missing for account | Skip that account, continue others |
| Slack MCP | Unreachable | Skip Slack, report skipped |

## MCP Tools Used

| Tool | Purpose |
|------|---------|
| `outlook_email_search` | Search Outlook inbox/sent by date |
| `read_resource` | Fetch full Outlook email body |
| `outlook_calendar_search` | Get upcoming events |
| `slack_search_channels` | Detect connected workspace |
| `slack_read_channel` | Read channel messages |
| Bash (`gmail-reader.py`) | Fetch Gmail messages (3 accounts, local OAuth) |
