.PHONY: help install install-dev test lint format clean run docker-build docker-up docker-down

help:
	@echo "Gen Z Slang Explainer - Available Commands"
	@echo ""
	@echo "  make install      - Install production dependencies"
	@echo "  make install-dev  - Install development dependencies"
	@echo "  make test         - Run tests with coverage"
	@echo "  make lint         - Run linting (ruff + black check)"
	@echo "  make format       - Format code with black"
	@echo "  make run          - Run the API server locally"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-up    - Start Docker containers"
	@echo "  make docker-down  - Stop Docker containers"
	@echo "  make clean        - Remove generated files"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

test:
	cd api && pytest --cov=src --cov-report=term-missing --cov-report=html

lint:
	ruff check api/src api/tests
	black --check api/src api/tests

format:
	black api/src api/tests
	ruff check --fix api/src api/tests

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

run:
	cd api && uvicorn src.router:app --host 0.0.0.0 --port 8000 --reload

docker-build:
	docker-compose build

docker-up:
	docker-compose up -d
	@echo "API running at http://localhost:8000"
	@echo "Docs available at http://localhost:8000/docs"

docker-down:
	docker-compose down
