#!/usr/bin/env python3
"""rice-scoring verification gate.

Reads candidates from a JSON file, validates schema and scale ranges, flags
any axis value that is not traceable to an evidence note as `unmeasured`,
computes RICE, ranks (ties: higher Confidence, then lower Effort), and prints
a ranked table.

Usage:
    python3 score.py candidates.json

Input schema (array of candidates):
    {
      "name": "string (required)",
      "description": "string (optional)",
      "reach": 1..5 (int) | null,
      "impact": 1..5 (int) | null,
      "confidence": 0.0..1.0 (float) | null,
      "effort": 1..20 (int) | null,
      "evidence": {
          "reach": "string" | "",
          "impact": "string" | "",
          "confidence": "string" | "",
          "effort": "string" | ""
      }
    }

Exit codes:
    0  success (valid input, correct ranking emitted)
    1  schema / range / evidence error
    2  usage error (missing/invalid file argument)

A numeric axis value with an empty or missing evidence note is flagged as
`unmeasured`. Confidence that is `unmeasured` is floored to 0.5 and flags the
candidate LOW-CONFIDENCE.
"""

import json
import sys

LOW_CONFIDENCE_FLOOR = 0.5

RANGES = {
    "reach": (1, 5),
    "impact": (1, 5),
    "confidence": (0.0, 1.0),
    "effort": (1, 20),
}


def validate_candidate(cand, idx):
    """Validate one candidate; return list of error strings (empty if valid)."""
    errors = []
    if not isinstance(cand, dict):
        return [f"candidate[{idx}]: not an object"]
    if not cand.get("name"):
        errors.append(f"candidate[{idx}]: missing non-empty 'name'")

    for axis, (lo, hi) in RANGES.items():
        val = cand.get(axis)
        if val is None:
            continue  # explicitly unmeasured -> allowed, no range check
        if isinstance(val, bool):
            errors.append(f"candidate[{idx}].{axis}: boolean is not a valid value")
            continue
        try:
            v = float(val)
        except (TypeError, ValueError):
            errors.append(f"candidate[{idx}].{axis}: not numeric")
            continue
        if axis in ("reach", "impact", "effort") and v != int(v):
            errors.append(f"candidate[{idx}].{axis}: must be an integer, got {val}")
        if not (lo <= v <= hi):
            errors.append(
                f"candidate[{idx}].{axis}: out of range [{lo}, {hi}], got {val}"
            )
        # NOTE: a value present with an empty/missing evidence note is NOT a hard
        # error — it is soft-flagged as `unmeasured` in compute()/axis_state().
    return errors


def axis_state(cand, axis):
    """Return (value, is_measured) for a candidate axis."""
    val = cand.get(axis)
    ev = (cand.get("evidence") or {}).get(axis)
    if val is None:
        return None, False
    if not isinstance(ev, str) or not ev.strip():
        return None, False  # measured-without-evidence is treated as unmeasured
    try:
        return float(val), True
    except (TypeError, ValueError):
        return None, False


def compute(cand):
    """Return (rice, confidence_for_rank, low_confidence_flag)."""
    reach, r_ok = axis_state(cand, "reach")
    impact, i_ok = axis_state(cand, "impact")
    confidence, c_ok = axis_state(cand, "confidence")
    effort, e_ok = axis_state(cand, "effort")

    low_conf = not c_ok
    c = confidence if c_ok else LOW_CONFIDENCE_FLOOR

    if not (r_ok and i_ok and e_ok):
        # cannot compute RICE without reach/impact/effort measured
        return None, c, low_conf
    if effort == 0:
        return None, c, low_conf

    rice = (reach * impact * c) / effort
    return rice, c, low_conf


def main(argv):
    if len(argv) != 2:
        print("Usage: python3 score.py candidates.json", file=sys.stderr)
        return 2

    path = argv[1]
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"error: file not found: {path}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as e:
        print(f"error: invalid JSON: {e}", file=sys.stderr)
        return 2

    if not isinstance(data, list):
        print("error: top-level JSON must be an array of candidates", file=sys.stderr)
        return 1

    if len(data) < 2:
        print("error: at least 2 candidates required", file=sys.stderr)
        return 1

    all_errors = []
    for i, cand in enumerate(data):
        all_errors.extend(validate_candidate(cand, i))

    if all_errors:
        for e in all_errors:
            print(f"error: {e}", file=sys.stderr)
        return 1

    rows = []
    for i, cand in enumerate(data):
        rice, conf, low_conf = compute(cand)
        if rice is None:
            continue  # unmeasured reach/impact/effort -> cannot score
        rows.append({
            "name": cand["name"],
            "reach": cand.get("reach"),
            "impact": cand.get("impact"),
            "confidence": cand.get("confidence") if axis_state(cand, "confidence")[1] else "unmeasured",
            "effort": cand.get("effort"),
            "rice": rice,
            "conf_for_rank": conf,
            "low_conf": low_conf,
            "evidence": cand.get("evidence") or {},
        })

    rows.sort(key=lambda r: (-r["rice"], -r["conf_for_rank"], r["effort"]))

    # render table
    header = f"{'Rank':<5} {'Name':<28} {'Reach':<6} {'Impact':<7} {'Confidence':<11} {'Effort':<7} {'RICE':<8}"
    print(header)
    print("-" * len(header))
    for rank, r in enumerate(rows, start=1):
        conf_disp = r["confidence"]
        if isinstance(conf_disp, float):
            conf_disp = f"{conf_disp:.2f}"
        flag = "  [LOW-CONFIDENCE]" if r["low_conf"] else ""
        print(
            f"{rank:<5} {r['name']:<28} {r['reach']:<6} {r['impact']:<7} "
            f"{conf_disp:<11} {r['effort']:<7} {r['rice']:<8.4f}{flag}"
        )

    print()
    if rows:
        top = rows[0]
        print(f"Top recommendation: {top['name']} (RICE = {top['rice']:.4f})")
    else:
        print("No candidate had measurable Reach, Impact, and Effort — nothing to rank.")

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
