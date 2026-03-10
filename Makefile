.PHONY: dev build up down test lint clean help

# ==========================================
#  Swarm Simulation MVP — Unified Makefile
# ==========================================

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-18s\033[0m %s\n", $$1, $$2}'

# ---------- Development ----------

dev: ## Start backend + frontend for local development (no Docker)
	@echo "Starting Backend (Uvicorn)..."
	cd backend && python run.py &
	@echo "Starting Frontend (Vite)..."
	cd frontend && npm run dev

# ---------- Docker ----------

build: ## Build all Docker images
	docker compose -f docker-compose.dev.yml build

up: ## Start all services via Docker Compose
	docker compose -f docker-compose.dev.yml up -d
	@echo "Frontend: http://localhost:3000"
	@echo "Backend:  http://localhost:5000"

down: ## Stop all Docker Compose services
	docker compose -f docker-compose.dev.yml down

# ---------- Quality ----------

test: ## Run all tests (backend pytest + frontend vitest)
	cd backend && python -m pytest tests -v
	cd frontend && npm run test

lint: ## Run linters (Ruff for Python, ESLint for TypeScript)
	cd backend && python -m ruff check app/ tests/
	cd frontend && npx eslint src/ --ext .ts,.vue

format: ## Auto-format code
	cd backend && python -m ruff format app/ tests/
	cd frontend && npx eslint src/ --ext .ts,.vue --fix

# ---------- Cleanup ----------

clean: ## Remove build artifacts and caches
	cd backend && rm -rf __pycache__ .pytest_cache
	cd frontend && rm -rf dist node_modules/.vite
