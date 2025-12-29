# Review Goals

## Task

Show active goals and check in on progress.

## Steps

1. **Query active goals:**
   ```bash
   .claude/skills/query/query.py goals --view current
   ```

2. **Present goals:**
   Show the list in a simple format:
   > "You have X active goals:
   > - Goal 1 (Priority)
   > - Goal 2 (Priority)
   > ..."

3. **Quick check-in (optional):**
   Ask: "Any updates on these? Or should we move on to planning?"
   
   If they want to update:
   - Note any progress
   - Optionally update goal files

4. **Proceed to planning**

## If No Goals Found

Say: "No active goals found. Want to create one, or skip to planning the day?"

## Tips

- Keep it brief
- Don't force detailed updates
- Just awareness, not a full review
