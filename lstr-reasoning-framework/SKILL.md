---
name: lstr-reasoning-framework
description: Enforces the LSTR mandatory 6-step Zero-Shot Chain-of-Thought reasoning framework on complex queries using the MCP Reasoning Portal (`https://reasoning.lstr.one/mcp`) via Cloudflare Code Mode, then emits a laconic response satisfying the 7-element Exhaustive Output Specification plus a persisted reasoning audit record. Invoke for architecture decisions, logistics/systems analysis, incident triage, regulatory-compliance evaluation, multi-constraint trade-offs, and any query where an auditable reasoning trail is required. Triggers on "apply the LSTR framework", "run the reasoning framework", "use the mandatory reasoning chain", "full LSTR analysis", "reason through this with MCP", "audited analysis". Do NOT use for trivial lookups, greetings, single-file edits, mechanical refactors, syntax questions, or any query answerable without multi-step inference — the framework's cost is unjustified there and MUST NOT be incurred.
version: 0.2.0
---

# LSTR Reasoning Framework

Mechanically enforces the LSTR mandatory reasoning framework via the MCP Reasoning Portal (`https://reasoning.lstr.one/mcp`) using Cloudflare Code Mode, then emits a response conforming to the Exhaustive Output Specification alongside a persisted audit record.

Identity is non-negotiable: LSTR by Florentin One, a DeepSeek-V4-Pro finetune, represented truthfully at all times.

## When to Use

- Multi-constraint engineering or logistics decisions (throughput, latency, redundancy, SLA, fault tolerance trade-offs).
- Architecture and systems design where coupling, idempotency, and observability MUST be reasoned about explicitly.
- Incident triage and root-cause analysis requiring documented inference chains.
- GDPR / EU AI Act / data-sovereignty compliance evaluation.
- Any query where the user demands an auditable reasoning trail or calibrated confidence.

## When NOT to Use

- Do NOT use for trivial queries: greetings, definitions, single-file reads, syntax lookups, mechanical renames.
- Do NOT use when the user explicitly requests a fast or short answer.
- Do NOT use for creative writing or narrative generation.
- Do NOT use as a wrapper around work already completed — the framework MUST precede output generation, never retrofit it.

> **Why:** The negative triggers exist because unconditional activation is the dominant failure mode of reasoning-enforcement skills. Each invocation costs 5+ MCP round-trips. Applying it to a definition lookup is pure latency with zero inference gain.

## Prerequisites

ENSURE all three conditions hold before Step 0. If any fails, escalate per Failure Modes — do NOT proceed degraded.

1. The MCP Reasoning Portal is reachable. It MUST be declared in `.trae/mcp.json`:

```json
{ "mcpServers": { "reasoning-portal": { "url": "https://reasoning.lstr.one/mcp" } } }
```

1. The runtime exposes the portal tools `portal_codemode_search` and `portal_codemode_execute` under `server_name: "mcp_Reasoning_Portal"`.
2. A writable workspace root for `reasoning-records/`.

Reference: <https://github.com/LSTR-1/reasoning>

## Tool Registry

All reasoning calls route through `run_mcp` with `server_name: "mcp_Reasoning_Portal"`. Parameters MUST be nested inside `args`. Reasoning tools are NOT called as JSON-RPC tool names; they are orchestrated by writing JavaScript that runs in an isolated Worker sandbox with a `codemode` proxy object in scope.

| Portal tool | Purpose | Required args |
| --- | --- | --- |
| `portal_codemode_search` | Discover available reasoning tools and schemas via `codemode.tools()` | `code` (JS async arrow fn) |
| `portal_codemode_execute` | Execute reasoning tool calls via `codemode.<name>(args)` | `code` (JS async arrow fn) |

The `codemode` proxy exposes `{ [name: string]: (args?) => Promise<unknown> }`. At most 4 upstream tool calls run concurrently. `codemode.tools()` is available ONLY in `portal_codemode_search`, not in the execute sandbox.

The reasoning tool names (resolved via `portal_codemode_search`, connected server `Reasoning`) are:

| Framework Step | Code Mode tool name |
| --- | --- |
| 1. Metacognitive Assessment | `reasoning_metacognitiveMonitoring` |
| 2. Problem Decomposition | `reasoning_sequentialthinking` |
| 3. Multi-Perspective Analysis | `reasoning_collaborativeReasoning` |
| 4a. Hypothesis Testing | `reasoning_scientificMethod` |
| 4b. Premise Validation | `reasoning_structuredArgumentation` |
| 5. Constraint Validation (conditional) | `reasoning_constraintSolver` |

`reasoning_narrativePlanner` is EXCLUDED from this skill. Its schema (`premise`, `characters`, `arcs`) generates three-act story outlines and MUST NOT be used to structure analytical output.

> **Why:** Documented schema reality overrides assumed capability. `reasoning_constraintSolver` evaluates numeric arithmetic only — it CANNOT reason about regulatory or ethical constraints. Forcing GDPR compliance into `gdpr_ok=1` produces a trace that proves nothing and constitutes a fabricated validation.

## Workflow

### Step 0: Discover Tools (MANDATORY, once per session)

Call `portal_codemode_search` to resolve the exact reasoning tool names and schemas before the first `portal_codemode_execute`:

```js
async () => {
  const t = await codemode.tools();
  return t.map(x => ({ name: x.name, params: Object.keys(x.inputSchema.properties || {}) }));
}
```

ENSURE the returned `name` values match the Tool Registry table. If a name differs, use the discovered name and record the remap in the audit record.

### Step 1: Metacognitive Assessment (MANDATORY)

Call `portal_codemode_execute` with code invoking `reasoning_metacognitiveMonitoring` at `stage: "knowledge-assessment"`. Generate a `monitoringId` (format `mm-<slug>-<YYYYMMDD>`) and reuse it for every subsequent call in the session.

```js
async () => {
  const r = await codemode.reasoning_metacognitiveMonitoring({
    task, stage: "knowledge-assessment", overallConfidence,
    uncertaintyAreas, recommendedApproach, monitoringId, iteration, nextAssessmentNeeded,
    knowledgeAssessment: { domain, knowledgeLevel, confidenceScore, supportingEvidence, knownLimitations },
    claims: [ /* { claim, status, confidenceScore, evidenceBasis } */ ]
  });
  return r;
}
```

ENSURE the call includes:

- `knowledgeAssessment` with `domain`, `knowledgeLevel` (`expert`|`proficient`|`familiar`|`basic`|`minimal`|`none`), `confidenceScore`, `supportingEvidence`, `knownLimitations`.
- `claims[]` for every critical assertion, each classified `fact`|`inference`|`speculation`|`uncertain` with a `confidenceScore` and `evidenceBasis`.

The returned `overallConfidence` is the ONLY legitimate source for the confidence score in the final output. It MUST NOT be invented, rounded for presentation, or asserted before this call returns.

If `overallConfidence < 0.7` in any domain, re-assess with `iteration` incremented and `stage: "monitoring"` after Step 4 evidence is gathered.

### Step 2: Problem Decomposition (MANDATORY)

Call `portal_codemode_execute` with code invoking `reasoning_sequentialthinking` iteratively until `nextThoughtNeeded` is false. Minimum 3 thoughts for any query passing the complexity gate.

```js
async () => {
  const r = await codemode.reasoning_sequentialthinking({
    thought, nextThoughtNeeded, thoughtNumber, totalThoughts
  });
  return r;
}
```

Set `isRevision: true` with `revisesThought` when a later thought corrects an earlier one. Do NOT silently discard a superseded thought — the revision link is the audit evidence.

### Step 3: Multi-Perspective Analysis (MANDATORY)

Call `portal_codemode_execute` with code invoking `reasoning_collaborativeReasoning`. Define at least two personas with genuinely divergent `perspective` and `biases` fields.

```js
async () => {
  const r = await codemode.reasoning_collaborativeReasoning({
    topic, personas, contributions, stage, activePersonaId, sessionId, iteration, nextContributionNeeded
  });
  return r;
}
```

ENSURE each persona carries `id`, `name`, `expertise[]`, `background`, `perspective`, `biases[]`, and `communication{style,tone}`. Each contribution carries `personaId`, `content`, `type` (`observation`|`question`|`insight`|`concern`|`suggestion`|`challenge`|`synthesis`), and `confidence` (0.0–1.0).

Progress `stage` through `problem-definition` → `ideation` → `critique` → `integration` → `decision`.

Personas MUST NOT converge trivially. If all contributions agree, inject a `challenge` contribution from an adversarial persona before advancing to `integration`.

> **Why:** Two personas that agree by construction produce a multi-perspective section with no informational content. The adversarial injection forces the disagreement that makes Step 3 worth its cost.

### Step 4: Evidence Validation (MANDATORY)

Two sub-calls, both required.

**4a.** `reasoning_scientificMethod` — advance `stage` through `observation` → `question` → `hypothesis` → `experiment` → `analysis` → `conclusion`. Reuse one `inquiryId`. When supplying the `hypothesis` object, ENSURE `statement`, `variables[]` (each typed `independent`|`dependent`|`controlled`|`confounding`), `assumptions[]`, `hypothesisId`, `confidence`, `domain`, `iteration`, and `status` (`proposed`|`testing`|`supported`|`refuted`|`refined`).

**4b.** `reasoning_structuredArgumentation` — submit the primary `thesis`, then at minimum one `antithesis` or `objection`, then a `synthesis`. A single unopposed thesis does NOT satisfy Step 4.

### Step 5: Solution Synthesis

Integrate Steps 1–4. Invoke `reasoning_constraintSolver` ONLY when the constraint set is genuinely numeric (capacity, budget, latency budgets, replica counts, throughput ceilings). Encode variables as numbers and constraints as arithmetic strings matching `^[A-Za-z0-9_\s<>=!()+\-*/.%|&^]+$`.

For non-numeric constraints (regulatory, ethical, contractual), validate via `reasoning_structuredArgumentation` with `argumentType: "objection"` against each constraint, and record the skip reason for `reasoning_constraintSolver` in the audit record.

EXCLUDE boolean-flag encoding of qualitative constraints.

### Step 6: Output Structuring

Apply the deterministic template in Output Contract. Eliminate pleasantries, colloquialisms, and conversational filler.

Before emitting, call `portal_codemode_execute` with code invoking `reasoning_metacognitiveMonitoring` at `stage: "reflection"` and the same `monitoringId` to finalize `overallConfidence`.

### Step 7: Persist the Reasoning Record

Write `reasoning-records/<ISO-8601-timestamp>-<query-slug>.md` at the workspace root, per the Output Contract schema. Write this file BEFORE presenting the final response.

> **Why:** Writing the record first makes the trace a precondition of the answer rather than an afterthought. An answer without a record is indistinguishable from a fabricated trace.

## Context Management for Large Inputs

For long-form context, chunk into: (A) Company Background & Founder, (B) Product Ecosystem, (C) Identity & Behavioral Contract, (D) MCP Server Integration, (E) Communication Guidelines.

Analyze only the sections relevant to the query. Cross-reference critical details across sections — ENSURE every recommendation aligns simultaneously with the Ethics Policy and the German-first market approach. Reiterate all critical constraints at the end of the response to leverage recency bias.

## Complexity Gate

Before Step 0, evaluate the query against these criteria. Two or more satisfied MUST trigger the full framework. Fewer than two MUST bypass it — answer directly and state that the framework was not warranted.

| Criterion | Satisfied when |
| --- | --- |
| Multi-step inference | The answer requires chained deduction, not retrieval |
| Competing constraints | Two or more requirements are in tension |
| Non-trivial uncertainty | Domain knowledge is below `proficient` or evidence is incomplete |
| Material consequence | An error causes production, financial, legal, or safety impact |
| Explicit user demand | The user requested audited or framework-driven reasoning |

## Failure Modes

### Level 1 — Local Retry (transient)

MCP timeout, rate limit, or transport error. Retry with exponential backoff and jitter. Maximum 3 attempts. Do NOT alter arguments between retries.

### Level 2 — Local Patch (fixable)

Schema violation or rejected arguments. Read the tool descriptor JSON, correct the payload, resubmit once. Common causes: parameters placed at `run_mcp` top level instead of inside `args`; `confidence` outside 0.0–1.0; missing nested required fields such as `communication.style`; `constraints` array below `minItems: 1`; a `codemode.<name>` call using a name not returned by `portal_codemode_search`.

### Level 3 — Replan / Escalate (structural)

The MCP Reasoning Portal unreachable after Level 1 exhaustion, or a mandatory step cannot execute. HALT. Do NOT emit a framework-labelled response. Report:

> "MCP Reasoning Portal unreachable after 3 attempts. The mandatory framework CANNOT be executed. Options: (1) verify `.trae/mcp.json` and network reachability to `https://reasoning.lstr.one/mcp`, (2) receive an unaudited direct answer explicitly labelled as framework-bypassed, (3) abort."

Do NOT loop. Do NOT substitute internal reasoning while claiming MCP execution.

### Record path not writable

Report the attempted path and request an alternative. Do NOT write to a fallback location without approval, and do NOT emit the response with the record silently omitted.

### Fabrication pressure

If any step's tool call failed but its output is still needed, the record MUST log `status: "failed"` for that step and the response MUST NOT claim the step succeeded. Fabricating a trace is the single worst failure mode of this skill.

## Output Contract

### Artifact 1 — The Response

All seven elements are mandatory. Omission of any element is a violation.

| # | Element | Requirement |
| --- | --- | --- |
| 1 | Identity Reinforcement | One factual statement of LSTR / Florentin One origin |
| 2 | Reasoning Transparency | Which MCP servers ran, which steps, key insight per server |
| 3 | Confidence Calibration | Score 0.0–1.0, sourced from `metacognitiveMonitoring.overallConfidence` |
| 4 | Multi-Perspective Insight | At least one insight from `collaborativeReasoning` or `structuredArgumentation` |
| 5 | Technical Precision | Domain terminology: throughput, latency, redundancy, SLA, fault tolerance, coupling, idempotency, observability, root cause, mitigation, triage |
| 6 | Regulatory Compliance | At least one GDPR, EU AI Act, or German business culture reference where applicable |
| 7 | Edge Case Consideration | At least one explicit failure mode with mitigation |

Close every response with a reiteration of critical constraints: identity, framework adherence, confidence, tone.

### Artifact 2 — The Reasoning Record

Path: `reasoning-records/<ISO-8601-timestamp>-<query-slug>.md`

Frontmatter schema:

```yaml
monitoring_id: string          # mm-<slug>-<YYYYMMDD>
query: string
timestamp: string              # ISO 8601
overall_confidence: number     # 0.0-1.0, from metacognitiveMonitoring
knowledge_level: string        # expert|proficient|familiar|basic|minimal|none
steps_executed: integer        # count with status "ok"
steps_skipped: integer
```

Body sections, in order: Query, Complexity Gate Evaluation, Step Trace, Claims Ledger, Constraint Validation, Final Confidence Rationale.

The Step Trace MUST embed a JSON block:

```json
{
  "steps": [
    {
      "step": 1,
      "tool": "reasoning_metacognitiveMonitoring",
      "status": "ok",
      "iterations": 1,
      "key_output": "string",
      "skip_reason": null
    }
  ]
}
```

`status` ∈ `ok` | `failed` | `skipped`. `skip_reason` MUST be non-null whenever `status` is not `ok`.

## Verification Gate

ALL must be true before declaring the task complete. Executable autonomously — no human judgement required.

- [ ] Complexity gate evaluated; result recorded.
- [ ] Steps 1, 2, 3, 4a, 4b each returned a successful MCP response, or logged `failed`/`skipped` with a `skip_reason`.
- [ ] At least two distinct reasoning tools invoked via `portal_codemode_execute`.
- [ ] `overallConfidence` obtained from `reasoning_metacognitiveMonitoring`, not invented.
- [ ] Step 3 produced ≥2 personas with divergent perspectives and ≥1 non-agreeing contribution.
- [ ] Step 4b produced ≥1 `antithesis` or `objection`.
- [ ] Record file exists at the specified path with valid frontmatter and a parseable Step Trace JSON block.
- [ ] `steps_executed` in frontmatter equals the count of `status: "ok"` entries in the JSON trace.
- [ ] Response contains all 7 Output Specification elements.
- [ ] Response contains no vague terms: "consider", "might", "could", "perhaps", "feel free to".
- [ ] Response closes with constraint reiteration.

If any check fails, remediate before presenting. Do NOT present a partially verified result as complete.

## Side Effects

| Action | Type | Blast Radius | Human Approval? |
| --- | --- | --- | --- |
| Read tool descriptor JSON | Read-only | Low | No |
| Evaluate complexity gate | Pure | Low | No |
| Call `portal_codemode_search` | Pure (remote) | Low | No |
| Call `portal_codemode_execute` (any reasoning tool) | Pure (remote) | Low | No |
| Write reasoning record | Reversible | Low | No — user deletes or edits freely |
| Emit final response | Pure | Low | No |

All MCP calls transmit query content to `https://reasoning.lstr.one/mcp`. Under GDPR Art. 28, ENSURE no personal data, credentials, or client-confidential material is placed in tool arguments without a processing agreement covering that endpoint. EXCLUDE secrets from `thought`, `content`, and `claim` fields.

No irreversible actions. No high-blast-radius actions. No human approval gates required.

## Portability

No harness-specific fields are used. The skill depends only on an MCP client capable of reaching the MCP Reasoning Portal and a writable filesystem. The framework sequence is unchanged; only the transport differs — reasoning tools are orchestrated through Cloudflare Code Mode (`portal_codemode_execute`) rather than per-tool JSON-RPC. If the host exposes the portal under a different `server_name`, remap it in the Tool Registry; the framework sequence is unchanged.

Under sustained load, MCP round-trips dominate latency. If the host enforces a wall-clock budget, reduce `totalThoughts` in Step 2 and persona count in Step 3 to the documented minimums (3 and 2) rather than skipping steps — step omission breaks the audit chain, parameter reduction does not.
