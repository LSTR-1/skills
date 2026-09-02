# Meta-Study Prompt Templates

Type-specific prompts for all five research types. Use with `nlm report create --format "Create Your Own" --prompt "<prompt>"`.

**Universal Grounding Anchor** — append to EVERY prompt:

```
Use only uploaded sources. Do not invent statistics, quotes, names, or examples not in the sources. Flag any claim that cannot be grounded in the sources with [Inferred].
```

---

## SR — Systematic Review

### Report Prompt

```
Audience: Academic researchers and domain experts.
Goal: Conduct a PRISMA-informed systematic review of [TOPIC].
Structure:
  1. Research Question & Protocol — Formulate a focused research question. Define the review protocol (PICO framework where applicable).
  2. Search Strategy & Selection Criteria — Describe the search approach. List inclusion and exclusion criteria applied.
  3. Included Studies Summary Table — Tabulate all included studies with key characteristics.
  4. Thematic Synthesis of Findings — Organize findings by theme, not by source. Cross-reference multiple sources per theme.
  5. Risk of Bias Assessment — Evaluate methodological quality of included studies. Rate each as Low/Moderate/High risk of bias.
  6. Gaps & Future Research — Identify evidence gaps, unanswered questions, and future research directions.
  7. Conclusions — Summarize key findings with confidence levels.
Constraints:
  - Academic tone. Every claim must map to at least one source.
  - Flag contradictions between sources explicitly.
  - Distinguish evidence-based conclusions from author interpretations.
  - ~3000-5000 words.
Use only uploaded sources. Do not invent statistics, quotes, names, or examples not in the sources.
```

### Data Table Schema

```
Included studies from the systematic review. Columns: Author/Year, Study Design, Sample Size, Intervention, Comparator, Key Findings, Risk of Bias (Low/Moderate/High), Source. One row per study. N/A if not in sources.
```

### Infographic Focus

```
PRISMA flow diagram summary: sources screened → eligible → included. Key findings highlighted with source citations. Professional scientific layout. Use only uploaded sources.
```

---

## MA — Meta-Analysis

### Report Prompt

```
Audience: Quantitative researchers and statisticians.
Goal: Extract and synthesize quantitative findings across studies on [TOPIC].
Structure:
  1. Research Question & Hypotheses — State the meta-analytic research question and directional hypotheses.
  2. Included Studies — For each study: design, sample size, population, measures used, effect size type.
  3. Effect Size Extraction — Per study: effect size value, 95% CI, direction, statistical significance.
  4. Heterogeneity Assessment — Report I² statistic, Q-test results. Interpret heterogeneity (Low/Moderate/High).
  5. Combined Effect & Interpretation — Report pooled effect size, confidence interval, statistical significance. Forest plot description.
  6. Publication Bias Indicators — Funnel plot symmetry assessment, Egger's test where available.
  7. Limitations — Between-study heterogeneity, measurement differences, generalizability constraints.
Constraints:
  - Numeric values from sources only. Mark extrapolations as [Inferred].
  - Report exact values where available; do not round prematurely.
  - Distinguish statistical significance from practical significance.
Use only uploaded sources. Do not invent statistics, quotes, names, or examples not in the sources.
```

### Data Table Schema

```
Study characteristics and effect sizes. Columns: Study, Design, N, Outcome Measure, Effect Size (type + value), 95% CI, Weight, Notes. One row per study. N/A if not in sources.
```

### Quiz Focus

```
Multiple-choice quiz testing understanding of meta-analytic findings: effect size interpretation, heterogeneity concepts, publication bias indicators, study quality assessment. 10 questions, medium difficulty. Use only uploaded sources.
```

---

## ES — Evidence Synthesis

### Report Prompt

```
Audience: Policy-makers and practitioners.
Goal: GRADE-informed evidence synthesis on [TOPIC].
Structure:
  1. PICO Framework — Population, Intervention, Comparison, Outcome(s) defined from sources.
  2. Evidence Profile Table per Outcome — For each outcome: number of studies, study designs, risk of bias, inconsistency, indirectness, imprecision, publication bias.
  3. Overall Certainty of Evidence — Rate each outcome as High, Moderate, Low, or Very Low certainty. Justify ratings.
  4. Balance of Benefits vs Harms — Quantify or describe the benefit-harm ratio from sources.
  5. Recommendations with Strength — Strong vs conditional recommendations, grounded in evidence certainty.
  6. Implementation Considerations — Feasibility, resource requirements, equity implications.
  7. Evidence Gaps — What additional research would change the certainty rating?
Constraints:
  - Rate evidence quality explicitly using GRADE terminology.
  - Distinguish evidence-based statements from expert-opinion statements.
  - Use "we recommend" for strong recommendations, "we suggest" for conditional.
Use only uploaded sources. Do not invent statistics, quotes, names, or examples not in the sources.
```

### Data Table Schema

```
Evidence profile per outcome. Columns: Outcome, Number of Studies, Study Design(s), Risk of Bias, Inconsistency, Indirectness, Imprecision, Publication Bias, Overall Certainty, Source. One row per outcome. N/A if not in sources.
```

### Infographic Focus

```
Evidence pyramid visualization: outcomes ranked by certainty (High to Very Low). Key findings with GRADE ratings. Scientific style, landscape orientation. Use only uploaded sources.
```

### Flashcards Focus

```
Scenario-based cards testing evidence interpretation skills: (1) Rate a study's risk of bias, (2) Assess certainty for a given outcome, (3) Choose the appropriate recommendation strength. Use only uploaded sources.
```

---

## LS — Literature Survey

### Report Prompt

```
Audience: Graduate students and early-career researchers entering [DOMAIN].
Goal: Comprehensive but accessible literature survey of [TOPIC].
Structure:
  1. Domain Overview & Significance — Why this field matters, its scope and boundaries.
  2. Historical Development — Chronological milestones and paradigm shifts.
  3. Current Research Clusters — Thematic map of active research areas (3-5 clusters).
  4. Key Debates & Contested Findings — Where do researchers disagree? What evidence exists on each side?
  5. Methodological Trends — Dominant methods, emerging approaches, methodological critiques.
  6. Influential Works & Authors — Seminal papers, highly-cited works, key research groups.
  7. Future Directions — Emerging trends, unanswered questions, predicted developments.
Constraints:
  - Accessible language. Define all domain-specific terms on first use.
  - ~3000 words. Prioritize breadth over depth.
  - Organize by idea, not by source.
Use only uploaded sources. Do not invent statistics, quotes, names, or examples not in the sources.
```

### Mind Map Focus

```
Literature survey concept map: central topic with branches for historical development, current clusters, key debates, methods, and future directions. Title: "[TOPIC] Literature Landscape".
```

### Slides Focus

```
Teaching deck for visual learners. Hook with surprising stat → 3 core research clusters (diagram each) → key debate → future directions. White background, infographic-style charts. Use only uploaded sources.
```

---

## MR — Multi-Source Research Report

### Report Prompt

```
Audience: [as specified by user, default: informed professionals].
Goal: Synthesize diverse sources into a coherent research report on [TOPIC].
Structure:
  1. Executive Summary — One-page synthesis of key findings, methods, and recommendations.
  2. Background & Context — Why this research was conducted, scope, and boundaries.
  3. Multi-Source Findings — Organized by theme, not source. Each section cross-references 2+ sources.
  4. Cross-Source Patterns & Contradictions — Where do sources agree? Where do they conflict? Resolve or flag tensions.
  5. Implications — For [domain/practice/policy]. Actionable insights.
  6. Source Quality Assessment — Brief evaluation of each major source's credibility, currency, and relevance.
  7. Recommendations — Prioritized, source-grounded.
  8. Appendices — Source inventory, methodology notes, glossary.
Constraints:
  - Professional tone. Every section cross-references multiple sources.
  - Flag source disagreements explicitly.
  - ~2500-5000 words depending on source volume.
Use only uploaded sources. Do not invent statistics, quotes, names, or events not in the sources.
```

### Audio Focus (Deep Dive, ~20 min)

```
Deep-dive podcast for informed professionals. Cover: (1) Why [TOPIC] matters now, (2) Key findings from sources, (3) Where sources disagree, (4) Practical implications, (5) What's next. Conversational tone. Use only uploaded sources.
```

### Slides Focus

```
Board-ready deck. Structure: situation → 3 findings → implications → recommendations → risks. Professional tone. Navy background, white text, blue KPI accents. Use only uploaded sources.
```

---

## Supplementary Artefact Prompts (Cross-Type)

### Audio (Brief, ~5 min)

```
Single-narrator executive brief. Summarize the top 3 findings from sources. Under 5 minutes. For busy professionals who need the essentials. Use only uploaded sources.
```

### Quiz (General, 10 questions)

```
Multiple-choice quiz on [TOPIC] from sources. Mix: (1) definition questions, (2) comparison scenarios, (3) application questions. 10 questions, medium difficulty. Use only uploaded sources.
```

### Flashcards (General)

```
Mix 4 card types: (1) Definition + example, (2) Cause-effect, (3) Comparison A vs B, (4) Application scenario. Focus on repeated terms and key concepts from sources. Use only uploaded sources.
```

### Data Table (General)

```
Extract key [entities/concepts/metrics] from sources. Columns: [Col1], [Col2], [Col3], [Col4], Source. One row per [entity]. N/A if not in sources. Use only uploaded sources.
```
