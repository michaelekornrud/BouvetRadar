# Data Sources Documentation

## Overview

BouvetRadar Backend integrates data from multiple Norwegian public data sources. This document provides detailed information about each data source, their structure, and how they are used in the application.

---

## 1. Doffin API

### Description
Doffin (Database for Offentlige Innkjøp - Database for Public Procurement) is Norway's official database for public procurement notices. It contains information about all public procurement contracts above certain thresholds.

### API Information
- **Base URL**: `https://api.doffin.no/public/v2/`
- **Authentication**: API key required (Ocp-Apim-Subscription-Key header)
- **Documentation**: [https://api.doffin.no](https://api.doffin.no)
- **Rate Limits**: Subject to API provider limits

### Endpoints Used

#### Search Endpoint
```
GET /search
```

**Parameters:**
- `searchString` - Free text search
- `cpvCode` - CPV code filter (array)
- `location` - NUTS location code (array)
- `status` - Notice status (array: ACTIVE, EXPIRED, etc.)
- `page` - Page number
- `numHitsPerPage` - Results per page

**Response Structure:**
```json
{
  "hits": [
    {
      "id": "string",
      "title": "string",
      "description": "string",
      "cpvCodes": [48000000],
      "location": "NO081",
      "status": "ACTIVE",
      "publishedDate": "2024-01-01",
      "deadline": "2024-02-01",
      "organization": "string"
    }
  ],
  "totalHits": 150,
  "page": 1,
  "hitsPerPage": 100
}
```

### Data Usage in Application

**Client:** `src/clients/doffin_client.py`
- Handles HTTP communication with Doffin API
- Manages authentication headers
- Provides search and download methods

**Service:** `src/service/doffin_service.py`
- Transforms location names to NUTS codes
- Filters and processes search results
- Coordinates with SSB service for location lookups

**API:** `src/api/doffin_api.py`
- Exposes search endpoint to frontend
- Validates query parameters
- Returns formatted JSON responses

### How to Get API Key

1. Visit [Doffin API Portal](https://api.doffin.no)
2. Create an account
3. Subscribe to the API
4. Generate API key
5. Add to `.env` file: `DOFFIN_API_KEY=your_key_here`

---

## 2. SSB (Statistics Norway) API

### Description
Statistics Norway (Statistisk sentralbyrå - SSB) provides official Norwegian statistics through their classification API (KLASS). The API provides hierarchical classification systems including geographical codes (NUTS) and occupation codes (STYRK).

### API Information
- **Base URL**: `https://data.ssb.no/api/klass/v1/`
- **Authentication**: None required (public API)
- **Documentation**: [https://www.ssb.no/klass/](https://www.ssb.no/klass/)
- **Format**: CSV with ISO-8859-1 encoding

### Classifications Used

#### NUTS Codes (Version 2482)
Norwegian geographical classification based on EU NUTS (Nomenclature of Territorial Units for Statistics) standard.

**Hierarchy:**
```
Level 1: Regions (Landsdeler)
  └── Level 2: Counties (Fylker)
      └── Level 3: Municipalities (Kommuner)
```

**Endpoint:**
```
GET /versions/2482
```

**Response Structure (CSV):**
```csv
code;parentCode;level;name
NO01;;1;Oslo og Akershus
NO011;NO01;2;Oslo
NO0301;NO011;3;Oslo
```

**Example Data:**
| Code | Parent Code | Level | Name |
|------|-------------|-------|------|
| NO01 | - | 1 | Oslo og Akershus |
| NO011 | NO01 | 2 | Oslo |
| NO0301 | NO011 | 3 | Oslo |
| NO02 | - | 1 | Hedmark og Oppland |
| NO021 | NO02 | 2 | Hedmark |

**Usage:**
- Filter Doffin searches by geographical location
- Display hierarchical location selectors in frontend
- Convert location names to NUTS codes

#### STYRK Codes (Version 33)
Norwegian Standard Classification of Occupations (Standard for yrkesklassifisering).

**Hierarchy:**
```
Level 1: Major Groups (Hovedgrupper)
  └── Level 2: Minor Groups (Grupper)
      └── Level 3: Unit Groups (Undergrupper)
          └── Level 4: Occupations (Yrker)
```

**Endpoint:**
```
GET /versions/33
```

**Response Structure (CSV):**
```csv
code;parentCode;level;name
1;;1;Ledere
11;1;2;Administrative ledere og politikere
111;11;3;Daglige ledere
1111;111;4;Administrerende direktører
```

**Example Data:**
| Code | Parent Code | Level | Name |
|------|-------------|-------|------|
| 1 | - | 1 | Ledere |
| 11 | 1 | 2 | Administrative ledere og politikere |
| 111 | 11 | 3 | Daglige ledere |
| 1111 | 111 | 4 | Administrerende direktører |

**Usage:**
- Classify job opportunities by occupation type
- Filter procurement notices by relevant occupations
- Business intelligence and market analysis

### Data Usage in Application

**Client:** `src/clients/ssb_client.py`
- Fetches CSV data from SSB API
- Handles ISO-8859-1 encoding
- No authentication required

**Service:** `src/service/ssb_service.py`
Contains three service classes:

1. **SSBService** (Base class)
   - Loads and processes CSV data into Pandas DataFrame
   - Provides lookup by code or name
   - Supports hierarchical queries

2. **NUTSService**
   - Specialized for geographical classifications
   - Methods: `get_regions()`, `get_counties()`, `get_municipalities()`
   - Provides hierarchical structure by level

3. **STYRKService**
   - Specialized for occupation classifications
   - Methods: `get_major_groups()`, `get_minor_groups()`, etc.
   - Provides hierarchical structure by level

**API:**
- `src/api/nuts_api.py` - Exposes NUTS endpoints
- `src/api/styrk_api.py` - Exposes STYRK endpoints

---

## 3. CPV Codes (Internal Data)

### Description
Common Procurement Vocabulary (CPV) is a classification system for public procurement used across the European Union. The CPV codes are maintained internally in the application.

### Data Structure

**Location:** `src/service/cpv_service.py`

**Format:** Python dictionary
```python
CPV_CODES: dict[int, str] = {
    48000000: "Programvare og informasjonssystemer",
    48100000: "Bransjespesifikk programvare",
    # ... more codes
}
```

### Code Categories

The application focuses on IT and consulting-related procurement:

1. **Software and Information Systems (48000000)**
   - Business software
   - Communication software
   - Operating systems
   - Information systems

2. **Telecommunications Services (64000000)**
   - Line rental
   - Telecommunication services

3. **Data Services (72000000)**
   - Software development
   - System consulting
   - Data processing
   - Network operations

4. **Research and Development (73000000)**
   - Research consulting
   - Development consulting

5. **Business Services (79000000)**
   - Market research
   - Business consulting
   - Project management
   - Design services

6. **Education and Training (80000000)**
   - E-learning services
   - Training services

### CPV Code Hierarchy

CPV codes follow a hierarchical structure based on the digits:

```
48000000 - Main division (2 digits: 48)
  48100000 - Group (3 digits: 481)
    48151000 - Class (4 digits: 4815)
      48151100 - Category (5 digits: 48151)
```

**Example:**
- `48000000` - Software and information systems (main)
- `48100000` - Industry-specific software (sub)
- `48151000` - Computer control system (specific)

### Data Usage

**Service:** `src/service/cpv_service.py`
- `CPVService` class with static methods
- Search, filter, and categorize CPV codes
- Automatic category detection by code prefix

**API:** `src/api/cpv_api.py`
- List all codes
- Search by description
- Filter by category
- Get statistics

### Maintenance

To add new CPV codes:

1. Open `src/service/cpv_service.py`
2. Add code to `CPV_CODES` dictionary:
   ```python
   CPV_CODES: dict[int, str] = {
       # ... existing codes ...
       99000000: "New Category Description",
   }
   ```
3. If adding a new main category, update `CPVMainCategory` enum:
   ```python
   class CPVMainCategory(Enum):
       # ... existing categories ...
       NEW_CATEGORY = 99000000
   ```
4. Update `get_category_for_code()` method to handle new prefix

---

## Data Refresh Strategy

### Static Data (CPV Codes)
- **Frequency:** Manual updates as needed
- **Source:** Internal dictionary
- **Update Process:** Code changes and deployment

### Dynamic Data (Doffin)
- **Frequency:** Real-time via API
- **Caching:** Not currently implemented
- **Future:** Consider caching frequently accessed data

### Semi-Static Data (NUTS/STYRK)
- **Frequency:** On application startup
- **Loading:** Loaded once when service is instantiated
- **Update Process:** Change version number in service initialization

---

## Data Quality Considerations

### Doffin Data
- **Completeness:** Depends on API availability
- **Accuracy:** Official government data
- **Timeliness:** Real-time updates
- **Limitations:** Requires API key, subject to rate limits

### SSB Data
- **Completeness:** Full classification sets
- **Accuracy:** Official statistics
- **Timeliness:** Periodically updated by SSB
- **Limitations:** Version numbers may change

### CPV Data
- **Completeness:** Subset relevant to IT/consulting
- **Accuracy:** Manual maintenance required
- **Timeliness:** Manual updates
- **Limitations:** Not all CPV codes included (only relevant subset)

---

## External Resources

### Official Documentation
- **Doffin:** [https://doffin.no](https://doffin.no)
- **Doffin API:** [https://api.doffin.no](https://api.doffin.no)
- **SSB KLASS:** [https://www.ssb.no/klass/](https://www.ssb.no/klass/)
- **CPV Codes:** [https://simap.ted.europa.eu/cpv](https://simap.ted.europa.eu/cpv)

### Version Information
- **NUTS Version:** 2482 (update in `NUTSService.__init__()`)
- **STYRK Version:** 33 (update in `STYRKService.__init__()`)

### Data Privacy
All data sources are public and do not contain personal information. No GDPR concerns for the data accessed through these APIs.

---

## Troubleshooting Data Issues

### Issue: Doffin API returns empty results
**Possible causes:**
- Invalid API key
- Incorrect query parameters
- API downtime

**Solution:**
1. Verify API key in `.env` file
2. Check API status at Doffin portal
3. Review query parameters

### Issue: SSB data not loading
**Possible causes:**
- Incorrect version number
- SSB API downtime
- Network connectivity issues

**Solution:**
1. Verify version number is correct
2. Check SSB KLASS website for current versions
3. Test API endpoint directly in browser

### Issue: CPV code not found
**Possible causes:**
- Code not in internal dictionary
- Typo in code number

**Solution:**
1. Verify code exists in `CPV_CODES` dictionary
2. Check official CPV documentation
3. Add code if missing and relevant

---

## Future Enhancements

### Potential Improvements
1. **Database Integration:** Store cached API responses
2. **Automatic Updates:** Scheduled jobs to refresh SSB data
3. **Extended CPV Coverage:** Add more CPV code categories
4. **Data Validation:** Implement data quality checks
5. **Versioning:** Track data source versions
6. **Webhooks:** Real-time Doffin updates (if available)
