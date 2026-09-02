---
name: research-to-feature
description: Produces a single RICE-scored feature recommendation backed by a NotebookLM meta-study and a business use-case review, ready for a developer to pick up and implement. Chains self-discover → notebooklm-meta-study → review-business-use-case → RICE scoring into one pipeline. The trigger phrases are "research a feature for", "evidence-backed feature proposal", "RICE-scored feature from research", "turn research into a feature spec", "meta-study to feature", and "research-to-feature pipeline". Do NOT use for trivial lookups, single-skill tasks, feature ideas without research backing, or any query where the user already has a fully specified feature — this skill generates evidence from scratch.
version: 0.1.1
allowed-tools: Read, Write, LS, Glob, Grep, WebSearch, WebFetch, run_mcp, Skill, Task
---

# research-to-feature

Bridges the gap between research synthesis and implementation-ready feature specifications. Chains three existing skills — `self-discover`, `notebooklm-meta-study`, `review-business-use-case` — into a single pipeline that terminates in exactly one RICE-scored feature recommendation with a developer-ready implementation spec.

## When to Use

- The user has a research topic and wants a concrete, evidence-backed feature to build.
- The user wants to validate a product idea against published research before committing development effort.
- The user needs a prioritized, scored feature recommendation with traceable evidence.
- The user says: "research a feature for X", "give me an evidence-backed feature proposal for Y", "turn this research into something I can build", "RICE-scored feature from research on Z".

## When NOT to Use

- The user already has a fully specified feature and just needs implementation — this skill generates evidence, not code.
- The user wants a general literature review without a feature recommendation — use `notebooklm-meta-study` directly.
- The user wants a business assessment without research backing — use `review-business-use-case` directly.
- The user asks a trivial question answerable without multi-step inference.
- The user wants multiple feature recommendations — this skill produces exactly one top-scored feature.

> **Why:** Unconditional activation is the dominant failure mode. This skill costs significant MCP round-trips (meta-study + reasoning framework). It MUST only activate when the user genuinely needs the full research-to-feature pipeline.

## Prerequisites

Three skills MUST be installed and operational. Verify via `self-discover` in Phase 1.

| Skill | Purpose | Verification |
| --- | --- | --- |
| `self-discover` | Capability inventory at pipeline start | Invoke and confirm it returns a capability table |
| `notebooklm-meta-study` | Deep web research and evidence synthesis | `nlm doctor` passes; `nlm login` passes |
| `review-business-use-case` | Commercial assessment of meta-study findings | `lstr-reasoning-framework` MCP servers reachable |

Required MCP servers:

- `mcp_NotebookLM` — for the meta-study phase
- `mcp_lstr-reasoning` — for the business-use-case review phase

If `self-discover` reports any prerequisite missing, HALT and output the exact installation command. Do NOT proceed degraded.

## Workflow

The pipeline executes four sequential phases. Each phase MUST complete before the next begins. No phase may be skipped.

### Phase 1: Capability Discovery

Invoke `self-discover` to inventory available skills and MCP servers.

Verify the capability table contains entries for `self-discover`, `notebooklm-meta-study`, and `review-business-use-case`. Verify `mcp_NotebookLM` and `mcp_lstr-reasoning` appear in the MCP tools inventory.

If any prerequisite is absent:

```
HALT: Missing prerequisite: <skill-or-server-name>.
Installation: <command or instruction>.
Re-run after installation.
```

If all prerequisites are present, capture the capability inventory for the report appendix and proceed to Phase 2.

> **Why:** Self-discover at pipeline start prevents the most common failure mode — discovering a missing dependency mid-pipeline after already spending time and API budget on partial work.

### Phase 2: Meta-Study

Delegate to `notebooklm-meta-study` with the user's topic. The meta-study skill executes its full 7-step workflow: topic decomposition, deep web research, deduplication, cross-source synthesis, cross-notebook aggregation, artifact generation, and local export.

Capture the meta-study output:

- The master notebook ID
- The exported report file path (`exports/<topic-slug>/report.md`)
- The confidence annotation from Step 4 of the meta-study workflow
- The cross-notebook synthesis from Step 5

If the meta-study fails after exhausting its retry budget, HALT and report:

```
Meta-study failed: <failure reason from notebooklm-meta-study>.
The pipeline cannot proceed without evidence synthesis.
Options: (1) Retry with a narrower topic, (2) Provide URLs directly for source ingestion, (3) Abort.
```

> **Why:** The meta-study is the evidence backbone. Without it, the RICE Confidence axis has no empirical basis and the entire recommendation becomes speculative. The pipeline MUST NOT fabricate evidence.

### Phase 3: Business-Use-Case Review

Delegate to `review-business-use-case` with the meta-study output as the reviewable resource. Pass the exported report file path and the cross-notebook synthesis as inputs.

The review skill executes its 6-step reasoning pipeline and produces:

- A contextualized report mapping findings to Florentin One products
- A usability consultation with prioritized recommendations
- A calibrated confidence score from `metacognitiveMonitoring`

Capture the business-use-case report path and the confidence score.

If the review fails after exhausting its retry budget, HALT and report:

```
Business-use-case review failed: <failure reason>.
Options: (1) Retry with the meta-study report only, (2) Proceed with RICE scoring using meta-study evidence alone (confidence will be capped at 0.5), (3) Abort.
```

> **Why:** The business-use-case review provides the commercial lens — strategic fit, market pull, and regulatory compliance flags. Without it, the RICE Reach and Impact axes lack market grounding. However, a meta-study alone still provides evidence for a research-backed feature; the pipeline can proceed degraded with a confidence cap.

### Phase 4: RICE Scoring and Feature Specification

Extract candidate features from the meta-study synthesis and business-use-case review. Each candidate MUST trace to a specific finding in the meta-study report or business-use-case review.

Score each candidate on the RICE framework (see RICE Scoring Framework section below). Select exactly one candidate with the highest RICE score.

Generate the implementation-ready feature specification for the selected candidate (see Output Contract section below).

Write the final report to disk.

## RICE Scoring Framework

Score each candidate feature on four axes. Every score MUST be traceable to evidence in the meta-study or business-use-case review. Fabricated scores are the single worst failure mode.

| Axis | Range | Definition | Evidence Source |
| --- | --- | --- | --- |
| **Reach** | 1–5 | Estimated users or systems affected within the target market | Business-use-case review: market pull axis |
| **Impact** | 1–5 | User value delivered: 1 = marginal, 3 = significant, 5 = transformative | Meta-study: effect sizes, consensus strength |
| **Confidence** | 0.0–1.0 | Strength of supporting evidence | Meta-study confidence annotation + business-use-case confidence calibration |
| **Effort** | 1–20 | Estimated person-days for a solo developer | Business-use-case review: effort-to-exploit axis |

**Formula:**

```
RICE = (Reach × Impact × Confidence) / Effort
```

**Scoring rules:**

- Reach and Impact MUST be integers 1–5. Do NOT use decimals.
- Confidence MUST be sourced from `metacognitiveMonitoring.overallConfidence` (business-use-case review) or the meta-study confidence annotation. Do NOT invent.
- Effort MUST be an integer 1–20. Default to 10 if the business-use-case review does not provide an estimate, and flag as `unmeasured`.
- If Confidence < 0.5, flag the recommendation as `LOW-CONFIDENCE` and include a "Validation Required" subsection specifying what evidence would raise confidence above 0.5.
- If multiple candidates tie on RICE score, prefer the one with higher Confidence. If still tied, prefer lower Effort.

**Example scoring:**

```
Candidate: "Automated GDPR compliance scanner for MCP server outputs"
Reach: 4 (all EU-based MCP server operators)
Impact: 4 (prevents regulatory fines, mandatory for German market)
Confidence: 0.72 (from meta-study + business-use-case review)
Effort: 8 person-days
RICE = (4 × 4 × 0.72) / 8 = 1.44
```

## Output Contract

The skill produces exactly one file:

**`research-to-feature-reports/<ISO-8601>-<topic-slug>.md`**

The report MUST contain these seven sections in order:

### 1. Executive Summary

Verdict in ≤ 5 sentences. States the selected feature, its RICE score, and the primary evidence backing it.

### 2. Meta-Study Digest

- Topic decomposition (research sub-questions)
- Source count and quality summary
- Key synthesized findings (3–5 bullet points)
- Confidence annotation from the meta-study
- Reference: master notebook ID and exported report path

### 3. Business-Use-Case Digest

- Strategic fit assessment
- Market pull evidence
- GDPR / EU AI Act flags
- Reference: business-use-case report path

### 4. RICE-Scored Feature Recommendation

- Table of all scored candidates with Reach, Impact, Confidence, Effort, and RICE score
- Selected feature: name, description, RICE score, and selection rationale
- If LOW-CONFIDENCE: "Validation Required" subsection

### 5. Implementation Specification

For the selected feature:

- **User Story:** "As a [role], I want [capability] so that [outcome]."
- **Acceptance Criteria:** 3–5 verifiable, testable conditions
- **Technical Approach:** ≤ 3 paragraphs describing architecture, key components, and integration points
- **Affected Components:** List of files, services, or systems that MUST change
- **First Actionable Task:** A single, concrete, executable step a developer can take immediately (e.g., "Create `src/scanner.py` with the `scan_mcp_output()` function stub and its unit test.")

### 6. Confidence Calibration

- Overall confidence score (0.0–1.0), sourced from `metacognitiveMonitoring.overallConfidence`
- Factors raising confidence
- Factors lowering confidence
- `unmeasured` values stated explicitly as `unmeasured` with reason

### 7. Edge Cases & Risks

- At least one explicit failure mode with mitigation
- Regulatory risks (GDPR, EU AI Act)
- Maintenance burden assessment (solo-developer, ~1 month/year budget)
- Free/hobby tier operability assessment

## Failure Modes

### Level 1 — Local Retry (transient)

MCP timeout, rate limit, or transport error during any phase. Retry with exponential backoff and jitter, maximum 3 attempts, arguments unchanged. On exhaustion, log the phase `failed` and proceed to Level 2 or 3 as appropriate.

### Level 2 — Local Patch (fixable)

Missing prerequisite skill or MCP server. HALT and output the exact installation command. Do NOT attempt to work around the missing dependency.

Meta-study returns fewer than 5 sources after two research attempts. Flag the topic as under-sourced. Cap Confidence at 0.4. Proceed with available evidence and document the limitation prominently.

### Level 3 — Replan / Escalate (structural)

Meta-study or business-use-case review fails after exhausting Level 1 retries. HALT. Report the blocking condition. Offer: (1) retry with narrower topic, (2) proceed with partial evidence (Confidence capped at 0.5), (3) abort.

No candidate features extractable from the meta-study or review. HALT. Report: "No actionable features identified. The research did not yield implementable recommendations. Consider broadening the topic or providing additional sources."

### Fabrication pressure

If a RICE axis value cannot be traced to evidence, it MUST be written `unmeasured` with the reason. The report MUST NOT assert it as measured. Fabricating a score is the single worst failure mode.

## Verification Gate

ALL checks MUST pass before presenting the report:

- [ ] Phase 1 completed: `self-discover` confirmed all prerequisites.
- [ ] Phase 2 completed: meta-study report file exists and is non-empty.
- [ ] Phase 3 completed: business-use-case review report file exists and is non-empty (or phase was skipped with documented reason and confidence capped at 0.5).
- [ ] Phase 4 completed: at least one candidate scored; exactly one selected.
- [ ] RICE score computed correctly: `(Reach × Impact × Confidence) / Effort`.
- [ ] Confidence sourced from `metacognitiveMonitoring.overallConfidence` or meta-study annotation, not invented.
- [ ] Report file exists at `research-to-feature-reports/<ISO-8601>-<topic-slug>.md`.
- [ ] All seven report sections present and non-empty.
- [ ] Implementation Specification contains all five subsections.
- [ ] First Actionable Task is a single, concrete, executable step.
- [ ] No RICE axis value asserted as measured when it is `unmeasured`.
- [ ] No recommendation depends on paid or enterprise-tier tooling.

## Side Effects

| Action | Type | Blast Radius | Human Approval? |
| --- | --- | --- | --- |
| Invoke `self-discover` | Read-only | Low | No |
| Invoke `notebooklm-meta-study` | Reversible (notebooks, sources, artifacts) | Medium | No — user can delete notebooks |
| Invoke `review-business-use-case` | Pure (remote reasoning) + Reversible (report write) | Low | No |
| Extract and score candidate features | Pure | Low | No |
| Write final report to disk | Reversible | Low | No — user deletes or edits freely |
| Read meta-study and review outputs | Read-only | Low | No |

No irreversible actions. All MCP calls transmit query content to remote endpoints — under GDPR Art. 28, EXCLUDE secrets, credentials, and personal data from all tool arguments.

## Portability

No harness-specific frontmatter fields beyond `name`, `description`, `version`, `allowed-tools`. The skill requires:

- A filesystem-reading and -writing agent
- `Skill` tool for delegating to constituent skills
- `run_mcp` for MCP server access
- `WebSearch` and `WebFetch` for the meta-study phase

Where `run_mcp` is unavailable, remap to direct MCP client calls. The workflow sequence does not change.

Tested on: TraeCode (primary). Compatible with any agentskills.io-compliant runtime that supports skill delegation and MCP.
