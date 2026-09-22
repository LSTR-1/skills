# Platform Tool Reference

> **Port note — `unverified` runtime.** This document references runtime modules under
> `scripts/lib/*.mjs`. Those modules are NOT present in the source plugin directory `sex/`
> and were NOT ported. Every such reference is `unverified`: the agent MUST probe for the
> module at runtime and continue in degraded mode when it is absent. Do NOT assume the module
> exists. Affected modules in this file: `scripts/lib/platform.mjs`.

> Skills reference this document for platform-specific tool syntax. All platforms share the same skill files — this reference resolves the differences.

## Platform Detection

The current platform is determined by the `scripts/lib/platform.mjs` library (`unverified` — see port note above):
- `$SO_PLATFORM` = `trae`
- Environment: `$ORCHESTRATOR_PLUGIN_ROOT`

> **Port note:** The original plugin targeted Claude Code, Codex CLI and Cursor IDE. This port
> targets **TRAE IDE SOLO Mode** exclusively. The three platform branches collapse into one.
> The tables below retain the original columns for traceability; the TRAE column is authoritative.

## Identical Tools (no mapping needed)

These tools have the same name and behavior on TRAE. TRAE uses equivalent built-in tools for file operations and terminal commands.
- **Read** — read file contents
- **Write** — create/overwrite files
- **SearchReplace** — string replacement in files (maps to the original `Edit`)
- **RunCommand** — execute shell commands (maps to the original `Bash`)
- **Glob** — file pattern matching
- **Grep** — content search (ripgrep)
- **LS** — directory listing

## TRAE Tool Mapping (authoritative)

| Function | TRAE IDE SOLO | Notes |
|----------|---------------|-------|
| Present choices to user | `AskUserQuestion` tool with structured options | Native; no numbered-list fallback required |
| Dispatch subagent | `Task({ description, prompt, subagent_type })` | `subagent_type` ∈ `search`, `general_purpose_task`, `browser_use`, `florentin-one-guardian` |
| Track tasks | `TodoWrite` | Structured todo list with status and priority |
| Enter plan mode | Spec Mode (`spec.md` / `tasks.md` / `checklist.md`) | Document-driven, not tool-driven |
| Web search | `WebSearch` tool | Native |
| Web fetch | `WebFetch` tool | Native |
| Read file | `Read` | Native |
| Edit file | `SearchReplace` | Native |
| Run shell | `RunCommand` | Native |
| List directory | `LS` | Native |

## Legacy Platform-Specific Tool Mapping (historical reference)

| Function | Claude Code | Codex CLI | Cursor IDE |
|----------|------------|-----------|------------|
| Present choices to user | `AskUserQuestion` tool with structured options | Numbered Markdown list as plain text, wait for user reply | Numbered Markdown list (same as Codex) |
| Dispatch subagent | `Task({ description, prompt, subagent_type })` | Delegate via Codex subagents / typed roles (`explorer`, `worker`) when available; otherwise execute sequentially in the main session | Sequential execution — no parallel subagents. Execute tasks one by one within a single session. |
| Track tasks | `TaskCreate` / `TaskUpdate` / `TaskList` | Plain-text checklist in response context | Plain-text checklist (same as Codex) |
| Enter plan mode | `EnterPlanMode` / `ExitPlanMode` tools | `/plan` slash command (prompt-level, not tool-based) | Instruction-based: "Focus on analysis and planning. Do not modify files until the user approves." |
| Web search | `WebSearch` tool | Built-in web search (invoke via instruction) | `@web` in Cursor chat |
| Web fetch | `WebFetch` tool | Not available natively; use MCP or Bash curl | Bash curl (same as Codex) |

## AskUserQuestion Fallback Pattern

When a skill instructs "Use the AskUserQuestion tool", apply this pattern:

**On TRAE IDE SOLO:** Use the `AskUserQuestion` tool with structured options as documented. It is native — no fallback required.

**Legacy fallback (Claude Code / Codex CLI / Cursor IDE):** Present the same choices as a numbered Markdown list and ask the user to respond:
```
Choose one:
1. Option A — description
2. Option B — description  
3. Option C — description

Reply with the number of your choice.
```

## Agent Dispatch Pattern

**On TRAE IDE SOLO:**
```
Task({
  description: "3-5 word summary",
  query: "full task context...",
  subagent_type: "general_purpose_task",
  response_language: "German"
})
```
Available `subagent_type` values: `search` (read-only codebase exploration), `general_purpose_task` (implementation), `browser_use` (browser automation), `florentin-one-guardian` (framework validation).

**Legacy (Claude Code):**
```
Task({
  description: "3-5 word summary",
  query: "full task context...",
  subagent_type: "general_purpose_task",
})
```

**Legacy (Codex CLI / Codex Desktop):**
Delegate the task in detail using the available Codex subagent mechanism when it exists. Map work to these roles:
- **explorer** — read-only evidence gathering (maps to TRAE's `search` subagent)
- **worker** — implementation tasks (maps to TRAE's `general_purpose_task` subagent)
- **session-reviewer** — quality review when a dedicated review role is available; otherwise perform the review in the main session

**Legacy (Cursor IDE):**
No Agent() tool or typed agent roles. Execute wave tasks sequentially within the active Composer session. After completing each task, report status and move to the next. Parallel execution is not possible — `agents-per-wave` config is ignored on Cursor.

## Model Preference Mapping

> **Port note:** The original plugin encoded model preferences in skill frontmatter via
> `model-preference`, `model-preference-codex` and `model-preference-cursor`. Those fields were
> REMOVED during the port (harness-specific lock-in). Model selection is now delegated to the
> TRAE runtime. The table below is retained as historical reference only.

| Claude Code | Codex CLI | Cursor IDE | Use Case |
|------------|-----------|------------|----------|
| opus | gpt-5.4 | claude-opus-4-6 | Complex reasoning, architecture, session coordination |
| sonnet | gpt-5.4-mini | claude-sonnet-4-6 | Implementation, review, routine tasks |
| haiku | gpt-5.4-mini | claude-sonnet-4-6 | Simple lookups, fast checks |

## State Directory

- **TRAE IDE SOLO:** `.orchestrator/` (STATE.md, wave-scope.json, session.lock)
- **Shared:** `.orchestrator/metrics/` (sessions.jsonl, learnings.jsonl)

> **Port note:** The original plugin used platform-native state directories (`.orchestrator/`,
> `.orchestrator/`, `.orchestrator/`). This port collapses them to a single `.orchestrator/` directory.
> Legacy references to `.orchestrator/` in ported skills resolve to `.orchestrator/`.

## Config File

- **TRAE IDE SOLO:** Session Config in `AGENTS.md` under `## Session Config`
- **Alias:** `CLAUDE.md` is accepted as a transparent alias per `instruction-file-resolution.md`
- Format is identical across all platforms.
