#!/usr/bin/env python3
"""Query Obsidian notes via headless-bases plugin using dataview."""

import sys
import json
import urllib.request
import urllib.error

BASE_URL = "http://127.0.0.1:27124"

# Collections - define your folders here
COLLECTIONS = {
    "goals": {
        "folder": "Goals",
        "fields": ["Status", "Priority", "Area", "Frequency"],
        "views": {
            "current": 'p.Status === "In progress"',
            "all": None,
        },
        "default_view": "current",
    },
    "tasks": {
        "folder": "Tasks",
        "fields": ["Status", "Priority", "Project", "Due"],
        "views": {
            "active": 'p.Status !== "Done" && p.Status !== "Cancelled"',
            "today": 'p.Due === dv.date("today").toFormat("yyyy-MM-dd")',
            "all": None,
        },
        "default_view": "active",
    },
    "daily": {
        "folder": "Daily",
        "fields": ["Energy", "Mood"],
        "views": {
            "recent": None,
        },
        "default_view": "recent",
        "sort": "file.name",
        "sort_order": "desc",
    },
}


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
        return {"error": f"Connection failed: {e.reason}. Is Obsidian running?"}


def eval_js(code: str) -> dict:
    """Execute JavaScript in Obsidian."""
    return request("/eval", "POST", {"code": code})


def build_query(folder: str, filter_expr: str = None, where: dict = None, 
                sort: str = None, sort_order: str = "asc", limit: int = None) -> str:
    """Build dataview query code."""
    lines = [
        'const dv = app.plugins.plugins.dataview.api;',
        f'let pages = dv.pages("\\"{folder}\\"");',
    ]
    
    if filter_expr:
        lines.append(f'pages = pages.where(p => {filter_expr});')
    
    if where:
        for field, value in where.items():
            escaped = value.replace('"', '\\"')
            lines.append(f'pages = pages.where(p => p.{field} === "{escaped}");')
    
    if sort:
        order = "'desc'" if sort_order == "desc" else "'asc'"
        lines.append(f'pages = pages.sort(p => p.{sort}, {order});')
    
    if limit:
        lines.append(f'pages = pages.limit({limit});')
    
    lines.append('''pages = pages.map(p => ({
        file: p.file.path,
        name: p.file.name,
        ...Object.fromEntries(
            Object.entries(p).filter(([k]) => !k.startsWith("file"))
        )
    }));''')
    lines.append('return pages.array();')
    
    return '\n'.join(lines)


def cmd_status():
    """Check connection."""
    result = request("/status")
    if "error" in result:
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)
    print(f"Connected to: {result.get('vault', 'unknown')}")
    print(f"Collections: {', '.join(COLLECTIONS.keys())}")


def cmd_collections():
    """List available collections."""
    for name, coll in COLLECTIONS.items():
        views = list(coll.get("views", {}).keys())
        print(f"{name}: {coll['folder']}/ (views: {', '.join(views)})")


def cmd_query(collection: str, view: str = None, where: dict = None, 
              sort: str = None, limit: int = None, output: str = "table"):
    """Query a collection."""
    if collection not in COLLECTIONS:
        print(f"Unknown collection: {collection}", file=sys.stderr)
        print(f"Available: {', '.join(COLLECTIONS.keys())}", file=sys.stderr)
        sys.exit(1)
    
    coll = COLLECTIONS[collection]
    folder = coll["folder"]
    
    # Get view filter
    if not view:
        view = coll.get("default_view")
    
    filter_expr = None
    if view and view in coll.get("views", {}):
        filter_expr = coll["views"][view]
    
    # Default sort
    sort_field = sort or coll.get("sort")
    sort_order = coll.get("sort_order", "asc")
    
    code = build_query(folder, filter_expr, where, sort_field, sort_order, limit)
    result = eval_js(code)
    
    if "error" in result:
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)
    
    items = result.get("result", [])
    
    if output == "json":
        print(json.dumps(items, indent=2, default=str))
    else:
        # Table output
        if not items:
            print("No results.")
            return
        
        fields = ["name"] + coll.get("fields", [])[:3]
        
        # Header
        header = " | ".join(f"{f:20}" for f in fields)
        print(header)
        print("-" * len(header))
        
        # Rows
        for item in items:
            row = []
            for f in fields:
                val = str(item.get(f, ""))[:20]
                row.append(f"{val:20}")
            print(" | ".join(row))


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
    
    for item in result.get("result", []):
        print(f"{item['name']:40} {item.get('modified', '')}")


def cmd_create(collection: str, title: str, fields: dict = None):
    """Create a new item."""
    if collection not in COLLECTIONS:
        print(f"Unknown collection: {collection}", file=sys.stderr)
        sys.exit(1)
    
    coll = COLLECTIONS[collection]
    folder = coll["folder"]
    
    # Sanitize title
    safe_title = title.replace("/", "-").replace("\\", "-")
    path = f"{folder}/{safe_title}.md"
    
    # Build frontmatter
    fm_lines = ["---"]
    if fields:
        for k, v in fields.items():
            if isinstance(v, str):
                fm_lines.append(f'{k}: "{v}"')
            else:
                fm_lines.append(f"{k}: {v}")
    fm_lines.append("---")
    fm_lines.append("")
    fm_lines.append(f"# {title}")
    fm_lines.append("")
    
    content = "\\n".join(fm_lines)
    
    code = f'''
const path = "{path}";
const content = "{content}";
let file = app.vault.getAbstractFileByPath(path);
if (file) {{
    return {{ error: "File already exists: " + path }};
}}
await app.vault.create(path, content.replace(/\\\\n/g, "\\n"));
return {{ created: path }};
'''
    result = eval_js(code)
    if "error" in result:
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)
    
    print(f"Created: {result.get('result', {}).get('created', path)}")


def parse_where(s: str) -> dict:
    """Parse 'Key=value,Key2=value2' into dict."""
    if not s:
        return {}
    result = {}
    for pair in s.split(","):
        if "=" in pair:
            k, v = pair.split("=", 1)
            result[k.strip()] = v.strip()
    return result


def parse_fields(s: str) -> dict:
    """Parse 'Key=value,Key2=value2' into dict."""
    return parse_where(s)


def main():
    if len(sys.argv) < 2:
        print("Usage: query.py <command> [args]")
        print("")
        print("Commands:")
        print("  status              Check connection")
        print("  collections         List available collections")
        print("  goals               Query goals (shortcut)")
        print("  tasks               Query tasks (shortcut)")
        print("  <collection>        Query any collection")
        print("  recent [n]          Recent files")
        print("  create <coll> <title> [--fields 'k=v']  Create item")
        print("")
        print("Options:")
        print("  --view <name>       Use specific view")
        print("  --where 'k=v'       Filter by field")
        print("  --limit <n>         Limit results")
        print("  --json              JSON output")
        sys.exit(1)
    
    cmd = sys.argv[1]
    args = sys.argv[2:]
    
    # Parse flags
    view = None
    where = {}
    limit = None
    output = "table"
    fields = {}
    
    i = 0
    positional = []
    while i < len(args):
        if args[i] == "--view" and i + 1 < len(args):
            view = args[i + 1]
            i += 2
        elif args[i] == "--where" and i + 1 < len(args):
            where = parse_where(args[i + 1])
            i += 2
        elif args[i] == "--limit" and i + 1 < len(args):
            limit = int(args[i + 1])
            i += 2
        elif args[i] == "--json":
            output = "json"
            i += 1
        elif args[i] == "--fields" and i + 1 < len(args):
            fields = parse_fields(args[i + 1])
            i += 2
        else:
            positional.append(args[i])
            i += 1
    
    if cmd == "status":
        cmd_status()
    elif cmd == "collections":
        cmd_collections()
    elif cmd == "recent":
        count = int(positional[0]) if positional else 5
        cmd_recent(count)
    elif cmd == "create":
        if len(positional) < 2:
            print("Usage: query.py create <collection> <title> [--fields 'k=v']")
            sys.exit(1)
        cmd_create(positional[0], positional[1], fields)
    elif cmd in COLLECTIONS:
        cmd_query(cmd, view, where, limit=limit, output=output)
    else:
        # Try as collection name
        print(f"Unknown command: {cmd}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
