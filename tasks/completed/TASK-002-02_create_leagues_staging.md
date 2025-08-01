# TASK-002-02: Create Leagues Staging Table

## Task Overview
- **Task ID**: TASK-002-02
- **Created**: 2025-07-31
- **Status**: REVIEW
- **Priority**: HIGH
- **Epic**: EPIC-002 (Create Staging Tables for API Data)
- **Dependencies**: TASK-002-01 (Countries staging table)

## 🎯 Objective
Create PostgreSQL staging table for leagues data and validate it with real API calls. This task will establish the pattern for handling large datasets by implementing a test strategy with a subset of countries.

## 📋 Acceptance Criteria
- [x] Leagues staging table created in `staging` schema
- [x] Table schema matches `/leagues` API response structure
- [x] Test script loads leagues for 5-10 representative countries
- [x] SQL verification query retrieves exact same data as original API response
- [x] All field mappings validated (data types, null handling, etc.)
- [x] Strategy documented for full data collection in future task

## 🔍 Context
This is the second task in EPIC-002. The `/leagues` endpoint has significant data volume (~3,700 leagues across 225 countries). We need to establish the pattern for handling large datasets by:
1. Creating the staging table and ETL process
2. Testing with a representative subset of countries
3. Documenting the strategy for full data collection

## 📝 Implementation Steps

1. **Review Leagues API Documentation**
   - [x] Read `/leagues` endpoint documentation
   - [x] Analyze API response structure and field types
   - [x] Identify required fields and data types

2. **Design Leagues Staging Table Schema**
   - [x] Map API fields to database columns
   - [x] Define appropriate PostgreSQL data types
   - [x] Add standard audit fields (created_at, updated_at)
   - [x] Define primary key and indexes

3. **Create SQL Script**
   - [x] Write `src/database/create_leagues_staging.sql`
   - [x] Include table comments and field descriptions
   - [x] Add appropriate indexes for performance

4. **FBR Client Setup and Verification**
   - [x] Verify `FBRClient.get_leagues()` method exists and works correctly
   - [x] Test client method with real API calls (with country_code parameter)
   - [x] Validate response structure matches API documentation
   - [x] Confirm rate limiting is enforced (6-second delay between calls)
   - [x] Test error handling with invalid country codes

5. **Implement and Test**
   - [x] Execute SQL script and verify table structure
   - [x] Create test script `src/etl/load_leagues_data_test.py`
   - [x] Use `FBRClient.get_leagues(country_code)` to make API calls for 5 test countries
   - [x] Store API responses in staging table
   - [x] Write SQL query to retrieve stored data
   - [x] Compare original API responses with SQL query results
   - [x] Verify data integrity and field mapping accuracy

6. **Create Verification Script**
   - [x] Create `src/verification/verify_leagues_data_comparison.py`
   - [x] Compare fresh API calls with stored data for test countries
   - [x] Ensure all fields match exactly

7. **Document Full Data Collection Strategy**
   - [x] Create `TASK-002-02A_full_leagues_collection.md` for future task
   - [x] Document estimated volume and collection strategy
   - [x] Plan for handling rate limits and error recovery

## 🛠️ Technical Details

### Database Configuration:
- **Database**: PostgreSQL (via `DATABASE_URL` environment variable)
- **Schema**: `staging` (as defined in `config/config.yaml`)
- **Connection**: Using `psycopg2` with environment variables from `.env`
- **Table**: `staging.leagues`

### API Endpoint:
- **URL**: `/leagues`
- **Method**: GET
- **Required Parameters**: `country_code` (string)
- **Response**: Array of league type objects with nested leagues array

### Files to Create:
- `src/database/create_leagues_staging.sql`
- `src/etl/test_leagues_data.py`

### Dependencies:
- PostgreSQL database access via `DATABASE_URL`
- Countries staging table (TASK-002-01)
- API documentation from TASK-001
- FBR API client configuration (`src/api/fbr_client.py`)
- Environment variables loaded from `.env` file

### FBR Client Method:
- **Method**: `FBRClient.get_leagues(country_code: Optional[str] = None)`
- **Parameters**: `country_code` (optional string for filtering by country)
- **Returns**: `Dict[str, Any]` with leagues data organized by type
- **Rate Limiting**: 6-second delay between calls
- **Error Handling**: Returns `{"error": str(e)}` on failure

## 📚 Resources
- [Leagues API Documentation](src/api/endpoint_documentation/leagues.md)
- [Countries staging table](src/database/create_countries_staging.sql)
- [FBR API Client](src/api/fbr_client.py)

## 🚧 Blockers
- Requires TASK-002-01 (Countries staging table) to be completed first

## 📊 Data Volume Analysis

### Current Test Scope:
- **Countries**: 5 representative countries (ENG, USA, BRA, GER, FRA)
- **Estimated Leagues**: ~90 leagues
- **API Calls**: 5 calls (one per country)
- **Test Duration**: ~30 seconds (with rate limiting)

### Full Collection Scope (Future Task):
- **Countries**: All 225 countries from countries table
- **Estimated Leagues**: ~3,700 leagues
- **API Calls**: 225 calls (one per country)
- **Collection Duration**: ~22 minutes (with rate limiting)
- **Error Recovery**: Need strategy for failed calls

## 💡 Notes
This task establishes the pattern for handling large datasets. The test approach with 5 countries validates the table structure and ETL process, while the future task (TASK-002-02A) will handle the full data collection with proper error handling and recovery strategies.

---
*Created: 2025-07-31*
*Last Updated: 2025-07-31*
*Status: DONE* 