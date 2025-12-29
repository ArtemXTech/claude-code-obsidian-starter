# Claude Code Starter Kit for Obsidian

A working Obsidian vault with Claude Code skills pre-configured. Open it, try a command, see the magic.

## Quick Start

### 1. Download & Open

```bash
# Clone this repo (or download zip)
git clone https://github.com/ArtemXTech/claude-code-obsidian-starter.git

# Open in Obsidian
# File → Open Vault → Select this folder

# Open in Claude Code
cd claude-code-obsidian-starter
claude .
```

### 2. Setup TaskNotes (2 minutes)

1. In Obsidian, go to **Settings → Community Plugins → TaskNotes**
2. Enable **HTTP API**
3. Copy the **API Token**
4. Create `.env` file in vault root:
   ```
   TASKNOTES_API_KEY=paste_your_token_here
   ```

### 3. Try These Commands

```
"Create a task: Review the workshop feedback, high priority"
```
Creates a task file in Obsidian instantly.

```
"Show my tasks"
```
Lists all your tasks in a table.

```
"What should I work on?"
```
Shows your in-progress tasks.

## What's Included

### Skills (AI capabilities)
| Skill | What It Does |
|-------|--------------|
| tasknotes | Create, update, list, delete tasks |
| obases | Query Obsidian Bases (structured data) |
| morning-routine | Daily overview + create daily note |

### Obsidian Plugins (pre-installed)
- TaskNotes - Task management with HTTP API
- Dataview - Query your notes like a database
- headless-bases - API access to Obsidian Bases

### Folder Structure
```
├── Daily/           # Daily notes
├── Tasks/           # Your tasks (auto-managed)
├── Goals/           # Goal tracking
├── Templates/Bases/ # Tasks.base, Goals.base
└── .claude/skills/  # AI skills
```

## Full Guide

See `guide/quick-start-guide.pdf` for detailed setup instructions.

## Want More?

This starter kit is a taste of what's possible.

Join the workshop to build your complete Personal AI System:
- Custom skills for your workflow
- Calendar integration
- Morning briefings

https://workshop.artemzhutov.com

---

Made by Artem Zhutov - https://www.youtube.com/@ArtemXTech
