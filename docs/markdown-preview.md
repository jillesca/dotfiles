# cursor/markdown-preview.css

Reading-mode layout for Cursor/VS Code's Markdown preview: caps the body
width and centers it, instead of text stretching edge-to-edge.

Source: [`cursor/markdown-preview.css`](../cursor/markdown-preview.css)

## Enable in a new project

Run from the project root:

```sh
mkdir -p .vscode
ln -s ~/dotfiles/cursor/markdown-preview.css .vscode/markdown-preview.css
printf '\n.vscode/markdown-preview.css\n' >> .gitignore
```

(The leading `\n` above is deliberate — it guards against merging onto an
existing last line if `.gitignore` doesn't already end with a newline.)

Then add this to that project's `.vscode/settings.json` — create the file
if it doesn't exist yet, or merge just the `markdown.styles` key in if it
already has other settings (copy it from
[`cursor/settings.workspace.json`](../cursor/settings.workspace.json)):

```json
{
  "markdown.styles": [".vscode/markdown-preview.css"]
}
```

Reload the Markdown preview (`Cmd+Shift+V`, close and reopen) to see it.

Edit `cursor/markdown-preview.css` here and every project symlinking to it
picks up the change immediately — no reinstall step needed.

## Why a symlink

Cursor/VS Code only allows a workspace's `markdown.styles` setting to load
CSS files that live _inside_ that workspace (it won't point at arbitrary
files on disk). The symlink satisfies that rule while still keeping this one
file as the single source of truth.

## Related setting

The global `markdown.preview.fontSize` setting controls preview text size
(currently `20`). It lives in
`~/Library/Application Support/Cursor/User/settings.json`. It's global — set
once, it applies to every project, so there's nothing to repeat per project.
It isn't tracked in this repo because that settings.json bundles a lot of
unrelated machine-specific config.
