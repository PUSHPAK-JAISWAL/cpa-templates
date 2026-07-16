"""Health feature HTTP routes."""

from fastapi import APIRouter, Request

from app.features.health.schemas import HealthStatus
from app.features.health.service import get_health_status
from app.schemas.common.responses import APIResponse, make_item_response

router = APIRouter(tags=["health"])


@router.get(
    "/healthz",
    response_model=APIResponse[HealthStatus],
    responses={200: {"description": "Service is healthy"}},
)
async def health_check(request: Request) -> APIResponse[HealthStatus]:
    """Service health endpoint."""
    return make_item_response(
        data=get_health_status(),
        dev_code="HEALTH_OK",
        message="Service is healthy",
        request_id=getattr(request.state, "request_id", "unknown"),
    )
