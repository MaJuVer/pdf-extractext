FROM python:3.11-slim AS builder

ARG UV_VERSION=0.4.0

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT="/opt/venv"

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir uv==${UV_VERSION}

COPY pyproject.toml uv.lock* ./

RUN uv sync --frozen --no-dev --no-install-project

FROM python:3.11-slim

LABEL maintainer="MaJuVer" \
      description="API RESTful construida con FastAPI para extraer texto de un PDF"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH" \
    ENVIRONMENT=production \
    MONGO_URL=""

RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -r -s /bin/false -g appgroup appuser

WORKDIR /app

RUN apt-get update && apt-get upgrade -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
    
COPY --from=builder --chown=appuser:appgroup /app/.venv /app/.venv
COPY --chown=appuser:appgroup src/ ./src/

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "src.interface.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]