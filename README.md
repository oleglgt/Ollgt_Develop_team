# Hello World API

A simple REST API built with FastAPI that returns a "Hello, World!" message. This project demonstrates the basic setup of a FastAPI application with proper project structure, dependency management, and testing.

## Features

- ✅ RESTful API with FastAPI
- ✅ GET `/hello` endpoint returning a greeting message
- ✅ Pydantic models for request/response validation
- ✅ Automatic interactive API documentation (Swagger UI)
- ✅ Type hints and comprehensive docstrings
- ✅ Unit tests with pytest
- ✅ CORS middleware enabled
- ✅ PEP 8 compliant code

## Requirements

- Python 3.11 or higher
- pip (Python package installer)

## Installation

1. **Clone the repository** (or navigate to the project directory)

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - On Linux/macOS:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Using Uvicorn directly:
```bash
uvicorn src.main:app --reload
```

### Using Python:
```bash
python -m src.main
```

The API will be available at `http://localhost:8000`

### Application Configuration:
- **Host**: 0.0.0.0 (all interfaces)
- **Port**: 8000
- **Reload**: Enabled (development mode)

## API Documentation

Once the application is running, you can access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## API Endpoints

### Root Endpoint
- **URL**: `/`
- **Method**: `GET`
- **Description**: Returns API information
- **Response**:
  ```json
  {
    "name": "Hello World API",
    "version": "1.0.0",
    "docs": "/docs"
  }
  ```

### Hello Endpoint
- **URL**: `/hello`
- **Method**: `GET`
- **Description**: Returns a greeting message
- **Response**:
  ```json
  {
    "message": "Hello, World!"
  }
  ```

### Example cURL Request:
```bash
curl -X GET "http://localhost:8000/hello"
```

### Example Response:
```json
{
  "message": "Hello, World!"
}
```

## Running Tests

Run all tests with pytest:
```bash
pytest
```

Run tests with verbose output:
```bash
pytest -v
```

Run tests with coverage report:
```bash
pytest --cov=src --cov-report=html
```

## Project Structure

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

## Development

### Code Quality Standards
- All code follows PEP 8 style guide
- Type hints on all function signatures
- Docstrings on all public functions and classes
- Error handling with specific exceptions
- Meaningful variable and function names

### Adding New Endpoints
1. Create a new route file in `src/api/routes/`
2. Define response models in `src/models/responses.py`
3. Include the router in `src/main.py`
4. Add tests in `tests/`

## Dependencies

- **fastapi**: Modern, fast web framework for building APIs
- **uvicorn**: ASGI server for running FastAPI applications
- **pydantic**: Data validation using Python type hints
- **pytest**: Testing framework
- **httpx**: HTTP client for testing

## License

This project is open source and available under the MIT License.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests to ensure everything passes
5. Submit a pull request

## Support

For issues, questions, or contributions, please refer to the project's issue tracker.

---

**Version**: 1.0.0  
**Python**: 3.11+  
**Framework**: FastAPI
