"""Example feature HTTP routes."""

from fastapi import APIRouter, Request

from app.features._feature_template_.schemas import ExampleResource
from app.features._feature_template_.service import get_example_resource
from app.schemas.common.responses import APIResponse, make_item_response

router = APIRouter(prefix="/examples", tags=["examples"])


@router.get("/{resource_id}", response_model=APIResponse[ExampleResource])
async def get_example(resource_id: str, request: Request) -> APIResponse[ExampleResource]:
    """Example endpoint structure for a feature module."""
    resource = get_example_resource()
    resource.id = resource_id
    return make_item_response(
        data=resource,
        dev_code="EXAMPLE_FOUND",
        message="Example resource loaded",
        request_id=getattr(request.state, "request_id", "unknown"),
    )
