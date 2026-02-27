"""Tests for hello endpoint."""

from fastapi.testclient import TestClient


def test_hello_endpoint_success(client: TestClient) -> None:
    """Test that the hello endpoint returns 200 OK.
    
    Args:
        client: FastAPI test client fixture.
    """
    response = client.get("/hello")
    assert response.status_code == 200


def test_hello_endpoint_response_structure(client: TestClient) -> None:
    """Test that the response has the correct structure.
    
    Args:
        client: FastAPI test client fixture.
    """
    response = client.get("/hello")
    data = response.json()
    
    assert "message" in data
    assert isinstance(data["message"], str)


def test_hello_endpoint_response_content(client: TestClient) -> None:
    """Test that the response contains the correct message.
    
    Args:
        client: FastAPI test client fixture.
    """
    response = client.get("/hello")
    data = response.json()
    
    assert data["message"] == "Hello, World!"


def test_hello_endpoint_content_type(client: TestClient) -> None:
    """Test that the response has the correct content type.
    
    Args:
        client: FastAPI test client fixture.
    """
    response = client.get("/hello")
    
    assert response.headers["content-type"] == "application/json"


def test_hello_endpoint_response_schema(client: TestClient) -> None:
    """Test that the response validates against the expected schema.
    
    Args:
        client: FastAPI test client fixture.
    """
    response = client.get("/hello")
    data = response.json()
    
    # Check that only expected fields are present
    assert set(data.keys()) == {"message"}
    
    # Validate field types
    assert isinstance(data["message"], str)
    assert len(data["message"]) > 0
