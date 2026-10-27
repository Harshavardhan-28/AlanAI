SHELL := /bin/bash
.DEFAULT_GOAL := help

COMPOSE := docker compose -f infra/docker-compose.yml

.PHONY: help dev down logs test test-py test-ts test-e2e lint typecheck fmt migrate seed psql clean

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'

dev: ## Bring up the full dev stack (db, redis, minio, api, worker, web)
	$(COMPOSE) up --build -d
	$(COMPOSE) ps

down: ## Tear down the dev stack
	$(COMPOSE) down

logs: ## Tail all service logs
	$(COMPOSE) logs -f --tail=200

migrate: ## Run DB migrations
	$(COMPOSE) exec api alembic upgrade head

seed: ## Seed dev data + fixture corpus
	$(COMPOSE) exec api python -m app.seed

test: test-py test-ts ## Run all tests

test-py: ## Python tests (api + worker + contracts)
	pytest apps/api/tests apps/worker/tests packages/shared/python/tests -q

test-ts: ## TypeScript tests (cli, gateway, shared)
	pnpm -r --filter "./packages/**" test

test-e2e: ## End-to-end tests (requires make dev)
	cd tests/e2e && pnpm test

lint: ## Lint everything
	ruff check apps packages/shared/python
	pnpm -r lint

typecheck: ## Type-check everything
	mypy apps/api/app apps/worker/src packages/shared/python/mcpaudit_shared
	pnpm -r typecheck

fmt: ## Format everything
	ruff format apps packages/shared/python
	pnpm -r format

psql: ## Open a psql shell
	$(COMPOSE) exec db psql -U mcpaudit -d mcpaudit

clean: ## Remove build artifacts and local volumes
	$(COMPOSE) down -v
	rm -rf .infra-data
