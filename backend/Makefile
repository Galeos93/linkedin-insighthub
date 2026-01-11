IMAGE_NAME ?= galeos93/linkedin-insight-hub-backend
TAG ?= latest

install:
	@echo "📦 Installing dependencies..."
	poetry install --no-root

run: install ## Run the application
	@echo "🚀 Running the application..."
	poetry run python -m main

test:
	@echo "🧪 Running tests..."
	poetry run pytest tests/

docker-build: ## Build Docker image
	@echo "🐳 Building Docker image..."
	docker build -f docker/Dockerfile -t $(IMAGE_NAME):$(TAG) .

docker-run: ## Run Docker container
	@echo "🚀 Running Docker container..."
	docker run -p 8000:8000 $(IMAGE_NAME):$(TAG)

docker-push: ## Push Docker image to registry
	@echo "📤 Pushing Docker image to registry..."
	docker push $(IMAGE_NAME):$(TAG)