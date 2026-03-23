.PHONY: help lint test test-smoke test-smoke-stable test-smoke-integration test-regression test-negative test-workflow

help: ## Show available commands
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## ' Makefile | sed 's/:.*## / - /'

lint: ## Run pre-commit hooks
	uv run pre-commit run --all-files

test: ## Run all tests
	uv run pytest

test-smoke: ## Run stable smoke tests (PR-safe)
	uv run pytest -m smoke_stable -q

test-smoke-stable: ## Run stable smoke tests (PR-safe)
	uv run pytest -m smoke_stable -q

test-smoke-integration: ## Run integration smoke tests (env-dependent)
	uv run pytest -m smoke_integration -q

test-regression: ## Run regression tests
	uv run pytest -m regression -q

test-negative: ## Run negative tests
	uv run pytest -m negative -q

test-workflow: ## Run workflow tests
	uv run pytest -m workflow -q
