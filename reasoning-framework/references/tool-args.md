# LSTR MCP Tool Argument Reference (L3)

> On-demand reference for the exact `run_mcp` invocation schema of the LSTR reasoning tools via the MCP Reasoning Portal (Cloudflare Code Mode).
> Load this file only when the agent needs the full required-arg contract per tool.

## Invocation Map (`run_mcp` → this runtime)

All reasoning calls route through `run_mcp` with `server_name: "mcp_Reasoning_Portal"`. Reasoning tools are NOT called as JSON-RPC tool names; they are orchestrated by writing JavaScript that runs in an isolated Worker sandbox with a `codemode` proxy object in scope.

| Portal tool | Purpose | Required args |
| --- | --- | --- |
| `portal_codemode_search` | Discover reasoning tools and schemas via `codemode.tools()` | `code` (JS async arrow fn) |
| `portal_codemode_execute` | Execute reasoning tool calls via `codemode.<name>(args)` | `code` (JS async arrow fn) |

The `codemode` proxy exposes `{ [name: string]: (args?) => Promise<unknown> }`. At most 4 upstream tool calls run concurrently. `codemode.tools()` is available ONLY in `portal_codemode_search`.

| Framework Step | Code Mode tool name | Required args (per schema) |
| --- | --- | --- |
| 1. Metacognitive Assessment | `reasoning_metacognitiveMonitoring` | `task`, `stage`, `overallConfidence`, `uncertaintyAreas`, `recommendedApproach`, `monitoringId`, `iteration`, `nextAssessmentNeeded` |
| 2. Problem Decomposition | `reasoning_sequentialthinking` | `thought`, `nextThoughtNeeded`, `thoughtNumber`, `totalThoughts` |
| 3. Multi-Perspective Analysis | `reasoning_collaborativeReasoning` | `topic`, `personas`, `contributions`, `stage`, `activePersonaId`, `sessionId`, `iteration`, `nextContributionNeeded` |
| 4a. Hypothesis Testing | `reasoning_scientificMethod` | `stage`, `inquiryId`, `iteration`, `nextStageNeeded` |
| 4b. Premise Validation | `reasoning_structuredArgumentation` | `claim`, `premises`, `conclusion`, `argumentType`, `confidence`, `nextArgumentNeeded` |
| 5. Constraint Validation (conditional) | `reasoning_constraintSolver` | `variables` (object of numbers), `constraints` (array of arithmetic strings, minItems 1) |
| EXCLUDED | `reasoning_narrativePlanner` | `premise`, `characters` (array), `arcs` (array) |

## Per-Tool Detail

### 1. reasoning_metacognitiveMonitoring

- `stage` enum: `knowledge-assessment`, `planning`, `execution`, `monitoring`, `evaluation`, `reflection`.
- `knowledgeAssessment` (optional object): `domain`, `knowledgeLevel`
  (expert/proficient/familiar/basic/minimal/none), `confidenceScore` (0–1),
  `supportingEvidence`, `knownLimitations`, `relevantTrainingCutoff`.
- `claims` (optional array): each `{claim, status(fact|inference|speculation|uncertain),
  confidenceScore, evidenceBasis, alternativeInterpretations, falsifiabilityCriteria}`.
- `reasoningSteps` (optional array): each `{step, potentialBiases, assumptions, logicalValidity,
  inferenceStrength}`.
- Required: `task`, `stage`, `overallConfidence`, `uncertaintyAreas`, `recommendedApproach`,
  `monitoringId`, `iteration`, `nextAssessmentNeeded`.

### 2. reasoning_sequentialthinking

- Required: `thought`, `nextThoughtNeeded`, `thoughtNumber`, `totalThoughts`.
- Optional: `isRevision`, `revisesThought`, `branchFromThought`, `branchId`, `needsMoreThoughts`.
- Terminate when `nextThoughtNeeded:false` with a single final answer.

### 3. reasoning_collaborativeReasoning

- `stage` enum: `problem-definition`, `ideation`, `critique`, `integration`, `decision`, `reflection`.
- `personas[]`: each requires `id`, `name`, `expertise[]`, `background`, `perspective`, `biases[]`,
  `communication{style, tone}`.
- `contributions[]`: each requires `personaId`, `content`, `type`
  (observation/question/insight/concern/suggestion/challenge/synthesis), `confidence`.
- Required: `topic`, `personas`, `contributions`, `stage`, `activePersonaId`, `sessionId`,
  `iteration`, `nextContributionNeeded`.

### 4. reasoning_scientificMethod

- `stage` enum: `observation`, `question`, `hypothesis`, `experiment`, `analysis`, `conclusion`,
  `iteration`.
- `hypothesis` (optional object): `statement`, `variables[]`, `assumptions[]`, `hypothesisId`,
  `confidence`, `domain`, `iteration`, `status(proposed/testing/supported/refuted/refined)`.
- `experiment` (optional object): `design`, `methodology`, `predictions[]`, `experimentId`,
  `hypothesisId`, `controlMeasures[]`.
- Required: `stage`, `inquiryId`, `iteration`, `nextStageNeeded`.

### 5. reasoning_constraintSolver

- `variables`: object mapping name → **number**.
- `constraints`: array of **single** boolean-expression strings; allowed charset
  `A-Za-z0-9_ \s<>=!()+*/.%|&^`. Use `&`/`|` (not `&&`/`||`), no commas.
- Required: `variables`, `constraints` (minItems 1).

### 6. reasoning_narrativePlanner (EXCLUDED)

- Required: `premise` (minLength 1), `characters` (array, minItems 1), `arcs` (array, minItems 1).
- Three-act story tool; MUST NOT be used to structure analytical output.

### 7. reasoning_structuredArgumentation

- `argumentType` enum: `thesis`, `antithesis`, `synthesis`, `objection`, `rebuttal`.
- Optional linkage: `argumentId`, `respondsTo`, `supports[]`, `contradicts[]`,
  `strengths[]`, `weaknesses[]`, `suggestedNextTypes[]`.
- Required: `claim`, `premises`, `conclusion`, `argumentType`, `confidence`, `nextArgumentNeeded`.
