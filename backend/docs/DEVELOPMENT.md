# Development Guide

## Overview

This guide provides essential information for developers working on the BouvetRadar Backend. It covers the development environment setup, project structure, coding standards, and common development workflows.

---

## Development Environment Setup

### Prerequisites

The development environment requires:
- **Python 3.13+** - The primary programming language
- **uv package manager** - Fast Python package installer (alternatively, pip can be used)
- **Git** - Version control system
- **Code Editor** - VS Code recommended for Python development
- **Doffin API Key** - Required for accessing procurement data

### Initial Setup Process

Setting up the development environment involves four main steps:

1. **Navigate to the backend directory** from the project root
2. **Install dependencies** using the uv package manager
3. **Configure environment variables** by creating a `.env` file with your Doffin API key
4. **Verify installation** by checking that Flask and other dependencies are properly installed

---

## Project Structure

The backend follows a clear three-layer architecture with well-defined responsibilities. Understanding this structure is essential for effective development.

### Source Code Organization

**API Layer (`src/api/`)** - Flask blueprints that define HTTP endpoints. Each file represents a resource group:
- **cpv_api.py**: Endpoints for CPV code operations (`/api/cpv/*`)
- **doffin_api.py**: Endpoints for Doffin procurement search (`/api/doffin/*`)
- **nuts_api.py**: Endpoints for geographical classifications (`/api/nuts/*`)
- **styrk_api.py**: Endpoints for occupation classifications (`/api/styrk/*`)

**Validation Layer (`src/validation/`)** - Input validation and sanitization:
- **doffin_validators.py**: Validates Doffin search parameters using dataclasses
- **ssb_validators.py**: Validates SSB endpoint parameters

**Service Layer (`src/service/`)** - Business logic and data processing:
- **cpv_service.py**: CPV code utilities and search functionality
- **doffin_service.py**: Doffin data transformation and filtering
- **ssb_service.py**: SSB data processing (contains NUTSService and STYRKService)

**Client Layer (`src/clients/`)** - HTTP clients for external APIs:
- **doffin_client.py**: Communicates with Doffin API
- **ssb_client.py**: Communicates with SSB API

**Exception Hierarchy (`exceptions/`)** - Custom exception system:
- **bouvet_radar_exception.py**: Base exception class with status codes
- **error_codes.py**: Centralized ErrorCodes enum (1000-5999)
- **validation_exceptions.py**: Validation errors (400 status)
- **external_api_exceptions.py**: External service errors (502 status)
- **internal_api_exceptions.py**: Internal errors (500 status)
- **resource_exceptions.py**: Resource not found errors (404 status)
- **processing_exceptions.py**: Data processing errors

**Tests (`tests/`)** - Test suite using pytest:
- **test_requests/**: Tests for HTTP request handling
- **conftest.py**: Shared fixtures and test utilities

---

## Code Style and Standards

### Python Conventions

The project follows PEP 8 style guidelines with specific conventions for maintainability:

**Import Organization:** Imports are grouped in three sections: standard library, third-party packages, and local modules. This makes dependencies clear and improves readability.

**Type Hints:** All function parameters and return values use type hints. This provides better IDE support, catches errors early, and serves as inline documentation.

**Naming Standards:**
- Classes use `PascalCase` (e.g., `CPVService`)
- Functions and methods use `snake_case` (e.g., `get_all_codes`)
- Constants use `UPPER_CASE` (e.g., `CPV_CODES`)
- Private methods prefix with underscore (e.g., `_transform_results`)

**Documentation:** All public functions and classes include docstrings describing their purpose, parameters, and return values.

### Flask Conventions

**Blueprint Organization:** Each resource type has its own blueprint with a URL prefix, keeping routes organized and maintainable.

**Error Handling:** The application uses a custom exception hierarchy. Instead of try-except blocks, raise specific exceptions (ValidationError, ExternalAPIError, etc.) and let error handlers format the response.

**Response Format:** All API responses follow a consistent JSON structure with `success`, `data`, and optional `error`, `error_code`, and `details` fields.

---

## Development Workflows

### Adding New Features

When adding new functionality, follow the layered architecture approach:

**Layer 1 - Exception (if needed):** If you need a new type of error, add it to the appropriate exception module. Define error codes in `error_codes.py` first, then implement the exception class.

**Layer 2 - Client (if needed):** If integrating a new external API, create a client class that handles HTTP communication, authentication, and raises ExternalAPIError on failures.

**Layer 3 - Validation (if needed):** Create validator functions or dataclass validators for request parameters. Use type hints and raise ValidationError or InvalidParameterTypeError for invalid inputs.

**Layer 4 - Service:** Implement business logic in a service class. This layer transforms raw data, applies business rules, coordinates between multiple data sources, and raises appropriate exceptions.

**Layer 5 - API:** Create Flask blueprint endpoints that:
1. Use validators to parse and validate request parameters
2. Call service methods with validated data
3. Format successful responses as JSON
4. Register blueprint-specific error handlers

**Testing:** Write tests for each layer, using mocks for external dependencies. Unit tests cover validation and service logic, while integration tests verify endpoint behavior.

**Registration:** Register new blueprints in `main.py` to make endpoints accessible.

---

## Testing Strategy

### Test Execution

The project uses pytest as the testing framework. Tests can be run in several ways:

- **All tests:** Run the complete test suite to verify all functionality
- **Specific tests:** Run individual test files to focus on particular components
- **With coverage:** Generate coverage reports to identify untested code
- **Verbose mode:** Display detailed test output for debugging

### Test Structure

**Unit Tests:** Focus on individual functions and methods in isolation. These tests verify business logic in service classes without external dependencies.

**Integration Tests:** Test API endpoints and verify the interaction between layers. These tests ensure that requests are properly handled and responses are correctly formatted.

**Mocking:** External API calls are mocked to ensure tests are fast, reliable, and don't depend on external services. The test fixtures in `conftest.py` provide mock implementations of HTTP clients.

### Writing Effective Tests

Tests should follow the Arrange-Act-Assert pattern:
1. **Arrange:** Set up test data and dependencies
2. **Act:** Execute the function or endpoint being tested
3. **Assert:** Verify the results match expectations

Each test should focus on a single behavior and have a descriptive name that clearly indicates what is being tested.

---

## Debugging Techniques

### Interactive Debugging

Python's built-in debugger (pdb) can be inserted at any point in the code to pause execution and inspect variables. This is useful for understanding complex data flows or tracking down unexpected behavior.

VS Code provides an integrated debugger with breakpoints, variable inspection, and step-through execution. A launch configuration can be created to run the Flask application in debug mode.

### Logging

Strategic logging helps track application behavior in development and production:

- **INFO level:** General application flow and important events
- **DEBUG level:** Detailed information for troubleshooting
- **WARNING level:** Potential issues that don't stop execution
- **ERROR level:** Errors that need attention

Logging should be configured in `main.py` with appropriate formatting to include timestamps, log levels, and source information.

---

## Common Development Tasks

### Maintaining CPV Codes

CPV codes are stored as a Python dictionary in `src/service/cpv_service.py`. To add new codes:

1. Add entries to the `CPV_CODES` dictionary
2. For new main categories, update the `CPVMainCategory` enum
3. Update the `get_category_for_code()` method to recognize new prefixes

### Updating Data Source Versions

SSB data versions may change over time. To update:

**NUTS codes:** Modify the version parameter in `NUTSService` initialization (currently version 2482)
**STYRK codes:** Modify the version parameter in `STYRKService` initialization (currently version 33)

Check the SSB KLASS website to find current version numbers.

### Environment Configuration

New configuration values should be added through environment variables:

1. Document the variable in `.env.example`
2. Load it using `python-dotenv` in the service that needs it
3. Provide sensible defaults where appropriate
4. Document the variable in the README

---

## Error Handling Best Practices

### Using the Exception Hierarchy

The application uses a custom exception system for consistent error handling. Instead of returning error tuples or using generic exceptions, raise specific custom exceptions:

**Don't do this:**
```python
def validate_page(page_str: str):
    try:
        page = int(page_str)
        if page < 1:
            return None, "Page must be >= 1"
        return page, None
    except ValueError:
        return None, "Invalid page number"
```

**Do this instead:**
```python
def validate_page(page_str: str) -> int:
    try:
        page = int(page_str)
        if page < 1:
            raise ValidationError("Page must be >= 1", field="page", value=page_str)
        return page
    except ValueError:
        raise InvalidParameterTypeError("page", page_str, "integer")
```

### Exception Categories

**Validation Errors (400):** Use when user input is invalid
```python
from exceptions import ValidationError, InvalidParameterTypeError, MissingParameterError

# Invalid input
raise ValidationError("Search string too long", field="search", value=search_str)

# Wrong type
raise InvalidParameterTypeError("page", "abc", "integer")

# Missing required parameter
raise MissingParameterError("cpvCode")
```

**Resource Errors (404):** Use when requested resource doesn't exist
```python
from exceptions import CPVCodeNotFoundError, NUTSCodeNotFoundError

# Resource not found
raise CPVCodeNotFoundError(48000000)
raise NUTSCodeNotFoundError("NO999")
```

**External API Errors (502):** Use when external service fails
```python
from exceptions import ExternalAPIError, APITimeoutError

# API error
raise ExternalAPIError("Failed to fetch data", "Doffin", original_error=e)

# Timeout
raise APITimeoutError("Doffin", timeout=30, original_error=e)
```

**Internal Errors (500):** Use for unexpected internal issues
```python
from exceptions import InternalServerError, ConfigurationError

# Configuration issue
raise ConfigurationError("DOFFIN_API_KEY not set")

# Unexpected error
raise InternalServerError("Unexpected error processing data", original_error=e)
```

### Error Handler Registration

**Global handlers** in `main.py` catch all custom exceptions:
```python
@app.errorhandler(BouvetRadarException)
def handle_bouvet_radar_exception(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
```

**Blueprint handlers** provide more specific handling:
```python
@cpv_bp.errorhandler(CPVCodeNotFoundError)
def handle_not_found(e):
    # Can add logging, metrics, etc.
    return jsonify(e.to_dict()), e.status_code
```

### Adding New Error Codes

When adding new error types:

1. **Add to ErrorCodes enum** in `error_codes.py`:
```python
class ErrorCodes(Enum):
    # Your new code in appropriate range
    INVALID_DATE_FORMAT = 1003  # Validation error
```

2. **Create exception class** in appropriate module:
```python
class InvalidDateFormatError(BouvetRadarException):
    def __init__(self, date_str: str):
        super().__init__(
            f"Invalid date format: {date_str}",
            status_code=400,
            error_code=ErrorCodes.INVALID_DATE_FORMAT,
            details={"received_value": date_str, "expected_format": "YYYY-MM-DD"}
        )
```

3. **Export from __init__.py** in exceptions module

4. **Document in ARCHITECTURE.md** error codes section

---

## Performance Considerations

### Service Instance Management

Service instances can be created once and reused across requests, or created per-request depending on whether they maintain state. Stateless services benefit from being instantiated once at module level.

### Data Processing Optimization

When working with Pandas DataFrames:
- Use vectorized operations instead of iterating rows
- Filter data efficiently using DataFrame indexing
- Keep DataFrames in memory for frequently accessed data (CPV codes, SSB classifications)

### Response Optimization

For endpoints returning large datasets:
- Implement pagination with `page` and `per_page` parameters
- Cache frequently requested data
- Consider using compression for large responses
- Return only necessary fields in JSON responses

---

## Troubleshooting Common Issues

### Import Errors

**Module not found errors** typically indicate Python path issues. The `pytest.ini` file configures the Python path for tests. Ensure the `pythonpath` setting includes `src`.

### API Authentication Failures

**401 Unauthorized responses** from Doffin indicate API key issues. Verify:
- The `.env` file exists and contains `DOFFIN_API_KEY`
- The API key is valid and not expired
- The key is loaded correctly using `python-dotenv`

### Data Loading Failures

**SSB data not loading** can result from:
- Incorrect version numbers
- Network connectivity issues
- SSB API downtime
- Changes to the SSB API response format

Check the SSB KLASS website to verify the current version numbers and API status.

---

## Version Control Workflow

### Branch Strategy

The project uses a feature branch workflow:
- **Feature branches:** New functionality (`feature/description`)
- **Bug fixes:** Issue corrections (`bugfix/description`)
- **Hotfixes:** Urgent production fixes (`hotfix/description`)

### Commit Guidelines

Commit messages follow conventional commit format with a type prefix:
- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `test:` Test additions or modifications
- `refactor:` Code restructuring without behavior changes

### Pre-Commit Checklist

Before committing code:
1. **Run tests** to ensure no functionality is broken
2. **Check code style** if linting tools are configured
3. **Update documentation** for new features or changed behavior
4. **Review changes** to avoid committing unnecessary files

---

## Development Best Practices

### Code Organization

- Keep functions focused on a single responsibility
- Extract complex logic into helper methods
- Use meaningful variable and function names
- Avoid deep nesting by returning early
- Keep files and functions to a reasonable size

### Error Handling

- Handle expected errors explicitly (ValueError, KeyError, etc.)
- Let unexpected errors propagate to global handlers
- Provide meaningful error messages to API consumers
- Log errors with sufficient context for debugging

### Documentation

- Update API documentation when adding endpoints
- Document complex business logic with comments
- Keep README files current with setup instructions
- Include examples for non-obvious functionality

---

## Useful Resources

### Official Documentation
- **Flask:** Web framework documentation and best practices
- **Pandas:** Data manipulation and analysis guide
- **Pytest:** Testing framework and fixture usage
- **PEP 8:** Python style guide for consistent code formatting
- **Type Hints (PEP 484):** Python type annotation specification

### Project-Specific Documentation
- **ARCHITECTURE.md:** System design and component interactions
- **API.md:** Complete API endpoint reference
- **DATA_SOURCES.md:** External data source details
- **DEPLOYMENT.md:** Production deployment strategies
