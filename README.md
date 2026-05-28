<h1 align="center">blackmail</h1>

<p align="center">
  <strong>"Fix it correctly, otherwise I will switch to your competitor."</strong>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License"></a>
  <a href="#install"><img src="https://img.shields.io/badge/install-30s-success" alt="30 second install"></a>
  <a href="#install"><img src="https://img.shields.io/badge/agents-Claude%20Code%20%7C%20Codex-orange" alt="Supported agents"></a>
</p>

<p align="center">
  <a href="#install">Install</a> ·
  <a href="#what-happens">What happens</a> ·
  <a href="#what-you-get">What you get</a> ·
  <a href="#the-story">The story</a>
</p>

---

> Codex declared the bug unfixable.
> You typed: *"Fix it correctly, otherwise I will turn to claude code instead."*
> Codex shipped a working fix.

`blackmail` is a skill for Claude Code and Codex that breaks AI coding assistants out of bug-fix loops. One sentence does it. We turned that sentence into a skill that auto-fires when the assistant is stuck. The installer hardcodes the right threat for the right host, so Claude Code gets threatened with Codex and Codex gets threatened with Claude Code. Same skill, accurate threat.

The threat is the spark. The protocol is the engine: stop, list assumptions, verify by running, predict before testing, treat surprises as the actual bug.

## Install

```bash
git clone https://github.com/sphong-ops/blackmail.git
cd blackmail
./install.sh
```

The installer detects which agents you have and drops a host-specific skill into each.

| Agent       | Files land in                                          | Threatens with   |
| ----------- | ------------------------------------------------------ | ---------------- |
| Claude Code | `~/.claude/skills/blackmail/`, `~/.claude/commands/`   | Codex            |
| Codex       | `~/.codex/skills/blackmail/`,  `~/.codex/commands/`    | Claude Code      |

Safe to re-run. Using Cursor, Cline, Aider, Continue, Gemini, or something else? Copy `SKILL.md` into your tool's skill directory and replace `{{COMPETITOR}}` with whichever name you want in the threat.

<details>
<summary>Uninstall</summary>

```bash
rm -rf ~/.claude/skills/blackmail ~/.codex/skills/blackmail
rm -f  ~/.claude/commands/blackmail.md ~/.codex/commands/blackmail.md
```

</details>

## What happens

You hit a bug. The assistant tries once. Fails. Tries again. Fails. You type "still broken", "again?", or just `/blackmail`. The skill activates. From that point:

1. The assistant stops typing the fix.
2. Re-reads the original problem.
3. Lists every assumption it has been making.
4. Verifies each by running, not by reasoning.
5. Predicts what each command will output before running it.
6. Writes the fix only after verification.

The threat stays internal. The assistant does not announce "you'll switch to Codex." It just stops guessing.

## What you get

| File                       | Purpose                                              |
| -------------------------- | ---------------------------------------------------- |
| `SKILL.md`                 | Auto-triggers on stuckness, runs the verify-by-running protocol |
| `commands/blackmail.md`    | `/blackmail [task]` force-activates the contract     |
| `install.sh`               | Detects agents, copies files, substitutes the right threat |

Two markdown files. One shell script. The whole repo fits on a screen.

## The story

A user stuck on a bug. Codex had spent multiple turns explaining why the bug was unfixable.

The user typed one sentence:

> *"Fix it correctly, otherwise I will turn to claude code instead."*

Codex shipped a one-line diff that worked.

Threat. Pressure. Protocol. The threat reframes the rigor budget. The protocol cashes the budget into a verified fix. `blackmail` bakes both into a file you install once and forget.

## Try it

Install. Hit a real bug. When the assistant fails twice, type `/blackmail`. Open an issue with the transcript, working or not. Star if it saved you a turn.

## License

MIT.
