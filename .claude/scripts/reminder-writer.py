#!/usr/bin/env python3
"""Apple Reminders writer via AppleScript.

Usage:
    reminder-writer.py --list "Avitia" --title "Review document" --due "2026-03-26"
    reminder-writer.py --list "Personal" --title "Update Disney+ card" --due "2026-03-25" --notes "Card expiring"
    reminder-writer.py --list-all                # Show available reminder lists

No API tokens needed — uses native macOS Reminders.app via osascript.
Reminders sync to iPhone via iCloud automatically.
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime


def list_reminder_lists():
    """List all reminder lists in Reminders.app."""
    script = '''
    tell application "Reminders"
        set listNames to {}
        repeat with L in lists
            set end of listNames to (name of L)
        end repeat
        return listNames
    end tell
    '''
    result = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True, text=True, timeout=10
    )
    if result.returncode != 0:
        return {"error": result.stderr.strip()}
    names = [n.strip() for n in result.stdout.strip().split(", ")]
    return {"lists": names}


def ensure_list_exists(list_name):
    """Create a reminder list if it doesn't exist."""
    escaped = list_name.replace('"', '\\"')
    script = f'''
    tell application "Reminders"
        try
            set targetList to list "{escaped}"
        on error
            make new list with properties {{name:"{escaped}"}}
        end try
        return name of list "{escaped}"
    end tell
    '''
    result = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True, text=True, timeout=10
    )
    return result.returncode == 0


def create_reminder(list_name, title, due_date=None, notes=None, priority=None):
    """Create a reminder in Apple Reminders via AppleScript."""
    escaped_title = title.replace('"', '\\"')
    escaped_list = list_name.replace('"', '\\"')

    # Build properties
    props = f'name:"{escaped_title}"'

    if priority:
        # AppleScript priority: 0=none, 1=high, 5=medium, 9=low
        props += f", priority:{priority}"

    # Build the script
    due_line = ""
    if due_date:
        due_str = due_date.strftime("%B %d, %Y 9:00:00 AM")
        due_line = f'set due date of newReminder to date "{due_str}"'

    notes_line = ""
    if notes:
        escaped_notes = notes.replace('"', '\\"')
        notes_line = f'set body of newReminder to "{escaped_notes}"'

    script = f'''
    tell application "Reminders"
        tell list "{escaped_list}"
            set newReminder to make new reminder with properties {{{props}}}
            {due_line}
            {notes_line}
            set remID to id of newReminder
            return remID
        end tell
    end tell
    '''

    result = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True, text=True, timeout=15
    )

    if result.returncode != 0:
        return {"error": result.stderr.strip(), "list": list_name}

    reminder_id = result.stdout.strip()
    output = {
        "action": "created",
        "id": reminder_id,
        "list": list_name,
        "title": title,
    }
    if due_date:
        output["due"] = due_date.strftime("%Y-%m-%d")
    return output


def parse_date(date_str):
    """Parse date string (YYYY-MM-DD or ISO 8601)."""
    for fmt in ["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M"]:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    try:
        return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    except ValueError:
        raise ValueError(f"Cannot parse date: {date_str}")


def main():
    parser = argparse.ArgumentParser(description="Apple Reminders writer")
    parser.add_argument("--list", help="Reminders list name (e.g., 'Avitia', 'Personal')")
    parser.add_argument("--title", help="Reminder title")
    parser.add_argument("--due", help="Due date (YYYY-MM-DD)")
    parser.add_argument("--notes", help="Reminder notes/description")
    parser.add_argument(
        "--priority",
        type=int,
        choices=[0, 1, 5, 9],
        help="Priority: 0=none, 1=high, 5=medium, 9=low",
    )
    parser.add_argument("--list-all", action="store_true", help="List available reminder lists")
    args = parser.parse_args()

    if args.list_all:
        result = list_reminder_lists()
        print(json.dumps(result, indent=2))
        sys.exit(0)

    if not args.list or not args.title:
        print(json.dumps({"error": "--list and --title are required"}), file=sys.stderr)
        sys.exit(1)

    # Ensure target list exists
    ensure_list_exists(args.list)

    # Parse due date if provided
    due_date = None
    if args.due:
        try:
            due_date = parse_date(args.due)
        except ValueError as e:
            print(json.dumps({"error": str(e)}), file=sys.stderr)
            sys.exit(1)

    result = create_reminder(args.list, args.title, due_date, args.notes, args.priority)

    if "error" in result:
        print(json.dumps(result), file=sys.stderr)
        sys.exit(1)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
