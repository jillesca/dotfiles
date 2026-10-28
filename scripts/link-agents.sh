#!/usr/bin/env bash
# Symlink agents/AGENTS.md to the global instruction file of each AI tool.
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/agents/AGENTS.md"

# Add a destination here to support another tool.
TARGETS=(
  "$HOME/.claude/CLAUDE.md"                # Claude Code
  "$HOME/.copilot/copilot-instructions.md" # VS Code Copilot / Copilot CLI
)

[[ -f "$SRC" ]] || { echo "Missing source: $SRC" >&2; exit 1; }

for dest in "${TARGETS[@]}"; do
  mkdir -p "$(dirname "$dest")"
  if [[ -L "$dest" && "$(readlink "$dest")" == "$SRC" ]]; then
    echo "ok       $dest"
    continue
  fi
  if [[ -e "$dest" || -L "$dest" ]]; then
    backup="$dest.bak.$(date +%Y%m%d%H%M%S)"
    mv "$dest" "$backup"
    echo "backup   $dest -> $backup"
  fi
  ln -s "$SRC" "$dest"
  echo "linked   $dest -> $SRC"
done
