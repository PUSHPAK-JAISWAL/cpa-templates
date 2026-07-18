# OpenTelemetry tracing

This extension adds a small OpenTelemetry bootstrap for FastAPI so you can
inspect request flows locally (console exporter) or ship spans to an OTLP
collector.

## What it adds

| Path | Purpose |
|------|---------|
| `pyproject.toml` | Merges OpenTelemetry API/SDK + FastAPI/logging instrumentation + OTLP/HTTP exporter |
| `app/core/telemetry.py` | `configure_telemetry(app)` helper (no-op unless `OTEL_ENABLED` is set) |
| `.env.example` entries | Documents `OTEL_*` variables |

## Wire it up

In `app/main.py`, after you create the FastAPI `app`:

```python
from app.core.telemetry import configure_telemetry

# ... create app, middleware, routers ...
configure_telemetry(app)
```

Initialization is a **no-op** when `OTEL_ENABLED` is unset/false, so local
development stays quiet until you opt in.

## Configure

Add these values to your `.env` file:

```env
OTEL_ENABLED=true
OTEL_SERVICE_NAME=my-api
# Optional — when empty, spans print to the console (great for local debug)
OTEL_EXPORTER_OTLP_ENDPOINT=
```

To send spans to a collector (for example the OTEL Collector or Jaeger OTLP):

```env
OTEL_ENABLED=true
OTEL_SERVICE_NAME=my-api
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318/v1/traces
```

## Verify

```sh
uv sync
OTEL_ENABLED=true OTEL_SERVICE_NAME=my-api \
  uv run python -c "from fastapi import FastAPI; from app.core.telemetry import configure_telemetry; configure_telemetry(FastAPI()); print('ok')"
```

With the wire-up in `app/main.py`, start the app and hit an endpoint — you
should see span output in the terminal when the OTLP endpoint is empty.
