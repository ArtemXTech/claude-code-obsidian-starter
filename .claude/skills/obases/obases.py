#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "typer",
#     "httpx",
# ]
# ///
"""
obases - CLI for querying Obsidian Bases.

Human-friendly output by default. Use --json for machine-readable output.
Requires the headless-bases Obsidian plugin running on http://127.0.0.1:27124
"""

import json
import sys
from typing import Optional

import httpx
import typer

__version__ = "0.2.0"

app = typer.Typer(
    name="obases",
    help="Query Obsidian Bases via the headless-bases plugin.",
    add_completion=False,
    no_args_is_help=True,
)

BASE_URL = "http://127.0.0.1:27124"
TIMEOUT = 10.0


# =============================================================================
# Helpers
# =============================================================================

def is_tty() -> bool:
    return sys.stdout.isatty()


def output_json(data):
    """Print JSON output."""
    print(json.dumps(data, indent=2, ensure_ascii=False))


def _request(method: str, endpoint: str, **kwargs) -> dict:
    """Make HTTP request to the headless-bases server."""
    url = f"{BASE_URL}{endpoint}"
    try:
        with httpx.Client(timeout=TIMEOUT) as client:
            if method == "GET":
                resp = client.get(url, params=kwargs.get("params"))
            else:
                resp = client.post(url, json=kwargs.get("json"))
            resp.raise_for_status()
            return resp.json()
    except httpx.ConnectError:
        typer.echo("Error: Cannot connect to Obsidian.", err=True)
        typer.echo("Is the headless-bases plugin running?", err=True)
        typer.echo(f"Expected server at: {BASE_URL}", err=True)
        raise typer.Exit(1)
    except httpx.HTTPStatusError as e:
        typer.echo(f"Error: {e.response.status_code} - {e.response.text}", err=True)
        raise typer.Exit(1)
    except Exception as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(1)


def _output_table(data: dict, short_paths: bool = True):
    """Output view data as a table (TSV format)."""
    columns = data.get("columns", [])
    rows = data.get("rows", [])
    
    if not columns or not rows:
        typer.echo("No data", err=True)
        return
    
    col_names = [c["name"] for c in columns]
    
    # Print header
    typer.echo("\t".join(col_names))
    
    # Print rows
    for row in rows:
        values = []
        for col in col_names:
            val = row.get(col, "")
            if short_paths and col == "file" and "/" in str(val):
                val = val.split("/")[-1].replace(".md", "")
            values.append(str(val))
        typer.echo("\t".join(values))


# =============================================================================
# Commands
# =============================================================================

def version_callback(value: bool):
    if value:
        print(f"obases {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        None, "--version", "-V", callback=version_callback, is_eager=True,
        help="Show version and exit."
    ),
):
    """Query Obsidian Bases via the headless-bases plugin."""
    pass


@app.command()
def status():
    """Check if the headless-bases server is running."""
    data = _request("GET", "/status")
    if is_tty():
        typer.echo(f"✓ Connected to Obsidian ({BASE_URL})")
        if "vault" in data:
            typer.echo(f"  Vault: {data['vault']}")
    else:
        output_json(data)


@app.command()
def bases():
    """List all .base files in the vault."""
    data = _request("GET", "/bases")
    if is_tty():
        files = data.get("files", [])
        if files:
            typer.echo(f"Found {len(files)} base(s):\n")
            for f in files:
                typer.echo(f"  {f}")
        else:
            typer.echo("No .base files found")
    else:
        output_json(data)


@app.command()
def views(path: str = typer.Argument(..., help="Path to .base file")):
    """List available views in a base file.
    
    Example: obases views "Templates/Bases/Goals.base"
    """
    _request("POST", "/bases/open-file", json={"path": path, "sidebar": True})
    
    code = f"""
    const leaves = app.workspace.getLeavesOfType('bases');
    for (const leaf of leaves) {{
        const state = leaf.view?.getState?.();
        if (state?.file === '{path}') {{
            const viewState = leaf.view?.leaf?.view;
            const config = viewState?.config;
            if (config?.views) {{
                return Object.keys(config.views);
            }}
        }}
    }}
    return ['Could not read views - try opening the file in Obsidian first'];
    """
    data = _request("POST", "/eval", json={"code": code})
    views_list = data.get("result", [])
    
    if is_tty():
        typer.echo(f"Views in {path}:\n")
        for v in views_list:
            typer.echo(f"  {v}")
    else:
        output_json(views_list)


@app.command()
def view(
    path: str = typer.Argument(..., help="Path to .base file"),
    view_name: str = typer.Argument(..., help="View name (e.g., 'Current', 'All')"),
    output: str = typer.Option("auto", "--output", "-o", help="Output format: auto, json, table"),
    full_paths: bool = typer.Option(False, "--full-paths", "-f", help="Show full file paths"),
    wait: float = typer.Option(0.5, "--wait", "-w", help="Wait time for view to load (seconds)"),
):
    """Query a specific view from a base file.
    
    Examples:
        obases view "Templates/Bases/Goals.base" "Current"
        obases view "Templates/Bases/Goals.base" "Current" -o table
    """
    # Auto-open base before querying (required for data to be available)
    _request("POST", "/bases/open-file", json={"path": path, "sidebar": False})
    
    data = _request("GET", "/bases/view", params={"path": path, "view": view_name, "wait": wait})
    
    if "error" in data:
        typer.echo(f"Error: {data['error']}", err=True)
        if "hint" in data:
            typer.echo(f"Hint: {data['hint']}", err=True)
        raise typer.Exit(1)
    
    # Auto-detect format
    if output == "auto":
        output = "table" if is_tty() else "json"
    
    if output == "table":
        _output_table(data, short_paths=not full_paths)
    else:
        output_json(data)


@app.command(name="open")
def open_base(
    path: str = typer.Argument(..., help="Path to .base file"),
    sidebar: bool = typer.Option(False, "--sidebar/--no-sidebar", help="Open in sidebar"),
):
    """Open a base file (required before querying).
    
    Example: obases open "Templates/Bases/Goals.base"
    """
    data = _request("POST", "/bases/open-file", json={"path": path, "sidebar": sidebar})
    if is_tty():
        typer.echo(f"✓ Opened: {path}")
    else:
        output_json(data)


@app.command()
def preload():
    """Preload all bases in the vault (opens them in sidebar)."""
    data = _request("POST", "/bases/preload")
    if is_tty():
        count = data.get("loaded", 0)
        typer.echo(f"✓ Preloaded {count} base(s)")
    else:
        output_json(data)


@app.command()
def schema(
    path: str = typer.Argument(..., help="Path to .base file"),
):
    """Get schema for a base (fields, types, example).
    
    Use this to discover available fields before creating items.
    
    Example: obases schema "Templates/Bases/Goals.base"
    """
    data = _request("GET", "/bases/schema", params={"path": path})
    output_json(data)  # Schema is complex, always JSON


@app.command()
def create(
    base: str = typer.Argument(..., help="Path to .base file"),
    title: str = typer.Argument(..., help="Title for the new item"),
    json_fields: str = typer.Option(None, "--json", "-j", help="Fields as JSON object"),
    folder: str = typer.Option(None, "--folder", "-d", help="Target folder"),
    body: str = typer.Option(None, "--body", "-b", help="Note body content"),
):
    """Create a new item in a base.
    
    Examples:
        obases create "Templates/Bases/Goals.base" "Learn Rust" --json '{"Status": "In progress"}'
        obases create "Templates/Bases/Goals.base" "Learn Rust" -j '{"Status": "In progress"}' -b "Description"
    """
    fields = {}
    if json_fields:
        try:
            fields = json.loads(json_fields)
        except json.JSONDecodeError as e:
            typer.echo(f"Error: Invalid JSON: {e}", err=True)
            raise typer.Exit(1)
    
    payload = {
        "base": base,
        "title": title,
        "fields": fields,
    }
    if folder:
        payload["folder"] = folder
    if body:
        payload["body"] = body
    
    data = _request("POST", "/bases/create", json=payload)
    
    if is_tty():
        file_path = data.get("path", title)
        typer.echo(f"✓ Created: {file_path}")
    else:
        output_json(data)


@app.command()
def query(
    path: str = typer.Argument(..., help="Path to .base file"),
):
    """Query a base file using simple engine (works on closed files).
    
    Note: Doesn't support formulas. Use 'view' command for full support.
    
    Example: obases query "Templates/Bases/Goals.base"
    """
    data = _request("GET", "/query", params={"path": path})
    output_json(data)


@app.command(name="eval")
def eval_code(
    code: str = typer.Argument(..., help="JavaScript code to execute"),
):
    """Execute JavaScript code in Obsidian (advanced).
    
    Example: obases eval "return vault.getName()"
    """
    data = _request("POST", "/eval", json={"code": code})
    output_json(data)


if __name__ == "__main__":
    app()
