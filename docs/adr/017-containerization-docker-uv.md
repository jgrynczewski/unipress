# ADR-017: Containerization with Docker, uv, and Multi-Stage Builds

## Status
Accepted

## Context
We want to package and run Unipress consistently across environments (local, CI, deployment) while preserving our quality gates (ruff, mypy, pytest). The project uses the Arcade framework and audio libraries, which require system packages (OpenGL/X11/OpenAL). We already standardized on `uv` for dependency management (ADR-001) and on a rigorous CI pipeline (ADR-007). We need a container approach that:

- Produces reproducible builds
- Enforces quality checks during image build
- Ships a lean runtime image with only what’s necessary
- Supports headless testing (CI) and interactive graphics locally
- Follows least-privilege (non-root) and includes a healthcheck

## Decision
Adopt a multi-stage Docker build using `python:3.12-slim`, install `uv` in a build stage, run QA in a dedicated dev/test stage under `xvfb`, and assemble a minimal runtime image with a non-root user and a basic healthcheck.

Artifacts added:
- `Dockerfile` (multi-stage: base → dev → runtime)
- `.dockerignore` (exclude caches, VCS, editor files)
- `docker-compose.yml` (optional dev runner using host display)

## Rationale
- **Reproducibility**: Pin to Python slim base, use `uv` with `uv.lock` (ADR-001) and `--frozen` to guarantee dependency versions.
- **Quality Assurance**: Run `ruff`, `mypy`, and `pytest` in an intermediate dev stage; the image build fails if checks fail, aligning with ADR-007.
- **Performance**: Cache `uv` operations via build cache mounts; only copy lockfiles before dependency sync to maximize layer re-use.
- **Security/Footprint**: Runtime image excludes build tools; uses a non-root `app` user; installs only required runtime libs (OpenGL/X11/OpenAL/audio) used by Arcade.
- **Headless CI**: `xvfb-run` enables windowed tests in containerized CI.
- **Operability**: Healthcheck verifies Python Arcade import; `ENTRYPOINT` starts `main.py` with difficulty override via env/args.

## Consequences
### Positive
- Consistent local/CI/deploy environments
- Early failure on quality gates during image build
- Smaller runtime image and reduced attack surface
- Simple developer experience with `docker compose up` for local runs

### Considerations
- Requires GPU/X server passthrough for full-screen rendering on hosts; compose file demonstrates host display integration on Linux. For CI, tests run headlessly with `xvfb-run`.
- Audio in containers depends on host sound server configuration. The project’s tests avoid hard sound requirements.

## Implementation
### Dockerfile (summary)
- Stage `base`: install system libs, install `uv`, `uv sync --frozen --no-dev` using `pyproject.toml` and `uv.lock` only.
- Stage `dev`: copy source, `uv sync` with dev deps, install `xvfb`, run `ruff`, `mypy`, and `pytest` under `xvfb-run`.
- Stage `runtime`: copy venv from base, copy app sources and assets, create non-root user, configure PATH, add healthcheck, run `main.py` by default.

### Compose
- Binds project into `/app` for rapid iteration; sets `DISPLAY` and uses host networking as an optional Linux-friendly setup. Not required for CI images.

## Alternatives Considered
1. Single-stage image with dev tools: simpler but larger and less secure; QA not enforced during build boundaries.
2. Poetry-based images: conflict with ADR-001 (uv decision), slower installs.
3. Conda-based images: unnecessary complexity for this project’s dependency set.

## Links
- ADR-001 (uv), ADR-002 (Arcade), ADR-003 (QA tools), ADR-007 (CI/CD)






