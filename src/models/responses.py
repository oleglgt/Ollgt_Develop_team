"""Response models for API endpoints."""

from pydantic import BaseModel, Field


class HelloResponse(BaseModel):
    """Response model for hello endpoint.
    
    Attributes:
        message: A greeting message string.
    """
    
    message: str = Field(
        ...,
        description="Greeting message",
        example="Hello, World!"
    )
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "message": "Hello, World!"
                }
            ]
        }
    }
