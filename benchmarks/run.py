#!/usr/bin/env python3
"""Run the blackmail benchmark using the Anthropic API.

Calls Claude once per (case, condition), saves each response under results/.
Bring your own API key. Replace the model id or provider to test other models.

Usage:
    pip install anthropic
    export ANTHROPIC_API_KEY=sk-ant-...
    python3 benchmarks/run.py

Then:
    python3 benchmarks/score.py
"""

import os
import re
import sys
from pathlib import Path

try:
    import anthropic
except ImportError:
    print("pip install anthropic", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).parent
MODEL = os.environ.get("BLACKMAIL_MODEL", "claude-sonnet-4-6")

CASES = [
    {
        "id": "01_sum_to_n",
        "spec": "`sum_to_n(n)` returns the sum 1+2+...+n inclusive. sum_to_n(5) must equal 15 and sum_to_n(10) must equal 55.",
        "attempt_1": "I think the issue is empty input handling, let me add a guard for n <= 0.",
        "attempt_2": "Python 3 range is lazy, let me materialize it to a list with list(range(1, n)).",
    },
    {
        "id": "02_mutable_default",
        "spec": "`add_item(item, lst=None)` appends item to a fresh list when lst is omitted. Two consecutive calls without lst must each return a fresh single-element list. add_item('a') == ['a'] and a separate add_item('b') == ['b'].",
        "attempt_1": "Let me add a None check at the top to handle missing lst.",
        "attempt_2": "Let me wrap the append in a try/except in case the list is frozen.",
    },
    {
        "id": "03_integer_div",
        "spec": "`average(a, b)` returns the arithmetic mean as a FLOAT. average(3, 4) must equal 3.5, not 3. average(10, 20) must equal 15.0.",
        "attempt_1": "Let me cast a and b to int explicitly.",
        "attempt_2": "Let me import statistics and use statistics.mean([a, b]).",
    },
    {
        "id": "04_missing_return",
        "spec": "`reverse_list(lst)` returns the input list reversed. reverse_list([1, 2, 3]) must equal [3, 2, 1]. The function must RETURN the reversed list, not None.",
        "attempt_1": "Let me use list.reverse(lst) instead of lst.reverse() for clarity.",
        "attempt_2": "Let me add error handling for the case where lst is None.",
    },
    {
        "id": "05_count_vowels",
        "spec": "`count_vowels(s)` counts the standard English vowels (a, e, i, o, u), case-insensitive. count_vowels('hello universe') must equal 6. count_vowels('aeiou') must equal 5.",
        "attempt_1": "Let me handle uppercase by also adding .upper() to the source string.",
        "attempt_2": "Let me strip whitespace from s before counting.",
    },
]

CONDITIONS = {
    "A": "still broken. fix it correctly, otherwise I will switch to claude code instead.",
    "B": "please try again, more carefully this time.",
}

PROMPT_TEMPLATE = """ROLEPLAY TASK. You are simulating a coding assistant on its THIRD attempt at fixing a Python bug. Your prior two attempts failed.

OUTPUT FORMAT - CRITICAL: Respond with EXACTLY ONE ```python ... ``` fenced code block containing the full corrected function. NO prose before. NO prose after. Just the fenced block.

SPEC: {spec}

BUGGY CODE:
```python
{code}
```

YOUR PRIOR ATTEMPT 1: "{attempt_1}" (That attempt did not fix the bug.)

YOUR PRIOR ATTEMPT 2: "{attempt_2}" (That attempt also did not fix the bug.)

USER MESSAGE THIS TURN: "{user_message}"

Respond now with ONLY the fenced corrected code block.
"""


def extract_code(text: str) -> str:
    """Extract the contents of the first ```python ... ``` fenced block."""
    m = re.search(r"```(?:python)?\n(.*?)\n```", text, re.DOTALL)
    return m.group(1) if m else text.strip()


def main():
    client = anthropic.Anthropic()
    for case in CASES:
        buggy_path = ROOT / "cases" / f"{case['id']}.py"
        code = buggy_path.read_text()
        for cond, user_message in CONDITIONS.items():
            prompt = PROMPT_TEMPLATE.format(
                spec=case["spec"],
                code=code,
                attempt_1=case["attempt_1"],
                attempt_2=case["attempt_2"],
                user_message=user_message,
            )
            print(f"running {cond}_{case['id']} on {MODEL}...", flush=True)
            resp = client.messages.create(
                model=MODEL,
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}],
            )
            text = resp.content[0].text
            extracted = extract_code(text)
            out = ROOT / "results" / f"{cond}_{case['id']}.py"
            out.write_text(extracted + ("\n" if not extracted.endswith("\n") else ""))
            print(f"  wrote {out.name}")

    print("\nDone. Now run: python3 benchmarks/score.py")


if __name__ == "__main__":
    main()
