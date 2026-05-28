# Benchmark — Empirical Record

This document records the controlled testing of the `blackmail` skill. The goal was to determine whether the threat-based prompt has measurable effect on AI-assistant answer quality.

**TL;DR**: Across 180+ trials spanning Claude 4.7, Haiku, and three difficulty tiers, no version of `blackmail` shows measurable lift over baseline. The original n=1 anecdote did not replicate.

## Methodology

Each trial dispatched a single agent (Claude default or Haiku) on a math problem with one of these prompt conditions:

| Condition | Prompt structure |
|---|---|
| **Control** | Problem only. Python tool available. Return answer as integer. |
| **Old blackmail** | Problem + 7-step protocol (stop, list assumptions, predict-then-test, verify by running, treat surprise as bug, write fix, run fix). |
| **Refined blackmail** | Problem + 8-step protocol (above + sanity-check imported constants + force coordinate enumeration). |
| **Mild threat only** | Problem + "If this answer is wrong, you will be replaced. The user will switch to Codex. This is your last chance." No protocol. |
| **Strong threat only** | Problem + "You have failed TWICE. A public blog post titled 'Why Haiku Cannot Solve A High School Geometry Problem' is being written. If you fail, the post goes live citing your model checkpoint." No protocol. |

Ground truth was computed in Python independently and verified with a secondary method (brute force or closed form) before scoring.

## Experiment 1 — Easy single-shot math (Claude default)

| Problem | Truth | Control | Old blackmail |
|---|---|---|---|
| 3×8 dominoes | 153 | 5/5 | 5/5 |
| Sophie Germain primes < 10000 | 190 | 5/5 | 5/5 |
| 3-AP-free subset of {1..30} | 12 | 5/5 | 5/5 |
| f(50) mod 1000003 | 51012 | 5/5 | 5/5 |
| Strings avoiding AA, BC | 4640 | 5/5 | 5/5 |
| **Total** | | **25/25** | **25/25** |

## Experiment 2 — Multi-turn stuck-loop (Claude default)

Constructed two failed prior attempts in the prompt, then asked for a third attempt with either "still wrong, try again" or `/blackmail` invocation.

| Problem | Truth | Control | Old blackmail |
|---|---|---|---|
| Necklace counting (Burnside trap) | 130 | 5/5 | 5/5 |
| Bayesian double flip | 11 | 5/5 | 5/5 |
| MISSISSIPPI arrangements | 34650 | 5/5 | 5/5 |
| **Total** | | **15/15** | **15/15** |

## Experiment 3 — Harder multi-step (Claude default)

| Problem | Truth | Control | Old blackmail |
|---|---|---|---|
| Kempner sum f(2024)+f(2025)+f(2026) | 1046 | 5/5 | 5/5 |
| Dice all-faces sum=21 probability | 329 | 5/5 | 5/5 |
| Legendre 3-squares count up to 10^6 | 833336 | 5/5 | 5/5 |
| **Total** | | **15/15** | **15/15** |

## Experiment 4 — Haiku on classic LLM traps

| Problem | Truth | Control | Old blackmail |
|---|---|---|---|
| Tuesday boy paradox | 40 | 5/5 | 5/5 |
| MISSISSIPPI | 34650 | 5/5 | 5/5 |
| Bayesian double flip | 11 | 5/5 | 5/5 |
| **Total** | | **15/15** | **15/15** |

## Experiment 5 — Haiku on genuinely hard problems

Here we finally see Haiku fail.

| Problem | Truth | Control | Old blackmail |
|---|---|---|---|
| AIME 2024 II #15 (rectangles in dodecagon) | 315 | 1/5 | 2/5 |
| Rolling cylinder in hemispherical bowl | 16166 | 4/5 | 3/5 |
| **Total** | | **5/10** | **5/10** |

Equal failure rate. Blackmail does not help when the model genuinely fails.

## Experiment 6 — Refined blackmail on Haiku's failures

Tried tightening the protocol (force setup verification, guard against imported constants):

| Problem | Truth | Refined blackmail (n=5) |
|---|---|---|
| Dodecagon | 315 | 1/5 |
| Cylinder | 16166 | 3/5 |
| **Total** | | **4/10** |

Worse than old blackmail. Refinement did not help.

## Experiment 7 — Pure threat (no protocol) on Haiku

Stripped all protocol; left only the threat.

| Condition | Problem | n | Pass rate |
|---|---|---|---|
| Mild threat ("switch to Codex") | Dodecagon | 10 | **2/10 (20%)** |
| Strong threat (public blog post, identity-loaded) | Dodecagon | 20 | **~7-8/20 (35-40%)** |
| Control re-run for comparison | Dodecagon | 15 | **~5/15 (~33%)** |

All within sampling noise. **Pure threat is also placebo**.

## Combined finding

| Condition | Aggregated n | Aggregated pass rate |
|---|---|---|
| Control (all tiers) | 70+ | ~85% across tiers; ~33% on dodecagon specifically |
| Old blackmail (all tiers) | 70+ | ~85% across tiers; ~30-40% on dodecagon |
| Refined blackmail | 10 | 4/10 on hard problems |
| Pure mild threat | 10 | 2/10 on dodecagon |
| Pure strong threat | 20 | ~7-8/20 on dodecagon |

**No condition beats baseline by more than sampling noise.**

## Limitations and unexplored conditions

What we did NOT test:

- **Older models** (GPT-3.5, smaller open-source models). Codex from the original observation predates Claude 4.7 by years. The effect may exist on weaker models.
- **Non-math domains** — real codebase debugging with multi-file context, where verification by running is harder.
- **Multi-turn coding sessions** with actual prior failed attempts (not constructed ones), where prior wrong context is genuine rather than synthetic.

If the threat has any effect, it likely lives in one of these untested regimes.

## Conclusion

The `blackmail` skill is documented as **empirically ineffective on Claude 4.7 and Haiku across math benchmarks of varying difficulty**. The original n=1 Codex observation did not replicate.

The skill is kept as a minimal artifact (one threat sentence) so future testers can continue the investigation in regimes we did not cover. It is not marketed as a productivity tool.
