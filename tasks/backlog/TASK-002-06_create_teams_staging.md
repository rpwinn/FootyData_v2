# TASK-002-06: Create Teams Staging Table

## Task Overview
- **Task ID**: TASK-002-06
- **Created**: 2025-07-31
- **Status**: TODO
- **Priority**: HIGH
- **Epic**: EPIC-002 (Create Staging Tables for API Data)
- **Dependencies**: None (independent)

## 🎯 Objective
Create PostgreSQL staging table for teams data and validate it with real API calls. This endpoint requires team IDs which can be obtained from known team IDs or API documentation.

## 📋 Acceptance Criteria
- [ ] Teams staging table created in `staging` schema
- [ ] Table schema matches `/teams` API response structure
- [ ] Test script makes 2-3 API calls using known team IDs
- [ ] SQL verification query retrieves exact same data as original API response
- [ ] All field mappings validated (data types, null handling, etc.)

## 🔍 Context
This task is independent and can be completed without waiting for other tasks. The `/teams` endpoint requires a `team_id` parameter, which can be obtained from API documentation examples or known team IDs.

## 📝 Implementation Steps

1. **Review Teams API Documentation**
   - [ ] Read `/teams` endpoint documentation
   - [ ] Analyze API response structure and field types
   - [ ] Identify required fields and data types

2. **Design Teams Staging Table Schema**
   - [ ] Map API fields to database columns
   - [ ] Define appropriate PostgreSQL data types
   - [ ] Add standard audit fields (created_at, updated_at)
   - [ ] Define primary key and indexes

3. **Create SQL Script**
   - [ ] Write `src/database/create_teams_staging.sql`
   - [ ] Include table comments and field descriptions
   - [ ] Add appropriate indexes for performance

4. **FBR Client Setup and Verification**
   - [ ] Verify `FBRClient.get_teams()` method exists and works correctly
   - [ ] Test client method with real API calls (with team_id and optional season_id parameters)
   - [ ] Validate response structure matches API documentation
   - [ ] Confirm rate limiting is enforced (6-second delay between calls)
   - [ ] Test error handling with invalid team IDs

5. **Implement and Test**
   - [ ] Execute SQL script and verify table structure
   - [ ] Create test script `src/etl/test_teams_data.py`
   - [ ] Use known team IDs from API documentation for testing
   - [ ] Use `FBRClient.get_teams(team_id, season_id)` to make API calls
   - [ ] Store API responses in staging table
   - [ ] Write SQL query to retrieve stored data
   - [ ] Compare original API responses with SQL query results
   - [ ] Verify data integrity and field mapping accuracy

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
- **Response**: Object with team_info, roster, and schedule arrays

### Files to Create:
- `src/database/create_teams_staging.sql`
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
- None (independent task)

## 💡 Notes
This endpoint provides comprehensive team data including roster and schedule information. The test script should use team IDs from API documentation examples to ensure valid test data.

---
*Created: 2025-07-31*
*Last Updated: 2025-07-31*
*Status: TODO* 