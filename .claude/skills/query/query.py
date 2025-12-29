#!/usr/bin/env python3
"""Query Obsidian notes via headless-bases plugin."""

import sys
import json
import urllib.request
import urllib.error

BASE_URL = "http://127.0.0.1:27124"


def request(endpoint: str, method: str = "GET", data: dict = None) -> dict:
    """Make HTTP request to headless-bases."""
    url = f"{BASE_URL}{endpoint}"
    req = urllib.request.Request(url, method=method)
    req.add_header("Content-Type", "application/json")
    
    if data:
        req.data = json.dumps(data).encode()
    
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.URLError as e:
        return {"error": f"Connection failed: {e.reason}. Is Obsidian running with headless-bases?"}


def eval_js(code: str) -> dict:
    """Execute JavaScript in Obsidian."""
    return request("/eval", "POST", {"code": code})


def cmd_status():
    """Check connection status."""
    result = request("/status")
    if "error" in result:
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)
    print(json.dumps(result, indent=2))


def cmd_folder(folder: str, where: dict = None):
    """Query all files in a folder."""
    # Build dataview query
    where_clause = ""
    if where:
        conditions = [f'p.{k} === "{v}"' for k, v in where.items()]
        where_clause = f".where(p => {' && '.join(conditions)})"
    
    code = f'''
const dv = app.plugins.plugins.dataview.api;
let pages = dv.pages('"{folder}"'){where_clause};
return pages.map(p => ({{
    file: p.file.path,
    name: p.file.name,
    ...Object.fromEntries(
        Object.entries(p).filter(([k]) => !k.startsWith("file"))
    )
}})).array();
'''
    result = eval_js(code)
    if "error" in result:
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)
    
    rows = result.get("result", [])
    if not rows:
        print("No results found.")
        return
    
    print(json.dumps(rows, indent=2, default=str))


def cmd_recent(count: int = 5):
    """Get recently modified files."""
    code = f'''
const dv = app.plugins.plugins.dataview.api;
let pages = dv.pages()
    .sort(p => p.file.mtime, "desc")
    .limit({count});
return pages.map(p => ({{
    file: p.file.path,
    name: p.file.name,
    modified: p.file.mtime
}})).array();
'''
    result = eval_js(code)
    if "error" in result:
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)
    
    print(json.dumps(result.get("result", []), indent=2, default=str))


def cmd_base(base_path: str, view_name: str):
    """Query a base view."""
    result = request(f"/bases/view?path={base_path}&view={view_name}")
    if "error" in result:
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)
    print(json.dumps(result, indent=2))


def parse_where(where_str: str) -> dict:
    """Parse 'key=value,key2=value2' into dict."""
    if not where_str:
        return {}
    result = {}
    for pair in where_str.split(","):
        if "=" in pair:
            k, v = pair.split("=", 1)
            result[k.strip()] = v.strip()
    return result


def main():
    if len(sys.argv) < 2:
        print("Usage: query.py <command> [args]")
        print("Commands: status, folder, recent, base")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "status":
        cmd_status()
    
    elif cmd == "folder":
        if len(sys.argv) < 3:
            print("Usage: query.py folder <folder-name> [--where 'key=value']")
            sys.exit(1)
        folder = sys.argv[2]
        where = {}
        if "--where" in sys.argv:
            idx = sys.argv.index("--where")
            if idx + 1 < len(sys.argv):
                where = parse_where(sys.argv[idx + 1])
        cmd_folder(folder, where)
    
    elif cmd == "recent":
        count = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        cmd_recent(count)
    
    elif cmd == "base":
        if len(sys.argv) < 4:
            print("Usage: query.py base <base-path> <view-name>")
            sys.exit(1)
        cmd_base(sys.argv[2], sys.argv[3])
    
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
