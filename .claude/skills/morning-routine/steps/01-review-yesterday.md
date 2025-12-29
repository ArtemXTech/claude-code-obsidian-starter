# Review Yesterday

## Task

Look back at yesterday to set context for today.

## Steps

1. **Find yesterday's notes:**
   ```bash
   find Daily -name "$(date -v-1d +%Y-%m-%d)*" -type f 2>/dev/null
   ```

2. **Read what you find:**
   - Morning Check-in (mood, energy, intentions)
   - Any other daily notes

3. **Summarize briefly:**
   - What happened yesterday?
   - Any wins or blockers?
   - Anything carried over to today?

4. **Present to user:**
   > "Yesterday you were feeling [X], focused on [Y]. You [accomplished/struggled with Z]."

## If No Notes Found

Just say: "No notes from yesterday. Let's start fresh!"

Then proceed to the check-in.
