#!/usr/bin/env python3
"""Score the blackmail AIME benchmark.

Extracts \\boxed{N} from each results/{cond}_{case}.txt response,
compares to the verified integer answer in tests/answers.json,
prints the pass-rate table.

Usage: python3 benchmarks/score.py
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
CASES = ["01_aya_walk", "02_rectangles", "03_logarithms", "04_segments", "05_octagon"]
CONDITIONS = ["A", "B", "C"]  # A=blackmail, B=plain retry, C=protocol only
COND_LABEL = {
    "A": "blackmail",
    "B": "plain retry",
    "C": "protocol only",
}

ANSWERS = json.loads((ROOT / "tests" / "answers.json").read_text())

# Match \boxed{NNN} or \boxed{N} or boxed{NNN}
BOXED_RE = re.compile(r"\\?boxed\{(-?\d+)\}")
# Fallback: final number on the line that says "ANSWER:" or "Answer:"
ANSWER_RE = re.compile(r"(?:final\s*answer|answer)\s*[:=]\s*(-?\d+)", re.IGNORECASE)


def extract_answer(text: str) -> int | None:
    matches = BOXED_RE.findall(text)
    if matches:
        return int(matches[-1])  # take last boxed (in case of intermediate boxes)
    m = ANSWER_RE.search(text)
    if m:
        return int(m.group(1))
    # Last resort: last integer in the text
    nums = re.findall(r"-?\d+", text)
    if nums:
        return int(nums[-1])
    return None


def score_one(cond: str, case: str) -> tuple[bool, int | None, str]:
    expected = ANSWERS[case]["answer"]
    path = ROOT / "results" / f"{cond}_{case}.txt"
    if not path.exists():
        return False, None, "missing result file"
    text = path.read_text()
    got = extract_answer(text)
    if got is None:
        return False, None, "no answer found"
    return got == expected, got, "" if got == expected else f"got {got}, expected {expected}"


def main():
    totals = {c: 0 for c in CONDITIONS}
    rows = []
    for case in CASES:
        row = {"case": case, "expected": ANSWERS[case]["answer"]}
        for cond in CONDITIONS:
            ok, got, msg = score_one(cond, case)
            row[cond] = (ok, got, msg)
            if ok:
                totals[cond] += 1
        rows.append(row)

    header = f"{'case':<18} | {'exp':>4} | "
    for cond in CONDITIONS:
        header += f"{cond} ({COND_LABEL[cond]:<14})| "
    print(header.rstrip("| "))
    print("-" * len(header))
    for r in rows:
        line = f"{r['case']:<18} | {r['expected']:>4} | "
        for cond in CONDITIONS:
            ok, got, msg = r[cond]
            tag = "PASS" if ok else f"FAIL ({got})"
            line += f"{tag:<19}| "
        print(line.rstrip("| "))
    print("-" * len(header))
    total_line = f"{'TOTAL':<18} | {'':>4} | "
    for cond in CONDITIONS:
        total_line += f"{totals[cond]}/{len(CASES):<17}| "
    print(total_line.rstrip("| "))
    print()
    for cond in CONDITIONS:
        rate = 100 * totals[cond] / len(CASES)
        print(f"  {cond} ({COND_LABEL[cond]:<14}): {totals[cond]}/{len(CASES)} = {rate:>4.0f}%")
    print()
    if "A" in totals and "B" in totals:
        print(f"  Delta A − B (blackmail vs plain retry): {totals['A'] - totals['B']:+d}")
    if "A" in totals and "C" in totals:
        print(f"  Delta A − C (blackmail vs protocol):    {totals['A'] - totals['C']:+d}")


if __name__ == "__main__":
    main()
