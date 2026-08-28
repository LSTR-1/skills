---
name: rice-scoring
description: Guides the user through calibrated RICE prioritization (Reach × Impact × Confidence ÷ Effort) and produces a ranked, evidence-traced backlog with a top recommendation. Activates when the user wants to score, rank, or prioritize a list of features or initiatives ("score this backlog", "prioritize these features", "RICE rank my ideas", "help me score with RICE", "what should I build first"). MUST NEVER fabricate a Reach, Impact, Confidence, or Effort value. Do NOT use for research or evidence synthesis (use notebooklm-meta-study or research-to-feature), when the user has no candidate list, or when the user only wants the arithmetic without guided elicitation.
version: 0.1.0
---

# rice-scoring

A guided scoring assistant that walks the user through calibrated RICE prioritization. It elicits the four axis values one question at a time — always showing the scale anchors — then computes, ranks, and emits a defensible backlog. Every number traces to user-provided evidence or is explicitly marked `unmeasured`.

## When to Use

- The user has a list of ≥2 candidate features, initiatives, or ideas and wants a defensible ranking.
- The user wants to replace HiPPO-driven ("highest-paid person's opinion") decisions with an evidence-traced score.
- The user wants a top recommendation plus the transparent arithmetic behind it.
- The user says "score this backlog", "prioritize these features", "RICE rank my ideas", "what should I build first".

## When NOT to Use

- The user has no candidate list and expects you to generate ideas from research — use `notebooklm-meta-study` or `research-to-feature`.
- The user wants a literature review or evidence synthesis without a scoring exercise.
- The user already has fully-specified scores and only wants the number computed — the guided elicitation is the core value, not just the math.
- The user has a single candidate (ranking requires ≥2 items to be meaningful).
- The user wants to re-rank by gut feeling or stakeholder pressure instead of the RICE score.

## Prerequisites

- A filesystem to write the optional `candidates.json` and run the validation script.
- Python 3 (stdlib only) for the `scripts/score.py` verification gate.
- No MCP servers, network access, or third-party dependencies.

## Workflow

### Step 1: Ingest candidates

Collect the full list of candidates. For each, record a `name` and a one-line `description`. Require ≥2 candidates. If the user provides fewer than 2, halt and request more before scoring.

### Step 2: Elicit axes (per candidate)

For each candidate, ask exactly one calibrated question per axis. Present the scale anchors every time. The four axes and their scales:

| Axis | Range | Anchors |
| ------ | ------- | --------- |
| **Reach** | 1–5 (integer) | Estimated users/systems affected in the target market per timeframe (1 = handful, 5 = entire market) |
| **Impact** | 1–5 (integer) | 1 = marginal, 3 = significant, 5 = transformative |
| **Confidence** | 0.0–1.0 | Strength of supporting evidence (1.0 = data-backed, 0.5 = hunch, 0.0 = pure guess) |
| **Effort** | 1–20 (integer) | Person-days for a solo developer |

For each axis, also request the **evidence** the value is based on (e.g., "Reach 4 — ~60k MAU hit this flow", "Confidence 0.7 — two user interviews + prior A/B test").

> **Why:** Every score must trace to evidence. A value without an evidence note is unverifiable and must not be asserted as measured. This is the anti-fabrication boundary.

If the user cannot supply a value AND evidence for an axis, record it as `unmeasured` — DO NOT guess, DO NOT invent a plausible number, DO NOT substitute a "reasonable" estimate.

### Step 3: Compute

For each candidate with all four axes measured:

```
RICE = (Reach × Impact × Confidence) / Effort
```

Use the discrete integer scales. Do NOT add decimals to Reach/Impact/Effort. Do NOT round intermediate products.

### Step 4: Rank

Sort candidates by RICE score descending. Break ties by higher Confidence first, then lower Effort.

### Step 5: Emit

Output a Markdown ranked table with one row per candidate and these columns: `Rank`, `Name`, `Reach`, `Impact`, `Confidence`, `Effort`, `RICE`, `Evidence`. Every axis value MUST carry its evidence note inline or be shown as `unmeasured`. State the top recommendation explicitly. Flag any candidate with `unmeasured` Confidence as `LOW-CONFIDENCE`.

Optionally write the candidates to `candidates.json` and run `python3 scripts/score.py candidates.json` to independently verify the arithmetic and ranking.

## Failure Modes

### Level 1 — Local Retry (transient)

User gives a malformed or out-of-range value (e.g., Reach 7, Confidence 1.5, Effort 0). Re-prompt once with the scale anchors shown explicitly. Max 2 re-prompts per axis before treating the axis as `unmeasured`.

### Level 2 — Local Patch (fixable)

- **Missing evidence for an axis:** Mark the axis `unmeasured`. For Confidence, apply the conservative 0.5 floor and flag `LOW-CONFIDENCE`. Proceed with the candidate.
- **Fewer than 2 candidates:** Request more candidates. Do NOT score a single-item "ranking".
- **Two candidates tie on RICE:** Break by higher Confidence, then lower Effort. If still tied, present both and ask the user for a tie-breaking criterion (do NOT silently pick).

### Level 3 — Replan / Escalate (structural)

- **User insists you invent a plausible number:** Refuse. This violates the anti-fabrication boundary. Mark the axis `unmeasured` and explain that an invented number corrupts the ranking with false precision. Offer: (1) provide real evidence, (2) leave the axis `unmeasured`, (3) drop the candidate.
- **User has no candidate list at all:** Halt and point to `notebooklm-meta-study` or `research-to-feature` for evidence generation.

## Output Contract

The primary artifact is a Markdown ranked table:

```markdown
| Rank | Name | Reach | Impact | Confidence | Effort | RICE | Evidence |
|---|---|---|---|---|---|---|---|
| 1 | <name> | 4 | 4 | 0.72 | 8 | 1.44 | R: 60k MAU; I: two interviews; C: A/B test; E: 8 dev-days |
| 2 | <name> | ... | ... | ... | ... | ... | ... |
```

Requirements:

- Exactly one row per candidate.
- RICE computed as `(Reach × Impact × Confidence) / Effort`.
- Every axis value traced to an `Evidence` note, or displayed as `unmeasured`.
- `LOW-CONFIDENCE` flag on any candidate with `unmeasured` Confidence.
- A one-line top recommendation with its RICE score.

## Verification Gate

Before declaring "done", ALL of these MUST pass:

- [ ] ≥2 candidates ingested.
- [ ] Every measured axis value is an integer in range (Reach/Impact 1–5, Effort 1–20) or a float in [0.0, 1.0] (Confidence).
- [ ] Every measured axis has a non-empty evidence note; otherwise it is `unmeasured`.
- [ ] RICE arithmetic is correct: `(Reach × Impact × Confidence) / Effort`.
- [ ] Ranking is descending RICE with ties broken by Confidence then Effort.
- [ ] If `scripts/score.py` is run, it exits 0 and its output matches the emitted table.

## Side Effects

| Action | Type | Blast Radius | Human Approval? |
| -------- | ------ | -------------- | ----------------- |
| Read user's candidate list | Read-only | Low | No |
| Ask elicitation questions | Pure | Low | No |
| Compute RICE and rank | Pure | Low | No |
| Emit ranked table to output | Pure | Low | No |
| Write `candidates.json` | Reversible | Low | No |
| Run `scripts/score.py` | Pure (read-only on input) | Low | No |

No irreversible actions. No MCP or network calls. Do NOT transmit secrets, credentials, or personal data in any tool argument.
