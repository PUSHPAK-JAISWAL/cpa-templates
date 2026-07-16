# Docker

Run the API in a container with [uv](https://docs.astral.sh/uv/). Compose files follow the same convention as [cna-templates](https://github.com/Create-Node-App/cna-templates): **`compose.yml`** (not `docker-compose.yml`).

## When to use

- You want a reproducible local dev environment without installing Python on the host.
- You deploy the API as a container image.
- You need a production-style compose overlay (`compose.prod.yml`) alongside dev settings.

Pair with **`python-postgres`** when the API needs a database — see that extension's README for multi-file compose commands.

## What it adds

| Path | Purpose |
|------|---------|
| `Dockerfile` | Multi-stage-friendly image based on `ghcr.io/astral-sh/uv:python3.12-bookworm-slim` |
| `.dockerignore` | Keeps `.venv`, caches, and git metadata out of the build context |
| `compose.yml` | Dev: bind-mount source, `--reload`, port `8000` |
| `compose.prod.yml` | Prod overlay: no bind mount, `restart: always`, no reload |

## Environment variables

Create `.env` at the project root (copy from `.env.example` after scaffold). Common keys from `fastapi-starter`:

| Variable | Default | Notes |
|----------|---------|-------|
| `DEBUG` | `false` | Set `true` for local dev outside Docker |
| `HOST` | `127.0.0.1` | Compose overrides via uvicorn `--host 0.0.0.0` |
| `PORT` | `8000` | Mapped in `compose.yml` |
| `API_PREFIX` | `/api/v1` | From template scaffold options |
| `CORS_ORIGINS` | localhost URLs | Comma-separated |

For production-style runs, set `DEBUG=false` in `.env`.

## Development

```sh
docker compose up --build
```

- API docs: http://localhost:8000/docs
- Health probe: http://localhost:8000/ping

The dev compose file bind-mounts the project directory and runs uvicorn with `--reload`.

## Production-style run

```sh
docker compose -f compose.yml -f compose.prod.yml up --build -d
```

The prod overlay removes the source bind mount and `--reload`, and sets `restart: always`.

## With `python-postgres`

From the project root (after both extensions are applied):

```sh
docker compose -f compose.yml -f docker/postgres/compose.yml up --build
```

The postgres extension's compose file adds a `db` service and wires `DATABASE_URL` on the `api` service when files are merged.

## Verification

1. **Build:** `docker compose build` completes without errors.
2. **Start:** `docker compose up --build` — container stays running.
3. **Health:** `curl -s http://localhost:8000/ping` returns `{"status":"ok"}`.
4. **Docs:** Open http://localhost:8000/docs in a browser.
5. **Prod overlay:** `docker compose -f compose.yml -f compose.prod.yml config` validates merged config.

## Production notes

- Set `DEBUG=false` in `.env`.
- Use a process manager or orchestrator for multi-instance deployments.
- Add health checks targeting `/ping` in your orchestrator or compose prod file.
- Pin base image tags in `Dockerfile` for reproducible builds.
