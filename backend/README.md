# Backend Service

This directory contains the backend API responsible for ingesting, processing, and analyzing LinkedIn saved jobs data uploaded from the frontend.

The backend is implemented in **Python**, managed with **Poetry**, and containerized using **Docker**. All runtime configuration, including the entry point `main.py`, is defined in `config.yaml`.

---

## Tech Stack

* Python 3
* Poetry (dependency management)
* FastAPI (API entry point via `main.py`)
* Docker
* Postman (API testing)

---

## Project Structure

```
backend/
├── application/        # Application / use-case layer
├── domain/             # Domain models and business logic
├── infrastructure/     # Persistence and external interfaces
├── tests/              # Automated tests
├── docker/             # Dockerfile and related assets
├── main.py             # API entry point
├── config.yaml         # Service configuration
├── pyproject.toml      # Poetry configuration
├── poetry.lock         # Locked dependencies
├── Makefile            # Common development and Docker commands
├── postman_collection.json
└── README.md
```

---

## Makefile Commands

The `Makefile` includes commands for both Poetry-based local development and Docker usage.

### Local Development (Poetry)

* **Install dependencies:**

  ```bash
  make install
  ```

  Installs all Python dependencies via Poetry.

* **Run API locally:**

  ```bash
  make run
  ```

  Starts the API using Poetry. The `config.yaml` defines the `main.py` entry point.

* **Run tests:**

  ```bash
  make test
  ```

  Executes all backend tests via Poetry.

### Docker Commands

* **Build Docker image:**

  ```bash
  make docker-build
  ```

  Builds the Docker image defined in `docker/Dockerfile`.

* **Run Docker container:**

  ```bash
  make docker-run
  ```

  Runs the container exposing the API on `http://localhost:8000`.

* **Push Docker image:**

  ```bash
  make docker-push
  ```

  Pushes the image to the registry.

---

## API Testing (Postman)

A Postman collection is provided:

```
postman_collection.json
```

Import this file into Postman to explore and manually test the available API endpoints.

---

## Configuration

Runtime configuration is defined in `config.yaml`.

* Defines the API entry point (`main.py`) and other service-wide settings.
* Used in both local and Dockerized executions.

---

## Notes

* The backend does **not** require LinkedIn credentials.
* All data is processed locally.
* The service is stateless and upload-driven.

---

## License

See the root `LICENSE` file for details.
