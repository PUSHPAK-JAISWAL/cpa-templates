"""Health feature schemas."""

from pydantic import BaseModel


class HealthStatus(BaseModel):
    """Service health payload."""

    status: str
    service: str
    timestamp: str
