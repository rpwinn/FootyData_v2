# TASK-002-01: Create Countries Staging Table

## Task Overview
- **Task ID**: TASK-002-01
- **Created**: 2025-07-31
- **Status**: DONE
- **Priority**: HIGH
- **Epic**: EPIC-002 (Create Staging Tables for API Data)

## 🎯 Objective
Create PostgreSQL staging table for countries data and validate it with real API calls. This is the first endpoint/staging table combination in the epic.

## 📋 Acceptance Criteria
- [x] Countries staging table created in `staging` schema
- [x] Table schema matches `/countries` API response structure
- [x] Test script makes 2-3 API calls and stores data correctly
- [x] SQL verification query retrieves exact same data as original API response
- [x] All field mappings validated (data types, null handling, etc.)

## 🔍 Context
This is the first task in EPIC-002. We need to create a staging table for countries data that will serve as the foundation for all country-related data collection. The `/countries` endpoint provides basic country information used throughout the system.

## 📝 Implementation Steps

1. **Review Countries API Documentation**
   - [x] Read `/countries` endpoint documentation
   - [x] Analyze API response structure and field types
   - [x] Identify required fields and data types

2. **Design Countries Staging Table Schema**
   - [x] Map API fields to database columns
   - [x] Define appropriate PostgreSQL data types
   - [x] Add standard audit fields (created_at, updated_at)
   - [x] Define primary key and indexes

3. **Create SQL Script**
   - [x] Write `src/database/create_countries_staging.sql`
   - [x] Include table comments and field descriptions
   - [x] Add appropriate indexes for performance

4. **FBR Client Setup and Verification**
   - [x] Verify `FBRClient.get_countries()` method exists and works correctly
   - [x] Test client method with real API calls (no parameters, with country parameter)
   - [x] Validate response structure matches API documentation
   - [x] Confirm rate limiting is enforced (6-second delay between calls)
   - [x] Test error handling with invalid parameters

5. **Implement and Test**
   - [x] Execute SQL script and verify table structure
   - [x] Create test script `src/etl/load_countries_data_simple.py`
   - [x] Use `FBRClient.get_countries()` to make API calls for all 225 countries
   - [x] Store API responses in staging table
   - [x] Write SQL query to retrieve stored data
   - [x] Compare original API responses with SQL query results
   - [x] Verify data integrity and field mapping accuracy

## 🛠️ Technical Details

### Database Configuration:
- **Database**: PostgreSQL (via `DATABASE_URL` environment variable)
- **Schema**: `staging` (as defined in `config/config.yaml`)
- **Connection**: Using `psycopg2` with environment variables from `.env`
- **Table**: `staging.countries`

### API Endpoint:
- **URL**: `/countries`
- **Method**: GET
- **Response**: Array of country objects with country_code, country_name, etc.

### Files to Create:
- `src/database/create_countries_staging.sql`
- `src/etl/test_countries_data.py`

### Dependencies:
- PostgreSQL database access via `DATABASE_URL`
- API documentation from TASK-001
- FBR API client configuration (`src/api/fbr_client.py`)
- Environment variables loaded from `.env` file

### FBR Client Method:
- **Method**: `FBRClient.get_countries(country: Optional[str] = None)`
- **Parameters**: `country` (optional string for filtering)
- **Returns**: `Dict[str, Any]` with countries data
- **Rate Limiting**: 6-second delay between calls
- **Error Handling**: Returns `{"error": str(e)}` on failure

## 📚 Resources
- [Countries API Documentation](src/api/endpoint_documentation/countries.md)
- [FBR API Client](src/api/fbr_client.py)

## 🚧 Blockers
- None currently identified

## 💡 Notes
This task establishes the pattern for all subsequent endpoint/staging table combinations. The verification process should be thorough as it will serve as a template for the remaining 12 endpoints.

---
*Created: 2025-07-31*
*Last Updated: 2025-07-31*
*Status: TODO* 