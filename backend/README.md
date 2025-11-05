# BouvetRadar Backend

A Flask-based REST API service that provides access to Norwegian procurement data, statistical classifications, and business intelligence information.

## Overview

BouvetRadar Backend is a Python-based API service that aggregates and serves data from multiple Norwegian public data sources including:
- **Doffin** - Norwegian public procurement database
- **SSB (Statistics Norway)** - NUTS geographical codes and STYRK occupation classifications
- **CPV Codes** - Common Procurement Vocabulary for categorizing public contracts

## Features

- 🔍 **Procurement Search** - Search and filter Doffin notices by CPV codes, locations, and status
- 🏢 **CPV Code Management** - Browse and search common procurement vocabulary codes
- 📍 **NUTS Codes** - Hierarchical Norwegian geographical classification (regions, counties, municipalities)
- 👔 **STYRK Codes** - Norwegian occupation classification system
- 🚀 **RESTful API** - Clean, documented API endpoints with JSON responses
- ⚡ **Fast & Lightweight** - Built with Flask for optimal performance
- 📝 **Structured Logging** - Rotating file-based logging with configurable levels
- 🛡️ **Error Handling** - Comprehensive exception hierarchy with detailed error responses
- 🧪 **Tested** - Includes test suite with pytest

## Technology Stack

- **Python 3.13+**
- **Flask** - Web framework
- **Flask-CORS** - Cross-origin resource sharing support
- **Pandas** - Data manipulation and analysis
- **Requests** - HTTP library for API clients
- **aiohttp** - Asynchronous HTTP client (async support)
- **python-dotenv** - Environment variable management
- **pytest** - Testing framework
- **pytest-asyncio** - Async testing support
- **uv** - Fast Python package manager

## Project Structure

```
backend/
├── main.py                    # Application entry point and Flask app factory
├── pyproject.toml            # Project dependencies and configuration
├── pytest.ini                # Pytest configuration
├── .env.example              # Environment variable template
├── README.md                 # This file
├── src/
│   ├── api/                  # API endpoints (Flask blueprints)
│   │   ├── cpv_api.py       # CPV code endpoints
│   │   ├── doffin_api.py    # Doffin search endpoints
│   │   ├── nuts_api.py      # NUTS geographical codes
│   │   └── styrk_api.py     # STYRK occupation codes
│   ├── clients/              # HTTP clients for external APIs
│   │   ├── doffin_client.py # Doffin API client
│   │   └── ssb_client.py    # SSB API client
│   ├── service/              # Business logic layer
│   │   ├── cpv_service.py   # CPV code processing
│   │   ├── doffin_service.py # Doffin data transformation
│   │   └── ssb_service.py    # SSB data processing (NUTS & STYRK)
│   ├── validation/           # Input validation logic
│   │   ├── doffin_validators.py # Doffin endpoint validators
│   │   └── ssb_validators.py    # SSB endpoint validators
│   └── utils/                # Utility modules
│       └── logging_config.py # Centralized logging configuration
├── exceptions/               # Custom exception hierarchy
│   ├── bouvet_radar_exception.py # Base exception class
│   ├── error_codes.py           # Error code enumerations
│   ├── external_api_exceptions.py # External API errors
│   ├── internal_api_exceptions.py # Internal server errors
│   ├── processing_exceptions.py   # Data processing errors
│   ├── resource_exceptions.py     # Resource not found errors
│   └── validation_exceptions.py   # Input validation errors
├── logs/                     # Application logs (auto-created, git-ignored)
│   ├── app.log              # General application logs (rotating, 10MB max)
│   └── error.log            # Error-only logs (rotating, 5MB max)
├── tests/                    # Test suite
│   └── test_requests/       # HTTP request tests
└── docs/                     # Documentation
    ├── API.md               # API endpoint documentation
    ├── ARCHITECTURE.md      # System architecture details
    ├── DATA_SOURCES.md      # External data sources documentation
    ├── DEPLOYMENT.md        # Deployment guide
    └── DEVELOPMENT.md       # Development guide
```

## Getting Started

### Prerequisites

- **Python 3.13** or higher
- **uv** package manager (recommended) or **pip**
- **Doffin API key** - Obtain from [Doffin API Portal](https://dof-notices-prod-api.developer.azure-api.net/)

### Installation

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Install dependencies**
   
   Using `uv` (recommended):
   ```bash
   uv sync
   ```
   
   Or using `pip`:
   ```bash
   pip install -e .
   ```

3. **Set up environment variables**
   
   Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your credentials:
   ```bash
   DOFFIN_API_KEY=your_api_key_here
   LOG_LEVEL=INFO  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
   ```
   
   **Note:** The `DATABASE_URL` in `.env.example` is for future use and not currently required.

### Running the Application

#### Development Mode

```bash
uv run python main.py
```

The API will be available at:
- **Local**: `http://localhost:8080`
- **Network**: `http://0.0.0.0:8080`

The development server includes:
- **Auto-reload** on code changes (Werkzeug reloader)
- **Debug mode** with interactive debugger
- **Detailed error pages**
- **Console logging** with timestamps

**Note:** You'll see the application initialize twice - this is normal Flask behavior with the reloader enabled.

#### Production Mode

For production deployment, use a WSGI server like Gunicorn:

```bash
gunicorn -w 4 -b 0.0.0.0:8080 "main:create_app()"
```

**Production considerations:**
- Set `LOG_LEVEL=WARNING` or `LOG_LEVEL=ERROR` in `.env`
- Use a reverse proxy (nginx/Apache) in front of Gunicorn
- Disable Flask debug mode (automatically disabled when using Gunicorn)
- Configure proper log rotation and monitoring
- Set up SSL/TLS certificates

### Running Tests

Run all tests:
```bash
pytest
```

Run with coverage report:
```bash
pytest --cov=src tests/
```

Run specific test file:
```bash
pytest tests/test_requests/test_request_handler.py
```

Run with verbose output:
```bash
pytest -v
```

## API Documentation

The API provides the following main endpoints:

### Health Check
- `GET /api/health` - API health status

### CPV Codes
- `GET /api/cpv/categories` - Get main CPV categories
- `GET /api/cpv/codes` - Get all CPV codes (supports filtering)
- `GET /api/cpv/codes/<code>` - Get specific CPV code details
- `GET /api/cpv/stats` - Get CPV statistics

### Doffin (Procurement Notices)
- `GET /api/doffin/search` - Search procurement notices
  - Query params: `search`, `cpvCode`, `location`, `status`, `page`, `hitsPerPage`

### NUTS (Geographical Codes)
- `GET /api/nuts/codes?level=<level>` - Get hierarchical NUTS structure (levels 1-3)

### STYRK (Occupation Codes)
- `GET /api/styrk/codes?level=<level>` - Get hierarchical STYRK structure (levels 1-4)

For detailed API documentation, see [docs/API.md](docs/API.md)

## Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `DOFFIN_API_KEY` | API key for Doffin service | Yes | - |
| `LOG_LEVEL` | Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL) | No | INFO |
| `DATABASE_URL` | Database connection (future use) | No | - |

### Application Settings

- **Host**: `0.0.0.0` (all interfaces)
- **Port**: `8080`
- **Debug Mode**: Enabled in development (auto-reload, detailed errors)
- **CORS**: Enabled for frontend integration
- **Logging**: 
  - Console output with timestamps and context
  - File logging with rotation (app.log, error.log)
  - Configurable log levels per environment

## Architecture

The application follows a **three-layer architecture** pattern with clear separation of concerns:

1. **API Layer** (`src/api/`) - Flask blueprints handling HTTP requests/responses
   - Request validation using dedicated validators
   - Response formatting (JSON)
   - Error handling and status codes
   - Blueprint registration

2. **Service Layer** (`src/service/`) - Business logic and data transformation
   - Data processing and filtering
   - Business rule enforcement
   - Coordination between multiple data sources
   - SSB data hierarchies (NUTS, STYRK)

3. **Client Layer** (`src/clients/`) - External API communication
   - HTTP requests to Doffin and SSB APIs
   - Authentication handling
   - Raw data fetching
   - Timeout and error management

**Supporting Modules:**
- **Exceptions** (`exceptions/`) - Comprehensive exception hierarchy with error codes
- **Validators** (`src/validation/`) - Input validation logic separated by endpoint
- **Utils** (`src/utils/`) - Shared utilities (logging configuration)

For detailed architecture documentation, see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

## Development

### Code Style

- **Follow PEP 8** guidelines strictly
- **Use type hints** for all function signatures
- **Document** all public functions and classes with docstrings
- **Keep functions focused** on single responsibility
- **Write idiomatic Python** using comprehensions, context managers, and built-ins
- **Prefer explicit over implicit** - clear variable names and logic

### Logging Guidelines

The application uses structured logging with the following levels:
- **DEBUG**: Detailed information for diagnosing issues (development only)
- **INFO**: General informational messages about application flow
- **WARNING**: Warning messages for recoverable issues
- **ERROR**: Error messages with context and tracebacks
- **CRITICAL**: Critical errors requiring immediate attention

**Usage example:**
```python
from src.utils import get_logger

logger = get_logger(__name__)

logger.info("Processing request", extra={"user_id": 123})
logger.error("API call failed", exc_info=True)
```

**Log files location:**
- `logs/app.log` - All INFO+ messages (rotates at 10MB, keeps 10 backups)
- `logs/error.log` - ERROR+ messages only (rotates at 5MB, keeps 10 backups)

### Adding New Endpoints

1. **Create validators** in `src/validation/` for input validation
2. **Create service** in `src/service/` for business logic
3. **Create client** in `src/clients/` if external API needed
4. **Create API blueprint** in `src/api/` for HTTP endpoints
5. **Register blueprint** in `main.py` `create_app()` function
6. **Add logging** at appropriate levels (API → Service → Client)
7. **Write tests** in `tests/` with mocked dependencies
8. **Update documentation** in `docs/API.md`

### Error Handling

The application uses a comprehensive exception hierarchy:
- **ValidationError** - Invalid input (400)
- **NotFoundError** - Resource not found (404)
- **ExternalAPIError** - External service failures (502)
- **InternalServerError** - Unexpected errors (500)

All exceptions inherit from `BouvetRadarException` and include:
- Error codes (from `ErrorCodes` enum)
- Detailed error messages
- Context information (field names, values, etc.)
- Proper HTTP status codes

### Testing

Tests are located in the `tests/` directory and use:
- **pytest** - Testing framework
- **pytest-asyncio** - Async test support
- **Mocked clients** - No real API calls in tests
- **Fixtures** - Reusable test components in `conftest.py`

**Running specific test categories:**
```bash
pytest tests/test_requests/  # Only request handler tests
pytest -k "doffin"           # Tests matching "doffin"
pytest -v --tb=short         # Verbose with short tracebacks
```

## Contributing

1. Create a feature branch
2. Make your changes
3. Write/update tests
4. Ensure all tests pass
5. Submit a pull request

## License

[Add your license information here]

## Support

For issues and questions:
- Create an issue in the project repository
- Contact the development team

## Additional Documentation

- **[API.md](docs/API.md)** - Complete API endpoint reference with examples
- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - System design and component interactions
- **[DATA_SOURCES.md](docs/DATA_SOURCES.md)** - External data source details (Doffin, SSB, CPV)
- **[DEPLOYMENT.md](docs/DEPLOYMENT.md)** - Production deployment strategies
- **[DEVELOPMENT.md](docs/DEVELOPMENT.md)** - Comprehensive development guide

## Changelog

### Version 0.1.0 (Current - November 2025)
- ✅ Initial release
- ✅ CPV code management with search and filtering
- ✅ Doffin search integration with validation
- ✅ NUTS geographical code hierarchies (3 levels)
- ✅ STYRK occupation code hierarchies (4 levels)
- ✅ Structured logging system with file rotation
- ✅ Comprehensive exception hierarchy with error codes
- ✅ Input validation layer
- ✅ Test suite with pytest
- ✅ Complete documentation suite
