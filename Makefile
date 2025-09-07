.PHONY: help install check test run build clean docs release

# Default target
.DEFAULT_GOAL := help

# Variables
PYTHON := uv run python
PACKAGE := n8n-lint
DIST_DIR := dist
SITE_DIR := site

help: ## Show this help message
	@echo "🚀 N8n JSON Linter - Development Commands"
	@echo ""
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install dependencies and pre-commit hooks
	@echo "📦 Installing dependencies..."
	@uv sync
	@echo "🔧 Installing pre-commit hooks..."
	@uv run pre-commit install

check: ## Run all quality checks (linting, formatting, type checking)
	@echo "🔍 Running quality checks..."
	@uv lock --locked
	@uv run pre-commit run -a

clean: ## Clean build artifacts
	@echo "🧹 Cleaning build artifacts..."
	@rm -rf $(DIST_DIR) build *.egg-info .pytest_cache .coverage
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true

docs-build: ## Build documentation
	@echo "📚 Building documentation..."
	@uv run mkdocs build

docs-serve: ## Serve documentation locally
	@echo "🌐 Serving documentation at http://127.0.0.1:8000"
	@uv run mkdocs serve

docs-check: ## Check documentation build
	@echo "✅ Checking documentation..."
	@uv run mkdocs build -s
