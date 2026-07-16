# PostgreSQL

Postgres Compose service under `docker/postgres/` — same layout pattern as cna-templates DB extensions (`docker/<engine>/compose.yml`).

This extension also merges a partial `pyproject.toml` that adds `psycopg[binary]`, and appends Postgres env vars via `.env.example.append`.

## When to use

- The API will persist data in PostgreSQL.
- You want a local Postgres instance via Docker without hand-writing compose YAML.
- You use SQLAlchemy, psycopg, or another Postgres driver and need the client library in `pyproject.toml`.

The extension ships the **database service and driver dependency** — wire your ORM and migrations in application code after scaffold.

## What it adds

| Path | Purpose |
|------|---------|
| `pyproject.toml` | Merges `psycopg[binary]>=3.2` into project dependencies |
| `.env.example.append` | Appends Postgres keys to root `.env.example` |
| `docker/postgres/compose.yml` | Postgres 16 service + volume + healthcheck |
| `docker/postgres/.env.example` | Standalone env reference for the DB compose file |

## Environment variables

Root `.env.example` gains these keys from `.env.example.append`:

| Variable | Default | Notes |
|----------|---------|-------|
| `POSTGRES_USER` | `app` | DB superuser for local dev |
| `POSTGRES_PASSWORD` | `app` | Change in production |
| `POSTGRES_DB` | `app` | Database name |
| `DATABASE_URL` | (commented) | Example: `postgresql+psycopg://app:app@localhost:5432/app` |

When combined with **`python-docker`**, the postgres compose overlay sets:

```env
DATABASE_URL=postgresql+psycopg://app:app@db:5432/app
```

Use host `db` (Docker service name) inside compose; use `localhost` when connecting from the host machine.

## Quick start (Postgres only)

```sh
docker compose -f docker/postgres/compose.yml up -d
```

Connect from the host:

```sh
psql "postgresql://app:app@localhost:5432/app"
```

Or use any Postgres client on port `5432`.

## With the `python-docker` extension

From the project root (after both extensions are applied):

```sh
# API (compose.yml) + Postgres (docker/postgres/compose.yml)
docker compose -f compose.yml -f docker/postgres/compose.yml up --build
```

The postgres compose file declares:

- `db` — Postgres 16 Alpine with a named volume and `pg_isready` healthcheck
- `api` — `depends_on` with `condition: service_healthy` and `DATABASE_URL` injected

## Local development without Docker

`psycopg` is added automatically via the merged `pyproject.toml`:

```sh
uv sync
```

Install and run Postgres on the host (or use a cloud instance), then set `DATABASE_URL` in `.env` pointing at your instance. Wire SQLAlchemy or your ORM when you add persistence.

## Verification

1. **Postgres only:** `docker compose -f docker/postgres/compose.yml up -d` — `db` reaches healthy state.
2. **Healthcheck:** `docker compose -f docker/postgres/compose.yml ps` shows `healthy` for `db`.
3. **Connect:** `psql postgresql://app:app@localhost:5432/app -c 'SELECT 1'`.
4. **With API:** After full stack compose, `curl http://localhost:8000/ping` still returns OK (API does not require DB until you wire it).
5. **Dependency:** `uv run python -c "import psycopg"` succeeds after `uv sync`.

## Compose notes

- Data persists in the `postgres_data` Docker volume between restarts.
- To reset: `docker compose -f docker/postgres/compose.yml down -v` (destroys data).
- For production, use managed Postgres; this compose file is for local development.
