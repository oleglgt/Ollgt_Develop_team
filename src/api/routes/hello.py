"""Hello endpoint implementation.

This module contains the hello endpoint that returns a simple greeting message.
"""

from fastapi import APIRouter

from src.models.responses import HelloResponse

# Create router for hello endpoints
router = APIRouter(tags=["hello"])


@router.get(
    "/hello",
    response_model=HelloResponse,
    status_code=200,
    summary="Get hello message",
    description="Returns a simple greeting message."
)
async def get_hello() -> HelloResponse:
    """Return a hello world greeting message.
    
    Returns:
        HelloResponse: A response object containing the greeting message.
        
    Example:
        >>> response = await get_hello()
        >>> response.message
        'Hello, World!'
    """
    return HelloResponse(message="Hello, World!")
