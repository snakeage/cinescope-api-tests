.PHONY: help lint test test-smoke test-regression test-negative test-workflow

PRECOMMIT=.venv/bin/pre-commit
PYTEST=.venv/bin/pytest

help: ## Show available commands
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## ' Makefile | sed 's/:.*## / - /'

lint: ## Run pre-commit hooks
	$(PRECOMMIT) run --all-files

test: ## Run all tests
	$(PYTEST)

test-smoke: ## Run smoke tests
	$(PYTEST) -m smoke -q

test-regression: ## Run regression tests
	$(PYTEST) -m regression -q

test-negative: ## Run negative tests
	$(PYTEST) -m negative -q

test-workflow: ## Run workflow tests
	$(PYTEST) -m workflow -q
