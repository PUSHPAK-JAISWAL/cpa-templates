"""OpenTelemetry bootstrap helpers."""

from fastapi import FastAPI

from app.core.config import settings
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter


def configure_telemetry(app: FastAPI | None = None) -> None:
    """Enable tracing when telemetry is explicitly enabled."""
    if not settings.otel_enabled:
        return

    service_name = settings.otel_service_name or "fastapi-starter"
    resource = Resource.create({"service.name": service_name})
    provider = TracerProvider(resource=resource)
    provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
    trace.set_tracer_provider(provider)

    if app is not None:
        FastAPIInstrumentor.instrument_app(app)
        LoggingInstrumentor().instrument()
