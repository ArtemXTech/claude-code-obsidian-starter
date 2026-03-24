# Obsidian + Claude Code Agent System

Personal knowledge management vault with integrated AI agent capabilities. Mobile-accessible via Telegram. Inspired by [@ArtemXTech](https://x.com/ArtemXTech) setups.

## Architecture

```
Vault Root
├── Amuse/              # Workspace: clients, tasks, decisions
├── Avitia/             # Workspace: CSO operations
├── Daily/              # Daily notes + dialogue logs
├── Tasks/              # TaskNotes plugin target
├── Meetings/           # Granola meeting sync
├── Notes/Plans/        # Day plans (accountability reference)
├── Notes/Projects/     # Session dialogues, research
├── Automations/        # Scheduled loop files (source of truth)
├── Inbox/              # Unrouted items
├── Claude-Sessions/    # Session index
├── Bases/              # Obsidian structured data views
├── .claude/skills/     # 13 Claude Code skills
└── .claude/scripts/    # Session launcher, utilities
```

## Skills

| Skill | Trigger | Purpose |
|-------|---------|---------|
| ingest | "pull updates", "ingest" | Email/Slack/calendar → workspace Inboxes |
| daily-ops | "daily ops", "briefing" | Cross-source triage + intelligence |
| review | "morning routine", "weekly review" | Time-boxed review workflows |
| think | "think", "what's emerging" | Pattern detection across vault |
| automations | "/automations" | Manage scheduled loops from Automations/ |
| reddit-read | "check reddit", "reddit-read" | Scan subreddits via WebSearch |
| ytcli | "ytcli", "youtube transcript" | YouTube transcript extraction |
| journal | "journal", "quick note" | Quick capture to daily note |
| research | "research", "look up" | Web research → workspace Inbox |
| query | data lookups | Grep-based vault queries |
| client | "who needs follow-up?" | Client relationship tracking |
| granola | "sync my meetings" | Granola meeting sync |
| tasknotes | task CRUD | TaskNotes API (port 8090) |

## Automations (Automations/)

| File | Interval | Purpose |
|------|----------|---------|
| accountability-check.md | 30m | Drift detection vs day plan |
| executive-coach.md | 3h | Pattern interrupt — hard questions |
| source-monitor.md | 8h | Reddit + YouTube content scan |

Run `/automations` to schedule all enabled loops. Files are source of truth — session dies, jobs die, files stay.

## Mobile Access (Telegram)

```bash
# Launch persistent agent with Telegram channel
bash .claude/scripts/start-channel-session.sh
# Attach: tmux attach -t claude-agent
```

Bot: `@kam_agent_bot` — DM to interact. Full vault access (skills, MCP, memory).

Auto-restart via launchd: `~/Library/LaunchAgents/com.user.claude-agent.plist`

## Memory Layers

| Layer | Location | Purpose |
|-------|----------|---------|
| Auto-memory | `~/.claude/projects/*/memory/` | Session-persistent markdown |
| project-memory | `~/.project-memory/memory.db` | SQLite tagged notes |
| claude-mem | `~/.claude-mem/` | Vector DB + observations |
| Session logs | `~/.claude/projects/` | JSONL raw transcripts |
| Dialogue logs | `Daily/YYYY-MM-DD.dialogue.md` | Real-time exchange log |
| Session dialogues | `Notes/Projects/session-dialogues/` | Clean post-session extraction |

## Hooks Pipeline

| Event | Script | Purpose |
|-------|--------|---------|
| UserPromptSubmit | memory-status.sh | Check memory DB status |
| UserPromptSubmit | log-exchange.sh | Real-time dialogue logging |
| PostToolUse (Write/Edit) | privacy-guard.sh | Privacy check on writes |
| Stop | write-back-check.sh | Remind about Drive sync |
| Stop | deliverable-tracker.sh | Track deliverables |
| Stop | index-sessions.sh | Extract sessions → QMD |
| Stop | extract-dialogue.sh | Clean dialogue extraction |

## MCP Servers

claude-mem, voicemode, Gmail, project-memory, Claude in Chrome, Claude Preview, M365 (Outlook/Calendar), Slack

## Scheduled Tasks

| Task | Schedule | Purpose |
|------|----------|---------|
| morning-routine | 7:07 AM weekdays | Full workspace triage |
| drive-sync-check | 9:05 AM weekdays | Local vs Drive file staleness |

## Quick Start

```
"morning routine"     → Start your day
"daily ops"           → Intelligent cross-source triage
"pull updates"        → Ingest from email, Slack, calendar
"what's emerging"     → Think across accumulated data
/automations          → Start all scheduled loops
"journal: <thought>"  → Quick capture to daily note
"research <topic>"    → Web research to vault
```
