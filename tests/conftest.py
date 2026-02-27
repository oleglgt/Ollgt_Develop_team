"""Pytest configuration and fixtures.

This module provides shared test fixtures for the test suite.
"""

import pytest
from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture
def client() -> TestClient:
    """Create a test client for the FastAPI application.
    
    Returns:
        TestClient: A test client instance for making test requests.
    """
    return TestClient(app)
