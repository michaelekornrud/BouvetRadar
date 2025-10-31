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
- 🧪 **Tested** - Includes test suite with pytest

## Technology Stack

- **Python 3.13+**
- **Flask** - Web framework
- **Flask-CORS** - Cross-origin resource sharing support
- **Pandas** - Data manipulation and analysis
- **Requests** - HTTP library for API clients
- **aiohttp** - Asynchronous HTTP client
- **pytest** - Testing framework
- **uv** - Package management

## Project Structure

```
backend/
├── main.py                 # Application entry point
├── pyproject.toml         # Project dependencies and configuration
├── pytest.ini             # Pytest configuration
├── README.md              # This file
├── src/
│   ├── api/               # API endpoints (Flask blueprints)
│   │   ├── cpv_api.py    # CPV code endpoints
│   │   ├── doffin_api.py # Doffin search endpoints
│   │   ├── nuts_api.py   # NUTS geographical codes
│   │   └── styrk_api.py  # STYRK occupation codes
│   ├── clients/           # HTTP clients for external APIs
│   │   ├── doffin_client.py  # Doffin API client
│   │   └── ssb_client.py     # SSB API client
│   └── service/           # Business logic layer
│       ├── cpv_service.py    # CPV code processing
│       ├── doffin_service.py # Doffin data transformation
│       └── ssb_service.py    # SSB data processing
└── tests/                 # Test suite
    └── test_requests/     # HTTP request tests
```

## Getting Started

### Prerequisites

- Python 3.13 or higher
- `uv` package manager (recommended) or `pip`
- Doffin API key (obtain from [Doffin API Portal](https://api.doffin.no))

### Installation

1. **Clone the repository**
   ```bash
   cd backend
   ```

2. **Install dependencies**
   
   Using `uv`:
   ```bash
   uv sync
   ```
   
   Or using `pip`:
   ```bash
   pip install -e .
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the backend directory:
   ```bash
   DOFFIN_API_KEY=your_api_key_here
   ```

### Running the Application

#### Development Mode

```bash
python main.py
```

The API will be available at `http://localhost:8080`

#### Production Mode

For production deployment, use a WSGI server like Gunicorn:

```bash
gunicorn -w 4 -b 0.0.0.0:8080 "main:create_app()"
```

### Running Tests

```bash
pytest
```

Run with coverage:
```bash
pytest --cov=src tests/
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

### Doffin
- `GET /api/doffin/search` - Search procurement notices

### NUTS (Geographical Codes)
- `GET /api/nuts/codes/level/<level>` - Get hierarchical NUTS structure

### STYRK (Occupation Codes)
- `GET /api/styrk/codes/level/<level>` - Get hierarchical STYRK structure

For detailed API documentation, see [docs/API.md](docs/API.md)

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DOFFIN_API_KEY` | API key for Doffin service | Yes |

### Application Settings

- **Host**: `0.0.0.0` (all interfaces)
- **Port**: `8080`
- **Debug Mode**: Enabled in development
- **CORS**: Enabled for frontend integration

## Architecture

The application follows a layered architecture pattern:

1. **API Layer** (`src/api/`) - Flask blueprints handling HTTP requests/responses
2. **Service Layer** (`src/service/`) - Business logic and data transformation
3. **Client Layer** (`src/clients/`) - External API communication

For detailed architecture documentation, see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

## Development

### Code Style

- Follow PEP 8 guidelines
- Use type hints for function signatures
- Document all public functions and classes
- Keep functions focused and testable

### Adding New Endpoints

1. Create a new API blueprint in `src/api/`
2. Implement business logic in `src/service/`
3. Add external API clients in `src/clients/` if needed
4. Register the blueprint in `main.py`
5. Write tests in `tests/`

### Testing

Tests are located in the `tests/` directory. The project uses pytest with fixtures for mocking external dependencies.

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

## Changelog

### Version 0.1.0 (Current)
- Initial release
- CPV code management
- Doffin search integration
- NUTS and STYRK code hierarchies
- Basic test coverage
