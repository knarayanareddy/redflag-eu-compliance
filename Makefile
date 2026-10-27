UV ?= uv

.PHONY: help sample check test serve demo ui build-pages clean

help:
	@echo "Available commands:"
	@echo "  make sample  - Run offline API, gate, and schema tests"
	@echo "  make check   - Run tests and Ruff linting"
	@echo "  make serve   - Start the local API on 0.0.0.0:8000"
	@echo "  make ui      - Start the Vite UI on 0.0.0.0:5173 (API must be running)"
	@echo "  make build-pages - Build the static client-side GitHub Pages demo"
	@echo "  make clean   - Remove virtualenvs, caches, and build artifacts"

sample test:
	cd backend && $(UV) run --extra dev pytest tests/ -v

check:
	cd backend && $(UV) run --extra dev pytest tests/ -v
	cd backend && $(UV) run --extra dev ruff check app tests

serve demo:
	cd backend && $(UV) run uvicorn app.main:app --host 0.0.0.0 --port 8000

ui:
	cd frontend && npm run dev -- --host 0.0.0.0

build-pages:
	cd frontend && VITE_STATIC_DEMO=true npm run build

clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -prune -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -prune -exec rm -rf {} +
	rm -rf backend/.venv backend/build backend/*.egg-info frontend/node_modules frontend/dist
