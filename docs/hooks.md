# hooks/

Global hooks for AI coding assistants. Today: a Copilot `postToolUse` hook that
formats, lints and type-checks each file the agent edits, without any
per-project config.

## Layout

```text
hooks/
├── copilot/
│   └── format-lint.json      # hook definition: which event, which command
└── format-lint/
    ├── format_lint.py        # the script the definition runs
    └── config/
        └── black.toml        # tool config, passed to the CLI with --config
```

- `hooks/<assistant>/*.json` only says _when_ and _what to run_. Add
  `hooks/claude/…` for another assistant; it can reuse the same script.
- `hooks/<name>/` holds the script and a `config/` directory with one file per
  CLI. [`format_lint.py`](../hooks/format-lint/format_lint.py) hands them to the
  tool with its `--config` flag.

## Usage

```sh
make install-hooks
```

This `brew install`s the CLIs the hook calls (`ruff`, `black`, `ty`,
`prettier`, `markdownlint-cli2`) and runs
[`scripts/link-hooks.sh`](../scripts/link-hooks.sh), which symlinks into
`~/.copilot/hooks/` (or `$COPILOT_HOME/hooks/`):

- each `hooks/copilot/*.json` file
- each `hooks/<name>/` directory

An existing file is moved to `*.bak.<timestamp>` first. Edit the files here; the
symlinks pick up changes immediately. Start a new Copilot session after
changing the JSON.

## What runs

`postToolUse` fires after every tool call. The payload carries the tool name
and arguments, so the hook takes the edited paths from there; no transcript
parsing. Non-edit tools (read, search, terminal) are ignored. Files with no
pipeline, and files in `node_modules`, `.venv` or `.git`, are skipped.

Formatters rewrite the file in place. If problems remain, the hook returns
`additionalContext` and the agent sees them right after the edit. Nothing
blocks or loops. Because the file changes under the agent,
[`agents/AGENTS.md`](../agents/AGENTS.md) tells agents to expect small changes
and re-read before editing again.

The pipelines are the `PYTHON`, `MARKDOWN` and `PRETTIER` lists at the top of
the script. Each step is a CLI call; steps marked `report` surface their output
when they fail.

| Files                                                      | Steps (same order as VS Code on save: fixAll, then format)                 |
| ---------------------------------------------------------- | -------------------------------------------------------------------------- |
| `.py`                                                      | `ruff check --fix`, `ty check --fix`, `black`, then report `ruff` and `ty` |
| `.md`                                                      | `markdownlint-cli2 --fix`, `prettier --write`, then report markdownlint    |
| `.js .jsx .mjs .cjs .ts .tsx .mdx .css .scss .html .jsonc` | `prettier --write`                                                         |

Each tool runs from the project root, so project config (`pyproject.toml`,
`.prettierrc`, `.markdownlint*`) is honored, and a project-local
`node_modules/.bin/<tool>` is preferred. A missing CLI is skipped silently.

## Config files

| File                                                   | Used by                       |
| ------------------------------------------------------ | ----------------------------- |
| [`black.toml`](../hooks/format-lint/config/black.toml) | `black --config` (79 columns) |

Black's `--config` replaces the project's own Black config, matching your
`black-formatter.args` in VS Code. To configure another tool, drop its file in
`config/` and add `--config <file>` (or the tool's equivalent flag) to its
`Step` in the script.

## Parity with VS Code settings

- ESLint is not run (disabled in your user settings).
- Prettier, ruff and markdownlint have no user overrides; defaults match.
- Not covered: `.json` (VS Code built-in), YAML (Red Hat), Go, Astro, YANG, XML.

## Notes

- Hooks run CLIs only. VS Code extensions can't be called from a hook; the CLIs
  read the same config.
- Lint and type errors are reported after every edit, so a half-finished
  multi-edit change may report errors the next edit fixes.
- Set `COPILOT_HOOK_DEBUG=1` to log payloads to
  `~/.copilot/logs/format-lint.log`.
- Pylint and isort are not run; `ruff` sorts imports only if the project
  enables the `I` rules, same as the editor on save.
