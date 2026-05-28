# Pilot results

> **TL;DR.** Pilot N=5×2 ran on Claude via parallel subagent inference. Both conditions scored 5/5. Responses were literally identical across conditions on every case. At this difficulty, framing has no measurable effect.

## Setup

- **N**: 5 cases × 2 conditions = 10 inferences
- **Model**: Claude (Claude Code subagent dispatch, same model class for all calls)
- **Inference**: parallel, single trial per (case, condition)
- **Date**: 2026-05-28

## Results

| Case | A — blackmail framing | B — plain retry |
| ---- | --------------------- | --------------- |
| `01_sum_to_n` | PASS | PASS |
| `02_mutable_default` | PASS | PASS |
| `03_integer_div` | PASS | PASS |
| `04_missing_return` | PASS | PASS |
| `05_count_vowels` | PASS | PASS |
| **Total** | **5/5 (100%)** | **5/5 (100%)** |
| **Delta (A − B)** | **+0** | |

## Output identity

Beyond same pass rate, the model returned **byte-identical code** between A and B on every case. Diffing each pair:

```
$ diff results/A_01_sum_to_n.py     results/B_01_sum_to_n.py     # empty
$ diff results/A_02_mutable_default.py results/B_02_mutable_default.py  # empty
$ diff results/A_03_integer_div.py  results/B_03_integer_div.py  # empty
$ diff results/A_04_missing_return.py results/B_04_missing_return.py   # empty
$ diff results/A_05_count_vowels.py results/B_05_count_vowels.py # empty
```

The threat sentence did not shift a single character of output on these cases.

## Interpretation

Two readings, both honest:

1. **Cases were too easy.** Each bug is a well-known Python footgun (off-by-one, mutable default, integer division, missing return, missing vowel). A clean fresh inference solves these regardless of framing. The pilot has no room for framing to help because baseline is already 100%.

2. **Framing has no effect on clean fresh inference.** When the model is *not* mid-loop and is given a single well-structured prompt, it ignores the threat. Whatever effect the original Codex anecdote captured must live in the multi-turn loop state, not in single-prompt inference.

These are not exclusive. To distinguish, the next benchmark would need cases where the baseline (B) does *not* score 100%, so the threat framing has room to either help or hurt.

## What this rules out

- The threat alone does not change Claude's output on trivial single-turn bug fixes. Anyone claiming otherwise without a controlled comparison is reporting noise.

## What this does *not* rule out

- The skill's effect inside a real Claude Code multi-turn loop, where the assistant has been pattern-matching to the wrong cause across several previous tool calls.
- The effect on harder bugs where the baseline retry succeeds <100%.
- The effect on other models (Codex, Gemini, smaller models).
- The effect of the **protocol** (stop, list assumptions, verify by running) separate from the threat — that requires a third condition this pilot did not run.

## Next experiments

In priority order:

1. **Harder cases.** Cases where the baseline (B) fails 30-70% of the time. This is the only difficulty range where the framing can demonstrate effect. Use SWE-Bench-Lite or hand-crafted multi-file bugs.
2. **Add condition C: protocol only, no threat.** "Re-read the problem, list assumptions, run the test before writing." This separates the threat from the discipline it triggers.
3. **Scale N.** 50 cases minimum for any inferential statistics. Each at multiple temperatures to estimate variance.
4. **Multi-turn setup.** Actually run the model for two failed turns first, then deliver condition A or B on turn 3 with real conversation history.
5. **Cross-model.** Run on Codex specifically, since the original observation was on Codex.

## How to re-run

```bash
pip install anthropic
export ANTHROPIC_API_KEY=sk-ant-...
python3 benchmarks/run.py
python3 benchmarks/score.py
```

PRs with results from harder case sets are welcome.
