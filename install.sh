#!/usr/bin/env bash
# blackmail installer. Detects Claude Code and Codex, installs a host-specific
# skill into each. The Claude install is hardcoded to threaten switching to Codex;
# the Codex install is hardcoded to threaten switching to Claude Code.

set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE="$DIR/SKILL.md"
CMD="$DIR/commands/blackmail.md"
INSTALLED=0

if [ ! -f "$TEMPLATE" ] || [ ! -f "$CMD" ]; then
  echo "error: SKILL.md or commands/blackmail.md missing from $DIR" >&2
  exit 2
fi

install_to() {
  local label="$1"
  local skill_root="$2"
  local cmd_root="$3"
  local competitor="$4"

  mkdir -p "$skill_root/blackmail" "$cmd_root"
  sed "s/{{COMPETITOR}}/$competitor/g" "$TEMPLATE" > "$skill_root/blackmail/SKILL.md"
  cp "$CMD" "$cmd_root/blackmail.md"
  echo "  $label  ->  $skill_root/blackmail/  (threatens: $competitor)"
  INSTALLED=$((INSTALLED + 1))
}

echo "blackmail: detecting AI agents..."

if [ -d "$HOME/.claude" ]; then
  install_to "Claude Code" "$HOME/.claude/skills" "$HOME/.claude/commands" "Codex"
fi

if [ -d "$HOME/.codex" ]; then
  install_to "Codex      " "$HOME/.codex/skills"  "$HOME/.codex/commands"  "Claude Code"
fi

if [ "$INSTALLED" -eq 0 ]; then
  echo "  No ~/.claude or ~/.codex directory found."
  echo "  Manually copy SKILL.md and commands/blackmail.md into your agent's skill/command directory,"
  echo "  and replace {{COMPETITOR}} with whichever competitor you want named in the threat."
  exit 1
fi

echo
echo "Done. Open a new session and try /blackmail on a stuck task."
