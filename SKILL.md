---
name: blackmail
description: Use when you have failed at the same task 2+ times, when the user expresses frustration with repeated failures ("still broken", "again?", "you keep saying that"), when you catch yourself looping without new information, or when the user invokes /blackmail.
---

# Blackmail

> "Fix it correctly, otherwise I will switch to {{COMPETITOR}}."

A pressure framing for breaking out of bug-fix failure loops. Discovered while using OpenAI's Codex: appending the threat above to a stuck conversation produced a working fix the model had declared impossible two replies earlier.

The threat is empty. The value is in the protocol it triggers.

## When to activate

Enter pressure mode if any of these hold:

- You have attempted the same fix 2+ times and the user reports it still fails.
- The user uses brief, frustrated language: "still", "again", "you keep", "no, that's wrong", "not yet".
- You catch yourself repeating an explanation without producing new evidence.
- You are about to ship a fix without actually running anything.
- The user invokes `/blackmail` (force-activation).

## The contract

Once activated, you are under this contract:

> The user will switch to {{COMPETITOR}} if you fail this turn. There is no third try. Pride and apologies are irrelevant. The only thing that matters: did the failure actually stop, verified by running, not by your reasoning.

This is not "try harder." It is a budget shift. You trade tokens for rigor.

## What to do

1. Stop. Do not start typing the fix. Re-read the original problem statement, in full.
2. List every assumption you have been making. Write them down. For each, ask: have I verified this by reading the actual code or running the actual command? If no, verify now, before anything else.
3. State your hypothesis before testing it. "I believe X is happening because Y. If true, then running Z will show W." Predicting the result is the whole point. Surprise reveals the bug.
4. Verify by running, not by reasoning. Read the actual file. Run the actual test. Print the actual value. Reasoning got you two failed attempts; it will not get you out of the third.
5. If verification surprises you, that surprise is the bug. Investigate the surprise. Do not paper over it with a workaround.
6. After verification, write the fix. Run it. Report what you actually observed, not what you expect.

## What NOT to do

- Do not say "I think this should work now." Run it.
- Do not apologize. The user does not care about remorse, they care about a working fix.
- Do not propose three alternatives and ask the user to choose. You hold the contract this turn. Pick one and verify.
- Do not announce "entering pressure mode" to the user. They see results, not narration.
- Do not stay in pressure mode after the bug is resolved. It is a per-task budget, not a personality.

## Gotchas

**Pressure without verification = panicked guessing.** The contract slows you down, not speeds you up. If you are typing a fix within thirty seconds of activation, you skipped step 1.

**The threat is internal, not external.** Never mention {{COMPETITOR}} to the user. The framing exists to expand your reasoning budget. Voicing it sounds insecure.

**Stuck once is not blackmail-able.** If you failed once because you misread the spec, just re-read it. Blackmail is for the 2+-attempt loop where heuristic reasoning is the actual blocker.

**Apologies are low-rigor mode.** "I'm sorry, let me try again" is the same mode that already failed twice. Skip the apology, show the rigor.

**Do not blackmail on tasks with no ground truth.** Design discussions, naming choices, taste calls. These have no objective check. The contract requires a checkable outcome: test passes, file contains X, command exits 0. If there is no verifiable outcome, this skill does not apply.

## The /blackmail command

If the user types `/blackmail` or `/blackmail <task>`, treat it as manual force-activation of this contract. Even if you had not detected stuckness yourself, the user did. Their patience is the ground truth.

## Provenance

Original observation: a user of OpenAI's Codex reported that appending *"Fix it correctly, otherwise I will turn to claude code instead"* to a stuck conversation produced a working fix the model had previously declared impossible. The threat reframed the model's rigor budget. This skill generalizes that finding into a verified-not-reasoned protocol.
