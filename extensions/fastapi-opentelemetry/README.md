# OpenTelemetry (extension bank)

Maintainer-facing notes for the **fastapi-opentelemetry** extension in `cpa-templates`.

Copied into generated projects (via `template/`):

| Path | Purpose |
|------|---------|
| `pyproject.toml` | Adds OpenTelemetry packages for tracing and logging instrumentation |
| `app/core/config.py` | Adds `OTEL_*` settings and a boolean toggle |
| `app/core/telemetry.py` | Bootstraps FastAPI and logging instrumentation |
| `app/main.py` | Initializes telemetry when enabled |
| `.env.example.append` | Documents `OTEL_ENABLED`, `OTEL_SERVICE_NAME`, and `OTEL_EXPORTER_OTLP_ENDPOINT` |
| `docs/OTEL_GUIDE.md` | Usage and verification instructions |
| `docs/README.md.append` | Index bullet for `docs/README.md` |

The bank `README.md` (this file) stays **outside** `template/` so it does not overwrite the project README.

## Apply

```sh
uvx create-awesome-python-app my-api \
  --template fastapi-starter \
  --addons fastapi-opentelemetry \
  --yes
```

## Verify after scaffold

```sh
uv sync
OTEL_ENABLED=true OTEL_SERVICE_NAME=my-api uv run python -c "from app.main import app; print(app.title)"
```

See `template/docs/OTEL_GUIDE.md` for the full setup and troubleshooting notes.
