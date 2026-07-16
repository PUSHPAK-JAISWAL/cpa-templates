"""Standard API response envelope."""

from datetime import UTC, datetime

from pydantic import BaseModel, Field


class ResponseMetadata(BaseModel):
    """Metadata attached to every API response."""

    request_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))


class ErrorDetail(BaseModel):
    """A single validation or business error."""

    field: str | None = None
    message: str


class APIResponse[T](BaseModel):
    """Universal response envelope for API endpoints."""

    success: bool
    status_code: int
    dev_code: str
    message: str
    data: T | None
    errors: list[ErrorDetail] = Field(default_factory=list)
    metadata: ResponseMetadata


def make_item_response[T](
    data: T,
    dev_code: str,
    message: str,
    request_id: str,
    status_code: int = 200,
) -> APIResponse[T]:
    """Build a success response for a single resource."""
    return APIResponse(
        success=True,
        status_code=status_code,
        dev_code=dev_code,
        message=message,
        data=data,
        errors=[],
        metadata=ResponseMetadata(request_id=request_id),
    )


def make_error_response(
    status_code: int,
    dev_code: str,
    message: str,
    request_id: str,
    errors: list[ErrorDetail] | None = None,
) -> APIResponse[None]:
    """Build a standard error response."""
    return APIResponse(
        success=False,
        status_code=status_code,
        dev_code=dev_code,
        message=message,
        data=None,
        errors=errors or [],
        metadata=ResponseMetadata(request_id=request_id),
    )
