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

#let accent = rgb("#7c3aed")
#let muted = rgb("#666666")
#let code-bg = rgb("#1e1e1e")
#let code-fg = rgb("#d4d4d4")
#let frame-color = rgb("#e5e5e5")

// Helper for framed, centered images with optional caption
#let framed-image(path, img-width: 100%, caption: none) = {
  align(center)[
    #block(
      stroke: 1pt + frame-color,
      radius: 6pt,
      clip: true,
    )[
      #image(path, width: img-width)
    ]
    #if caption != none [
      #v(0.3cm)
      #text(size: 9pt, fill: muted, style: "italic")[#caption]
    ]
  ]
}

// ============================================
// COVER PAGE
// ============================================

#align(center)[
  #v(2cm)
  
  #grid(
    columns: (1fr, auto, 1fr),
    align: center + horizon,
    gutter: 30pt,
    [#image("claude-logo.jpg", height: 100pt)],
    [#text(size: 32pt, fill: muted)[+]],
    [#image("obsidian-ascii-logo.png", height: 120pt)],
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
      In the next 10 minutes, you'll:
    ]
    
    #v(0.5cm)
    
    #align(left)[
      #text(size: 11pt)[
        #text(fill: accent)[1.] Talk to your Obsidian vault in plain English \
        #text(fill: accent)[2.] Create tasks in 3 seconds (not 2 minutes) \
        #text(fill: accent)[3.] Query your goals, notes, and data instantly \
        #text(fill: accent)[4.] Try the morning routine that plans your day
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
        "Create a task for \
        meeting with client \
        tomorrow 9am"
      ]
      
      #v(1cm)
      
      #text(size: 10pt, fill: muted, style: "italic")[
        ~3 seconds
      ]
      
      #v(0.5cm)
      
      #text(size: 10pt)[
        Task appears in Obsidian. \
        Scheduled. Prioritized. \
        Ready to work on.
      ]
    ]
  ]
)

#v(1.5cm)

#align(center)[
  #text(size: 12pt, fill: muted)[
    This starter kit includes three Claude Code skills:
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
        #text(size: 10pt, weight: "bold")[🔍 query]
        #v(0.3cm)
        #text(size: 9pt, fill: muted)[Read goals, notes, data]
      ]
    ],
    [
      #block(
        stroke: 1pt + rgb("#e0e0e0"),
        inset: 12pt,
        radius: 4pt,
      )[
        #text(size: 10pt, weight: "bold")[✅ tasknotes]
        #v(0.3cm)
        #text(size: 9pt, fill: muted)[Create & manage tasks]
      ]
    ],
    [
      #block(
        stroke: 1pt + rgb("#e0e0e0"),
        inset: 12pt,
        radius: 4pt,
      )[
        #text(size: 10pt, weight: "bold")[☀️ morning-routine]
        #v(0.3cm)
        #text(size: 9pt, fill: muted)[Daily workflow]
      ]
    ]
  )
]

#pagebreak()

// ============================================
// STEP 1: OPEN THE VAULT
// ============================================

#text(size: 20pt, weight: "bold")[
  Step 1: Open the Vault
]

#v(0.5cm)

#line(length: 100%, stroke: 0.5pt + rgb("#e0e0e0"))

#v(0.8cm)

Open Obsidian and select this folder as a vault. When prompted, click *Trust author and enable plugins*.

#v(0.5cm)

#framed-image("screenshots/01-vault-open.png", caption: "The starter kit vault with CLAUDE.md open")

#v(0.5cm)

The vault comes pre-configured with:
- *Tasks* — Your tasks (managed by TaskNotes)
- *Goals* — Goal tracking with structured data
- *Daily* — Daily notes and check-ins
- *.claude/skills* — Claude Code skills that make this work

#v(0.5cm)

#block(
  fill: rgb("#f0fdf4"),
  inset: 14pt,
  radius: 6pt,
)[
  #text(size: 10pt)[
    *No setup needed.* The plugins (Dataview, TaskNotes, headless-bases) are pre-installed and configured. Just open and go.
  ]
]

#pagebreak()

// ============================================
// STEP 2: START CLAUDE CODE
// ============================================

#text(size: 20pt, weight: "bold")[
  Step 2: Start Claude Code
]

#v(0.5cm)

#line(length: 100%, stroke: 0.5pt + rgb("#e0e0e0"))

#v(1cm)

#block(
  fill: rgb("#f0f9ff"),
  inset: 14pt,
  radius: 6pt,
)[
  #text(size: 10pt)[
    *Don't have Claude Code?* Install it first: \
    `curl -fsSL https://claude.ai/install.sh | bash` (Mac/Linux) \
    `irm https://claude.ai/install.ps1 | iex` (Windows PowerShell)
  ]
]

#v(1cm)

Open your terminal, navigate to the vault folder, and start Claude:

#block(
  fill: code-bg,
  inset: 12pt,
  radius: 4pt,
)[
  #text(fill: code-fg, font: "Menlo", size: 10pt)[
    cd path/to/claude-code-obsidian-starter \
    claude
  ]
]

#v(0.5cm)

#framed-image("screenshots/02-claude-started.png", caption: "Claude Code ready and waiting")

#v(0.5cm)

You'll see the Claude Code logo and a prompt. The path shows you're in the starter kit folder. Now you're ready to talk to your vault.

#pagebreak()

// ============================================
// STEP 3: QUERY YOUR GOALS
// ============================================

#text(size: 20pt, weight: "bold")[
  Step 3: See the Magic
]

#v(0.5cm)

#line(length: 100%, stroke: 0.5pt + rgb("#e0e0e0"))

#v(0.8cm)

Type this in Claude Code:

#block(
  fill: code-bg,
  inset: 12pt,
  radius: 4pt,
)[
  #text(fill: code-fg, font: "Menlo", size: 11pt)[
    Show my goals
  ]
]

#v(0.5cm)

Claude queries your vault and returns a formatted table:

#v(0.3cm)

#framed-image("screenshots/02-query-goals-terminal.png", caption: "Claude returns your goals in a formatted table")

#v(0.8cm)

Now look at the *same data* in Obsidian (Templates/Bases/Goals):

#v(0.3cm)

#framed-image("screenshots/03-query-goals-obsidian.png", caption: "Same data in Obsidian — proof it's real")

#v(0.5cm)

#align(center)[
  #block(
    fill: rgb("#fef3c7"),
    inset: 14pt,
    radius: 6pt,
    width: 90%,
  )[
    #text(size: 10pt)[
      *Same 6 goals. Same data.* Claude reads directly from your Obsidian vault — nothing is made up or cached.
    ]
  ]
]

#pagebreak()

// ============================================
// STEP 4: CREATE A TASK
// ============================================

#text(size: 20pt, weight: "bold")[
  Step 4: Create with Natural Language
]

#v(0.5cm)

#line(length: 100%, stroke: 0.5pt + rgb("#e0e0e0"))

#v(0.8cm)

Now try creating a task. Just describe what you need:

#block(
  fill: code-bg,
  inset: 12pt,
  radius: 4pt,
)[
  #text(fill: code-fg, font: "Menlo", size: 10pt)[
    Create a task to prepare for meeting with client tomorrow 9am
  ]
]

#v(0.5cm)

#framed-image("screenshots/04-task-created.png", caption: "Natural language → task with date, time, priority")

#v(0.5cm)

Claude understood:
- *What:* "Prepare for client meeting"
- *When:* Tomorrow at 9:00 AM
- *Priority:* High (inferred from "meeting with client")

The task appears in your `Tasks/` folder in Obsidian, properly formatted with frontmatter.

#v(0.8cm)

To see it on the Kanban board, open the command palette (Cmd+P) and search "kanban":

#v(0.3cm)

#framed-image("screenshots/05-open-kanban-command.png", img-width: 70%, caption: "Cmd+P → search 'kanban'")

#v(0.5cm)

Your task is right there, scheduled and ready:

#v(0.3cm)

#framed-image("screenshots/06-kanban-board.png", caption: "Task appears on the Kanban board, scheduled and ready")

#v(0.8cm)

#block(
  fill: rgb("#f0fdf4"),
  inset: 14pt,
  radius: 6pt,
)[
  #text(size: 10pt, weight: "medium")[
    This is the transformation:
  ]
  #v(0.3cm)
  #text(size: 10pt)[
    Instead of: navigate → create file → add frontmatter → fill fields → save \
    You just: *describe what you need in plain English*
  ]
]

#pagebreak()

// ============================================
// MORE THINGS TO TRY
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
  [`Show high priority goals`], [Filters by priority],
  [`What are my tasks?`], [Lists active tasks],
  [`What did I edit recently?`], [Shows recent files],
)

#v(1cm)

=== Task Commands

#table(
  columns: (1fr, 1fr),
  stroke: 0.5pt + rgb("#e0e0e0"),
  inset: 10pt,
  [*Say this*], [*What happens*],
  [`Create a task: Call mom tomorrow`], [Creates scheduled task],
  [`Add a high priority task for X`], [Creates with priority],
  [`Show my tasks for today`], [Filters by date],
)

#v(1cm)

=== Morning Routine

#table(
  columns: (1fr, 1fr),
  stroke: 0.5pt + rgb("#e0e0e0"),
  inset: 10pt,
  [*Say this*], [*What happens*],
  [`Start my morning`], [Runs full morning workflow],
  [`Review yesterday`], [Shows yesterday's summary],
  [`Plan my day`], [Creates tasks based on goals],
)

#pagebreak()

// ============================================
// BONUS: MORNING ROUTINE
// ============================================

#text(size: 20pt, weight: "bold")[
  Bonus: Morning Routine Skill
]

#v(0.5cm)

#line(length: 100%, stroke: 0.5pt + rgb("#e0e0e0"))

#v(0.8cm)

The starter kit includes a morning routine skill that helps you start each day with intention.

#v(0.5cm)

#block(
  fill: code-bg,
  inset: 12pt,
  radius: 4pt,
)[
  #text(fill: code-fg, font: "Menlo", size: 11pt)[
    Start my morning
  ]
]

#v(0.8cm)

=== What It Does

#v(0.3cm)

#grid(
  columns: (auto, 1fr),
  gutter: 15pt,
  row-gutter: 12pt,
  [#text(fill: accent, weight: "bold")[1.]], [*Reviews yesterday* — Reads your recent daily notes and summarizes what happened],
  [#text(fill: accent, weight: "bold")[2.]], [*Morning check-in* — Asks how you're feeling, your energy level, sleep quality],
  [#text(fill: accent, weight: "bold")[3.]], [*Shows your goals* — Queries active goals so you remember what matters],
  [#text(fill: accent, weight: "bold")[4.]], [*Plans the day* — Suggests tasks based on your energy and priorities],
)

#v(0.8cm)

=== The Daily Note

After the check-in, Claude creates a note in `Daily/` with your responses:

#v(0.3cm)

#block(
  fill: rgb("#f5f5f5"),
  inset: 14pt,
  radius: 6pt,
)[
  #text(font: "Menlo", size: 9pt)[
    \-\-\- \
    date: 2025-12-29 \
    mood: good \
    energy: 7 \
    sleep_quality: 8 \
    \-\-\- \
    \
    \# Morning Check-in \
    \
    \#\# How I'm feeling \
    Rested, ready to tackle the day...
  ]
]

#v(0.8cm)

#align(center)[
  #text(size: 10pt, fill: muted)[
    This creates a daily record you can look back on. \
    Over time, you'll see patterns in your energy and productivity.
  ]
]

#pagebreak()

// ============================================
// WHAT'S POSSIBLE
// ============================================

#text(size: 20pt, weight: "bold")[
  Automate Your Entire Workflow
]

#v(0.5cm)

#line(length: 100%, stroke: 0.5pt + rgb("#e0e0e0"))

#v(0.8cm)

The starter kit is just the beginning. With custom skills, you can automate entire parts of your day — hands-free.

#v(0.5cm)

=== Automated Daily Reports

Claude tracks your work throughout the day and generates a visual report:

#v(0.3cm)

#framed-image("screenshots/07-day-review.png", img-width: 85%, caption: "Auto-generated daily report with time tracking")

#v(0.5cm)

Then sends it to you automatically — no manual step required:

#v(0.3cm)

#framed-image("screenshots/08-telegram-report.png", img-width: 75%, caption: "Sent to Telegram automatically — no manual step")

#v(0.8cm)

#block(
  fill: rgb("#f5f5f5"),
  inset: 14pt,
  radius: 6pt,
)[
  #text(size: 10pt, weight: "medium")[
    What you can automate:
  ]
  #v(0.3cm)
  #text(size: 10pt)[
    - Morning briefs with weather, calendar, and priorities \
    - Email triage and draft responses \
    - Meeting prep with context from your notes \
    - Weekly reviews aggregating your progress \
    - Client reports, invoices, status updates
  ]
]

#v(0.5cm)

#align(center)[
  #text(size: 11pt, fill: muted)[
    If you can describe it, Claude can probably automate it.
  ]
]

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

=== "Cannot connect" or "Obsidian not responding"

Make sure Obsidian is open with this vault. The skills communicate with Obsidian through local plugins — Obsidian must be running.

#v(0.8cm)

=== "Skill not found"

Make sure you ran `claude` from inside the vault folder. Claude automatically loads skills from `.claude/skills/`.

#v(1.5cm)

#align(center)[
  #block(
    fill: rgb("#f5f5f5"),
    inset: 20pt,
    radius: 8pt,
    width: 85%,
  )[
    #text(size: 11pt)[
      *Want to build your own automations?*
      
      #v(0.3cm)
      
      Join the workshop to create custom skills for your specific workflows.
      
      #v(0.3cm)
      
      #link("https://workshop.artemzhutov.com")[
        #text(fill: accent)[workshop.artemzhutov.com]
      ]
    ]
  ]
]

#v(1.5cm)

#align(center)[
  #block(
    inset: 20pt,
    radius: 8pt,
  )[
    #grid(
      columns: (auto, 1fr),
      gutter: 20pt,
      align: horizon,
      [
        #block(
          clip: true,
          radius: 50pt,
        )[
          #image("profile.png", width: 60pt)
        ]
      ],
      [
        #align(left)[
          #text(size: 12pt, weight: "bold")[Artem Zhutov]
          #v(0.3cm)
          #text(size: 10pt, fill: muted)[
            Questions? Reach out:
          ]
          #v(0.2cm)
          #text(size: 9pt)[
            #link("https://wa.me/12263365520?text=Hi%20Artem%2C%20question%20about%20the%20starter%20kit")[WhatsApp] · 
            #link("https://x.com/ArtemXTech")[X/Twitter] · 
            #link("https://discord.gg/g5Z4Wk2fDk")[Community] · 
            #link("https://artemxtech.substack.com")[Substack]
          ]
        ]
      ]
    )
  ]
]
