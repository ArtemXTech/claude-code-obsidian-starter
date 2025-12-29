---
name: morning-routine
description: Run the morning routine workflow. Use when user says "start my morning", "morning routine", or "daily check-in".
---

# Morning Routine

Interactive morning workflow that reviews yesterday, does a check-in, reviews goals, and plans the day.

## Trigger

User says: "start my morning", "morning routine", "let's do the morning", "daily check-in"

## Workflow Steps

Run these in sequence. Each step is in `{baseDir}/steps/`.

### 1. Review Yesterday
Read `{baseDir}/steps/01-review-yesterday.md` and execute it.
- Find and read recent Daily notes
- Summarize what happened yesterday
- Identify patterns from last 3 days

### 2. Morning Check-in  
Read `{baseDir}/steps/02-check-in.md` and execute it.
- Ask reflection questions
- Capture mood, energy, sleep
- Create today's Morning Check-in note

### 3. Review Goals
Read `{baseDir}/steps/03-review-goals.md` and execute it.
- Query active goals using the query skill
- Ask about progress on each
- Update goal notes if needed

### 4. Plan the Day
Read `{baseDir}/steps/04-plan-day.md` and execute it.
- Based on goals and energy, suggest today's focus
- Create tasks for today
- Optional: time-block the calendar

## Quick Start

If user just wants a quick version:
```
1. Query goals: query.py goals
2. Query tasks: query.py tasks  
3. Ask: "What's your main focus today?"
4. Create 1-3 tasks for the day
```

## Files Created

- `Daily/YYYY-MM-DD. Morning Check-in.md` - Daily reflection
- Tasks created via tasknotes skill

## Dependencies

- query skill (for goals/tasks)
- tasknotes skill (for creating tasks)
- Obsidian running with headless-bases
