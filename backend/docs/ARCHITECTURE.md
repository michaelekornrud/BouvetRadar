# Architecture Documentation

## Overview

BouvetRadar Backend follows a **three-layer architecture** pattern that separates concerns and promotes maintainability, testability, and scalability.

## Architecture Layers

```
┌─────────────────────────────────────────────┐
│           API Layer (Flask Blueprints)      │
│  - HTTP Request/Response handling           │
│  - Input validation & serialization         │
│  - Error handling & status codes            │
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
```

---

## Layer Descriptions

### 1. API Layer (`src/api/`)

**Purpose:** Handle HTTP communication with frontend clients

**Responsibilities:**
- Accept and validate HTTP requests
- Call appropriate service layer methods
- Format responses as JSON
- Handle errors and return appropriate HTTP status codes
- Apply CORS headers

**Components:**
- `cpv_api.py` - CPV code endpoints
- `doffin_api.py` - Doffin search endpoints
- `nuts_api.py` - NUTS geographical codes
- `styrk_api.py` - STYRK occupation codes

**Example Flow:**
```python
@cpv_bp.route('/codes', methods=['GET'])
def get_all_codes():
    # 1. Extract request parameters
    search = request.args.get('search')
    
    # 2. Call service layer
    service = CPVService()
    codes = service.search_descriptions(search)
    
    # 3. Format and return response
    return jsonify({
        "success": True,
        "data": codes
    })
```

### 2. Service Layer (`src/service/`)

**Purpose:** Implement business logic and data transformation

**Responsibilities:**
- Process and transform data
- Implement business rules
- Aggregate data from multiple sources
- Cache data when appropriate
- Coordinate between multiple clients

**Components:**
- `cpv_service.py` - CPV code processing and search
- `doffin_service.py` - Doffin data transformation and filtering
- `ssb_service.py` - SSB data processing (NUTS & STYRK)

**Key Design Patterns:**
- **Service Classes:** Encapsulate related business logic
- **Static Methods:** For stateless operations
- **Dependency Injection:** Services receive client instances
- **Data Transformation:** Convert external API formats to internal models

**Example:**
```python
class DoffinService:
    def __init__(self):
        self.client = DoffinClient(api_key)
        self.ssb_service = SSBService()
    
    def search_notices(self, location_ids):
        # Transform location names to codes
        codes = self._process_location_ids(location_ids)
        
        # Call external API
        raw_data = self.client.search({"location": codes})
        
        # Transform results
        return self._transform_results(raw_data)
```

### 3. Client Layer (`src/clients/`)

**Purpose:** Handle communication with external APIs

**Responsibilities:**
- Make HTTP requests to external services
- Handle authentication (API keys, headers)
- Manage connection errors and timeouts
- Return raw data without transformation

**Components:**
- `doffin_client.py` - Doffin API HTTP client
- `ssb_client.py` - SSB API HTTP client

**Design Principles:**
- **Thin Clients:** Minimal logic, just HTTP communication
- **Error Propagation:** Let service layer handle errors
- **Configurable:** Accept API keys and base URLs
- **Reusable:** Can be used by multiple services

**Example:**
```python
class DoffinClient:
    BASE_URL = "https://api.doffin.no/public/v2/"
    
    def __init__(self, api_key: str):
        self.headers = {"Ocp-Apim-Subscription-Key": api_key}
    
    def search(self, params: dict) -> dict:
        response = requests.get(
            f"{self.BASE_URL}/search",
            headers=self.headers,
            params=params
        )
        response.raise_for_status()
        return response.json()
```

---

## Data Flow

### Request Flow (Top-Down)
```
1. Client HTTP Request
   ↓
2. Flask Blueprint (API Layer)
   ↓
3. Service Method (Business Logic)
   ↓
4. Client Method (External API Call)
   ↓
5. External API (Doffin/SSB)
```

### Response Flow (Bottom-Up)
```
1. External API Response
   ↓
2. Client returns raw data
   ↓
3. Service transforms/processes data
   ↓
4. API layer formats as JSON
   ↓
5. HTTP Response to client
```

---

## Component Interactions

### Example: Searching Doffin Notices

```
┌──────────┐      ┌──────────────┐      ┌────────────────┐      ┌──────────┐
│ Frontend │─────>│ doffin_api.py│─────>│doffin_service  │─────>│doffin_   │
│          │      │              │      │     .py        │      │client.py │
└──────────┘      └──────────────┘      └────────────────┘      └──────────┘
                                                │                       │
                                                │                       ▼
                                                │                 ┌──────────┐
                                                │                 │  Doffin  │
                                                │                 │   API    │
                                                │                 └──────────┘
                                                ▼
                                         ┌────────────────┐
                                         │ssb_service.py  │
                                         │(for location   │
                                         │ lookup)        │
                                         └────────────────┘
                                                │
                                                ▼
                                         ┌────────────────┐
                                         │ ssb_client.py  │
                                         └────────────────┘
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

### Global Error Handlers
```python
@app.errorhandler(404)
def not_found(error):
    return jsonify({"success": False, "error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"success": False, "error": "Internal server error"}), 500
```

### Endpoint-Level Error Handling
```python
try:
    # Business logic
    result = service.do_something()
    return jsonify({"success": True, "data": result})
except ValueError as e:
    return jsonify({"success": False, "error": str(e)}), 400
except Exception as e:
    return jsonify({"success": False, "error": str(e)}), 500
```

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
