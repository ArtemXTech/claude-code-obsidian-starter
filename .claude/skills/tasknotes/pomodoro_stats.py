#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["requests", "python-dotenv"]
# ///
"""
pomodoro_stats - Analyze pomodoro sessions by project/goal.

Usage:
    pomodoro_stats.py [--days N] [--by-project] [--by-task] [--json]
"""

__version__ = "0.2.0"

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

from dotenv import load_dotenv


def find_env_file() -> Path | None:
    """Find .env file: check symlink path first, then fall back to ~/.config"""
    symlink_path = Path(__file__).parent
    for parent in [symlink_path] + list(symlink_path.parents):
        env_file = parent / ".env"
        if env_file.exists():
            return env_file
    config_env = Path.home() / ".config" / "tasknotes" / ".env"
    if config_env.exists():
        return config_env
    return None


env_file = find_env_file()
if env_file:
    load_dotenv(env_file)


def load_pomodoro_history() -> list:
    """Load pomodoro history from TaskNotes plugin data."""
    data_path = Path(".obsidian/plugins/tasknotes/data.json")
    if not data_path.exists():
        print("Error: TaskNotes data.json not found", file=sys.stderr)
        sys.exit(1)

    with open(data_path) as f:
        data = json.load(f)

    return data.get("pomodoroHistory", [])


def load_task_projects() -> dict:
    """Load task -> projects mapping from API and files."""
    task_projects = {}

    # Try API first (has richer data)
    api_projects = load_projects_from_api()
    if api_projects:
        task_projects.update(api_projects)

    # Fallback to file parsing - check multiple possible locations
    task_folders = [Path("Tasks"), Path("Notes/Tasks")]

    for tasks_folder in task_folders:
        if tasks_folder.exists():
            for task_file in tasks_folder.glob("*.md"):
                rel_path = str(task_file)
                if rel_path not in task_projects:
                    projects = extract_projects_from_file(task_file)
                    if projects:
                        # Store with multiple path variants for matching
                        task_projects[rel_path] = projects
                        task_projects[f"{tasks_folder}/{task_file.name}"] = projects
                        task_projects[task_file.name] = projects

    return task_projects


def load_projects_from_api() -> dict:
    """Load task projects from TaskNotes API."""
    import urllib.request

    api_key = os.environ.get("TASKNOTES_API_KEY", "")
    api_port = os.environ.get("TASKNOTES_API_PORT", "8080")

    if not api_key:
        return {}

    try:
        url = f"http://localhost:{api_port}/api/tasks"
        req = urllib.request.Request(url)
        req.add_header("Authorization", f"Bearer {api_key}")

        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.load(resp)
            tasks = data.get("data", {}).get("tasks", [])

            result = {}
            for task in tasks:
                path = task.get("path", "")
                projects = task.get("projects", [])
                # Filter out None values
                projects = [p for p in projects if p]
                if path and projects:
                    result[path] = projects
                    # Normalize path variants
                    if "/" in path:
                        result[path.split("/")[-1]] = projects

            return result
    except Exception:
        return {}


def extract_projects_from_file(filepath: Path) -> list:
    """Extract projects from task file frontmatter."""
    try:
        content = filepath.read_text()
        # Simple YAML frontmatter extraction
        if content.startswith("---"):
            end = content.find("---", 3)
            if end > 0:
                frontmatter = content[3:end]
                lines = frontmatter.split("\n")
                projects = []
                in_projects = False

                for line in lines:
                    stripped = line.strip()

                    if stripped.startswith("projects:"):
                        in_projects = True
                        # Check for inline array
                        if "[" in line:
                            match = re.search(r'\[(.*?)\]', line)
                            if match:
                                items = match.group(1)
                                found = re.findall(r'\[\[(.*?)\]\]|"([^"]+)"', items)
                                projects = [p[0] or p[1] for p in found if p[0] or p[1]]
                            in_projects = False
                    elif in_projects:
                        # Multi-line array format: - "[[Goal]]"
                        if stripped.startswith("-"):
                            # Extract [[Goal]] or plain text
                            match = re.search(r'\[\[(.*?)\]\]', stripped)
                            if match:
                                projects.append(match.group(1))
                            else:
                                # Plain quoted string
                                match = re.search(r'"([^"]+)"', stripped)
                                if match:
                                    projects.append(match.group(1))
                        elif not stripped.startswith("-") and stripped and not stripped.startswith("#"):
                            # End of projects array
                            in_projects = False

                return projects
    except Exception:
        pass
    return []


def calc_duration_minutes(session: dict) -> float:
    """Calculate actual duration from active periods."""
    total = 0
    for period in session.get("activePeriods", []):
        start = datetime.fromisoformat(period["startTime"])
        end_str = period.get("endTime")
        if end_str:
            end = datetime.fromisoformat(end_str)
            total += (end - start).total_seconds() / 60
    return total


def filter_sessions(sessions: list, days: int = None, only_work: bool = True) -> list:
    """Filter sessions by date and type."""
    result = []
    cutoff = None
    if days:
        cutoff = datetime.now().astimezone() - timedelta(days=days)

    for s in sessions:
        if only_work and s.get("type") != "work":
            continue
        if not s.get("completed", False):
            continue

        start = datetime.fromisoformat(s["startTime"])
        # Make timezone-aware if needed for comparison
        if cutoff:
            if start.tzinfo is None:
                start = start.astimezone()
            if start < cutoff:
                continue

        result.append(s)

    return result


def aggregate_by_project(sessions: list, task_projects: dict) -> dict:
    """Aggregate time by project/goal."""
    by_project = defaultdict(lambda: {"minutes": 0, "sessions": 0, "tasks": set()})

    for s in sessions:
        task_path = s.get("taskPath", "")
        duration = calc_duration_minutes(s)

        # Find projects for this task
        projects = task_projects.get(task_path, [])
        if not projects:
            # Try alternate path formats
            for key in task_projects:
                if task_path.endswith(key) or key.endswith(task_path.split("/")[-1] if "/" in task_path else task_path):
                    projects = task_projects[key]
                    break

        if not projects:
            projects = ["(No Project)"]

        for project in projects:
            by_project[project]["minutes"] += duration
            by_project[project]["sessions"] += 1
            if task_path:
                by_project[project]["tasks"].add(task_path)

    # Convert sets to lists for JSON
    for p in by_project:
        by_project[p]["tasks"] = list(by_project[p]["tasks"])

    return dict(by_project)


def aggregate_by_task(sessions: list) -> dict:
    """Aggregate time by task."""
    by_task = defaultdict(lambda: {"minutes": 0, "sessions": 0})

    for s in sessions:
        task_path = s.get("taskPath", "(No Task)")
        duration = calc_duration_minutes(s)
        by_task[task_path]["minutes"] += duration
        by_task[task_path]["sessions"] += 1

    return dict(by_task)


def aggregate_by_date(sessions: list) -> dict:
    """Aggregate time by date."""
    by_date = defaultdict(lambda: {"minutes": 0, "sessions": 0})

    for s in sessions:
        start = datetime.fromisoformat(s["startTime"])
        date_key = start.strftime("%Y-%m-%d")
        duration = calc_duration_minutes(s)
        by_date[date_key]["minutes"] += duration
        by_date[date_key]["sessions"] += 1

    return dict(sorted(by_date.items()))


def format_table(data: dict, title: str) -> str:
    """Format data as ASCII table."""
    lines = [f"\n{title}", "=" * 60]

    # Sort by minutes descending
    sorted_items = sorted(data.items(), key=lambda x: x[1]["minutes"], reverse=True)

    total_mins = sum(d["minutes"] for d in data.values())
    total_sessions = sum(d["sessions"] for d in data.values())

    for name, stats in sorted_items:
        mins = stats["minutes"]
        sessions = stats["sessions"]
        hours = mins / 60
        pct = (mins / total_mins * 100) if total_mins > 0 else 0

        # Truncate long names
        display_name = name[:40] + "..." if len(name) > 43 else name
        lines.append(f"{display_name:<45} {hours:5.1f}h ({sessions:2} sessions) {pct:5.1f}%")

    lines.append("-" * 60)
    lines.append(f"{'TOTAL':<45} {total_mins/60:5.1f}h ({total_sessions:2} sessions)")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Pomodoro statistics analyzer")
    parser.add_argument("--days", type=int, help="Filter to last N days")
    parser.add_argument("--by-project", action="store_true", help="Aggregate by project/goal")
    parser.add_argument("--by-task", action="store_true", help="Aggregate by task")
    parser.add_argument("--by-date", action="store_true", help="Aggregate by date")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    # Load data
    history = load_pomodoro_history()
    task_projects = load_task_projects()

    # Filter
    sessions = filter_sessions(history, days=args.days)

    if not sessions:
        print("No completed work sessions found")
        return

    # Aggregate
    results = {}

    if args.by_project or (not args.by_task and not args.by_date):
        results["by_project"] = aggregate_by_project(sessions, task_projects)

    if args.by_task:
        results["by_task"] = aggregate_by_task(sessions)

    if args.by_date:
        results["by_date"] = aggregate_by_date(sessions)

    # Output
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        if "by_project" in results:
            print(format_table(results["by_project"], "TIME BY PROJECT/GOAL"))
        if "by_task" in results:
            print(format_table(results["by_task"], "TIME BY TASK"))
        if "by_date" in results:
            print(format_table(results["by_date"], "TIME BY DATE"))


if __name__ == "__main__":
    main()
