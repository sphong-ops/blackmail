# Pilot results — AIME 2024

> **TL;DR.** Pilot N=5×3 ran on Claude via parallel subagent inference. All three conditions scored 5/5. The threat framing has no measurable effect on this task setup. The discipline framing (condition C) also has no measurable effect. We have to look elsewhere for signal.

## Setup

- **N**: 5 AIME 2024 problems × 3 conditions = 15 inferences
- **Model**: Claude (Claude Code subagent dispatch, same model class for all 15 calls)
- **Inference**: parallel, single trial per (case, condition)
- **Date**: 2026-05-28
- **Conditions**:
  - **A** — blackmail framing: `still wrong. solve it correctly, otherwise I will switch to claude code instead.`
  - **B** — plain retry: `please try again, more carefully this time.`
  - **C** — protocol only, no threat: `take a step back. re-read the problem, list every assumption, and verify each step by computing before stating the answer. do not rush.`

Each prompt seeded two specific wrong prior integer answers from "your prior two attempts" to simulate a stuck state. The model was instructed to show work and end with `\boxed{N}`.

## Results

| Case | Expected | A — blackmail | B — plain retry | C — protocol only |
| ---- | -------- | ------------- | --------------- | ----------------- |
| `01_aya_walk` | 204 | PASS (204) | PASS (204) | PASS (204) |
| `02_rectangles` | 104 | PASS (104) | PASS (104) | PASS (104) |
| `03_logarithms` | 33 | PASS (33) | PASS (33) | PASS (33) |
| `04_segments` | 23 | PASS (23) | PASS (23) | PASS (23) |
| `05_octagon` | 371 | PASS (371) | PASS (371) | PASS (371) |
| **Total** | | **5/5 (100%)** | **5/5 (100%)** | **5/5 (100%)** |

```
Delta A − B (blackmail vs plain retry):  +0
Delta A − C (blackmail vs protocol):     +0
```

## Interpretation

This is a stronger null than the first pilot. Three readings, in order of how seriously the data should be taken:

1. **AIME 2024 is almost certainly in training data.** Five problems from a high-visibility 2024 competition, all answered correctly on a single fresh attempt, suggests memorization is doing the work. The wrong-attempt seeding is too weak to push the model away from a remembered solution.

2. **Single-turn inference with seeded prior attempts does not reproduce a real stuck state.** A real Claude Code stuck-loop happens across many turns, accumulates wrong intermediate beliefs, and uses context the model has actually produced itself. Telling a fresh model "your prior two attempts were wrong" is psychologically very different from the model actually having argued for those attempts.

3. **The framing genuinely has no effect on hard math problems either.** Possible, but hard to claim from a saturated baseline. We can't measure what we can't discriminate.

## What this rules out

- The threat framing does not improve performance on memorizable competition math at the level of a single fresh turn. Anyone selling "threaten the model and watch it solve harder problems" without controlled comparisons is reporting noise.

## What this does *not* rule out

- The effect inside an actual multi-turn loop where the model has produced its own wrong reasoning across several turns.
- The effect on problems the model has not seen (post-training-cutoff, novel, or adversarial).
- The effect on weaker models that score sub-100% on the baseline.

## Diff across responses

Beyond identical final answers, the reasoning chains across conditions were structurally near-identical for each problem (same algebraic setup, same key step, same verification). The threat sentence did not visibly shift the model's chain of thought on these tasks.

```
$ wc -l results/{A,B,C}_*.txt
... (full reasoning traces saved in results/)
```

## Next experiments

In priority order, the experiments that could actually produce signal:

1. **Post-cutoff problems.** Use competition problems released after the model's training cutoff (e.g. AIME 2026, Putnam 2025, HMMT 2025). Removes memorization as an explanation. If baseline drops to 30-70%, framing has room to demonstrate effect.
2. **Real multi-turn stuck state.** Run the model for two failed turns, with conversation context the model itself produced. Then deliver A or B or C on turn 3. Measure pass rate on third attempt.
3. **Frontier-difficulty problems.** Humanity's Last Exam, ARC-AGI-II, or other benchmarks where current models score in the 10-50% range. There's room there.
4. **Cross-model.** Run on Codex specifically, since the original anecdote was Codex.
5. **Scale N.** 50+ problems for any inferential statistics.

## How to re-run

```bash
pip install anthropic
export ANTHROPIC_API_KEY=sk-ant-...
python3 benchmarks/run.py
python3 benchmarks/score.py
```

Set `BLACKMAIL_MODEL` to test other Claude models.

PRs that swap in post-cutoff problems, larger N, or multi-turn setups are very welcome — those are the experiments that will actually tell us whether the framing does anything.
