# Plan the Day

## Task

Based on goals, energy, and focus - create today's tasks.

## Steps

1. **Check existing tasks:**
   ```bash
   .claude/skills/query/query.py tasks --view active
   ```

2. **Suggest focus:**
   Based on:
   - Their main focus from check-in
   - Active goals
   - Energy level
   
   Suggest 1-3 things to focus on today.

3. **Create tasks:**
   Ask: "Should I create tasks for these?"
   
   If yes, use tasknotes:
   ```bash
   .claude/skills/tasknotes/tasknotes.py create "Task title" --priority high
   ```

4. **Wrap up:**
   > "Morning routine complete! Your focus today:
   > - [Main focus]
   > - [Task 1]
   > - [Task 2]
   > 
   > Have a great day!"

## Tips

- Less is more - suggest 1-3 tasks max
- Match energy to task difficulty
- High energy = hard tasks, Low energy = easy wins
- Don't overwhelm
