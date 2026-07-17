"""Example feature schemas."""

from pydantic import BaseModel


class ExampleResource(BaseModel):
    """Example response payload."""

    id: str
    name: str
