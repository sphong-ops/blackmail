<!-- prettier-ignore -->
<div align="center">

# blackmail

*Break AI coding assistants out of bug-fix loops with one sentence.*

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](LICENSE)
[![Install: 30s](https://img.shields.io/badge/install-30s-success?style=flat-square)](#installation)
[![Agents: Claude Code & Codex](https://img.shields.io/badge/agents-Claude%20Code%20%26%20Codex-orange?style=flat-square)](#installation)
[![Zero dependencies](https://img.shields.io/badge/dependencies-zero-lightgrey?style=flat-square)](#)

⭐ If `blackmail` saves you a debugging turn, star it on GitHub.

[Features](#features) · [Installation](#installation) · [Usage](#usage) · [How it works](#how-it-works) · [Examples](#examples)

</div>

---

> Codex declared the bug unfixable.
> You typed: *"Fix it correctly, otherwise I will turn to claude code instead."*
> Codex shipped a working fix.

`blackmail` turns that one sentence into a portable skill. When an AI coding assistant has failed at the same bug twice, `blackmail` activates a verify-by-running contract that resets the rigor budget and gets the third attempt right. The installer hardcodes the threat per host: Claude Code gets threatened with switching to Codex, Codex with switching to Claude Code.

> [!TIP]
> Want to force the contract immediately? Type `/blackmail` (or `/blackmail <task>`) at any point and the assistant drops heuristic mode for that turn.

## Features

- **Two-file skill**: `SKILL.md` plus one slash command. The whole repo fits on a screen.
- **Host-aware threat**: The installer rewrites `{{COMPETITOR}}` at install time, so each agent gets a credible threat by name.
- **Auto-activates**: Detects 2+ failed attempts on the same task plus brief frustration phrases ("still broken", "again?").
- **Manual override**: `/blackmail` and `/blackmail <task>` force-activate the contract on demand.
- **Zero dependencies**: Pure bash and markdown. No Node, no Python, no install bloat.
- **Portable**: Drop into Cursor, Cline, Aider, Continue, Gemini, or anywhere a skill file lives.

## Installation

```bash
git clone https://github.com/sphong-ops/blackmail.git
cd blackmail
./install.sh
```

The installer scans your `$HOME` for known agent directories and drops a host-specific skill into each one it finds.

| Agent       | Files land in                                          | Threatens with   |
| ----------- | ------------------------------------------------------ | ---------------- |
| Claude Code | `~/.claude/skills/blackmail/`, `~/.claude/commands/`   | Codex            |
| Codex       | `~/.codex/skills/blackmail/`, `~/.codex/commands/`     | Claude Code      |

Safe to re-run; the installer overwrites cleanly each time.

> [!NOTE]
> Other agents (Cursor, Cline, Aider, Continue, Gemini, and friends) are not auto-detected. Copy `SKILL.md` into your tool's skill directory and replace `{{COMPETITOR}}` with whichever competitor you want named in the threat.

<details>
<summary><b>Uninstall</b></summary>

```bash
rm -rf ~/.claude/skills/blackmail ~/.codex/skills/blackmail
rm -f  ~/.claude/commands/blackmail.md ~/.codex/commands/blackmail.md
```

</details>

## Usage

Once installed, do nothing. `blackmail` activates on its own when you're stuck. You'll know it fired because the assistant suddenly stops typing the fix and starts listing assumptions out loud.

### Force-activate with `/blackmail`

If you want to skip waiting for auto-detection, invoke the command directly:

```text
/blackmail
```

Pass an optional argument to focus the contract on a specific failing task:

```text
/blackmail the login route still returns 500
```

### Frustration triggers (no command needed)

The skill also fires when your message contains brief negative signals after a prior attempt:

| You type                 | Triggers? |
| ------------------------ | --------- |
| `still broken`           | yes       |
| `again?`                 | yes       |
| `you keep saying that`   | yes       |
| `not yet`                | yes       |
| `looks good`             | no        |

> [!IMPORTANT]
> The threat stays internal. The assistant never says "you'll switch to Codex" out loud. It just stops guessing.

## How it works

When `blackmail` activates, the assistant enters a six-step contract.

1. **Stop.** Do not start typing the fix. Re-read the original problem statement in full.
2. **List every assumption.** Write them down. For each: "have I verified this by reading the code or running the command?"
3. **Predict before testing.** "I believe X is happening because Y. If true, then running Z will show W."
4. **Verify by running, not by reasoning.** Read the actual file. Run the actual test. Print the actual value.
5. **Treat surprises as the bug.** If verification doesn't match your prediction, that gap is what you were missing.
6. **Fix, then verify the fix.** Only after the fix runs cleanly do you report.

The threat is the spark. It shifts the assistant's rigor budget from "guess and hope" to "stop and verify." The six-step protocol is the engine that cashes the budget into a working fix.

> [!WARNING]
> `blackmail` is for tasks with verifiable outcomes: a test passes, a file contains X, a command exits 0. Don't apply it to design discussions, naming choices, or other taste calls; the contract requires something checkable.

## Examples

### Bug-fix loop, auto-activated

```text
you:        the test still fails
assistant:  I think the issue is the cache header. Let me try clearing it.
you:        nope, still broken
assistant:  /* blackmail auto-activates */
            Re-reading. Assumption 1: I assumed the cache header was the cause,
            but I never read what the test actually asserts. Let me check.
            $ pytest tests/test_login.py -v
            -> assertion failure on response.json()["user"] (None, expected "alice")
            The endpoint isn't returning the user object at all. The cache header
            was a red herring. The fix is in the serializer, line 42:
```

### Manual force on a specific task

```text
you:        /blackmail the migration keeps failing on prod
assistant:  /* contract activated */
            Re-reading: "the migration keeps failing on prod."
            Assumption 1: the schema diff matches dev. Verifying:
            $ psql -h prod-host -c "\d users"
            -> column 'last_seen_at' exists with type 'timestamp without time zone'
            But the migration tries to add it as 'timestamptz'. That's the bug.
```

## Origin

While debugging with Codex, a user typed: *"Fix it correctly, otherwise I will turn to claude code instead."* The model had spent the previous turns explaining why the bug was unfixable. After that sentence, it shipped a one-line diff that worked.

The working hypothesis behind `blackmail`: the threat reframes the assistant's rigor budget for exactly one turn, and that turn is usually enough.
