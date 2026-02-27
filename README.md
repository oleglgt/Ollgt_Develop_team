# Hello World API

A simple REST API built with FastAPI that provides a hello world endpoint. This project demonstrates best practices for structuring a FastAPI application with proper dependency management, testing, and documentation.

## Features

- ✨ Simple and clean FastAPI application structure
- 📝 Type hints and comprehensive docstrings
- ✅ Full test coverage with pytest
- 🔒 CORS middleware configured
- 📖 Auto-generated OpenAPI documentation
- 🎯 PEP 8 compliant code

## Requirements

- Python 3.11 or higher
- pip (Python package installer)

## Installation

1. **Clone the repository**

```bash
git clone <repository-url>
cd <repository-directory>
```

2. **Create a virtual environment**

```bash
python -m venv venv
```

3. **Activate the virtual environment**

On Linux/macOS:
```bash
source venv/bin/activate
```

On Windows:
```bash
venv\Scripts\activate
```

4. **Install dependencies**

```bash
pip install -r requirements.txt
```

## Usage

### Running the Application

Start the FastAPI application using uvicorn:

```bash
uvicorn src.main:app --reload
```

The API will be available at `http://localhost:8000`

**Options:**
- `--reload`: Enable auto-reload on code changes (development only)
- `--host 0.0.0.0`: Make the server accessible externally
- `--port 8080`: Use a different port

Example with custom port:
```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8080
```

### API Endpoints

#### GET /hello

Returns a simple greeting message.

**Request:**
```bash
curl -X GET "http://localhost:8000/hello"
```

**Response:**
```json
{
  "message": "Hello, World!"
}
```

#### GET /

Root endpoint providing API information.

**Request:**
```bash
curl -X GET "http://localhost:8000/"
```

**Response:**
```json
{
  "name": "Hello World API",
  "version": "0.1.0",
  "docs": "/docs"
}
```

### API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## Running Tests

Execute the test suite using pytest:

```bash
pytest
```

**Run with coverage report:**
```bash
pytest --cov=src --cov-report=html
```

This will generate a coverage report in the `htmlcov/` directory.

**Run specific test file:**
```bash
pytest tests/test_hello.py
```

**Run with verbose output:**
```bash
pytest -v
```

## Project Structure

```
.
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

## Development

### Code Quality Standards

This project follows these standards:
- **PEP 8**: Python code style guide
- **Type Hints**: All functions have type annotations
- **Docstrings**: All public functions and classes are documented
- **Testing**: Minimum 80% test coverage

### Adding New Endpoints

1. Create a new router file in `src/api/routes/`
2. Define response models in `src/models/responses.py`
3. Register the router in `src/main.py`
4. Add tests in `tests/`

Example:
```python
# src/api/routes/new_endpoint.py
from fastapi import APIRouter
from src.models.responses import YourResponse

router = APIRouter(tags=["your-tag"])

@router.get("/your-path")
async def your_endpoint() -> YourResponse:
    return YourResponse(...)
```

## Dependencies

- **fastapi**: Modern, fast web framework for building APIs
- **uvicorn**: ASGI server for running the application
- **pydantic**: Data validation using Python type hints
- **pytest**: Testing framework
- **httpx**: HTTP client for testing

See `requirements.txt` for specific versions.

## License

This project is part of a demonstration and learning exercise.

## Contributing

1. Create a feature branch
2. Make your changes
3. Ensure tests pass: `pytest`
4. Submit a pull request

## Support

For issues or questions, please open an issue in the repository.
