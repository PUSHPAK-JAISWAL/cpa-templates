# OpenTelemetry tracing

This extension wires in lightweight OpenTelemetry tracing for FastAPI applications so you can inspect request flows locally.

## What it adds

- An `OTEL_ENABLED` switch in the generated environment defaults
- A small telemetry bootstrap module under `app/core`
- FastAPI and logging instrumentation when telemetry is enabled

## Configure

Add these values to your `.env` file:

```env
OTEL_ENABLED=true
OTEL_SERVICE_NAME=my-api
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318
```

The exporter endpoint is optional; if it is left empty, the default console exporter is used so it is easy to test locally.

## Verify

Run the app and make a request to confirm instrumentation is active:

```sh
uv run python -m uvicorn app.main:app --reload
curl http://127.0.0.1:8000/ping
```

You should see span output in the terminal when telemetry is enabled.
