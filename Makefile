BIN_DIR := $(HOME)/.local/bin

install: install-sandbox-ssh
	@echo "=== All tools installed ==="

install-sandbox-ssh:
	@mkdir -p $(BIN_DIR)
	@chmod +x $(CURDIR)/sandbox-ssh
	@ln -sf $(CURDIR)/sandbox-ssh $(BIN_DIR)/sandbox-ssh
	@echo "sandbox-ssh -> $(BIN_DIR)/sandbox-ssh"

help:
	@echo "Available targets:"
	@echo "  install               - Install all tools (symlinks into $(BIN_DIR))"
	@echo "  install-sandbox-ssh   - Install only sandbox-ssh"
	@echo "  help                  - Show this help message"

.PHONY: install install-sandbox-ssh help
