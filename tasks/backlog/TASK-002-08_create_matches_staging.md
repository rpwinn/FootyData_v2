# TASK-002-08: Create Matches Staging Table

## Task Overview
- **Task ID**: TASK-002-08
- **Created**: 2025-07-31
- **Status**: TODO
- **Priority**: HIGH
- **Epic**: EPIC-002 (Create Staging Tables for API Data)
- **Dependencies**: TASK-002-03 (League Seasons staging table)

## 🎯 Objective
Create PostgreSQL staging table for matches data and validate it with real API calls. This endpoint requires league IDs and season IDs from the league seasons endpoint.

## 📋 Acceptance Criteria
- [ ] Matches staging table created in `staging` schema
- [ ] Table schema matches `/matches` API response structure
- [ ] Test script makes 2-3 API calls using league_id + season_id combinations
- [ ] SQL verification query retrieves exact same data as original API response
- [ ] All field mappings validated (data types, null handling, etc.)

## 🔍 Context
This task depends on TASK-002-03 (League Seasons staging table) because the `/matches` endpoint requires both `league_id` and `season_id` parameters. We'll use combinations from the league seasons table to test this endpoint.

## 📝 Implementation Steps

1. **Review Matches API Documentation**
   - [ ] Read `/matches` endpoint documentation
   - [ ] Analyze API response structure and field types
   - [ ] Identify required fields and data types

2. **Design Matches Staging Table Schema**
   - [ ] Map API fields to database columns
   - [ ] Define appropriate PostgreSQL data types
   - [ ] Add standard audit fields (created_at, updated_at)
   - [ ] Define primary key and indexes

3. **Create SQL Script**
   - [ ] Write `src/database/create_matches_staging.sql`
   - [ ] Include table comments and field descriptions
   - [ ] Add appropriate indexes for performance

4. **FBR Client Setup and Verification**
   - [ ] Verify `FBRClient.get_matches()` method exists and works correctly
   - [ ] Test client method with real API calls (with league_id, season_id, and optional team_id parameters)
   - [ ] Validate response structure matches API documentation
   - [ ] Confirm rate limiting is enforced (6-second delay between calls)
   - [ ] Test error handling with invalid league_id/season_id combinations

5. **Implement and Test**
   - [ ] Execute SQL script and verify table structure
   - [ ] Create test script `src/etl/test_matches_data.py`
   - [ ] Query league seasons table to get 2-3 league_id + season_id combinations
   - [ ] Use `FBRClient.get_matches(league_id, season_id, team_id)` to make API calls
   - [ ] Store API responses in staging table
   - [ ] Write SQL query to retrieve stored data
   - [ ] Compare original API responses with SQL query results
   - [ ] Verify data integrity and field mapping accuracy

## 🛠️ Technical Details

### Database Configuration:
- **Database**: PostgreSQL (via `DATABASE_URL` environment variable)
- **Schema**: `staging` (as defined in `config/config.yaml`)
- **Connection**: Using `psycopg2` with environment variables from `.env`
- **Table**: `staging.matches`

### API Endpoint:
- **URL**: `/matches`
- **Method**: GET
- **Required Parameters**: `league_id` (integer), `season_id` (string)
- **Optional Parameters**: `team_id` (string)
- **Response**: Array of match objects with teams, scores, venue, etc.

### Files to Create:
- `src/database/create_matches_staging.sql`
- `src/etl/test_matches_data.py`

### Dependencies:
- PostgreSQL database access via `DATABASE_URL`
- League seasons staging table (TASK-002-03)
- API documentation from TASK-001
- FBR API client configuration (`src/api/fbr_client.py`)
- Environment variables loaded from `.env` file

### FBR Client Method:
- **Method**: `FBRClient.get_matches(league_id: str, season_id: str, team_id: Optional[str] = None)`
- **Parameters**: `league_id` (required string), `season_id` (required string), `team_id` (optional string)
- **Returns**: `Dict[str, Any]` with matches data including teams, scores, venue
- **Rate Limiting**: 6-second delay between calls
- **Error Handling**: Returns `{"error": str(e)}` on failure

## 📚 Resources
- [Matches API Documentation](src/api/endpoint_documentation/matches.md)
- [League seasons staging table](src/database/create_league_seasons_staging.sql)
- [FBR API Client](src/api/fbr_client.py)

## 🚧 Blockers
- Requires TASK-002-03 (League seasons staging table) to be completed first

## 💡 Notes
This endpoint provides comprehensive match data including teams, scores, venue, and attendance. The test script should test both with and without the optional team_id parameter to validate different scenarios.

---
*Created: 2025-07-31*
*Last Updated: 2025-07-31*
*Status: TODO* 