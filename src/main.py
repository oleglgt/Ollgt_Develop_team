"""FastAPI application entry point.

This module initializes and configures the FastAPI application,
including route registration and middleware setup.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import hello

# Application metadata
APP_TITLE = "Hello World API"
APP_DESCRIPTION = """
A simple REST API with a Hello World endpoint.

This API demonstrates the basic setup of a FastAPI application with:
- Proper project structure
- Pydantic model validation
- Type hints and documentation
- RESTful endpoint design
"""
APP_VERSION = "0.1.0"

# Initialize FastAPI application
app = FastAPI(
    title=APP_TITLE,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(hello.router)


@app.get("/", tags=["root"])
async def root() -> dict[str, str]:
    """Root endpoint providing API information.
    
    Returns:
        dict: Basic API information including name and version.
    """
    return {
        "name": APP_TITLE,
        "version": APP_VERSION,
        "docs": "/docs"
    }
