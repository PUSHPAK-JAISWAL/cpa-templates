"""Example feature business logic."""

from app.features._feature_template_.schemas import ExampleResource


def get_example_resource() -> ExampleResource:
    """Return an example resource."""
    return ExampleResource(id="example", name="Example resource")
