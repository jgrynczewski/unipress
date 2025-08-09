# syntax=docker/dockerfile:1.7

ARG PYTHON_VERSION=3.12-slim

##############################
# Base image with uv and deps
##############################
FROM python:${PYTHON_VERSION} AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_INSTALL_DIR=/usr/local/bin \
    UV_PROJECT_ENVIRONMENT=/app/.venv \
    PATH="/usr/local/bin:/root/.local/bin:${PATH}"

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates git \
    libgl1 libglu1-mesa libx11-6 libxcursor1 libxrandr2 libxinerama1 libxi6 libxxf86vm1 \
    libgl1-mesa-dri \
    libopenal1 libsndfile1 libasound2 \
    libfreetype6 libfontconfig1 fonts-dejavu-core \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Install uv (respects UV_INSTALL_DIR); ensure it's on PATH
RUN curl -fsSL https://astral.sh/uv/install.sh | sh && \
    (command -v uv >/dev/null 2>&1 || ln -s /root/.local/bin/uv /usr/local/bin/uv) && \
    uv --version

WORKDIR /app

# Copy project manifests and sync dependencies (cached layer)
COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

##############################
# Dev/Test stage (runs QA)
##############################
FROM base AS dev
COPY . .
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

# Headless test dependencies
RUN apt-get update && apt-get install -y --no-install-recommends xvfb && rm -rf /var/lib/apt/lists/*

# Quality gates (fail fast if something breaks). Run tests under Xvfb.
RUN uv run ruff check && \
    uv run mypy unipress && \
    xvfb-run -a uv run pytest -q

##############################
# Runtime image (lean)
##############################
FROM python:${PYTHON_VERSION} AS runtime

# Runtime-only system libs (graphics/audio)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 libglu1-mesa libx11-6 libxcursor1 libxrandr2 libxinerama1 libxi6 libxxf86vm1 \
    libgl1-mesa-dri \
    libopenal1 libsndfile1 libasound2 \
    libfreetype6 libfontconfig1 fonts-dejavu-core \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Bring uv and the pre-synced virtualenv from base
COPY --from=base /usr/local/bin/uv /usr/local/bin/uv
WORKDIR /app
COPY --from=base /app/.venv /app/.venv

# Copy runtime sources and assets
COPY unipress ./unipress
COPY main.py README.md pyproject.toml uv.lock ./
COPY high_scores.json ./high_scores.json

# Non-root user
RUN groupadd -g 10001 app && useradd -m -u 10001 -g app app && \
    chown -R app:app /app
USER app

ENV PATH="/app/.venv/bin:${PATH}" \
    UV_PROJECT_ENVIRONMENT="/app/.venv"

# Basic healthcheck (validates arcade import)
HEALTHCHECK --interval=30s --timeout=3s CMD python -c "import arcade; print('ok')" || exit 1

# Default command runs the Jumper game via uv/module entry
ENV UNIPRESS_DIFFICULTY=5
ENTRYPOINT ["uv", "run", "python", "-m", "unipress.games.jumper.game"]
CMD []


