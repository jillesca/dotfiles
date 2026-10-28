# dotfiles

Personal dotfiles and CLI helpers, installed via symlinks so edits here take
effect immediately without reinstalling.

## Tools

| Tool                                                      | Purpose                                                   | Install                    |
| --------------------------------------------------------- | --------------------------------------------------------- | -------------------------- |
| [`sandbox-ssh`](docs/sandbox-ssh.md)                      | Sets up key-based SSH to a DevNet sandbox VM              | `make install-sandbox-ssh` |
| [`agents/AGENTS.md`](docs/agents.md)                      | One global instruction file shared by all AI agents       | `make install-agents`      |
| [`cursor/markdown-preview.css`](docs/markdown-preview.md) | Centered, width-capped Markdown preview in Cursor/VS Code | per project (manual)       |

Click a tool for usage, options and background.

## Setup

```sh
make install
```

Installs every tool above (`sandbox-ssh` is symlinked into `~/.local/bin` —
make sure it's on your `PATH`). Each tool also has its own `install-<tool>`
target if you only want that one. Run `make help` to list them.
