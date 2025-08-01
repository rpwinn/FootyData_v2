# TASK-002-05: Create League Standings Staging Table

## Task Overview
- **Task ID**: TASK-002-05
- **Created**: 2025-07-31
- **Status**: TODO
- **Priority**: HIGH
- **Epic**: EPIC-002 (Create Staging Tables for API Data)
- **Dependencies**: TASK-002-03 (League Seasons staging table)

## 🎯 Objective
Create PostgreSQL staging table for league standings data and validate it with real API calls. This endpoint requires league IDs and season IDs from the league seasons endpoint.

## 📋 Acceptance Criteria
- [ ] League standings staging table created in `staging` schema
- [ ] Table schema matches `/league-standings` API response structure
- [ ] Test script makes 2-3 API calls using league_id + season_id combinations
- [ ] SQL verification query retrieves exact same data as original API response
- [ ] All field mappings validated (data types, null handling, etc.)

## 🔍 Context
This task depends on TASK-002-03 (League Seasons staging table) because the `/league-standings` endpoint requires both `league_id` and `season_id` parameters. We'll use combinations from the league seasons table to test this endpoint.

## 📝 Implementation Steps

1. **Review League Standings API Documentation**
   - [ ] Read `/league-standings` endpoint documentation
   - [ ] Analyze API response structure and field types
   - [ ] Identify required fields and data types

2. **Design League Standings Staging Table Schema**
   - [ ] Map API fields to database columns
   - [ ] Define appropriate PostgreSQL data types
   - [ ] Add standard audit fields (created_at, updated_at)
   - [ ] Define primary key and indexes

3. **Create SQL Script**
   - [ ] Write `src/database/create_league_standings_staging.sql`
   - [ ] Include table comments and field descriptions
   - [ ] Add appropriate indexes for performance

4. **FBR Client Setup and Verification**
   - [ ] Verify `FBRClient.get_league_standings()` method exists and works correctly
   - [ ] Test client method with real API calls (with league_id and season_id parameters)
   - [ ] Validate response structure matches API documentation
   - [ ] Confirm rate limiting is enforced (6-second delay between calls)
   - [ ] Test error handling with invalid league_id/season_id combinations

5. **Implement and Test**
   - [ ] Execute SQL script and verify table structure
   - [ ] Create test script `src/etl/test_league_standings_data.py`
   - [ ] Query league seasons table to get 2-3 league_id + season_id combinations
   - [ ] Use `FBRClient.get_league_standings(league_id, season_id)` to make API calls
   - [ ] Store API responses in staging table
   - [ ] Write SQL query to retrieve stored data
   - [ ] Compare original API responses with SQL query results
   - [ ] Verify data integrity and field mapping accuracy

## 🛠️ Technical Details

### Database Configuration:
- **Database**: PostgreSQL (via `DATABASE_URL` environment variable)
- **Schema**: `staging` (as defined in `config/config.yaml`)
- **Connection**: Using `psycopg2` with environment variables from `.env`
- **Table**: `staging.league_standings`

### API Endpoint:
- **URL**: `/league-standings`
- **Method**: GET
- **Required Parameters**: `league_id` (integer), `season_id` (string, optional)
- **Response**: Array of team standings with position, points, goals, etc.

### Files to Create:
- `src/database/create_league_standings_staging.sql`
- `src/etl/test_league_standings_data.py`

### Dependencies:
- PostgreSQL database access via `DATABASE_URL`
- League seasons staging table (TASK-002-03)
- API documentation from TASK-001
- FBR API client configuration (`src/api/fbr_client.py`)
- Environment variables loaded from `.env` file

### FBR Client Method:
- **Method**: `FBRClient.get_league_standings(league_id: int, season_id: Optional[str] = None)`
- **Parameters**: `league_id` (required int), `season_id` (optional string)
- **Returns**: `Dict[str, Any]` with league standings data
- **Rate Limiting**: 6-second delay between calls
- **Error Handling**: Returns `{"error": str(e)}` on failure

## 📚 Resources
- [League Standings API Documentation](src/api/endpoint_documentation/league_standings.md)
- [League seasons staging table](src/database/create_league_seasons_staging.sql)
- [FBR API Client](src/api/fbr_client.py)

## 🚧 Blockers
- Requires TASK-002-03 (League seasons staging table) to be completed first

## 💡 Notes
This endpoint provides final standings data for leagues. The test script should include both completed seasons and current seasons to validate different data scenarios.

---
*Created: 2025-07-31*
*Last Updated: 2025-07-31*
*Status: TODO* 