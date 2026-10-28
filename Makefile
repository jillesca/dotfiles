BIN_DIR := $(HOME)/.local/bin
HOOK_TOOLS := ruff black ty prettier markdownlint-cli2

install: install-sandbox-ssh install-agents install-hooks
	@echo "=== All tools installed ==="

install-agents:
	@chmod +x $(CURDIR)/scripts/link-agents.sh
	@$(CURDIR)/scripts/link-agents.sh

install-hooks: install-hook-tools
	@chmod +x $(CURDIR)/scripts/link-hooks.sh
	@$(CURDIR)/scripts/link-hooks.sh

install-hook-tools:
	@command -v brew >/dev/null || { echo "Homebrew is required" >&2; exit 1; }
	@brew list --formula $(HOOK_TOOLS) >/dev/null 2>&1 || brew install $(HOOK_TOOLS)

install-sandbox-ssh:
	@mkdir -p $(BIN_DIR)
	@chmod +x $(CURDIR)/sandbox-ssh
	@ln -sf $(CURDIR)/sandbox-ssh $(BIN_DIR)/sandbox-ssh
	@echo "sandbox-ssh -> $(BIN_DIR)/sandbox-ssh"

help:
	@echo "Available targets:"
	@echo "  install               - Install all tools (symlinks into $(BIN_DIR))"
	@echo "  install-sandbox-ssh   - Install only sandbox-ssh"
	@echo "  install-agents        - Symlink agents/AGENTS.md to Claude Code and VS Code Copilot"
	@echo "  install-hooks         - Symlink Copilot hook definitions and scripts into ~/.copilot/hooks and brew-install their CLIs"
	@echo "  help                  - Show this help message"

.PHONY: install install-sandbox-ssh install-agents install-hooks install-hook-tools help
