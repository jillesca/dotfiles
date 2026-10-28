#!/usr/bin/env python3
"""postToolUse hook: format, lint and type-check the file an edit tool wrote.

The event on stdin names the tool and its arguments, so the edited file(s)
come straight from the payload. Each file goes through the pipeline for its
extension (see PIPELINES). Formatters rewrite the file in place; problems that
remain are returned as `additionalContext` for the agent to fix.

Set COPILOT_HOOK_DEBUG=1 to log raw payloads to ~/.copilot/logs/format-lint.log.
"""

import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

CONFIG_DIR = Path(__file__).resolve().parent / "config"
TOOL_TIMEOUT = 60
MAX_OUTPUT = 3000

EDIT_TOOL = re.compile(
    r"edit|create|write|patch|replace|insert", re.IGNORECASE
)
PATH_KEYS = {"filepath", "file_path", "path", "file"}
PATCH_FILE = re.compile(r"^\*\*\* (?:Add|Update) File: (.+)$", re.MULTILINE)
SKIP_DIRS = {"node_modules", ".venv", "venv", "site-packages", ".git"}
ROOT_MARKERS = (".git", "pyproject.toml", "package.json")


@dataclass
class Step:
    """One CLI call; the file path is appended to `cmd`."""

    cmd: list[str]
    report: bool = False  # a non-zero exit is reported to the agent


# Order mirrors VS Code on save: fixAll first, then the formatter.
PYTHON = [
    Step(["ruff", "check", "--fix", "--quiet"]),
    Step(["ty", "check", "--fix", "--color", "never"]),
    Step(["black", "--quiet", "--config", str(CONFIG_DIR / "black.toml")]),
    Step(["ruff", "check", "--quiet"], report=True),
    Step(["ty", "check", "--color", "never"], report=True),
]
MARKDOWN = [
    Step(["markdownlint-cli2", "--fix"]),
    Step(["prettier", "--write"], report=True),
    Step(["markdownlint-cli2"], report=True),
]
PRETTIER = [Step(["prettier", "--write"], report=True)]

PIPELINES = {
    ".py": PYTHON,
    ".md": MARKDOWN,
    **dict.fromkeys((".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx"), PRETTIER),
    **dict.fromkeys((".mdx", ".css", ".scss", ".html", ".jsonc"), PRETTIER),
}


def debug(payload: dict) -> None:
    if os.environ.get("COPILOT_HOOK_DEBUG") != "1":
        return
    log = Path.home() / ".copilot" / "logs" / "format-lint.log"
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("a") as fh:
        fh.write(json.dumps(payload) + "\n")


def collect_paths(value, found: list[str]) -> None:
    """Gather file paths from an edit tool's arguments, whatever their shape."""
    if isinstance(value, str):
        found.extend(PATCH_FILE.findall(value))
    elif isinstance(value, dict):
        for key, item in value.items():
            if key.lower() in PATH_KEYS and isinstance(item, str):
                found.append(item)
            else:
                collect_paths(item, found)
    elif isinstance(value, list):
        for item in value:
            collect_paths(item, found)


def edited_files(event: dict) -> list[Path]:
    # camelCase (Copilot CLI) and snake_case (VS Code) payloads both occur.
    tool = event.get("toolName") or event.get("tool_name") or ""
    if not EDIT_TOOL.search(tool):
        return []
    args = event.get("toolArgs") or event.get("tool_input")
    if isinstance(args, str):
        try:
            args = json.loads(args)
        except ValueError:
            pass
    names: list[str] = []
    collect_paths(args, names)
    cwd = Path(event.get("cwd") or os.getcwd())
    paths = (cwd / Path(name).expanduser() for name in names)
    return [p for p in paths if p.is_file() and not SKIP_DIRS & set(p.parts)]


def project_root(path: Path) -> Path:
    for parent in path.parents:
        if any((parent / marker).exists() for marker in ROOT_MARKERS):
            return parent
    return path.parent


def run(cmd: list[str], cwd: Path) -> tuple[int, str]:
    """Run a CLI from the project root; a missing CLI counts as success."""
    # Prefer the project's own binary, as the VS Code extensions do.
    local = cwd / "node_modules" / ".bin" / cmd[0]
    if local.exists():
        cmd = [str(local), *cmd[1:]]
    elif shutil.which(cmd[0]) is None:
        return 0, ""
    try:
        proc = subprocess.run(
            cmd,
            check=False,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=TOOL_TIMEOUT,
        )
    except subprocess.TimeoutExpired:
        return 1, f"timed out after {TOOL_TIMEOUT}s"
    return proc.returncode, (proc.stdout + proc.stderr).strip()


def check_file(path: Path) -> str:
    """Run the file's pipeline; return a report of what is still wrong."""
    root = project_root(path)
    problems = []
    for step in PIPELINES.get(path.suffix.lower(), []):
        code, out = run([*step.cmd, str(path)], root)
        if code and step.report:
            problems.append(f"{step.cmd[0]}:\n{out}")
    return f"{path}\n" + "\n".join(problems) if problems else ""


def main() -> None:
    try:
        event = json.load(sys.stdin)
    except ValueError:
        event = {}
    debug(event)
    reports = [r for r in map(check_file, edited_files(event)) if r]
    if not reports:
        print("{}")
        return
    context = (
        "Formatters already rewrote the file you just edited; re-read it "
        "before editing it again. Fix these remaining lint/type problems:\n\n"
        + "\n\n".join(reports)
    )
    print(json.dumps({"additionalContext": context[:MAX_OUTPUT]}))


if __name__ == "__main__":
    try:
        main()
    # Never break the agent because of the hook.
    except Exception as exc:  # noqa: BLE001
        print(f"format_lint hook error: {exc}", file=sys.stderr)
        print("{}")
