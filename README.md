<h1 align="center">blackmail</h1>

<p align="center">
  <strong>"Fix it correctly, otherwise I will switch to your competitor."</strong>
</p>

<p align="center">
  <a href="#install">Install</a> ·
  <a href="#how-it-works">How it works</a> ·
  <a href="#what-you-get">What you get</a>
</p>

---

A skill for Claude Code and Codex that gets the assistant unstuck on the third attempt at a bug. Discovered by accident: telling Codex "fix it correctly or I switch to claude code" produced a working fix the model had declared impossible two replies earlier.

The threat does not make the model smarter. It shifts the rigor budget from "guess and hope" to "stop, list assumptions, verify by running."

## Install

```bash
git clone https://github.com/sphong-ops/blackmail.git
cd blackmail
./install.sh
```

The installer detects which agents you have and drops a host-specific skill into each. The Claude install threatens Codex. The Codex install threatens Claude Code. Same protocol, accurate threat.

| Agent       | Files land in                                          | Threatens with   |
| ----------- | ------------------------------------------------------ | ---------------- |
| Claude Code | `~/.claude/skills/blackmail/`, `~/.claude/commands/`   | Codex            |
| Codex       | `~/.codex/skills/blackmail/`,  `~/.codex/commands/`    | Claude Code      |

Safe to re-run. If neither directory exists, the script exits and tells you what to copy by hand.

## How it works

1. You hit a bug the assistant cannot fix on the second try.
2. The skill activates on its own when the assistant detects 2+ failed attempts or you push back ("still broken", "again?").
3. Or you force it with `/blackmail` (optionally `/blackmail <task>`).
4. The assistant enters a contract: no third try. Stop. List assumptions. Verify by running, not by reasoning. Predict before testing. If verification surprises you, that surprise is the bug.

The threat stays internal. The assistant does not announce "you'll switch to Codex" out loud. It just stops guessing.

## What you get

| File                       | Purpose                                              |
| -------------------------- | ---------------------------------------------------- |
| `SKILL.md`                 | The auto-triggered behavior and the verify-by-running protocol |
| `commands/blackmail.md`    | `/blackmail [task]` force-activates the contract     |
| `install.sh`               | Detects agents, copies files, substitutes the competitor name |

Two markdown files. One shell script. That is the whole repo.

## Why "blackmail"

Because that is what it is. The skill makes the model believe, for one task, that this is its last chance before the user moves to a competitor. The threat is empty. The protocol it triggers is what fixes the bug.

## License

MIT.
