"""OpenTelemetry bootstrap helpers (fastapi-opentelemetry extension)."""

from __future__ import annotations

import os

from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter


def _env_bool(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def configure_telemetry(app: FastAPI | None = None) -> None:
    """Enable tracing when telemetry is explicitly enabled.

    No-op unless ``OTEL_ENABLED`` is truthy. Uses the console exporter by
    default; when ``OTEL_EXPORTER_OTLP_ENDPOINT`` is set, exports via OTLP/HTTP.
    """
    if not _env_bool("OTEL_ENABLED", default=False):
        return

    service_name = os.getenv("OTEL_SERVICE_NAME", "fastapi-starter").strip() or (
        "fastapi-starter"
    )
    resource = Resource.create({"service.name": service_name})
    provider = TracerProvider(resource=resource)

    endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "").strip()
    if endpoint:
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
            OTLPSpanExporter,
        )

        provider.add_span_processor(
            BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint))
        )
    else:
        provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))

    trace.set_tracer_provider(provider)

    if app is not None:
        FastAPIInstrumentor.instrument_app(app)
        LoggingInstrumentor().instrument()
