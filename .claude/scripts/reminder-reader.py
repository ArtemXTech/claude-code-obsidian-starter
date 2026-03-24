#!/usr/bin/env python3
"""Apple Reminders reader via AppleScript.

Usage:
    reminder-reader.py --open                          # All open reminders
    reminder-reader.py --open --list "Inbox"           # Open reminders in specific list
    reminder-reader.py --completed --since "2026-03-24" # Recently completed
    reminder-reader.py --all --list "Avitia"           # All reminders in a list

No API tokens needed — uses native macOS Reminders.app via osascript.
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime


def _run_osascript(script, timeout=15):
    """Run an AppleScript and return stdout."""
    result = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True, text=True, timeout=timeout
    )
    if result.returncode != 0:
        return None, result.stderr.strip()
    return result.stdout.strip(), None


def read_reminders(completed_filter=None, list_filter=None, since_date=None):
    """Read reminders from Apple Reminders.

    Args:
        completed_filter: True=completed only, False=open only, None=all
        list_filter: specific list name, or None for all lists
        since_date: only return completed items after this date (datetime)
    """
    # Build the filter clause
    if completed_filter is True:
        filter_clause = "whose completed is true"
    elif completed_filter is False:
        filter_clause = "whose completed is false"
    else:
        filter_clause = ""

    list_clause = ""
    if list_filter:
        escaped_list = list_filter.replace('"', '\\"')
        list_clause = f'of list "{escaped_list}"'

    # AppleScript to read reminders with all fields
    # We use a delimiter-based approach since AppleScript list handling is limited
    script = f'''
    set output to ""
    tell application "Reminders"
        set allReminders to (reminders {list_clause} {filter_clause})
        repeat with r in allReminders
            set rName to name of r
            set rID to id of r
            set rCompleted to completed of r
            set rList to name of container of r

            -- Due date
            try
                set rDue to due date of r as string
            on error
                set rDue to ""
            end try

            -- Completion date
            try
                set rCompDate to completion date of r as string
            on error
                set rCompDate to ""
            end try

            -- Body/notes
            try
                set rBody to body of r
                if rBody is missing value then set rBody to ""
            on error
                set rBody to ""
            end try

            -- Creation date
            try
                set rCreated to creation date of r as string
            on error
                set rCreated to ""
            end try

            -- Priority
            try
                set rPriority to priority of r as integer
            on error
                set rPriority to 0
            end try

            set output to output & rID & "|||" & rList & "|||" & rName & "|||" & rCompleted & "|||" & rDue & "|||" & rCompDate & "|||" & rBody & "|||" & rCreated & "|||" & rPriority & "\\n"
        end repeat
    end tell
    return output
    '''

    raw, err = _run_osascript(script, timeout=30)
    if err:
        return {"error": err}

    reminders = []
    for line in raw.split("\n"):
        line = line.strip()
        if not line or "|||" not in line:
            continue
        parts = line.split("|||")
        if len(parts) < 9:
            continue

        reminder = {
            "id": parts[0].strip(),
            "list": parts[1].strip(),
            "title": parts[2].strip(),
            "completed": parts[3].strip().lower() == "true",
            "due_date": parts[4].strip() or None,
            "completion_date": parts[5].strip() or None,
            "notes": parts[6].strip() or None,
            "creation_date": parts[7].strip() or None,
            "priority": int(parts[8].strip()) if parts[8].strip().isdigit() else 0,
        }

        # Filter by since_date if specified
        if since_date and reminder.get("completion_date"):
            try:
                # Parse AppleScript date format (e.g., "Tuesday, March 24, 2026 at 2:45:42 PM")
                comp_str = reminder["completion_date"]
                # Try multiple formats
                for fmt in [
                    "%A, %B %d, %Y at %I:%M:%S %p",
                    "%B %d, %Y at %I:%M:%S %p",
                    "%Y-%m-%d",
                ]:
                    try:
                        comp_dt = datetime.strptime(comp_str, fmt)
                        if comp_dt < since_date:
                            continue  # Skip items completed before since_date
                        break
                    except ValueError:
                        continue
            except Exception:
                pass  # Include if we can't parse the date

        reminders.append(reminder)

    return reminders


def main():
    parser = argparse.ArgumentParser(description="Apple Reminders reader")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--open", action="store_true", help="Only open/incomplete reminders")
    group.add_argument("--completed", action="store_true", help="Only completed reminders")
    group.add_argument("--all", action="store_true", help="All reminders (open + completed)")
    parser.add_argument("--list", help="Filter to specific list name")
    parser.add_argument("--since", help="For completed: only after this date (YYYY-MM-DD)")
    args = parser.parse_args()

    completed_filter = None
    if args.open:
        completed_filter = False
    elif args.completed:
        completed_filter = True

    since_date = None
    if args.since:
        try:
            since_date = datetime.strptime(args.since, "%Y-%m-%d")
        except ValueError:
            print(json.dumps({"error": f"Cannot parse --since date: {args.since}"}), file=sys.stderr)
            sys.exit(1)

    result = read_reminders(
        completed_filter=completed_filter,
        list_filter=args.list,
        since_date=since_date,
    )

    if isinstance(result, dict) and "error" in result:
        print(json.dumps(result), file=sys.stderr)
        sys.exit(1)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
