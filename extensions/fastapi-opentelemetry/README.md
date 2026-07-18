# OpenTelemetry (extension bank)

Maintainer-facing notes for the **fastapi-opentelemetry** extension in `cpa-templates`.

Copied into generated projects (via `template/`):

| Path | Purpose |
|------|---------|
| `pyproject.toml` | Adds OpenTelemetry packages for tracing, logging instrumentation, and OTLP/HTTP export |
| `app/core/telemetry.py` | `configure_telemetry(app)` bootstrap (no-op unless `OTEL_ENABLED`) |
| `.env.example.append` | Documents `OTEL_ENABLED`, `OTEL_SERVICE_NAME`, and `OTEL_EXPORTER_OTLP_ENDPOINT` |
| `docs/OTEL_GUIDE.md` | Usage and verification instructions |
| `docs/README.md.append` | Index bullet for `docs/README.md` |

The bank `README.md` (this file) stays **outside** `template/` so it does not overwrite the project README.

Like `fastapi-sentry`, this extension does **not** overwrite `app/main.py` /
`app/core/config.py` — callers add a one-line wire-up so other addons stay
composable.

## Apply

```sh
uvx create-awesome-python-app my-api \
  --template fastapi-starter \
  --addons fastapi-opentelemetry \
  --no-interactive
```

## Verify after scaffold

```sh
uv sync
OTEL_ENABLED=true OTEL_SERVICE_NAME=my-api \
  uv run python -c "from fastapi import FastAPI; from app.core.telemetry import configure_telemetry; configure_telemetry(FastAPI()); print('ok')"
```

See `template/docs/OTEL_GUIDE.md` for the full setup and troubleshooting notes.
