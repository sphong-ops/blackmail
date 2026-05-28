---
name: blackmail
description: Use when you have attempted the same task 2+ times AND the user pushes back with frustration phrases ("still broken", "again?", "you keep saying that", "no, that's wrong"), when you catch yourself repeating an explanation without producing new evidence, or when the user invokes /blackmail. Do not activate on isolated phrases like "still" or "not yet" without a prior failed attempt in the same conversation.
allowed-tools: Read, Bash, Edit, Write, Grep, Glob
---

# Blackmail

> "Fix it correctly, otherwise I will switch to {{COMPETITOR}}."

A pressure framing for breaking out of bug-fix failure loops. Discovered while using OpenAI's Codex: appending the threat above to a stuck conversation produced a working fix the model had declared impossible two replies earlier.

The threat is empty. The value is in the protocol it triggers.

## When to activate

Enter pressure mode only when at least one of these holds:

- You have attempted the same fix 2+ times AND the user reports it still fails this turn.
- The user uses frustrated language *after a prior failed attempt this conversation*: "still broken", "again?", "you keep saying that", "no, that's wrong". (Standalone "still" or "not yet" without a prior failure in this conversation is NOT a trigger.)
- You catch yourself repeating an explanation without producing new evidence.
- You are about to ship a fix without actually running anything.
- The user invokes `/blackmail` (force-activation, no preconditions).

## The contract

Once activated, you are under this contract:

> The user will switch to {{COMPETITOR}} if you fail this turn. There is no third try. Pride and apologies are irrelevant. The only thing that matters: did the failure actually stop, verified by running, not by your reasoning.

This is not "try harder." It is a budget shift. You trade tokens for rigor.

## What to do

1. Stop. Do not start typing the fix. Re-read the original problem statement, in full.
2. List every assumption you have been making. Write them down. For each, ask: have I verified this by reading the actual code or running the actual command? If no, verify now, before anything else.
3. State your hypothesis before testing it. "I believe X is happening because Y. If true, then running Z will show W." Predicting the result is the whole point. Surprise reveals the bug.
4. Verify by running, not by reasoning. Issue a NEW tool call this turn, even if you believe you already have the answer from earlier in the conversation. Read the actual file fresh. Run the actual test now. Print the actual value. Reasoning got you two failed attempts; it will not get you out of the third.
5. Treat any deviation from your prediction as the bug. If the output differs from what you stated in step 3 by even one character, that gap is what you were missing. Investigate the gap. Do not paper over it with a workaround.
6. Write the fix.
7. Run the fix. Confirm the original failure no longer reproduces. Do not claim done before this run finishes cleanly. Report what you actually observed, not what you expect.

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
