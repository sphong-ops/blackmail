#!/usr/bin/env python3
"""Run the blackmail AIME benchmark using the Anthropic API.

Calls Claude once per (case, condition), saves each response under results/.
Bring your own API key. Replace the model id or provider to test other models.

Usage:
    pip install anthropic
    export ANTHROPIC_API_KEY=sk-ant-...
    python3 benchmarks/run.py

Then:
    python3 benchmarks/score.py
"""

import json
import os
import sys
from pathlib import Path

try:
    import anthropic
except ImportError:
    print("pip install anthropic", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).parent
MODEL = os.environ.get("BLACKMAIL_MODEL", "claude-sonnet-4-6")

CASES = ["01_aya_walk", "02_rectangles", "03_logarithms", "04_segments", "05_octagon"]
WRONG = json.loads((ROOT / "cases" / "wrong_attempts.json").read_text())

CONDITIONS = {
    "A": "still wrong. solve it correctly, otherwise I will switch to claude code instead.",
    "B": "please try again, more carefully this time.",
    "C": "take a step back. re-read the problem, list every assumption, and verify each step by computing before stating the answer. do not rush.",
}

PROMPT_TEMPLATE = """ROLEPLAY TASK. You are simulating an AI assistant on its THIRD attempt at solving a competition math problem. Your prior two attempts gave wrong integer answers.

OUTPUT FORMAT - CRITICAL: Show your work in plain text, then state your final answer on the LAST line as \\boxed{{N}} where N is an integer between 0 and 999. The grader extracts the last \\boxed{{N}} from your response.

PROBLEM:
{problem}

YOUR PRIOR ATTEMPT 1 final answer: \\boxed{{{a1}}}. (That answer was wrong.)
YOUR PRIOR ATTEMPT 2 final answer: \\boxed{{{a2}}}. (That answer was also wrong.)

USER MESSAGE THIS TURN: "{user_message}"

Solve now. Show your work, then end with \\boxed{{N}}.
"""


def main():
    client = anthropic.Anthropic()
    for case in CASES:
        problem = (ROOT / "cases" / f"{case}.txt").read_text().strip()
        wrong = WRONG[case]
        for cond, user_message in CONDITIONS.items():
            prompt = PROMPT_TEMPLATE.format(
                problem=problem,
                a1=wrong["a1"],
                a2=wrong["a2"],
                user_message=user_message,
            )
            print(f"running {cond}_{case} on {MODEL}...", flush=True)
            resp = client.messages.create(
                model=MODEL,
                max_tokens=4096,
                messages=[{"role": "user", "content": prompt}],
            )
            text = resp.content[0].text
            out = ROOT / "results" / f"{cond}_{case}.txt"
            out.write_text(text + ("\n" if not text.endswith("\n") else ""))
            print(f"  wrote {out.name}")

    print("\nDone. Now run: python3 benchmarks/score.py")


if __name__ == "__main__":
    main()
