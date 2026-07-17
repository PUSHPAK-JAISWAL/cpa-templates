"""Health feature business logic."""

from datetime import UTC, datetime

from app.features.health.schemas import HealthStatus


def get_health_status() -> HealthStatus:
    """Return current service health."""
    return HealthStatus(
        status="healthy",
        service="fastapi-starter",
        timestamp=datetime.now(UTC).isoformat(),
    )
