# TASK-002-06: Create Teams Staging Table

## Task Overview
- **Task ID**: TASK-002-06
- **Created**: 2025-07-31
- **Status**: TODO
- **Priority**: HIGH
- **Epic**: EPIC-002 (Create Staging Tables for API Data)
- **Dependencies**: None (independent)

## 🎯 Objective
Create PostgreSQL staging tables for teams data and validate them with real API calls. The `/teams` endpoint returns nested data structures that require two separate tables: `team_rosters` for player data and `team_schedules` for match data. This endpoint requires team IDs which can be obtained from known team IDs or API documentation.

## 📋 Acceptance Criteria
- [x] Team rosters staging table created in `staging` schema
- [x] Team schedules staging table created in `staging` schema
- [x] Table schemas match `/teams` API response nested structure
- [x] Test script makes 2-3 API calls using known team IDs
- [x] SQL verification query retrieves exact same data as original API response
- [x] All field mappings validated (data types, null handling, etc.)
- [x] Load script updated to handle nested JSON structure
- [x] Both roster and schedule data properly normalized into separate tables

## 🔍 Context
This task is independent and can be completed without waiting for other tasks. The `/teams` endpoint requires a `team_id` parameter, which can be obtained from API documentation examples or known team IDs.

## 📝 Implementation Steps

1. **Review Teams API Documentation** ✅
   - [x] Read `/teams` endpoint documentation
   - [x] Analyze API response structure and field types
   - [x] Identify required fields and data types

2. **Design Teams Staging Table Schema** ✅
   - [x] Map API fields to database columns
   - [x] Define appropriate PostgreSQL data types
   - [x] Add standard audit fields (created_at, updated_at)
   - [x] Define primary key and indexes

3. **Create SQL Script** ✅
   - [x] Write `src/database/create_teams_staging.sql`
   - [x] Include table comments and field descriptions
   - [x] Add appropriate indexes for performance

4. **FBR Client Setup and Verification** ✅
   - [x] Verify `FBRClient.get_teams()` method exists and works correctly
   - [x] Test client method with real API calls (with team_id and optional season_id parameters)
   - [x] Validate response structure matches API documentation
   - [x] Confirm rate limiting is enforced (6-second delay between calls)
   - [x] Test error handling with invalid team IDs

5. **Implement and Test** ✅
   - [x] Execute SQL script and verify table structure
   - [x] Create test script `src/etl/test_teams_data.py`
   - [x] Use known team IDs from API documentation for testing
   - [x] Use `FBRClient.get_teams(team_id, season_id)` to make API calls
   - [x] Store API responses in staging table
   - [x] Write SQL query to retrieve stored data
   - [x] Compare original API responses with SQL query results
   - [x] Verify data integrity and field mapping accuracy

6. **Parameterized Loading Script** ✅
   - [x] Create `src/etl/load_teams_data.py`
   - [x] Implement optional filtering by team_ids and season_ids
   - [x] Add blacklist support for broken endpoints
   - [x] Handle API response structure differences from documentation

## 🛠️ Technical Details

### Database Configuration:
- **Database**: PostgreSQL (via `DATABASE_URL` environment variable)
- **Schema**: `staging` (as defined in `config/config.yaml`)
- **Connection**: Using `psycopg2` with environment variables from `.env`
- **Table**: `staging.teams`

### API Endpoint:
- **URL**: `/teams`
- **Method**: GET
- **Required Parameters**: `team_id` (string)
- **Response**: Object with nested `team_roster` and `team_schedule` data structures

### Files to Create:
- `src/database/create_team_rosters_staging.sql`
- `src/database/create_team_schedules_staging.sql`
- `src/etl/test_teams_data.py`

### Dependencies:
- PostgreSQL database access via `DATABASE_URL`
- API documentation from TASK-001
- FBR API client configuration (`src/api/fbr_client.py`)
- Environment variables loaded from `.env` file

### FBR Client Method:
- **Method**: `FBRClient.get_teams(team_id: str, season_id: Optional[str] = None)`
- **Parameters**: `team_id` (required string), `season_id` (optional string)
- **Returns**: `Dict[str, Any]` with team data including roster and schedule
- **Rate Limiting**: 6-second delay between calls
- **Error Handling**: Returns `{"error": str(e)}` on failure

## 📚 Resources
- [Teams API Documentation](src/api/endpoint_documentation/teams.md)
- [FBR API Client](src/api/fbr_client.py)

## 🚧 Blockers
- **Team ID Discovery**: No way to get team IDs for a league/season combination
- **Integration Dependency**: Cannot integrate into football collector without team ID discovery mechanism
- **API Limitation**: `/teams` endpoint requires individual `team_id` - no bulk team listing available

## 💡 Notes
This endpoint provides comprehensive team data including roster and schedule information. The test script should use team IDs from API documentation examples to ensure valid test data.

---
*Created: 2025-07-31*
*Last Updated: 2025-07-31*
*Status: BLOCKED*

## ⚠️ Important Note

### API Documentation Discrepancy
Our API documentation shows **3 categories** at the top level:
1. `team_info` - Team metadata (including team name)
2. `roster` - Player data  
3. `schedule` - Match data

**However, the actual API response only has 2 categories:**
1. `team_roster` - Player data
2. `team_schedule` - Match data

**The `team_info` section is missing from the actual API response!** This explains why we don't get team names - they should be in the `team_info` object that doesn't exist in the actual API response.

### API Stability Issues
The `/teams` endpoint has shown intermittent 500 Server Errors during testing. While the staging tables and scripts have been created and tested successfully when the API was working, the endpoint appears to be unstable. The collection has been blacklisted to prevent unnecessary API calls.

**Note**: The API response has a nested structure with `team_roster` and `team_schedule` data that requires two separate staging tables for proper normalization.

### 🔒 Integration Blocker
**Problem**: To integrate teams into the football collector, we need a way to get team IDs for a league/season combination.

**Current State**:
- ✅ Teams staging tables created and tested
- ✅ Load scripts working with nested JSON structure  
- ❌ **No team ID discovery mechanism**
- ❌ **Cannot integrate into cascading collection framework**

**Required Solution**:
- Need to find or create a way to get team IDs for a league
- Could be from other endpoints (`/matches`, `/league-standings`)
- Or test if `get_teams_by_league()` method actually works
- Or create manual team ID lists for major leagues 