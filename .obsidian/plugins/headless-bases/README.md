# Headless Obsidian Bases

Programmatically access Obsidian Bases data via HTTP API.

## What We Discovered

Obsidian Bases (v1.10.0+) doesn't expose a public query API, but we found ways to access the data:

```
┌─────────────────────────────────────────────────────────────────┐
│                     THREE APPROACHES                            │
│                                                                 │
│  1. /bases/open     → REAL Obsidian engine (formulas work!)   │
│                       ⚠️ Requires file to be OPEN              │
│                                                                 │
│  2. /query          → Our own query engine                     │
│                       ✅ Works on CLOSED files                  │
│                       ❌ No formula evaluation                  │
│                                                                 │
│  3. /eval           → Run any JavaScript                       │
│                       ✅ Full vault access                      │
│                       ✅ Complete flexibility                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Quick Start

### 1. Install the Plugin

```bash
cd obsidian-bases-headless
npm install
npm run build

# Copy to your vault
cp main.js manifest.json /path/to/vault/.obsidian/plugins/headless-bases/
```

### 2. Enable in Obsidian

Settings → Community Plugins → Enable "Headless Bases"

### 3. Use the API

```bash
# Check status
curl http://127.0.0.1:27124/status

# Get data from OPEN bases (with formulas!)
curl http://127.0.0.1:27124/bases/open

# Query any .base file (even closed)
curl "http://127.0.0.1:27124/query?path=my-projects.base"
```

## API Endpoints

### GET /status
Server status and available endpoints.

### GET /bases
List all `.base` files in the vault.

```bash
curl http://127.0.0.1:27124/bases
# {"count": 2, "bases": ["my-projects.base", "tasks.base"]}
```

### GET /bases/open ⭐
**Get REAL data from Obsidian's Bases engine** (including formulas!)

Requires the `.base` file to be open in Obsidian.

```bash
curl http://127.0.0.1:27124/bases/open
```

Response:
```json
{
  "file": "my-projects.base",
  "currentView": "All Projects",
  "availableViews": ["All Projects", "Board View"],
  "viewType": "table",
  "properties": ["file.name", "note.status", "formula.daysUntilDue"],
  "count": 3,
  "entries": [
    {
      "file": "Projects/Project Alpha.md",
      "values": {
        "file.name": "Project Alpha",
        "note.status": "active",
        "formula.daysUntilDue": "21 days"
      }
    }
  ]
}
```

### POST /bases/switch
Switch to a different view in an open base.

```bash
curl -X POST http://127.0.0.1:27124/bases/switch \
  -H "Content-Type: application/json" \
  -d '{"basePath": "my-projects.base", "viewName": "Board View"}'
```

### GET /query?path=X
Query a `.base` file using our own engine. Works even if file is closed, but no formula evaluation.

```bash
curl "http://127.0.0.1:27124/query?path=my-projects.base"
```

### GET /files
List all markdown files in the vault.

### POST /eval
Execute arbitrary JavaScript with full Obsidian access.

```bash
curl -X POST http://127.0.0.1:27124/eval \
  -H "Content-Type: application/json" \
  -d '{"code": "return vault.getMarkdownFiles().length"}'
```

Available objects: `app`, `vault`, `workspace`, `metadataCache`, `queryEngine`, `basesDataStore`

## Dev Script

Use `./dev.sh` for quick development:

```bash
./dev.sh dev        # Build + Copy + Reload Obsidian

./dev.sh status     # Check server
./dev.sh bases      # List .base files
./dev.sh open       # Get REAL data from open bases ⭐
./dev.sh query X    # Query a .base file
./dev.sh switch X Y # Switch view in open base
./dev.sh eval "js"  # Execute JavaScript
./dev.sh files      # List markdown files
./dev.sh console    # Open Obsidian dev console
./dev.sh reload     # Reload Obsidian
```

## How It Works

### Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         OBSIDIAN                                │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │                    Our Plugin                            │  │
│   │                                                          │  │
│   │   HTTP Server (port 27124)                              │  │
│   │        │                                                 │  │
│   │        ├── /bases/open ──► Access open BasesView        │  │
│   │        │                   └── controller.view.data     │  │
│   │        │                       (REAL BasesQueryResult)  │  │
│   │        │                                                 │  │
│   │        ├── /query ──► Our QueryEngine                   │  │
│   │        │              └── Parse YAML + MetadataCache    │  │
│   │        │                                                 │  │
│   │        └── /eval ──► new Function() execution           │  │
│   │                                                          │  │
│   └─────────────────────────────────────────────────────────┘  │
│                                                                 │
│   Obsidian Internal APIs Used:                                 │
│   • app.workspace.getLeavesOfType("bases")                     │
│   • view.controller.view.data (BasesQueryResult)               │
│   • view.controller.selectView(name)                           │
│   • app.vault, app.metadataCache                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Accessing Obsidian's Real Bases Engine

We discovered that open `.base` files expose their data through:

```javascript
// Get all open Base views
const leaves = app.workspace.getLeavesOfType("bases");

// Access the controller
const controller = leaves[0].view.controller;

// Get current view info
controller.viewName              // "All Projects"
controller.getQueryViewNames()   // ["All Projects", "Board View"]
controller.selectView("Board")   // Switch views!

// Get the REAL data with formulas
const basesView = controller.view;
basesView.data                   // BasesQueryResult
basesView.data.data              // Array of BasesEntry
basesView.allProperties          // All available properties

// Get values including formulas
const entry = basesView.data.data[0];
entry.file                       // TFile
entry.getValue("formula.daysUntilDue")  // Evaluated formula!
```

### .base File Format (YAML)

```yaml
filters:
  and:
    - file.folder == "Projects"
    - note.status == "active"

formulas:
  daysUntilDue: due - now()
  isOverdue: due < now()

properties:
  note.status:
    displayName: Status

views:
  - type: table
    name: All Projects
  - type: cards
    name: Card View
```

### Our Query Engine (for closed files)

When files aren't open, we parse the YAML and query the vault ourselves:

```javascript
class BasesQueryEngine {
    async executeQuery(basePath) {
        // 1. Read .base file
        const content = await vault.read(file);
        const config = parseYaml(content);
        
        // 2. Filter files based on config
        const files = vault.getMarkdownFiles().filter(f => 
            this.matchesFilter(f, config.filters)
        );
        
        // 3. Get properties from metadataCache
        return files.map(f => ({
            file: f,
            properties: this.getFileProperties(f)
        }));
    }
}
```

Supported filters:
- `file.folder == "X"` - folder matching
- `note.property == "value"` - frontmatter matching
- `folder("X")` - folder contains
- `tag(#x)` - has tag
- `and: [...]`, `or: [...]`, `not: [...]` - logical operators

## Requirements

- Obsidian v1.10.0+ (Bases feature)
- Bases must be enabled in vault settings
- Obsidian must be running (can be hidden)

## Limitations

| Feature | /bases/open | /query |
|---------|-------------|--------|
| Works on closed files | ❌ | ✅ |
| Formula evaluation | ✅ | ❌ |
| Uses real Bases engine | ✅ | ❌ |
| View switching | ✅ | N/A |

## FAQ

### Does Obsidian need to be open?
**Yes**, but it can be hidden (`Cmd+H` on Mac). The HTTP server runs inside Obsidian.

### Can I query closed .base files?
**Yes**, use `/query`. But you won't get formula results - only file and frontmatter properties.

### Can I get formula results?
**Yes**, but the `.base` file must be **open** in Obsidian. Use `/bases/open`.

### Can I access different views?
**Yes**, use `/bases/switch` to switch views, then `/bases/open` to get that view's data.

## Files

```
obsidian-bases-headless/
├── main.ts          # Plugin source
├── manifest.json    # Obsidian plugin manifest
├── package.json     # npm dependencies
├── dev.sh          # Development helper script
├── obsidian-api.sh # Shell functions for quick access
└── README.md       # This file
```

## License

MIT
