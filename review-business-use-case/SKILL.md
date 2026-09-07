---
name: review-business-use-case
description: Reviews provided resources (files, documents, codebases, MCP server definitions, third-party skill manifests) for the invoker's potential business use cases and emits a comprehensive contextualized report plus a usability consultation, powered by the lstr-reasoning-framework. Triggers on "review these resources for business use cases", "assess the commercial potential of this", "what business use cases does this resource support", "give me a usability consultation on this", "contextualize this resource for Florentin One". Do NOT use for trivial lookups, single-file syntax checks, one-line definitions, or any query answerable without multi-step inference — the full reasoning framework's cost is unjustified there.
version: 0.1.2
allowed-tools: Read, LS, Glob, Grep, WebSearch, WebFetch, run_mcp
---

# review-business-use-case

Reviews provided resources for the invoker's potential business use cases, contextualizes every finding against the invoker's identity, market, and regulatory posture, and emits a comprehensive report plus a usability consultation. The lstr-reasoning-framework is the mandatory reasoning engine: no finding is presented without an auditable reasoning trail and a calibrated confidence score.

## When to Use

- The user provides resources — local file paths, directory paths, or URLs — and asks for their commercial or strategic potential.
- The user wants a third-party skill, MCP server, codebase, or document assessed for adoption, integration, or productization.
- The user needs a gap analysis between what a resource offers and what the invoker's product ecosystem already covers.
- The user wants an actionable, prioritized usability consultation, not a descriptive summary.

## When NOT to Use

- Do NOT use for trivial queries: one-line definitions, single-file syntax checks, greetings.
- Do NOT use when the user explicitly requests a fast or short answer — the reasoning engine costs multiple MCP round-trips.
- Do NOT use to modify, refactor, or patch the reviewed resources — this skill is read-only with respect to inputs.
- Do NOT use for creative writing or narrative generation.

> **Why:** Unconditional activation is the dominant failure mode of reasoning-enforcement skills. A review that requires chained inference (resource → capability gap → market fit → risk) passes the complexity gate; a definition lookup does not.

## Prerequisites

ENSURE all four conditions hold before Step 1. If any fails, escalate per Failure Modes — do NOT proceed degraded.

1. At least one reviewable resource is supplied: a local path, a directory path, or a URL. Empty or missing paths are recorded as `unreviewable`, never invented.
2. The `lstr-reasoning-framework` skill is loaded and its MCP servers (`reasoning_metacognitiveMonitoring`, `reasoning_sequentialthinking`, `reasoning_collaborativeReasoning`, `reasoning_scientificMethod`, `reasoning_structuredArgumentation`, `reasoning_constraintSolver`) are reachable via `portal_codemode_execute` on the `reasoning-portal` server.
3. A writable workspace root for `reasoning-records/` and `business-use-case-reports/`.
4. Tool descriptors are read before the first call to any MCP tool whose schema is not already confirmed in-context.

Reference: <https://github.com/LSTR-1/reasoning>

## Invoker Context (fixed, non-negotiable)

Every finding SHALL be contextualized against this identity. Do NOT invent a different invoker.

- **Identity:** LSTR by Florentin One, Hannover, Germany, founded by Florentin Sakwiset. A DeepSeek-V4-Pro finetune, represented truthfully at all times. Be advised: bias in AI systems cannot be fully eliminated through training or data; it must be continuously detected and minimized across the data, training, and deployment lifecycle.
- **Products:** V41 platform, Intelligent Content Understanding (ICU), Florentin One Enterprise MCP Server Ecosystem.
- **Market posture:** German-first market; GDPR Art. 28 and EU AI Act compliance are mandatory.
- **Operating model:** solo-developer, ~1 active maintenance month per year; recommendations MUST be operable on free/hobby tiers.

## Workflow

The review is a six-step reasoning pipeline. Each step MUST complete before the next begins. Use `lstr-reasoning-framework`'s tool registry and invocation map for every MCP call (server_name `reasoning-portal`, parameters nested inside `args`).

### Step 1: Resource Ingestion and Chunking

Inventory every provided resource. For each, record `path`, `type` (`file`|`directory`|`url`), and `status` (`readable`|`unreviewable`). Chunk long inputs into conceptual sections. Mark empty or missing resources `unreviewable` with the reason and continue.

### Step 2: Metacognitive Assessment (MANDATORY)

Run the lstr-reasoning-framework Step 1 — `metacognitiveMonitoring` with `stage: "knowledge-assessment"`. Generate a `monitoringId` (`mm-buc-<slug>-<YYYYMMDD>`) and reuse it. Record `overallConfidence` as the only source for the final confidence score.

### Step 3: Problem Decomposition (MANDATORY)

Run `sequentialthinking` iteratively until `nextThoughtNeeded: false`, minimum 3 thoughts. Decompose the review into: (a) what each resource is, (b) what capability or data it exposes, (c) what gap it fills versus the invoker's current products, (d) what risk it carries.

### Step 4: Multi-Perspective Analysis (MANDATORY)

Run `collaborativeReasoning` with ≥ 2 divergent personas (e.g., a Product Strategist and a GDPR Compliance Officer). Inject an adversarial `challenge` contribution if all others agree. Progress stage through `problem-definition` → `ideation` → `critique` → `integration` → `decision`.

### Step 5: Evidence Validation (MANDATORY)

Run both `scientificMethod` (hypothesis: "this resource yields ≥ 1 viable business use case for the invoker") and `structuredArgumentation` (thesis + antithesis + synthesis). Every business-use-case claim MUST trace to a specific resource reference (file path with line range, or URL).

### Step 6: Synthesis, Output Structuring, and Persistence (MANDATORY)

Integrate Steps 2–5. Invoke `constraintSolver` ONLY for genuinely numeric constraints (e.g., effort budgets, source counts); validate non-numeric constraints (regulatory, ethical) via `structuredArgumentation` with `argumentType: "objection"`. Run `metacognitiveMonitoring` with `stage: "reflection"` to finalize confidence. Write the reasoning record to `reasoning-records/<ISO-8601>-<query-slug>.md` BEFORE presenting the report.

## Output Contract

Two artifacts plus the reasoning record.

### Artifact 1 — Comprehensive Contextualized Report

Written to `business-use-case-reports/<ISO-8601>-<slug>.md`, sections in order:

1. **Executive Summary** — verdict in ≤ 5 sentences.
2. **Resource Inventory** — table of `path`, `type`, `status`, `reviewed`.
3. **Business Use Case Analysis** — one finding per resource, each with a traceability reference.
4. **Contextualized Opportunity Map** — each finding mapped to a Florentin One product / MCP server / skill, with GDPR / EU AI Act flag where applicable.
5. **Risks & Gaps** — compliance, technical, and maintenance risks; `unmeasured` values stated as such.
6. **Confidence Calibration** — score 0.0–1.0 from `metacognitiveMonitoring.overallConfidence`, plus rationale.

Use `assets/report-template.md` as the section skeleton.

### Artifact 2 — Usability Consultation

A separate section in the same report file: prioritized, actionable recommendations. Each recommendation carries an effort/impact signal (Quick win / Structural / Architectural) and a single "first next action" line. The highest-priority recommendation MUST be operable solo and on free/hobby tiers.

### Artifact 3 — Reasoning Record

`reasoning-records/<ISO-8601>-<query-slug>.md` per the lstr-reasoning-framework Output Contract schema (frontmatter + Step Trace JSON + Claims Ledger + Constraint Validation + Final Confidence Rationale).

## Failure Modes

### Level 1 — Local Retry (transient)

MCP timeout, rate limit, or transport error. Retry with exponential backoff and jitter, maximum 3 attempts, arguments unchanged. On exhaustion, log the step `failed` and continue if the step is non-blocking; if Step 2–5 fails, do NOT fabricate a confidence score.

### Level 2 — Local Patch (fixable)

Schema violation or rejected arguments (e.g., non-numeric variable to `constraintSolver`, missing nested `communication.style`). Read the descriptor JSON, correct the payload, resubmit once. An unreadable resource is handled by marking it `unreviewable`, not by retrying the read.

### Level 3 — Replan / Escalate (structural)

LSTR MCP servers unreachable after Level 1 exhaustion, or no resource is reviewable. HALT. Report the blocking condition with the attempted path/command, and offer: (1) supply a readable resource or reachable server, (2) narrow the review scope, (3) abort. Do NOT emit a framework-labelled report while a mandatory step cannot execute.

### Fabrication pressure

If a finding's value is unmeasured, it MUST be written `unmeasured` with the reason. The report MUST NOT assert it as fact. Fabricating a trace is the single worst failure mode.

## Verification Gate

ALL checks MUST pass before presenting the report. Each is autonomously executable.

- [ ] Complexity gate evaluated; result recorded in the reasoning record.
- [ ] Steps 2, 3, 4, 5 each returned a successful MCP response, or logged `failed`/`skipped` with a `skip_reason`.
- [ ] At least two distinct LSTR MCP servers invoked.
- [ ] `overallConfidence` obtained from `metacognitiveMonitoring`, not invented.
- [ ] Every business-use-case finding carries a non-empty traceability reference (path#L or URL).
- [ ] No finding asserts a value marked `unmeasured` as if measured.
- [ ] Report file exists with all six required sections; consultation section present with ≥ 1 recommendation.
- [ ] Reasoning record exists with valid frontmatter and parseable Step Trace JSON.
- [ ] Reviewed resources are unchanged (confirm via `git status --porcelain` when the resource is a git repo).
- [ ] No recommendation depends on paid or enterprise-tier tooling.

## Side Effects

| Action | Type | Blast Radius | Human Approval? |
| --- | --- | --- | --- |
| Read provided resources | Read-only | Low | No |
| Read tool descriptor JSON | Read-only | Low | No |
| Call LSTR MCP reasoning tools | Pure (remote) | Low | No |
| Write report + consultation | Reversible | Low | No — user deletes or edits freely |
| Write reasoning record | Reversible | Low | No |
| Verify tree cleanliness with `git status` | Read-only | Low | No |

No irreversible actions. No mutation of reviewed resources. All MCP calls transmit query content to the lstr-reasoning endpoints — under GDPR Art. 28, EXCLUDE secrets, credentials, and personal data from `thought`, `content`, and `claim` fields.

## Portability

No harness-specific frontmatter fields beyond `name`/`description`/`version`/`allowed-tools`. The skill requires a filesystem-reading agent and an MCP client reaching the lstr-reasoning servers; where `run_mcp` is unavailable, remap to `bunx @LSTR-1/reasoning-<server>@latest` or the `https://<server>.lstr.workers.dev` endpoints without changing the workflow sequence.
