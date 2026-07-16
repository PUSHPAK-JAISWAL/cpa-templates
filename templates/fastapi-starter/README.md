# FastAPI Starter

Production-oriented FastAPI API starter with [uv](https://docs.astral.sh/uv/), [Ruff](https://docs.astral.sh/ruff/), and [pytest](https://docs.pytest.org/).

## Quick start

```sh
uv sync
uv run uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs for interactive API documentation.

## Commands

| Command | Description |
|---------|-------------|
| `uv run uvicorn app.main:app --reload` | Start dev server |
| `uv run ruff check .` | Lint |
| `uv run ruff format .` | Format |
| `uv run pytest` | Run tests |

## Project layout

```
app/
  api/        # API router composition
  core/       # Settings, middleware, logging, exception handlers
  features/   # Feature-based modules (router/service/schemas)
  schemas/    # Shared response/request schemas
tests/        # pytest suite
```

See [`docs/PROJECT_STRUCTURE.md`](docs/PROJECT_STRUCTURE.md) for the full
feature-based architecture guide.

## Configuration

Copy `.env.example` to `.env` and adjust values as needed.

The template also exposes scaffold-time options through `cpa.config.json`:

| Option | Default | Description |
|--------|---------|-------------|
| `apiPrefix` | `/api/v1` | Prefix used when mounting `app/api/router.py` |
| `enableCors` | `true` | Whether generated `app/main.py` registers CORS middleware |
