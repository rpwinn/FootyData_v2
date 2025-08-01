# TASK-002-11: Create Player Season Stats Staging Table

## Task Overview
- **Task ID**: TASK-002-11
- **Created**: 2025-07-31
- **Status**: TODO
- **Priority**: HIGH
- **Epic**: EPIC-002 (Create Staging Tables for API Data)
- **Dependencies**: TASK-002-06 (Teams staging table) + TASK-002-03 (League Seasons staging table)

## 🎯 Objective
Create PostgreSQL staging table for player season stats data and validate it with real API calls. This endpoint requires team IDs, league IDs, and season IDs from multiple staging tables.

## 📋 Acceptance Criteria
- [ ] Player season stats staging table created in `staging` schema
- [ ] Table schema matches `/player-season-stats` API response structure
- [ ] Test script makes 2-3 API calls using team_id + league_id + season_id combinations
- [ ] SQL verification query retrieves exact same data as original API response
- [ ] All field mappings validated (data types, null handling, etc.)

## 🔍 Context
This task depends on both TASK-002-06 (Teams staging table) and TASK-002-03 (League Seasons staging table) because the `/player-season-stats` endpoint requires `team_id`, `league_id`, and `season_id` parameters. We'll use combinations from both tables to test this endpoint.

## 📝 Implementation Steps

1. **Review Player Season Stats API Documentation**
   - [ ] Read `/player-season-stats` endpoint documentation
   - [ ] Analyze API response structure and field types
   - [ ] Identify required fields and data types

2. **Design Player Season Stats Staging Table Schema**
   - [ ] Map API fields to database columns
   - [ ] Define appropriate PostgreSQL data types
   - [ ] Add standard audit fields (created_at, updated_at)
   - [ ] Define primary key and indexes

3. **Create SQL Script**
   - [ ] Write `src/database/create_player_season_stats_staging.sql`
   - [ ] Include table comments and field descriptions
   - [ ] Add appropriate indexes for performance

4. **FBR Client Setup and Verification**
   - [ ] Verify `FBRClient.get_player_season_stats()` method exists and works correctly
   - [ ] Test client method with real API calls (with team_id, league_id, and optional season_id parameters)
   - [ ] Validate response structure matches API documentation
   - [ ] Confirm rate limiting is enforced (6-second delay between calls)
   - [ ] Test error handling with invalid team_id/league_id/season_id combinations

5. **Implement and Test**
   - [ ] Execute SQL script and verify table structure
   - [ ] Create test script `src/etl/test_player_season_stats_data.py`
   - [ ] Query teams and league seasons tables to get valid combinations
   - [ ] Use `FBRClient.get_player_season_stats(team_id, league_id, season_id)` to make API calls
   - [ ] Store API responses in staging table
   - [ ] Write SQL query to retrieve stored data
   - [ ] Compare original API responses with SQL query results
   - [ ] Verify data integrity and field mapping accuracy

## 🛠️ Technical Details

### Database Configuration:
- **Database**: PostgreSQL (via `DATABASE_URL` environment variable)
- **Schema**: `staging` (as defined in `config/config.yaml`)
- **Connection**: Using `psycopg2` with environment variables from `.env`
- **Table**: `staging.player_season_stats`

### API Endpoint:
- **URL**: `/player-season-stats`
- **Method**: GET
- **Required Parameters**: `team_id` (string), `league_id` (integer), `season_id` (string)
- **Response**: Object with meta_data and nested stats categories

### Files to Create:
- `src/database/create_player_season_stats_staging.sql`
- `src/etl/test_player_season_stats_data.py`

### Dependencies:
- PostgreSQL database access via `DATABASE_URL`
- Teams staging table (TASK-002-06)
- League seasons staging table (TASK-002-03)
- API documentation from TASK-001
- FBR API client configuration (`src/api/fbr_client.py`)
- Environment variables loaded from `.env` file

### FBR Client Method:
- **Method**: `FBRClient.get_player_season_stats(team_id: str, league_id: int, season_id: Optional[str] = None)`
- **Parameters**: `team_id` (required string), `league_id` (required int), `season_id` (optional string)
- **Returns**: `Dict[str, Any]` with player season statistics and nested stats categories
- **Rate Limiting**: 6-second delay between calls
- **Error Handling**: Returns `{"error": str(e)}` on failure

## 📚 Resources
- [Player Season Stats API Documentation](src/api/endpoint_documentation/player_season_stats.md)
- [Teams staging table](src/database/create_teams_staging.sql)
- [League seasons staging table](src/database/create_league_seasons_staging.sql)
- [FBR API Client](src/api/fbr_client.py)

## 🚧 Blockers
- Requires TASK-002-06 (Teams staging table) to be completed first
- Requires TASK-002-03 (League seasons staging table) to be completed first

## 💡 Notes
This endpoint provides detailed season-level statistics for players with nested data structures. The test script should validate that complex nested JSON data is properly stored and retrieved.

---
*Created: 2025-07-31*
*Last Updated: 2025-07-31*
*Status: TODO* 