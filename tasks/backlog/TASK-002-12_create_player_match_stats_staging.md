# TASK-002-12: Create Player Match Stats Staging Table

## Task Overview
- **Task ID**: TASK-002-12
- **Created**: 2025-07-31
- **Status**: TODO
- **Priority**: HIGH
- **Epic**: EPIC-002 (Create Staging Tables for API Data)
- **Dependencies**: TASK-002-08 (Matches staging table)

## 🎯 Objective
Create PostgreSQL staging table for player match stats data and validate it with real API calls. This endpoint requires match IDs from the matches endpoint.

## 📋 Acceptance Criteria
- [ ] Player match stats staging table created in `staging` schema
- [ ] Table schema matches `/player-match-stats` API response structure
- [ ] Test script makes 2-3 API calls using match IDs from matches table
- [ ] SQL verification query retrieves exact same data as original API response
- [ ] All field mappings validated (data types, null handling, etc.)

## 🔍 Context
This task depends on TASK-002-08 (Matches staging table) because the `/player-match-stats` endpoint requires a `match_id` parameter. We'll use match IDs from the matches table to test this endpoint.

## 📝 Implementation Steps

1. **Review Player Match Stats API Documentation**
   - [ ] Read `/player-match-stats` endpoint documentation
   - [ ] Analyze API response structure and field types
   - [ ] Identify required fields and data types

2. **Design Player Match Stats Staging Table Schema**
   - [ ] Map API fields to database columns
   - [ ] Define appropriate PostgreSQL data types
   - [ ] Add standard audit fields (created_at, updated_at)
   - [ ] Define primary key and indexes

3. **Create SQL Script**
   - [ ] Write `src/database/create_player_match_stats_staging.sql`
   - [ ] Include table comments and field descriptions
   - [ ] Add appropriate indexes for performance

4. **FBR Client Setup and Verification**
   - [ ] Verify `FBRClient.get_match_stats()` method exists and works correctly
   - [ ] Test client method with real API calls (with match_id parameter)
   - [ ] Validate response structure matches API documentation
   - [ ] Confirm rate limiting is enforced (6-second delay between calls)
   - [ ] Test error handling with invalid match IDs

5. **Implement and Test**
   - [ ] Execute SQL script and verify table structure
   - [ ] Create test script `src/etl/test_player_match_stats_data.py`
   - [ ] Query matches table to get 2-3 match IDs for testing
   - [ ] Use `FBRClient.get_match_stats(match_id)` to make API calls
   - [ ] Store API responses in staging table
   - [ ] Write SQL query to retrieve stored data
   - [ ] Compare original API responses with SQL query results
   - [ ] Verify data integrity and field mapping accuracy

## 🛠️ Technical Details

### Database Configuration:
- **Database**: PostgreSQL (via `DATABASE_URL` environment variable)
- **Schema**: `staging` (as defined in `config/config.yaml`)
- **Connection**: Using `psycopg2` with environment variables from `.env`
- **Table**: `staging.player_match_stats`

### API Endpoint:
- **URL**: `/player-match-stats`
- **Method**: GET
- **Required Parameters**: `match_id` (string)
- **Response**: Object with meta_data and nested stats categories

### Files to Create:
- `src/database/create_player_match_stats_staging.sql`
- `src/etl/test_player_match_stats_data.py`

### Dependencies:
- PostgreSQL database access via `DATABASE_URL`
- Matches staging table (TASK-002-08)
- API documentation from TASK-001
- FBR API client configuration (`src/api/fbr_client.py`)
- Environment variables loaded from `.env` file

### FBR Client Method:
- **Method**: `FBRClient.get_match_stats(match_id: str)`
- **Parameters**: `match_id` (required string)
- **Returns**: `Dict[str, Any]` with player match statistics and nested stats categories
- **Rate Limiting**: 6-second delay between calls
- **Error Handling**: Returns `{"error": str(e)}` on failure

## 📚 Resources
- [Player Match Stats API Documentation](src/api/endpoint_documentation/player_match_stats.md)
- [Matches staging table](src/database/create_matches_staging.sql)
- [FBR API Client](src/api/fbr_client.py)

## 🚧 Blockers
- Requires TASK-002-08 (Matches staging table) to be completed first

## 💡 Notes
This endpoint provides detailed match-level statistics for players with nested data structures. The test script should validate that complex nested JSON data is properly stored and retrieved.

---
*Created: 2025-07-31*
*Last Updated: 2025-07-31*
*Status: TODO* 