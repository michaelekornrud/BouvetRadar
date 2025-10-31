# API Documentation

## Base URL
```
http://localhost:8080/api
```

## Authentication
The Doffin API key is managed server-side via environment variables. No client-side authentication is required for the API endpoints.

---

## Health Check

### GET /health
Check if the API is running and healthy.

**Response:**
```json
{
  "success": true,
  "message": "API is running",
  "version": "1.0.0"
}
```

---

## CPV (Common Procurement Vocabulary) Endpoints

### GET /cpv/categories
Get main CPV categories for high-level visualization.

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "code": 48000000,
      "name": "Software and Information Systems",
      "description": "Programvare og informasjonssystemer"
    }
  ],
  "total": 6
}
```

### GET /cpv/codes
Get all CPV codes with optional filtering.

**Query Parameters:**
- `category` (optional) - Filter by main category code (e.g., 48000000)
- `search` (optional) - Search in code descriptions

**Examples:**
```
GET /cpv/codes?category=48000000
GET /cpv/codes?search=programvare
GET /cpv/codes
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "code": 48000000,
      "description": "Programvare og informasjonssystemer",
      "category": "Software and Information Systems"
    }
  ],
  "total": 85,
  "filters": {
    "category": "48000000",
    "search": null
  }
}
```

### GET /cpv/codes/{code}
Get details for a specific CPV code.

**Parameters:**
- `code` (path) - CPV code as integer

**Example:**
```
GET /cpv/codes/48000000
```

**Response:**
```json
{
  "success": true,
  "data": {
    "code": 48000000,
    "description": "Programvare og informasjonssystemer",
    "category": "Software and Information Systems",
    "related_codes": [
      {
        "code": 48100000,
        "description": "Bransjespesifikk programvare"
      }
    ]
  }
}
```

**Error Response (404):**
```json
{
  "success": false,
  "error": "CPV code not found"
}
```

### GET /cpv/stats
Get statistics about CPV codes for dashboard visualization.

**Response:**
```json
{
  "success": true,
  "data": {
    "total_codes": 85,
    "main_categories": {
      "Software and Information Systems": 45,
      "Data Services": 20
    },
    "top_level_distribution": {
      "48": 45,
      "72": 20
    },
    "category_details": [
      {
        "code": 48000000,
        "name": "Software and Information Systems",
        "description": "Programvare og informasjonssystemer",
        "count": 45
      }
    ]
  }
}
```

---

## Doffin Endpoints

### GET /doffin/search
Search for procurement notices from the Doffin API.

**Query Parameters:**
- `search` (optional) - Free text search string
- `cpvCode` (optional, multiple) - Filter by CPV codes (can be specified multiple times)
- `location` (optional, multiple) - Filter by location (NUTS code or location name)
- `status` (optional, multiple) - Filter by notice status (e.g., "ACTIVE")
- `page` (optional) - Page number (default: 1)
- `hitsPerPage` (optional) - Number of results per page (default: 100)

**Examples:**
```
GET /doffin/search?search=Forsvaret
GET /doffin/search?cpvCode=72000000&cpvCode=48000000
GET /doffin/search?location=NO081&status=ACTIVE
GET /doffin/search?search=software&page=2&hitsPerPage=50
```

**Response:**
```json
{
  "success": true,
  "data": {
    "hits": [
      {
        "id": "2024-12345",
        "title": "Software Development Services",
        "cpvCodes": [48000000],
        "location": "NO081",
        "status": "ACTIVE"
      }
    ],
    "totalHits": 150,
    "page": 1,
    "hitsPerPage": 100
  },
  "elements": 100
}
```

**Error Response (400):**
```json
{
  "success": false,
  "error": "Invalid input: ..."
}
```

---

## NUTS (Geographical Classification) Endpoints

### GET /nuts/codes/level/{level}
Get hierarchical NUTS structure up to a specified level.

**Parameters:**
- `level` (path) - Hierarchy level (1-3)
  - Level 1: Regions
  - Level 2: Counties
  - Level 3: Municipalities

**Examples:**
```
GET /nuts/codes/level/1  # Regions only
GET /nuts/codes/level/2  # Regions with counties
GET /nuts/codes/level/3  # Full hierarchy
```

**Response (Level 1):**
```json
{
  "success": true,
  "structure": [
    {
      "code": "NO01",
      "name": "Oslo og Akershus"
    }
  ],
  "total": 5
}
```

**Response (Level 3):**
```json
{
  "success": true,
  "structure": [
    {
      "code": "NO01",
      "name": "Oslo og Akershus",
      "counties": [
        {
          "code": "NO011",
          "name": "Oslo",
          "municipalities": [
            {
              "code": "NO0301",
              "name": "Oslo"
            }
          ]
        }
      ]
    }
  ],
  "total": 5
}
```

**Error Response (400):**
```json
{
  "success": false,
  "error": "Invalid level specified"
}
```

---

## STYRK (Occupation Classification) Endpoints

### GET /styrk/codes/level/{level}
Get hierarchical STYRK structure up to a specified level.

**Parameters:**
- `level` (path) - Hierarchy level (1-4)
  - Level 1: Major groups (profession categories)
  - Level 2: Minor groups (subgroups)
  - Level 3: Unit groups (roles)
  - Level 4: Specific occupations (titles)

**Examples:**
```
GET /styrk/codes/level/1  # Major groups only
GET /styrk/codes/level/2  # With subgroups
GET /styrk/codes/level/4  # Full hierarchy
```

**Response (Level 2):**
```json
{
  "success": true,
  "structure": [
    {
      "code": "1",
      "name": "Ledere",
      "subgroups": [
        {
          "code": "11",
          "name": "Administrative ledere og politikere"
        }
      ]
    }
  ],
  "total": 10
}
```

**Error Response (400):**
```json
{
  "success": false,
  "error": "Invalid level specified"
}
```

---

## Error Responses

### 404 Not Found
```json
{
  "success": false,
  "error": "Endpoint not found"
}
```

### 500 Internal Server Error
```json
{
  "success": false,
  "error": "Internal server error"
}
```

---

## Rate Limiting
Currently, there are no rate limits imposed by the backend. However, the Doffin API may have its own rate limits.

## CORS
CORS is enabled for all origins to support frontend integration.

## Content Type
All responses are in JSON format with `Content-Type: application/json`.
