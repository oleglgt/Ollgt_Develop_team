# Hello World API

## Overview
Create a simple REST API using FastAPI framework with a single endpoint that returns a "Hello, World!" message. This is a foundational service that demonstrates the basic setup of a FastAPI application with proper project structure, dependency management, and testing.

## Technical Requirements
- Python 3.11+
- FastAPI framework (latest stable version)
- Uvicorn ASGI server for running the application
- Pydantic for response model validation
- pytest for testing
- Type hints for all functions
- PEP 8 compliant code
- Proper project structure with configuration management

## API Design

### Endpoint: GET /hello

**Method:** GET  
**Path:** `/hello`  
**Description:** Returns a greeting message

**Request:**
- No parameters required
- No request body

**Response:**
- Status Code: `200 OK`
- Content-Type: `application/json`
- Body:
```json
{
  "message": "Hello, World!"
}
```

**Response Schema:**
```python
{
  "message": str  # Greeting message
}
```

**Example cURL:**
```bash
curl -X GET "http://localhost:8000/hello"
```

## Data Models

### HelloResponse
```python
from pydantic import BaseModel

class HelloResponse(BaseModel):
    """Response model for hello endpoint."""
    message: str
```

## File Structure

```
/
├── src/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       └── hello.py     # Hello endpoint implementation
│   └── models/
│       ├── __init__.py
│       └── responses.py     # Pydantic response models
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Pytest configuration and fixtures
│   └── test_hello.py        # Tests for hello endpoint
├── requirements.txt         # Project dependencies
├── .gitignore              # Git ignore rules
└── README.md               # Project documentation
```

## Implementation Details

### src/main.py
- Initialize FastAPI application
- Include routers from api/routes
- Configure CORS if needed
- Add application metadata (title, version, description)

### src/api/routes/hello.py
- Implement GET /hello endpoint
- Return HelloResponse model
- Include proper docstring and type hints

### src/models/responses.py
- Define HelloResponse Pydantic model
- Add proper docstrings

### tests/test_hello.py
- Test successful response (200 OK)
- Test response structure and content
- Test response content type
- Use FastAPI TestClient for testing

### requirements.txt
```
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.0.0
pytest>=7.4.0
httpx>=0.25.0
```

### README.md
- Project description
- Installation instructions
- How to run the application
- How to run tests
- API documentation link

## Acceptance Criteria

1. **Application starts successfully**: The FastAPI application starts on port 8000 without errors using `uvicorn src.main:app --reload`

2. **Endpoint responds correctly**: GET request to `/hello` returns status code 200 with JSON body `{"message": "Hello, World!"}`

3. **Response format is valid**: Response conforms to HelloResponse Pydantic model and has correct Content-Type header `application/json`

4. **Code quality standards met**: 
   - All code follows PEP 8
   - All functions have type hints
   - All public functions have docstrings
   - No linting errors

5. **Tests pass with coverage**: 
   - All tests in `tests/test_hello.py` pass
   - Test coverage is at least 80%
   - Tests cover: successful response, correct message content, response schema validation

6. **Documentation is complete**: 
   - README.md contains installation and usage instructions
   - FastAPI automatic documentation is accessible at `/docs`
   - All endpoints and models are properly documented

7. **Project structure is correct**: All files are in their designated locations according to the file structure specification

8. **Dependencies are properly specified**: `requirements.txt` contains all necessary dependencies with version constraints
