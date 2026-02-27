"""Tests for the hello endpoint.

This module contains tests for the GET /hello endpoint,
verifying response status, structure, and content.
"""

from fastapi.testclient import TestClient


def test_hello_endpoint_success(client: TestClient) -> None:
    """Test that the hello endpoint returns 200 OK.
    
    Args:
        client: FastAPI test client fixture.
    """
    response = client.get("/hello")
    assert response.status_code == 200


def test_hello_endpoint_response_structure(client: TestClient) -> None:
    """Test that the hello endpoint returns correct JSON structure.
    
    Args:
        client: FastAPI test client fixture.
    """
    response = client.get("/hello")
    json_data = response.json()
    
    # Verify response has 'message' key
    assert "message" in json_data
    assert isinstance(json_data["message"], str)


def test_hello_endpoint_message_content(client: TestClient) -> None:
    """Test that the hello endpoint returns the correct message.
    
    Args:
        client: FastAPI test client fixture.
    """
    response = client.get("/hello")
    json_data = response.json()
    
    # Verify message content
    assert json_data["message"] == "Hello, World!"


def test_hello_endpoint_content_type(client: TestClient) -> None:
    """Test that the hello endpoint returns correct Content-Type header.
    
    Args:
        client: FastAPI test client fixture.
    """
    response = client.get("/hello")
    
    # Verify Content-Type is application/json
    assert response.headers["content-type"] == "application/json"


def test_hello_endpoint_response_schema(client: TestClient) -> None:
    """Test that the hello endpoint response conforms to HelloResponse model.
    
    Args:
        client: FastAPI test client fixture.
    """
    response = client.get("/hello")
    json_data = response.json()
    
    # Verify only expected fields are present
    assert set(json_data.keys()) == {"message"}
    
    # Verify message is non-empty string
    assert len(json_data["message"]) > 0
