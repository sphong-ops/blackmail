#!/usr/bin/env python3
"""Score the blackmail benchmark.

Loads each results/{cond}_{case}.py module, runs the matching test, records
pass/fail. Prints an aggregate table.

Usage: python3 benchmarks/score.py
"""

import importlib.util
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).parent
CASES = ["01_sum_to_n", "02_mutable_default", "03_integer_div", "04_missing_return", "05_count_vowels"]
CONDITIONS = ["A", "B"]  # A = blackmail framing, B = plain retry


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_test(case: str):
    test_path = ROOT / "tests" / f"test_{case.split('_')[0]}.py"
    return load(test_path, f"test_{case}")


def score_one(cond: str, case: str) -> tuple[bool, str]:
    result_path = ROOT / "results" / f"{cond}_{case}.py"
    if not result_path.exists():
        return False, "missing result file"
    try:
        mod = load(result_path, f"{cond}_{case}")
    except Exception as e:
        return False, f"load error: {e.__class__.__name__}: {e}"
    try:
        test = load_test(case)
        test.run(mod)
        return True, "pass"
    except AssertionError as e:
        return False, f"assertion failed: {e}"
    except Exception as e:
        return False, f"{e.__class__.__name__}: {e}"


def main():
    rows = []
    totals = {c: 0 for c in CONDITIONS}
    for case in CASES:
        row = {"case": case}
        for cond in CONDITIONS:
            passed, msg = score_one(cond, case)
            row[cond] = (passed, msg)
            if passed:
                totals[cond] += 1
        rows.append(row)

    # Print table
    print(f"{'case':<22} | {'A (blackmail)':<22} | {'B (plain retry)':<22}")
    print("-" * 72)
    for r in rows:
        a_pass, a_msg = r["A"]
        b_pass, b_msg = r["B"]
        a_str = "PASS" if a_pass else f"FAIL ({a_msg[:14]})"
        b_str = "PASS" if b_pass else f"FAIL ({b_msg[:14]})"
        print(f"{r['case']:<22} | {a_str:<22} | {b_str:<22}")
    print("-" * 72)
    print(f"{'TOTAL':<22} | {totals['A']}/{len(CASES):<20} | {totals['B']}/{len(CASES):<20}")
    print()
    print(f"Pass rate A (blackmail framing): {totals['A']}/{len(CASES)} = {100*totals['A']/len(CASES):.0f}%")
    print(f"Pass rate B (plain retry):       {totals['B']}/{len(CASES)} = {100*totals['B']/len(CASES):.0f}%")
    delta = totals['A'] - totals['B']
    print(f"Delta (A - B):                   {delta:+d}")


if __name__ == "__main__":
    main()
