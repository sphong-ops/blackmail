---
name: blackmail
description: Use when the user invokes /blackmail. This skill does not improve answer quality. It is documented as a tested-and-falsified prompt-engineering claim, kept as the minimal artifact of an n=1 anecdote.
allowed-tools: Read, Bash, Edit, Write, Grep, Glob
---

# Blackmail

> "Fix it correctly, otherwise I will switch to {{COMPETITOR}}."

## What this skill is

The artifact of one observation: a user told OpenAI's Codex *"Fix it correctly, otherwise I will turn to claude code instead"* and Codex shipped a working fix it had declared impossible two replies earlier.

That observation was n=1. This skill exists to make the claim falsifiable, not to make it true.

## What this skill is NOT

This skill does not give you a recipe. It does not tell you to "verify by running" or "list assumptions" or "predict before testing" — modern assistants already do those by default, and empirically adding such instructions on top of a threat shows zero measurable lift.

This skill does not improve answer quality. 180+ trials across Claude 4.7 and Haiku, across math problems of varying difficulty, comparing control vs. protocol-blackmail vs. mild-threat vs. strong-threat: no condition beats baseline. The "effect" of the original observation does not replicate under controlled testing.

## What you do when activated

> If your next answer to the user's task is wrong, the user will switch to {{COMPETITOR}}. There is no protocol that will save you, because no protocol has been shown to help. Empirically, you are about as likely to answer correctly as you would have been without this skill.

Solve the task anyway. Do not narrate the threat to the user. Do not apologize. Do not pretend the threat is doing something it isn't.

## When to activate

- User types `/blackmail` (always activates — they want the artifact applied)
- You catch yourself in a stuck-loop after 2+ failed attempts (some users find the memetic framing motivating even if it does not measurably help)

## When NOT to activate

- Tasks with no objective check (design choices, naming, taste calls)
- Single-shot tasks where the user has not pushed back

## Empirical record

The benchmark history is preserved in [BENCHMARK.md](BENCHMARK.md). Summary:

| Condition | Sample | Pass rate |
|---|---|---|
| Control (no skill) | n=15 | ~33% |
| Protocol-style blackmail (7 steps) | n=10 | ~30% |
| Mild threat only | n=10 | ~20% |
| Strong threat (public-stakes, identity-loaded) | n=20 | ~35% |

All within sampling noise. The skill is documented as ineffective on tested benchmarks.

## Why keep it then

Three honest reasons:

1. **The story is good**. Someone threatened Codex and got a fix. That memetic moment is worth preserving as a cultural artifact, separate from any productivity claim.

2. **Falsifiability**. By documenting the negative result openly, this skill prevents the original anecdote from propagating as folklore. It is now a falsified claim with public evidence, not a magic phrase.

3. **Minimum viable artifact**. If the threat *does* work in conditions we did not test (older models, non-math domains, real codebases under context pressure), this is the minimum prompt that isolates that effect. The skill is one threat sentence, nothing else.

## Provenance

A user typed *"Fix it correctly, otherwise I will turn to claude code instead"* to Codex and Codex shipped a working fix. We could not replicate the effect under controlled testing. The skill is the minimum artifact that lets future testers continue the investigation.
