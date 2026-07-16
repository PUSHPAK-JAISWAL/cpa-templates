# Dev Container

Open the project in a [Dev Container](https://code.visualstudio.com/docs/devcontainers/containers) for a reproducible Python 3.12 + [uv](https://docs.astral.sh/uv/) environment inside VS Code (or compatible editors).

## When to use

- Contributors use different host OS versions and you want one consistent toolchain.
- You prefer developing inside a container without maintaining a full `python-docker` compose stack.
- You want Ruff, Python, and debugger extensions pre-installed in the editor.

This extension is **editor-focused** — it does not replace `python-docker` for deployment or CI container builds. You can use both: Dev Container for daily coding, Docker compose for integration testing.

## What it adds

| Path | Purpose |
|------|---------|
| `.devcontainer/devcontainer.json` | VS Code Dev Container config |
| `.devcontainer/Dockerfile` | Python 3.12 base image + uv installer |

### Pre-configured editor features

- **Extensions:** Python, Ruff, debugpy
- **Settings:** Format on save with Ruff
- **Ports:** `8000` forwarded with label "FastAPI"
- **Post-create:** `uv sync` runs automatically after container build

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) running on the host
- VS Code with the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) (or Cursor / compatible fork)

## Usage

Apply during scaffold:

```sh
uvx create-awesome-python-app my-api \
  --template fastapi-starter \
  --addons python-devcontainer
```

Then in VS Code:

1. **Command Palette** → **Dev Containers: Reopen in Container**
2. Wait for the image build and `uv sync` (post-create command)
3. Start the API from the integrated terminal:

```sh
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Port `8000` is forwarded to the host — open http://localhost:8000/docs.

## With `python-postgres`

The Dev Container does not start Postgres automatically. Options:

1. Run Postgres on the host: `docker compose -f docker/postgres/compose.yml up -d` (from a host terminal).
2. Use Docker-in-Docker or a `dockerComposeFile` override in a custom `devcontainer.json` (not included by default).

Set `DATABASE_URL` in `.env` to reach Postgres on `host.docker.internal` or the host's LAN IP when the DB runs outside the dev container.

## Verification

1. **Reopen in Container** completes without build errors.
2. Terminal: `uv --version` and `python --version` (3.12) work.
3. `uv sync` succeeds (also runs as `postCreateCommand`).
4. `uv run ruff check .` and `uv run pytest` pass.
5. `uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000` — http://localhost:8000/ping returns `{"status":"ok"}`.
6. VS Code shows Python and Ruff extensions active in the container.

## Customization

- **Python version:** Update `.devcontainer/Dockerfile` base tag and `devcontainer.json` if you change `requires-python` in `pyproject.toml`.
- **Extra tools:** Add `RUN apt-get install ...` or dev dependencies to `pyproject.toml` and re-run `uv sync`.
- **Compose integration:** Add `"dockerComposeFile"` and `"service"` keys to `devcontainer.json` if you want the editor to manage a multi-service stack.
