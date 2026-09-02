# nlm CLI Commands — Meta-Study Quick Reference

Abridged reference of the 25 most relevant `nlm` commands for meta-study workflows. For the complete reference, see `nlm-skill-export/nlm-skill/references/command_reference.md`.

---

## Authentication

```bash
nlm login                          # Launch browser auth flow
nlm login                  # Validate current credentials
nlm login --profile <name>         # Auth with named profile
nlm login switch <profile>         # Switch default profile
```

---

## Notebook Management

```bash
nlm notebook list                  # List all notebooks
nlm notebook list --json           # JSON output for parsing
nlm notebook create "<title>"      # Create notebook, returns ID
nlm notebook create "<title>" --json  # Machine-readable ID capture
nlm notebook get <id>              # Get notebook details
nlm notebook describe <id>         # AI-generated summary + topics
nlm notebook query <id> "<q>"      # One-shot Q&A with sources
nlm notebook query <id> "<q>" --source-ids "<id1,id2>"  # Scoped query
```

---

## Source Management

```bash
# Adding sources
nlm source add <nb-id> --url "<url>"              # Web page / YouTube
nlm source add <nb-id> --text "<content>" --title "<title>"  # Text
nlm source add <nb-id> --file "<path>" --wait      # Local file
nlm source add <nb-id> --drive <doc-id> --type doc # Drive doc

# Listing and viewing
nlm source list <nb-id>                # Table of sources
nlm source list <nb-id> --json         # JSON for parsing
nlm source list <nb-id> --drive        # Show Drive sources + freshness
nlm source describe <source-id>        # AI summary + keywords
nlm source content <source-id>         # Raw text content
```

---

## Research (Source Discovery)

```bash
nlm research start "<query>" --notebook-id <id>            # Fast web (~30s)
nlm research start "<query>" --notebook-id <id> --mode deep  # Deep web (~5min)
nlm research start "<query>" --notebook-id <id> --mode deep --auto-import  # Auto-import
nlm research start "<query>" --title "New Notebook"         # Create destination
nlm research status <nb-id>                                 # Poll progress
nlm research status <nb-id> --max-wait 900                  # Wait up to 15min
nlm research import <nb-id> <task-id>                       # Import all
nlm research import <nb-id> <task-id> --cited-only          # Import cited only
```

---

## Content Generation (Studio)

All generation commands require `--confirm` (or `-y`). Common flags: `--source-ids`, `--language <BCP-47>`, `--profile`.

```bash
# Report
nlm report create <id> --confirm
nlm report create <id> --format "Briefing Doc" --confirm
nlm report create <id> --format "Study Guide" --confirm
nlm report create <id> --format "Create Your Own" --prompt "<prompt>" --confirm

# Audio (Podcast)
nlm audio create <id> --confirm
nlm audio create <id> --format deep_dive --length long --confirm
nlm audio create <id> --format brief --length short --confirm
nlm audio create <id> --language de --focus "<topic>" --confirm

# Quiz
nlm quiz create <id> --confirm
nlm quiz create <id> --count 10 --difficulty 3 --focus "<topic>" --confirm

# Flashcards
nlm flashcards create <id> --confirm
nlm flashcards create <id> --difficulty medium --focus "<topic>" --confirm

# Slides
nlm slides create <id> --confirm
nlm slides create <id> --format detailed_deck --length default --confirm
nlm slides create <id> --format presenter_slides --length short --confirm

# Infographic
nlm infographic create <id> --confirm
nlm infographic create <id> --orientation landscape --detail standard --style scientific --confirm

# Data Table
nlm data-table create <id> "<description>" --confirm

# Mind Map
nlm mindmap create <id> --title "<title>" --confirm
```

---

## Studio & Download

```bash
# Status
nlm studio status <nb-id>                        # List artifacts
nlm studio status <nb-id> --json --full           # JSON with details + custom_instructions
nlm studio status <nb-id> --artifact-id <id>      # Poll one artifact

# Download
nlm download report <nb-id> --output report.md
nlm download audio <nb-id> --output podcast.mp3
nlm download quiz <nb-id> --output quiz.html --format html
nlm download all <nb-id> --output-dir ./exports/
nlm download all --all-notebooks --output-dir ./exports/ --skip-existing
```

---

## Organization & Cross-Notebook

```bash
# Aliases
nlm alias set <name> <uuid>
nlm alias get <name>
nlm alias list

# Tags
nlm tag add <nb-id> --tags "meta-study,sr"
nlm tag list
nlm tag select "meta-study"

# Cross-notebook query
nlm cross query "<question>" --notebooks "id1,id2"
nlm cross query "<question>" --tags "meta-study"

# Batch
nlm batch studio audio --tags "meta-study"

# Pipelines
nlm pipeline list
nlm pipeline run research-and-report --notebook <id> --input-url "<url>"
```

---

## Chat & Notes

```bash
# Query (one-shot — use this, NOT chat start)
nlm notebook query <nb-id> "<question>"
nlm notebook query <nb-id> "<follow-up>" --conversation-id <conv-id>

# Chat history
nlm chats list <nb-id>
nlm chats get <nb-id> [conversation-id]
nlm chats export <nb-id> --format md -o chat.md
```

---

## Diagnostics

```bash
nlm --version
nlm --help
nlm <command> --help
nlm doctor
nlm doctor --verbose
```
