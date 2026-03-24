#!/usr/bin/env python3
"""Apple Calendar event writer via AppleScript.

Usage:
    ical-writer.py --calendar "kkafi@icdh.com" --title "Meeting" --start "2026-03-25T18:30:00"
    ical-writer.py --calendar "Home" --title "AGM" --start "2026-03-25T18:30:00" --end "2026-03-25T20:00:00" --location "Zoom" --notes "Details here"
    ical-writer.py --list-calendars    # Show available calendars

No API tokens needed — uses native macOS Calendar.app via osascript.
Events sync to iPhone via iCloud/Google/Outlook depending on the calendar account.
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timedelta


def list_calendars():
    """List all calendars available in Apple Calendar."""
    script = '''
    tell application "Calendar"
        set calList to {}
        repeat with c in calendars
            set end of calList to (name of c)
        end repeat
        return calList
    end tell
    '''
    result = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True, text=True, timeout=10
    )
    if result.returncode != 0:
        return {"error": result.stderr.strip()}
    # Parse AppleScript list output
    names = [n.strip() for n in result.stdout.strip().split(", ")]
    return {"calendars": names}


def create_event(calendar_name, title, start_dt, end_dt, location=None, notes=None):
    """Create an event in Apple Calendar via AppleScript."""
    # Format dates for AppleScript: "March 25, 2026 6:30:00 PM"
    start_str = start_dt.strftime("%B %d, %Y %I:%M:%S %p")
    end_str = end_dt.strftime("%B %d, %Y %I:%M:%S %p")

    # Build AppleScript
    location_line = ""
    if location:
        escaped_loc = location.replace('"', '\\"')
        location_line = f'set location of newEvent to "{escaped_loc}"'

    notes_line = ""
    if notes:
        escaped_notes = notes.replace('"', '\\"')
        notes_line = f'set description of newEvent to "{escaped_notes}"'

    escaped_title = title.replace('"', '\\"')

    script = f'''
    tell application "Calendar"
        tell calendar "{calendar_name}"
            set startDate to date "{start_str}"
            set endDate to date "{end_str}"
            set newEvent to make new event with properties {{summary:"{escaped_title}", start date:startDate, end date:endDate}}
            {location_line}
            {notes_line}
            set eventUID to uid of newEvent
            return eventUID
        end tell
    end tell
    '''

    result = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True, text=True, timeout=15
    )

    if result.returncode != 0:
        return {"error": result.stderr.strip(), "calendar": calendar_name}

    event_uid = result.stdout.strip()
    return {
        "action": "created",
        "uid": event_uid,
        "calendar": calendar_name,
        "summary": title,
        "start": start_dt.isoformat(),
        "end": end_dt.isoformat(),
    }


def parse_datetime(dt_str):
    """Parse ISO 8601 or common datetime formats."""
    try:
        return datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
    except ValueError:
        pass
    for fmt in ["%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M"]:
        try:
            return datetime.strptime(dt_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"Cannot parse datetime: {dt_str}")


def main():
    parser = argparse.ArgumentParser(description="Apple Calendar event writer")
    parser.add_argument("--calendar", help="Calendar name (e.g., 'kkafi@icdh.com', 'Home')")
    parser.add_argument("--title", help="Event title")
    parser.add_argument("--start", help="Start datetime (ISO 8601)")
    parser.add_argument("--end", help="End datetime (default: start + 1 hour)")
    parser.add_argument("--location", help="Event location")
    parser.add_argument("--notes", help="Event notes/description")
    parser.add_argument("--list-calendars", action="store_true", help="List available calendars")
    args = parser.parse_args()

    if args.list_calendars:
        result = list_calendars()
        print(json.dumps(result, indent=2))
        sys.exit(0)

    if not args.calendar or not args.title or not args.start:
        print(json.dumps({"error": "--calendar, --title, and --start are required"}), file=sys.stderr)
        sys.exit(1)

    try:
        start_dt = parse_datetime(args.start)
        end_dt = parse_datetime(args.end) if args.end else start_dt + timedelta(hours=1)
    except ValueError as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)

    result = create_event(
        args.calendar, args.title, start_dt, end_dt, args.location, args.notes
    )

    if "error" in result:
        print(json.dumps(result), file=sys.stderr)
        sys.exit(1)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
