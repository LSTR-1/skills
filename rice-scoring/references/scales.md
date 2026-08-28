# RICE Scoring Scales & Anti-Gaming Reference

> **L3 reference for `rice-scoring`.** Load on demand when the agent needs to justify a scale or explain a failure mode. NOT needed for normal scoring.

## Primary rubric (used by this skill)

Sourced from the `research-to-feature` RICE Scoring Framework. Discrete integer scales suppress arbitrary precision and make gaming visible.

| Axis | Range | Anchors |
| ------ | ------- | --------- |
| Reach | 1–5 (integer) | 1 = handful of users, 5 = entire target market |
| Impact | 1–5 (integer) | 1 = marginal, 3 = significant, 5 = transformative |
| Confidence | 0.0–1.0 | 1.0 = data-backed, 0.5 = hunch, 0.0 = pure guess |
| Effort | 1–20 (integer) | Person-days for a solo developer |

Formula: `RICE = (Reach × Impact × Confidence) / Effort`

## Historical canonical (Intercom origin)

The framework was created by Sean McBride at Intercom (~2014) as an extension of ICE (Impact × Confidence × Ease) that adds Reach to account for user volume. Intercom's original published scales:

| Axis | Intercom scale |
| ------ | ---------------- |
| Reach | Users/events per timeframe (e.g., customers per quarter) |
| Impact | 3 = massive, 2 = high, 1 = medium, 0.5 = low, 0.25 = minimal |
| Confidence | 100% = high, 80% = medium, 50% = low |
| Effort | Person-months |

The skill's discrete 1–5 / 0.0–1.0 rubric is preferred for consistency with `research-to-feature`; the Intercom scale is documented here for traceability only.

## Anti-gaming failure modes (from the RICE meta-study)

These are the documented ways RICE scores get corrupted. The skill's anti-fabrication rules exist to prevent each one:

| Failure mode | What it is | Skill mitigation |
| -------------- | ----------- | ------------------ |
| **Confidence theater** | Inflating Confidence to "look objective" without real evidence | Confidence must trace to an evidence note, else `unmeasured` + 0.5 floor |
| **Fake reach** | Claiming reach without user-count data | Reach must cite a source (MAU, signups, transactions) |
| **GIGO (garbage in, garbage out)** | The formula cannot fix bad input estimates | Elicitation requires evidence for every measured axis |
| **False precision** | Adding decimals to disguise a guess as measurement | Discrete integer scales for Reach/Impact/Effort |
| **Gaming / score inflation** | Stakeholder pressure to inflate a favored item | The RICE ranking wins over unstated preference; re-ranking by gut feeling is refused |

## Why no fabrication

The single worst failure mode in prioritization is asserting a made-up number as a measurement. An invented score produces a defensible-looking but wrong ranking — worse than no ranking, because it launders a guess through a formula that looks objective ("politics with a math costume").

A value that cannot be traced to evidence MUST be rendered as `unmeasured`, and an `unmeasured` Confidence is floored at 0.5 and flagged `LOW-CONFIDENCE`. This keeps the ranking honest about what it does and does not know.
