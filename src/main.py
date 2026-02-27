"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import hello

# Application metadata
app = FastAPI(
    title="Hello World API",
    version="1.0.0",
    description="A simple REST API that returns a Hello, World! message",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(hello.router)


@app.get("/", tags=["root"])
async def root() -> dict[str, str]:
    """Root endpoint returning API information.
    
    Returns:
        dict: API name and version information.
    """
    return {
        "name": "Hello World API",
        "version": "1.0.0",
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
