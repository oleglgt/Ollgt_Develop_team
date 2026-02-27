"""Response models for the Hello World API.

This module defines Pydantic models used for API responses,
ensuring type safety and automatic validation.
"""

from pydantic import BaseModel, Field


class HelloResponse(BaseModel):
    """Response model for hello endpoint.
    
    Attributes:
        message: The greeting message to be returned.
    """
    
    message: str = Field(
        ...,
        description="Greeting message",
        example="Hello, World!"
    )
    
    class Config:
        """Pydantic model configuration."""
        
        json_schema_extra = {
            "example": {
                "message": "Hello, World!"
            }
        }
