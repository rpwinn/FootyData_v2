# TASK-002-07: Create Players Staging Table

## Task Overview
- **Task ID**: TASK-002-07
- **Created**: 2025-07-31
- **Status**: TODO
- **Priority**: HIGH
- **Epic**: EPIC-002 (Create Staging Tables for API Data)
- **Dependencies**: None (independent)

## 🎯 Objective
Create PostgreSQL staging table for players data and validate it with real API calls. This endpoint requires player IDs which can be obtained from known player IDs or API documentation.

## 📋 Acceptance Criteria
- [ ] Players staging table created in `staging` schema
- [ ] Table schema matches `/players` API response structure
- [ ] Test script makes 2-3 API calls using known player IDs
- [ ] SQL verification query retrieves exact same data as original API response
- [ ] All field mappings validated (data types, null handling, etc.)

## 🔍 Context
This task is independent and can be completed without waiting for other tasks. The `/players` endpoint requires a `player_id` parameter, which can be obtained from API documentation examples or known player IDs.

## 📝 Implementation Steps

1. **Review Players API Documentation**
   - [ ] Read `/players` endpoint documentation
   - [ ] Analyze API response structure and field types
   - [ ] Identify required fields and data types

2. **Design Players Staging Table Schema**
   - [ ] Map API fields to database columns
   - [ ] Define appropriate PostgreSQL data types
   - [ ] Add standard audit fields (created_at, updated_at)
   - [ ] Define primary key and indexes

3. **Create SQL Script**
   - [ ] Write `src/database/create_players_staging.sql`
   - [ ] Include table comments and field descriptions
   - [ ] Add appropriate indexes for performance

4. **FBR Client Setup and Verification**
   - [ ] Verify `FBRClient.get_players()` method exists and works correctly
   - [ ] Test client method with real API calls (with player_id parameter)
   - [ ] Validate response structure matches API documentation
   - [ ] Confirm rate limiting is enforced (6-second delay between calls)
   - [ ] Test error handling with invalid player IDs

5. **Implement and Test**
   - [ ] Execute SQL script and verify table structure
   - [ ] Create test script `src/etl/test_players_data.py`
   - [ ] Use known player IDs from API documentation for testing
   - [ ] Use `FBRClient.get_players(player_id)` to make API calls
   - [ ] Store API responses in staging table
   - [ ] Write SQL query to retrieve stored data
   - [ ] Compare original API responses with SQL query results
   - [ ] Verify data integrity and field mapping accuracy

## 🛠️ Technical Details

### Database Configuration:
- **Database**: PostgreSQL (via `DATABASE_URL` environment variable)
- **Schema**: `staging` (as defined in `config/config.yaml`)
- **Connection**: Using `psycopg2` with environment variables from `.env`
- **Table**: `staging.players`

### API Endpoint:
- **URL**: `/players`
- **Method**: GET
- **Required Parameters**: `player_id` (string)
- **Response**: Object with player info and career stats

### Files to Create:
- `src/database/create_players_staging.sql`
- `src/etl/test_players_data.py`

### Dependencies:
- PostgreSQL database access via `DATABASE_URL`
- API documentation from TASK-001
- FBR API client configuration (`src/api/fbr_client.py`)
- Environment variables loaded from `.env` file

### FBR Client Method:
- **Method**: `FBRClient.get_players(player_id: str)`
- **Parameters**: `player_id` (required string)
- **Returns**: `Dict[str, Any]` with player data and career stats
- **Rate Limiting**: 6-second delay between calls
- **Error Handling**: Returns `{"error": str(e)}` on failure

## 📚 Resources
- [Players API Documentation](src/api/endpoint_documentation/players.md)
- [FBR API Client](src/api/fbr_client.py)

## 🚧 Blockers
- None (independent task)

## 💡 Notes
This endpoint provides comprehensive player data including career statistics. The test script should use player IDs from API documentation examples to ensure valid test data.

---
*Created: 2025-07-31*
*Last Updated: 2025-07-31*
*Status: TODO* 