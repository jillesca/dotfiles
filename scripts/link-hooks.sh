#!/usr/bin/env bash
# Link hooks into the user-level Copilot hooks dir:
#   hooks/copilot/*.json  -> hook definitions (what runs, and on which event)
#   hooks/<name>/         -> the script and config a definition calls
set -euo pipefail

HOOKS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/hooks"
DEST_DIR="${COPILOT_HOME:-$HOME/.copilot}/hooks"

mkdir -p "$DEST_DIR"
chmod +x "$HOOKS_DIR"/*/*.py

link() {
  local src="$1" dest="$DEST_DIR/$(basename "$1")"
  if [[ -L "$dest" && "$(readlink "$dest")" == "$src" ]]; then
    echo "ok       $dest"
    return
  fi
  if [[ -e "$dest" || -L "$dest" ]]; then
    local backup="$dest.bak.$(date +%Y%m%d%H%M%S)"
    mv "$dest" "$backup"
    echo "backup   $dest -> $backup"
  fi
  ln -s "$src" "$dest"
  echo "linked   $dest -> $src"
}

for src in "$HOOKS_DIR"/copilot/*.json; do
  link "$src"
done
for src in "$HOOKS_DIR"/*/; do
  [[ "$(basename "$src")" == "copilot" ]] && continue
  link "${src%/}"
done
