# agents/AGENTS.md

Single source of truth for global instructions that apply to every AI agent
on this machine.

Source: [`agents/AGENTS.md`](../agents/AGENTS.md)

## Usage

Edit only this file, then run:

```sh
make install-agents
```

## Where it's linked

[`scripts/link-agents.sh`](../scripts/link-agents.sh) symlinks it to each
tool's global instruction file (an existing regular file is moved to
`*.bak.<timestamp>` first):

| Tool                          | Symlink                              |
| ----------------------------- | ------------------------------------ |
| Claude Code                   | `~/.claude/CLAUDE.md`                |
| VS Code Copilot / Copilot CLI | `~/.copilot/copilot-instructions.md` |

To support another tool, add its path to `TARGETS` in the script.
