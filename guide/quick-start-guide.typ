#set page(
  paper: "a4",
  margin: (x: 2.5cm, y: 2.5cm),
  fill: white,
)

#set text(
  font: "Helvetica Neue",
  size: 11pt,
  fill: rgb("#1a1a1a"),
)

#set heading(numbering: none)

#let accent = rgb("#7c3aed")  // Purple for Claude
#let obsidian = rgb("#7c3aed")
#let muted = rgb("#666666")
#let code-bg = rgb("#1e1e1e")
#let code-fg = rgb("#d4d4d4")

// ============================================
// COVER PAGE
// ============================================

#align(center)[
  #v(2cm)
  
  // Logos side by side
  #grid(
    columns: (1fr, auto, 1fr),
    align: center + horizon,
    gutter: 20pt,
    [#image("claude-logo.svg", width: 60pt)],
    [#text(size: 24pt, fill: muted)[+]],
    [#image("obsidian-ascii-logo.png", width: 60pt)],
  )
  
  #v(1.5cm)
  
  #text(size: 28pt, weight: "bold")[
    Claude Code + Obsidian
  ]
  
  #v(0.3cm)
  
  #text(size: 14pt, fill: muted)[
    Starter Kit
  ]
  
  #v(2cm)
  
  #block(
    fill: rgb("#f5f5f5"),
    inset: 20pt,
    radius: 8pt,
    width: 90%,
  )[
    #text(size: 12pt, weight: "medium")[
      What you'll do in the next 10 minutes:
    ]
    
    #v(0.5cm)
    
    #align(left)[
      #text(size: 11pt)[
        #text(fill: accent)[1.] Install Claude Code (if you haven't) \
        #text(fill: accent)[2.] Open this vault in Obsidian \
        #text(fill: accent)[3.] Create a task by just typing \
        #text(fill: accent)[4.] Query your notes like a database
      ]
    ]
  ]
  
  #v(2cm)
  
  #text(size: 10pt, fill: muted)[
    December 2025 · Artem Zhutov
  ]
]

#pagebreak()

// ============================================
// THE TRANSFORMATION
// ============================================

#text(size: 20pt, weight: "bold")[
  Why This Matters
]

#v(0.5cm)

#line(length: 100%, stroke: 0.5pt + rgb("#e0e0e0"))

#v(1cm)

#grid(
  columns: (1fr, 1fr),
  gutter: 20pt,
  [
    #block(
      fill: rgb("#fef2f2"),
      inset: 16pt,
      radius: 8pt,
    )[
      #text(size: 12pt, weight: "bold", fill: rgb("#991b1b"))[
        Before
      ]
      
      #v(0.5cm)
      
      #text(size: 10pt)[
        Open Obsidian \
        Navigate to Tasks folder \
        Create new note \
        Add frontmatter \
        Type task details \
        Set priority manually \
        Tag it correctly \
        Save and organize
      ]
      
      #v(0.5cm)
      
      #text(size: 10pt, fill: muted, style: "italic")[
        ~2 minutes per task
      ]
    ]
  ],
  [
    #block(
      fill: rgb("#f0fdf4"),
      inset: 16pt,
      radius: 8pt,
    )[
      #text(size: 12pt, weight: "bold", fill: rgb("#166534"))[
        After
      ]
      
      #v(0.5cm)
      
      #text(size: 10pt)[
        "Create a task: \
        Review feedback, \
        high priority"
      ]
      
      #v(1.5cm)
      
      #text(size: 10pt, fill: muted, style: "italic")[
        ~3 seconds
      ]
      
      #v(0.5cm)
      
      #text(size: 10pt)[
        Task appears in Obsidian. \
        Properly formatted. \
        Ready to work on.
      ]
    ]
  ]
)

#v(1.5cm)

#align(center)[
  #text(size: 12pt, fill: muted)[
    This starter kit gives you three Claude Code skills:
  ]
  
  #v(0.5cm)
  
  #grid(
    columns: (1fr, 1fr, 1fr),
    gutter: 12pt,
    [
      #block(
        stroke: 1pt + rgb("#e0e0e0"),
        inset: 12pt,
        radius: 4pt,
      )[
        #text(size: 10pt, weight: "bold")[query]
        #v(0.3cm)
        #text(size: 9pt, fill: muted)[Query & create notes]
      ]
    ],
    [
      #block(
        stroke: 1pt + rgb("#e0e0e0"),
        inset: 12pt,
        radius: 4pt,
      )[
        #text(size: 10pt, weight: "bold")[tasknotes]
        #v(0.3cm)
        #text(size: 9pt, fill: muted)[Task management]
      ]
    ],
    [
      #block(
        stroke: 1pt + rgb("#e0e0e0"),
        inset: 12pt,
        radius: 4pt,
      )[
        #text(size: 10pt, weight: "bold")[morning-routine]
        #v(0.3cm)
        #text(size: 9pt, fill: muted)[Daily workflow]
      ]
    ]
  )
]

#pagebreak()

// ============================================
// STEP 1: INSTALL CLAUDE CODE
// ============================================

#text(size: 20pt, weight: "bold")[
  Step 1: Install Claude Code
]

#v(0.5cm)

#line(length: 100%, stroke: 0.5pt + rgb("#e0e0e0"))

#v(1cm)

#block(
  fill: rgb("#f0f9ff"),
  inset: 16pt,
  radius: 8pt,
)[
  #text(size: 11pt)[
    *Already have Claude Code installed?* Skip to Step 2.
  ]
]

#v(1cm)

=== What is Claude Code?

Claude Code is Anthropic's official CLI tool that lets you work with Claude directly in your terminal. It can read files, run commands, and — with skills — interact with apps like Obsidian.

#v(0.5cm)

=== Installation

*macOS / Linux / WSL:*

#block(
  fill: code-bg,
  inset: 12pt,
  radius: 4pt,
)[
  #text(fill: code-fg, font: "Menlo", size: 10pt)[
    curl -fsSL https://claude.ai/install.sh | bash
  ]
]

#v(0.5cm)

*Windows PowerShell:*

#block(
  fill: code-bg,
  inset: 12pt,
  radius: 4pt,
)[
  #text(fill: code-fg, font: "Menlo", size: 10pt)[
    irm https://claude.ai/install.ps1 | iex
  ]
]

#v(0.5cm)

*Homebrew (macOS):*

#block(
  fill: code-bg,
  inset: 12pt,
  radius: 4pt,
)[
  #text(fill: code-fg, font: "Menlo", size: 10pt)[
    brew install --cask claude-code
  ]
]

#v(1cm)

=== First Run

After installation, run `claude` once to authenticate:

#block(
  fill: code-bg,
  inset: 12pt,
  radius: 4pt,
)[
  #text(fill: code-fg, font: "Menlo", size: 10pt)[
    claude
  ]
]

It will open a browser window to sign in with your Anthropic account.

#v(1cm)

=== Official Documentation

#link("https://docs.anthropic.com/en/docs/claude-code")[
  #text(fill: accent)[docs.anthropic.com/en/docs/claude-code]
]

#pagebreak()

// ============================================
// STEP 2: OPEN THE VAULT
// ============================================

#text(size: 20pt, weight: "bold")[
  Step 2: Open This Vault
]

#v(0.5cm)

#line(length: 100%, stroke: 0.5pt + rgb("#e0e0e0"))

#v(1cm)

=== In Obsidian

1. Open Obsidian
2. Click *Open another vault* (or File → Open Vault)
3. Select this folder: `claude-code-obsidian-starter`
4. When prompted, click *Trust author and enable plugins*

// TODO: Screenshot showing Obsidian with vault open, sidebar visible
// #image("screenshots/01-vault-open.png", width: 100%)

#v(0.5cm)

You should see folders: `Daily`, `Tasks`, `Goals`, `Templates`

#v(1cm)

=== Plugins That Load Automatically

The vault comes with these plugins pre-configured:

- *Dataview* — Query your notes like a database
- *TaskNotes* — Task management with views
- *headless-bases* — Lets Claude Code talk to Obsidian

#v(0.5cm)

#block(
  fill: rgb("#f0fdf4"),
  inset: 16pt,
  radius: 8pt,
)[
  #text(size: 11pt)[
    *No setup needed.* Just open the vault and everything works.
  ]
]

#v(1cm)

=== Open in Claude Code

In your terminal, navigate to this vault and start Claude:

#block(
  fill: code-bg,
  inset: 12pt,
  radius: 4pt,
)[
  #text(fill: code-fg, font: "Menlo", size: 10pt)[
    cd path/to/claude-code-obsidian-starter \
    claude .
  ]
]

#v(0.5cm)

The `.` tells Claude to use this folder as context. It reads `CLAUDE.md` and loads the skills automatically.

#pagebreak()

// ============================================
// STEP 3: TRY IT
// ============================================

#text(size: 20pt, weight: "bold")[
  Step 3: Try These Commands
]

#v(0.5cm)

#line(length: 100%, stroke: 0.5pt + rgb("#e0e0e0"))

#v(1cm)

Now for the magic. Type these in Claude Code:

#v(1cm)

=== Query Your Goals

#block(
  fill: code-bg,
  inset: 12pt,
  radius: 4pt,
)[
  #text(fill: code-fg, font: "Menlo", size: 10pt)[
    Show my goals
  ]
]

#v(0.3cm)

#text(size: 10pt, fill: muted)[
  Claude queries your Goals folder and shows them in a table.
]

// TODO: Screenshot of terminal showing goals table
// #image("screenshots/02-query-goals.png", width: 100%)

#v(1.5cm)

=== Create a Task

#block(
  fill: code-bg,
  inset: 12pt,
  radius: 4pt,
)[
  #text(fill: code-fg, font: "Menlo", size: 10pt)[
    Create a task: Test the starter kit
  ]
]

#v(0.3cm)

#text(size: 10pt, fill: muted)[
  A new file appears in `Tasks/` folder instantly.
]

// TODO: Screenshot of Obsidian showing new task
// #image("screenshots/03-task-created.png", width: 100%)

#v(1.5cm)

=== Filter by Priority

#block(
  fill: code-bg,
  inset: 12pt,
  radius: 4pt,
)[
  #text(fill: code-fg, font: "Menlo", size: 10pt)[
    Show high priority goals
  ]
]

#v(0.3cm)

#text(size: 10pt, fill: muted)[
  Filters to only show goals where Priority = High.
]

#v(1.5cm)

=== Start Your Morning

#block(
  fill: code-bg,
  inset: 12pt,
  radius: 4pt,
)[
  #text(fill: code-fg, font: "Menlo", size: 10pt)[
    Start my morning
  ]
]

#v(0.3cm)

#text(size: 10pt, fill: muted)[
  Runs the morning routine: reviews yesterday, does a check-in, shows goals.
]

#pagebreak()

// ============================================
// MORE COMMANDS
// ============================================

#text(size: 20pt, weight: "bold")[
  More Things to Try
]

#v(0.5cm)

#line(length: 100%, stroke: 0.5pt + rgb("#e0e0e0"))

#v(1cm)

=== Query Commands

#table(
  columns: (1fr, 1fr),
  stroke: 0.5pt + rgb("#e0e0e0"),
  inset: 10pt,
  [*Say this*], [*What happens*],
  [`Show my goals`], [Lists all active goals],
  [`Show my tasks`], [Lists active tasks],
  [`Show high priority goals`], [Filters by Priority = High],
  [`What did I edit recently?`], [Shows recently modified files],
  [`Create a goal: Learn Rust`], [Creates new goal file],
)

#v(1.5cm)

=== Task Management

#table(
  columns: (1fr, 1fr),
  stroke: 0.5pt + rgb("#e0e0e0"),
  inset: 10pt,
  [*Say this*], [*What happens*],
  [`Create a task: Call mom`], [Creates task in Tasks/],
  [`Show tasks for today`], [Filters by due date],
  [`What should I work on?`], [Suggests based on priority],
)

#v(1.5cm)

=== Morning Routine

#table(
  columns: (1fr, 1fr),
  stroke: 0.5pt + rgb("#e0e0e0"),
  inset: 10pt,
  [*Say this*], [*What happens*],
  [`Start my morning`], [Full morning workflow],
  [`Review yesterday`], [Shows what happened yesterday],
  [`Plan my day`], [Creates tasks based on goals],
)

#pagebreak()

// ============================================
// TROUBLESHOOTING
// ============================================

#text(size: 20pt, weight: "bold")[
  Troubleshooting
]

#v(0.5cm)

#line(length: 100%, stroke: 0.5pt + rgb("#e0e0e0"))

#v(1cm)

=== "Obsidian not responding" or "headless-bases not running"

- Make sure Obsidian is open with this vault
- Check that plugins are enabled (Settings → Community Plugins)
- Restart Obsidian if needed

#v(1cm)

=== "Skill not found"

- Make sure you ran `claude .` from the vault folder (not just `claude`)
- Check that `.claude/skills/` folder exists
- The `.` is important — it tells Claude to load skills from this folder

#v(1cm)

=== "No results found"

- The vault comes with sample tasks and goals
- If you deleted them, create new ones first
- Check the folder names match: `Tasks/`, `Goals/`

#v(1cm)

=== Queries not working

Make sure Obsidian is the active vault. The headless-bases plugin only works with the currently open vault.

#v(2cm)

#align(center)[
  #block(
    fill: rgb("#f5f5f5"),
    inset: 20pt,
    radius: 8pt,
    width: 80%,
  )[
    #text(size: 11pt)[
      *Want to go deeper?*
      
      #v(0.3cm)
      
      Join the workshop to build custom skills for your workflow.
      
      #v(0.3cm)
      
      #link("https://workshop.artemzhutov.com")[
        #text(fill: accent)[workshop.artemzhutov.com]
      ]
    ]
  ]
]

#v(2cm)

#align(center)[
  #text(size: 10pt, fill: muted)[
    Built by Artem Zhutov · \@ArtemXTech
  ]
]
