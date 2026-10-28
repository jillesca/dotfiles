# Global agent instructions

These rules apply to every AI agent running on this machine, in every project.

## Hooks

- A `postToolUse` hook runs after every file edit and formats, lints and type-checks the file you just wrote.
- Expect small changes to code you generated (formatting, import cleanup). Re-read the file before editing it again instead of assuming your last edit is verbatim on disk.
- If the hook reports lint or type problems, fix them in your next edit.

## Git

- Never stage (`git add`), commit, or push unless the user explicitly tells you to.
- If you believe a commit or push is warranted (for example, after a large amount of work), ask the user first and wait for their answer.
- Leave all changes in the working tree for the user to review.
