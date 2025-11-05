# Architecture Documentation

## Overview

BouvetRadar Backend follows a **four-layer architecture** pattern that separates concerns and promotes maintainability, testability, and scalability.

## Architecture Layers

```
┌─────────────────────────────────────────────┐
│           API Layer (Flask Blueprints)      │
│  - HTTP Request/Response handling           │
│  - Route definitions & URL prefixes         │
│  - Delegates to validation & service        │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│           Validation Layer                  │
│  - Input validation & type checking         │
│  - Request parameter sanitization           │
│  - Raises ValidationError on failures       │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│           Service Layer                     │
│  - Business logic                           │
│  - Data transformation                      │
│  - Aggregation & processing                 │
└─────────────────┬───────────────────────────┘
                  │
┌─────────────────▼───────────────────────────┐
│           Client Layer                      │
│  - External API communication               │
│  - HTTP requests to Doffin & SSB            │
│  - Raw data fetching                        │
└─────────────────────────────────────────────┘
        │
        │  (Exceptions propagate back up)
        │
┌───────▼─────────────────────────────────────┐
│           Exception Hierarchy               │
│  - Centralized error codes                  │
│  - Structured error responses               │
│  - Global exception handlers                │
└─────────────────────────────────────────────┘
```

---

## Layer Descriptions

### 1. API Layer (`src/api/`)

**Purpose:** Handle HTTP communication with frontend clients

**Responsibilities:**
- Accept HTTP requests via Flask Blueprints
- Delegate validation to validation layer
- Call appropriate service layer methods
- Format responses as JSON with consistent structure
- Handle blueprint-specific error handlers
- Apply CORS headers (configured in main.py)

**Components:**
- `cpv_api.py` - CPV code endpoints (`/api/cpv/*`)
- `doffin_api.py` - Doffin search endpoints (`/api/doffin/*`)
- `nuts_api.py` - NUTS geographical codes (`/api/nuts/*`)
- `styrk_api.py` - STYRK occupation codes (`/api/styrk/*`)

**Example Flow:**
```python
@doffin_bp.route('/search', methods=['GET'])
def search_notices():
    # 1. Validate request parameters
    params = DoffinSearchParams.from_request_args(request.args)
    
    # 2. Call service layer
    service = DoffinService()
    results = service.search_notices(params)
    
    # 3. Format and return response
    return jsonify({
        "success": True,
        "data": results
    })

# Blueprint-specific error handlers
@doffin_bp.errorhandler(ValidationError)
def handle_validation_error(e):
    return jsonify(e.to_dict()), e.status_code
```

### 2. Validation Layer (`src/validation/`)

**Purpose:** Validate and sanitize incoming request parameters

**Responsibilities:**
- Type checking and conversion
- Parameter range validation
- Input sanitization
- Raise structured validation exceptions

**Components:**
- `doffin_validators.py` - Validation for Doffin search parameters
- `ssb_validators.py` - Validation for SSB endpoints

**Key Features:**
- **Dataclass-based validators:** Use `@dataclass` for parameter grouping
- **Factory methods:** `from_request_args()` creates validated instances
- **Explicit error messages:** Validation errors include field names and received values
- **Type safety:** Converts string inputs to appropriate types (int, list, etc.)

**Example:**
```python
@dataclass
class DoffinSearchParams:
    search_str: str | None = None
    cpv_codes: list[str] | None = None
    page: int = 1
    hits_per_page: int = 100
    
    @classmethod
    def from_request_args(cls, args) -> 'DoffinSearchParams':
        return cls(
            search_str=validate_search_str(args.get('search')),
            cpv_codes=validate_cpv_codes(args.getlist('cpvCode')),
            page=validate_page(args.get('page', '1')),
            hits_per_page=validate_hits_per_page(args.get('hitsPerPage', '100'))
        )

def validate_page(page_str: str) -> int:
    try:
        page = int(page_str)
        if page < 1:
            raise ValidationError("Page must be >= 1", field="page", value=page_str)
        return page
    except ValueError:
        raise InvalidParameterTypeError("page", page_str, "integer")
```

### 3. Service Layer (`src/service/`)

**Purpose:** Implement business logic and data transformation

**Responsibilities:**
- Process and transform data
- Implement business rules
- Aggregate data from multiple sources
- Cache data when appropriate
- Coordinate between multiple clients
- Raise appropriate exceptions for error conditions

**Components:**
- `cpv_service.py` - CPV code processing and search
- `doffin_service.py` - Doffin data transformation and filtering
- `ssb_service.py` - SSB data processing (NUTS & STYRK)

**Key Design Patterns:**
- **Service Classes:** Encapsulate related business logic
- **Static Methods:** For stateless operations
- **Dependency Injection:** Services receive client instances
- **Data Transformation:** Convert external API formats to internal models
- **Exception Propagation:** Let exceptions bubble up with context

**Example:**
```python
class DoffinService:
    def __init__(self):
        self.client = DoffinClient(api_key)
        self.ssb_service = SSBService()
    
    def search_notices(self, params: DoffinSearchParams):
        # Transform location names to codes
        codes = self._process_location_ids(location_ids)
        
        # Call external API
        raw_data = self.client.search({"location": codes})
        
        # Transform results
        return self._transform_results(raw_data)
```

### 4. Client Layer (`src/clients/`)

**Purpose:** Handle communication with external APIs

**Responsibilities:**
- Make HTTP requests to external services
- Handle authentication (API keys, headers)
- Manage connection errors and timeouts
- Raise ExternalAPIError on failures
- Return raw data without transformation

**Components:**
- `doffin_client.py` - Doffin API HTTP client
- `ssb_client.py` - SSB API HTTP client

**Design Principles:**
- **Thin Clients:** Minimal logic, just HTTP communication
- **Error Wrapping:** Convert HTTP errors to custom exceptions
- **Configurable:** Accept API keys and base URLs
- **Reusable:** Can be used by multiple services

**Example:**
```python
class DoffinClient:
    BASE_URL = "https://api.doffin.no/public/v2/"
    
    def __init__(self, api_key: str):
        self.headers = {"Ocp-Apim-Subscription-Key": api_key}
    
    def search(self, params: dict) -> dict:
        try:
            response = requests.get(
                f"{self.BASE_URL}/search",
                headers=self.headers,
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.Timeout as e:
            raise APITimeoutError("Doffin", timeout=30, original_error=e)
        except requests.RequestException as e:
            raise ExternalAPIError("Search failed", "Doffin", original_error=e)
```

### 5. Exception Hierarchy (`exceptions/`)

**Purpose:** Provide structured, centralized error handling

**Components:**
- `bouvet_radar_exception.py` - Base exception class with status codes
- `error_codes.py` - Enum of all error codes (1000-5999)
- `validation_exceptions.py` - Input validation errors (400 status)
- `external_api_exceptions.py` - External service errors (502 status)
- `internal_api_exceptions.py` - Internal server errors (500 status)
- `resource_exceptions.py` - Resource not found errors (404 status)
- `processing_exceptions.py` - Data processing errors

**Error Code Ranges:**
- **1000-1999:** Validation errors (INVALID_INPUT, MISSING_PARAMETER, etc.)
- **2000-2999:** Internal API errors (INTERNAL_SERVER_ERROR, DATABASE_ERROR, etc.)
- **3000-3999:** External API errors (API_TIMEOUT, DOFFIN_API_ERROR, SSB_API_ERROR)
- **4000-4999:** Processing errors (DATA_PROCESSING_ERROR, TRANSFORMATION_ERROR)
- **5000-5999:** Resource errors (RESOURCE_NOT_FOUND, CPV_CODE_NOT_FOUND, etc.)

**Key Features:**
- **Consistent structure:** All exceptions extend BouvetRadarException
- **Status codes:** HTTP status code included in exception
- **Error codes:** Machine-readable error codes for frontend handling
- **Details dict:** Additional context (field names, values, services)
- **to_dict() method:** Converts to JSON-serializable format

**Example:**
```python
class BouvetRadarException(Exception):
    """Base exception for all BouvetRadar errors."""
    
    def __init__(
        self, 
        message: str,
        status_code: int = 500,
        error_code: ErrorCodes | None = None,
        details: dict | None = None
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)
    
    def to_dict(self) -> dict:
        result = {"success": False, "error": self.message}
        if self.error_code:
            result["error_code"] = self.error_code.value
            result["error_name"] = self.error_code.name
        if self.details:
            result["details"] = self.details
        return result

class CPVCodeNotFoundError(BouvetRadarException):
    """Raised when a CPV code is not found."""
    def __init__(self, code: int):
        super().__init__(
            f"CPV code {code} not found",
            status_code=404,
            error_code=ErrorCodes.CPV_CODE_NOT_FOUND,
            details={"code": code}
        )
```

**Global Error Handler:**
```python
# In main.py
@app.errorhandler(BouvetRadarException)
def handle_bouvet_radar_exception(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
```

---

## Data Flow

### Successful Request Flow (Top-Down)
```
1. Client HTTP Request
   ↓
2. Flask Blueprint (API Layer)
   ↓
3. Validation Layer (validate & sanitize parameters)
   ↓
4. Service Method (Business Logic)
   ↓
5. Client Method (External API Call)
   ↓
6. External API (Doffin/SSB)
```

### Successful Response Flow (Bottom-Up)
```
1. External API Response
   ↓
2. Client returns raw data
   ↓
3. Service transforms/processes data
   ↓
4. API layer formats as JSON
   ↓
5. HTTP Response to client (200 OK)
```

### Error Flow (Exception Handling)
```
1. Error occurs at any layer (validation, service, client)
   ↓
2. Appropriate custom exception is raised
   ↓
3. Exception propagates up through layers
   ↓
4. Blueprint error handler OR global error handler catches it
   ↓
5. Exception.to_dict() converts to JSON
   ↓
6. HTTP Response with appropriate status code (400, 404, 500, 502)
```

---

## Component Interactions

### Example: Searching Doffin Notices with Validation

```
┌──────────┐      ┌──────────────┐      ┌──────────────────┐
│ Frontend │─────>│ doffin_api.py│─────>│ DoffinSearch     │
│          │      │              │      │ Params.from_     │
└──────────┘      └──────────────┘      │ request_args()   │
                                        └─────────┬────────┘
                                         (validated params)
                                                  │ 
                                                  ▼
                                        ┌────────────────┐
                                        │doffin_service  │
                                        │     .py        │
                                        └────────┬───────┘
                                                 │
                             ┌───────────────────┴───────────────────┐
                             ▼                                       ▼
                      ┌──────────┐                            ┌─────────────┐
                      │doffin_   │                            │ssb_service  │
                      │client.py │                            │   .py       │
                      └────┬─────┘                            └──────┬──────┘
                           │                                         │
                           ▼                                         ▼
                     ┌──────────┐                            ┌─────────────┐
                     │  Doffin  │                            │ ssb_client  │
                     │   API    │                            │    .py      │
                     └──────────┘                            └──────┬──────┘
                                                                    │
                                                                    ▼
                                                             ┌─────────────┐
                                                             │  SSB API    │
                                                             └─────────────┘
```

### Error Propagation Example

```
┌──────────────┐     ┌─────────────────┐     ┌──────────────────┐
│ External API │────>│ Client Layer    │────>│ Service Layer    │
│ (Timeout)    │     │ (raises API     │     │ (propagates)     │
└──────────────┘     │  TimeoutError)  │     └──────────────────┘
                     └─────────────────┘              │
                                                      ▼
                     ┌─────────────────┐     ┌──────────────────┐
                     │ Error Handler   │<────│ API Layer        │
                     │ (formats JSON)  │     │ (catches error)  │
                     └─────────────────┘     └──────────────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │ Frontend        │
                     │ (displays error)│
                     └─────────────────┘
```

---

## Design Patterns

### 1. Application Factory Pattern
The `create_app()` function in `main.py` creates and configures the Flask application:
```python
def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(cpv_bp)
    app.register_blueprint(nuts_bp)
    # ...
    
    return app
```

**Benefits:**
- Easier testing with different configurations
- Support for multiple app instances
- Cleaner initialization

### 2. Blueprint Pattern
Each API module is a Flask Blueprint:
```python
cpv_bp = Blueprint('cpv', __name__, url_prefix='/api/cpv')
```

**Benefits:**
- Modular route organization
- URL prefix management
- Independent testing

### 3. Service Pattern
Business logic is encapsulated in service classes:
```python
class CPVService:
    @staticmethod
    def get_description(code: int) -> str | None:
        return CPV_CODES.get(code)
```

**Benefits:**
- Separation of concerns
- Reusable business logic
- Easier unit testing

### 4. Repository Pattern (Implicit)
SSB services act as repositories for external data:
```python
class NUTSService:
    def __init__(self):
        self._ssb_service = SSBService(version=2482)
    
    def get_municipalities(self, county_code: str):
        return self._ssb_service.get_children(county_code)
```

### 5. Exception Hierarchy Pattern
Custom exceptions provide structured error handling:
```python
# Base exception
class BouvetRadarException(Exception):
    def __init__(self, message, status_code, error_code, details):
        # ...
    
    def to_dict(self):
        return {"success": False, "error": self.message, ...}

# Specific exceptions inherit from base
class ValidationError(BouvetRadarException):
    def __init__(self, message, field=None, value=None):
        super().__init__(message, status_code=400, error_code=ErrorCodes.INVALID_INPUT, ...)
```

**Benefits:**
- Consistent error structure across the application
- Separation of error types with appropriate HTTP status codes
- Machine-readable error codes for frontend handling
- Detailed error context without exposing sensitive information

### 6. Dataclass Validator Pattern
Validators use dataclasses for type-safe parameter grouping:
```python
@dataclass
class DoffinSearchParams:
    search_str: str | None = None
    cpv_codes: list[str] | None = None
    page: int = 1
    
    @classmethod
    def from_request_args(cls, args) -> 'DoffinSearchParams':
        # Validates and converts all parameters
        return cls(...)
```

**Benefits:**
- Type safety with Python 3.10+ type hints
- Centralized validation logic
- Immutable parameter objects
- Clear validation error messages

---

## Data Models

### CPV Codes
- Stored as dictionary: `{code: int, description: str}`
- Hierarchical structure based on code prefixes
- Main categories defined as Enum

### NUTS Codes (Geographical)
- Loaded from SSB API into Pandas DataFrame
- Hierarchical: Regions → Counties → Municipalities
- Levels: 1 (Region), 2 (County), 3 (Municipality)

### STYRK Codes (Occupations)
- Loaded from SSB API into Pandas DataFrame
- Hierarchical: Major Groups → Minor Groups → Unit Groups → Occupations
- Levels: 1-4

### Doffin Notices
- Raw JSON from Doffin API
- Transformation pending frontend requirements

---

## Configuration Management

### Environment Variables
Managed via `python-dotenv`:
```python
load_dotenv()
api_key = os.getenv("DOFFIN_API_KEY")
```

### Application Configuration
- Host: `0.0.0.0` (all interfaces)
- Port: `8080`
- Debug mode: Controlled via `app.run(debug=True)`

---

## Error Handling

The application uses a comprehensive custom exception hierarchy for structured error handling.

### Global Error Handlers (main.py)
```python
@app.errorhandler(BouvetRadarException)
def handle_bouvet_radar_exception(error):
    """Catches all custom exceptions and formats them."""
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.errorhandler(404)
def not_found(error):
    return jsonify({"success": False, "error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"success": False, "error": "Internal server error"}), 500
```

### Blueprint-Level Error Handlers
Each blueprint can define specific handlers for its exceptions:
```python
# In doffin_api.py
@doffin_bp.errorhandler(ValidationError)
def handle_validation_error(e):
    return jsonify(e.to_dict()), e.status_code

@doffin_bp.errorhandler(ExternalAPIError)
def handle_external_api_error(e):
    # Could add logging here
    return jsonify(e.to_dict()), e.status_code
```

### Exception Response Format
All custom exceptions produce consistent JSON responses:
```json
{
  "success": false,
  "error": "Human-readable error message",
  "error_code": 1000,
  "error_name": "INVALID_INPUT",
  "details": {
    "field": "page",
    "received_value": "abc"
  }
}
```

### Error Code Categories
- **1000-1999**: Validation errors (400 status)
  - INVALID_INPUT, MISSING_PARAMETER, INVALID_PARAMETER_TYPE
- **2000-2999**: Internal errors (500 status)
  - INTERNAL_SERVER_ERROR, DATABASE_ERROR, CONFIGURATION_ERROR
- **3000-3999**: External API errors (502 status)
  - API_TIMEOUT, DOFFIN_API_ERROR, SSB_API_ERROR, NAV_API_ERROR
- **4000-4999**: Processing errors (500 status)
  - DATA_PROCESSING_ERROR, TRANSFORMATION_ERROR, PARSING_ERROR
- **5000-5999**: Resource errors (404 status)
  - RESOURCE_NOT_FOUND, CPV_CODE_NOT_FOUND, NUTS_CODE_NOT_FOUND

---

## Testing Strategy

### Unit Tests
- Mock external API calls
- Test service layer logic
- Validate data transformations

### Integration Tests
- Test API endpoints with mocked services
- Verify request/response formats
- Check error handling

### Test Fixtures
Located in `tests/test_requests/conftest.py`:
- `FakeAiohttpResponse` - Mock async responses
- `FakeAiohttpSession` - Mock async sessions
- `patch_client_session` - Patch aiohttp
- `install_requests` - Mock requests library

---

## Performance Considerations

### Caching
- CPV codes stored in-memory (static data)
- SSB data loaded once per service instance

### Async Support
- Client layer supports both sync (`requests`) and async (`aiohttp`)
- Future enhancement: Async endpoints for concurrent requests

### Database
- Currently no database (in-memory data)
- Future: Consider caching external API responses

---

## Security Considerations

1. **API Key Management**: Doffin API key stored in environment variables
2. **CORS**: Enabled for frontend integration (configure for production)
3. **Input Validation**: Query parameters validated in API layer
4. **Error Messages**: Avoid exposing sensitive information

---

## Future Enhancements

1. **Database Integration**: Cache external API data
2. **Authentication**: Add API key or OAuth for frontend
3. **Rate Limiting**: Implement request throttling
4. **Async Endpoints**: Full async/await support
5. **WebSocket Support**: Real-time data updates
6. **Logging**: Structured logging with log levels
7. **Monitoring**: Health checks, metrics, and alerting
8. **Documentation**: OpenAPI/Swagger specification
