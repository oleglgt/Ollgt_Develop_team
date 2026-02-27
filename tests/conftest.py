"""Pytest configuration and fixtures."""

import pytest
from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture(scope="module")
def client() -> TestClient:
    """Create a test client for the FastAPI application.
    
    Returns:
        TestClient: FastAPI test client instance.
    """
    return TestClient(app)
