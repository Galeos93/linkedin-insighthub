############################
# Stage 1 — Build wheels
############################
FROM python:3.11-slim AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /build

# Native build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libomp-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry==2.0.1
RUN poetry self add poetry-plugin-export

# Disable virtualenvs so wheels build against system Python
RUN poetry config virtualenvs.create false

# Copy dependency definitions only
COPY pyproject.toml poetry.lock* ./

# Export requirements and build wheels
RUN poetry export -f requirements.txt --only main --without-hashes -o requirements.txt \
    && pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt


############################
# Stage 2 — Runtime image
############################
FROM python:3.11-slim AS runtime

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    HOME=/home/app \
    HF_HOME=/home/app/.cache/huggingface \
    TRANSFORMERS_CACHE=/home/app/.cache/huggingface \
    SENTENCE_TRANSFORMERS_HOME=/home/app/.cache/sentence-transformers \
    MPLCONFIGDIR=/home/app/.config/matplotlib \
    NUMBA_CACHE_DIR=/tmp \
    NLTK_DATA=/home/app/nltk_data

WORKDIR /app

# Runtime dependencies only (NO compiler)
RUN apt-get update && apt-get install -y \
    libomp5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy wheels from builder
COPY --from=builder /wheels /wheels

# Install wheels
RUN pip install --no-cache-dir /wheels/*

# Copy application code
COPY ./application ./application
COPY ./domain ./domain
COPY ./infrastructure ./infrastructure
COPY ./main.py .
COPY ./config.yaml .

# Create non-root user and home directory
RUN groupadd -r app \
    && useradd -r -g app app \
    && mkdir -p /home/app \
    && mkdir -p \
        /home/app/.cache/huggingface \
        /home/app/.cache/sentence-transformers \
        /home/app/.config/matplotlib \
    && chown -R app:app /home/app

# Install NLTK data
RUN python - <<EOF
import nltk
nltk.download("stopwords", download_dir="/home/app/nltk_data")
EOF

USER app

EXPOSE 8000
CMD ["python", "main.py"]
