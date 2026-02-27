"""Hello endpoint route handler."""

from fastapi import APIRouter

from src.models.responses import HelloResponse

router = APIRouter(tags=["hello"])


@router.get(
    "/hello",
    response_model=HelloResponse,
    status_code=200,
    summary="Get hello message",
    description="Returns a simple greeting message.",
    response_description="Greeting message response"
)
async def get_hello() -> HelloResponse:
    """Return a Hello, World! greeting message.
    
    Returns:
        HelloResponse: Response object containing the greeting message.
    
    Example:
        >>> response = await get_hello()
        >>> response.message
        'Hello, World!'
    """
    return HelloResponse(message="Hello, World!")
