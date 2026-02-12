# AGENTS.md  Project Instructions

## Overview
- Project: basketball_worldwide
- Stack: FastAPI, SQLAlchemy, Alembic, Postgres
- Python version: see .python-version

## How to run
- Install deps: uv sync
- Run app: docker compose up --build or docker compose up -d
- Run tests: uv run pytest

## Conventions
- Prefer `rg` for search.
- Avoid editing unrelated files.
- Use `apply_patch` for small changes.
- Keep changes minimal and explain why.

## Alembic
- Alembic config: `alembic.ini`
- Env file: `alembic/env.py`
- DB URL is read from: (env var or settings module)
