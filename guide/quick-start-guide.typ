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
      What you'll do in the next 15 minutes:
    ]
    
    #v(0.5cm)
    
    #align(left)[
      #text(size: 11pt)[
        #text(fill: accent)[1.] Install Claude Code (if you haven't) \
        #text(fill: accent)[2.] Open this vault and connect it \
        #text(fill: accent)[3.] Create your first task by just typing \
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
        Correctly tagged. \
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
        #text(size: 10pt, weight: "bold")[tasknotes]
        #v(0.3cm)
        #text(size: 9pt, fill: muted)[Create, update, list tasks]
      ]
    ],
    [
      #block(
        stroke: 1pt + rgb("#e0e0e0"),
        inset: 12pt,
        radius: 4pt,
      )[
        #text(size: 10pt, weight: "bold")[obases]
        #v(0.3cm)
        #text(size: 9pt, fill: muted)[Query Obsidian Bases]
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
        #text(size: 9pt, fill: muted)[Daily overview]
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
4. When prompted about plugins, click *Trust author and enable plugins*

// TODO: Add screenshot - 01-obsidian-open-vault.png
// #image("screenshots/01-obsidian-open-vault.png", width: 100%)

#v(0.5cm)

You should see folders: `Daily`, `Tasks`, `Goals`, `Templates`

#v(1cm)

=== Enable TaskNotes API

The TaskNotes plugin needs its HTTP API enabled so Claude Code can create tasks.

1. Go to *Settings* → *Community Plugins* → *TaskNotes*
2. Scroll down to *HTTP API*
3. Toggle *Enable HTTP API* to ON
4. Copy the *API Token* shown

// TODO: Add screenshot - 02-tasknotes-settings.png
// #image("screenshots/02-tasknotes-settings.png", width: 100%)

#v(1cm)

=== Create Your `.env` File

In the vault's root folder, create a file named `.env`:

#block(
  fill: code-bg,
  inset: 12pt,
  radius: 4pt,
)[
  #text(fill: code-fg, font: "Menlo", size: 10pt)[
    TASKNOTES_API_KEY=paste_your_token_here
  ]
]

#v(0.5cm)

#text(size: 10pt, fill: muted)[
  Replace `paste_your_token_here` with the actual token you copied.
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

The `.` tells Claude to use this folder as context. It will read `CLAUDE.md` and load the skills.

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

Now for the magic. Type these commands in Claude Code:

#v(1cm)

=== Create a Task

#block(
  fill: code-bg,
  inset: 12pt,
  radius: 4pt,
)[
  #text(fill: code-fg, font: "Menlo", size: 10pt)[
    Create a task: Test the starter kit, high priority
  ]
]

#v(0.3cm)

#text(size: 10pt, fill: muted)[
  → Watch Obsidian. A new file appears in `Tasks/` folder instantly.
]

// TODO: Add screenshot - 04-claude-create-task.png (terminal)
// TODO: Add screenshot - 05-obsidian-task-created.png (obsidian)
// #grid(
//   columns: (1fr, 1fr),
//   gutter: 10pt,
//   image("screenshots/04-claude-create-task.png"),
//   image("screenshots/05-obsidian-task-created.png"),
// )

#v(1.5cm)

=== List Your Tasks

#block(
  fill: code-bg,
  inset: 12pt,
  radius: 4pt,
)[
  #text(fill: code-fg, font: "Menlo", size: 10pt)[
    Show my tasks
  ]
]

#v(0.3cm)

#text(size: 10pt, fill: muted)[
  → You get a formatted table with all tasks, their status, and priority.
]

#v(1.5cm)

=== Update a Task

#block(
  fill: code-bg,
  inset: 12pt,
  radius: 4pt,
)[
  #text(fill: code-fg, font: "Menlo", size: 10pt)[
    Mark "Test the starter kit" as done
  ]
]

#v(0.3cm)

#text(size: 10pt, fill: muted)[
  → The task's status changes to "done" in Obsidian.
]

#v(1.5cm)

=== Ask for Help

#block(
  fill: code-bg,
  inset: 12pt,
  radius: 4pt,
)[
  #text(fill: code-fg, font: "Menlo", size: 10pt)[
    What should I work on next?
  ]
]

#v(0.3cm)

#text(size: 10pt, fill: muted)[
  → Claude analyzes your tasks and suggests what to focus on.
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

=== Task Management

#table(
  columns: (1fr, 1fr),
  stroke: 0.5pt + rgb("#e0e0e0"),
  inset: 10pt,
  [*Say this*], [*What happens*],
  [`Create a task for tomorrow: Call mom`], [Creates task with scheduled date],
  [`Show in-progress tasks`], [Filters by status],
  [`Show high priority tasks`], [Filters by priority],
  [`Delete the task "old task"`], [Removes it from Obsidian],
  [`How much time did I track?`], [Shows Pomodoro stats],
)

#v(1.5cm)

=== Obsidian Bases (if configured)

#table(
  columns: (1fr, 1fr),
  stroke: 0.5pt + rgb("#e0e0e0"),
  inset: 10pt,
  [*Say this*], [*What happens*],
  [`Show my goals`], [Lists from Goals.base],
  [`What bases do I have?`], [Lists all Obsidian Bases],
  [`Query the Tasks base`], [Shows structured task data],
)

#v(1.5cm)

=== Daily Routine

#table(
  columns: (1fr, 1fr),
  stroke: 0.5pt + rgb("#e0e0e0"),
  inset: 10pt,
  [*Say this*], [*What happens*],
  [`Start my morning`], [Shows today's tasks + creates daily note],
  [`What's on my schedule?`], [Lists today's items],
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

=== "TaskNotes API not responding"

- Make sure Obsidian is open
- Check TaskNotes HTTP API is enabled in settings
- Verify your `.env` file has the correct token
- Default port is 8080 — make sure nothing else uses it

#v(1cm)

=== "Skill not found"

- Make sure you ran `claude .` from the vault folder
- Check that `.claude/skills/` folder exists
- Try: `claude . --help` to see available skills

#v(1cm)

=== "Command not working"

Be specific. Instead of "make a task", say:

#block(
  fill: code-bg,
  inset: 12pt,
  radius: 4pt,
)[
  #text(fill: code-fg, font: "Menlo", size: 10pt)[
    Create a task: [specific title], [priority]
  ]
]

#v(2cm)

#align(center)[
  #block(
    fill: rgb("#f5f5f5"),
    inset: 20pt,
    radius: 8pt,
    width: 80%,
  )[
    #text(size: 11pt)[
      *Need help?*
      
      #v(0.3cm)
      
      Open an issue on GitHub or check the README for updates.
    ]
  ]
]

#v(2cm)

#align(center)[
  #text(size: 10pt, fill: muted)[
    Built by Artem Zhutov · \@ArtemXTech
  ]
]
