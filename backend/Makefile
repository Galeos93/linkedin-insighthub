IMAGE_NAME ?= galeos93/linkedin-insight-hub-backend
TAG ?= latest

docker-build: ## Build Docker image
	@echo "🐳 Building Docker image..."
	docker build -f docker/Dockerfile -t $(IMAGE_NAME):$(TAG) .

docker-run: ## Run Docker container
	@echo "🚀 Running Docker container..."
	docker run -p 8000:8000 $(IMAGE_NAME):$(TAG)

docker-push: ## Push Docker image to registry
	@echo "📤 Pushing Docker image to registry..."
	docker push $(IMAGE_NAME):$(TAG)