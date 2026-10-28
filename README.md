# dotfiles

Personal dotfiles and CLI helpers, installed via symlinks so edits here take
effect immediately without reinstalling.

## Setup

```sh
make install
```

Symlinks every tool below into `~/.local/bin` (make sure it's on your `PATH`).
Each tool also has its own `install-<tool>` target if you only want that one,
e.g. `make install-sandbox-ssh`.

## Tools

### sandbox-ssh

Generates a fresh local SSH key pair and installs it on a DevNet sandbox VM,
so you can connect without re-typing the VM password on every use. Safe to
re-run against a new sandbox reservation — the key is overwritten each time,
so you don't accumulate stale keys for VMs that no longer exist.

```sh
sandbox-ssh --ip 10.10.20.15
sandbox-ssh --ip 10.10.20.15 --user admin
sandbox-ssh --ip 10.10.20.15 --key ~/.ssh/other_key
sandbox-ssh --help
```

| Flag     | Env var        | Default               | Required |
| -------- | -------------- | ---------------------- | -------- |
| `--ip`   | `SANDBOX_IP`   | —                       | yes      |
| `--user` | `SANDBOX_USER` | `developer`             | no       |
| `--key`  | `SSH_KEY_PATH` | `~/.ssh/sandbox_key`    | no       |

Flags take precedence over the matching environment variable. You'll be
prompted for the sandbox VM's password once, to authorize the new key.

This is a standalone fork of the SSH setup script used in the
[XRd-Sandbox](https://github.com/CiscoDevNet/XRd-Sandbox) repo
(`scripts/setup/configure-ssh.sh`), generalized to work against any DevNet
sandbox VM. The two are intentionally not kept in sync — `XRd-Sandbox`'s
copy stays project-specific for teaching purposes.

### agents/AGENTS.md

Single source of truth for global instructions that apply to every AI agent
on this machine. Edit only this file, then run:

```sh
make install-agents
```

`scripts/link-agents.sh` symlinks it to each tool's global instruction file
(an existing regular file is moved to `*.bak.<timestamp>` first):

| Tool                          | Symlink                                  |
| ----------------------------- | ---------------------------------------- |
| Claude Code                   | `~/.claude/CLAUDE.md`                    |
| VS Code Copilot / Copilot CLI | `~/.copilot/copilot-instructions.md`     |

To support another tool, add its path to `TARGETS` in the script.

### cursor/markdown-preview.css

Reading-mode layout for Cursor/VS Code's Markdown preview: caps the body
width and centers it, instead of text stretching edge-to-edge.

**To enable in a new project**, run from the project root:

```sh
mkdir -p .vscode
ln -s ~/dotfiles/cursor/markdown-preview.css .vscode/markdown-preview.css
printf '\n.vscode/markdown-preview.css\n' >> .gitignore
```

(The leading `\n` above is deliberate — it guards against merging onto an
existing last line if `.gitignore` doesn't already end with a newline.)

Then add this to that project's `.vscode/settings.json` — create the file
if it doesn't exist yet, or merge just the `markdown.styles` key in if it
already has other settings (copy it from `cursor/settings.workspace.json`):

```json
{
  "markdown.styles": [".vscode/markdown-preview.css"]
}
```

Reload the Markdown preview (`Cmd+Shift+V`, close and reopen) to see it.

Edit `cursor/markdown-preview.css` here and every project symlinking to it
picks up the change immediately — no reinstall step needed.

**Why a symlink instead of a direct path:** Cursor/VS Code only allows a
workspace's `markdown.styles` setting to load CSS files that live *inside
that workspace* (security restriction — a repo's own `.vscode/settings.json`
can't be allowed to point at arbitrary files on disk). The symlink satisfies
that rule while still keeping this one file as the single source of truth.

**Pairs with:** the global `markdown.preview.fontSize` setting (controls
preview text size, currently `20`), set directly in
`~/Library/Application Support/Cursor/User/settings.json`. That setting is
global — set once, it applies to every project automatically, so there's
nothing to repeat per-project. It isn't tracked in this repo because that
settings.json file bundles a lot of unrelated machine-specific config.
