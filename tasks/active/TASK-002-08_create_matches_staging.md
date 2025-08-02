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
- [x] Matches staging tables created in `staging` schema
- [x] Table schema matches `/matches` API response structure (both formats)
- [x] Test script makes 2-3 API calls using league_id + season_id combinations
- [x] SQL verification query retrieves exact same data as original API response
- [x] All field mappings validated (data types, null handling, etc.)

## 🔍 Context
This task depends on TASK-002-03 (League Seasons staging table) because the `/matches` endpoint requires both `league_id` and `season_id` parameters. We'll use combinations from the league seasons table to test this endpoint.

## 📝 Implementation Steps

1. **Review Matches API Documentation**
   - [x] Read `/matches` endpoint documentation
   - [x] Analyze API response structure and field types
   - [x] Identify required fields and data types

2. **Design Matches Staging Table Schema**
   - [x] Map API fields to database columns
   - [x] Define appropriate PostgreSQL data types
   - [x] Add standard audit fields (created_at, updated_at)
   - [x] Define primary key and indexes

3. **Create SQL Script**
   - [x] Write `src/database/create_matches_staging.sql`
   - [x] Include table comments and field descriptions
   - [x] Add appropriate indexes for performance

4. **FBR Client Setup and Verification**
   - [x] Verify `FBRClient.get_matches()` method exists and works correctly
   - [x] Test client method with real API calls (with league_id, season_id, and optional team_id parameters)
   - [x] Validate response structure matches API documentation
   - [x] Confirm rate limiting is enforced (6-second delay between calls)
   - [x] Test error handling with invalid league_id/season_id combinations

5. **Implement and Test**
   - [x] Execute SQL script and verify table structure
   - [x] Create test script `src/etl/test_matches_data.py`
   - [x] Query league seasons table to get 2-3 league_id + season_id combinations
   - [x] Use `FBRClient.get_matches(league_id, season_id, team_id)` to make API calls
   - [x] Store API responses in staging table
   - [x] Write SQL query to retrieve stored data
   - [x] Compare original API responses with SQL query results
   - [x] Verify data integrity and field mapping accuracy

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

### ⚠️ Important API Findings
**League Matches (no team_id)**: ✅ **WORKING - FIXTURES ONLY**
- Successfully collected thousands of matches across multiple leagues and seasons
- API response structure matches documentation
- **Important**: This endpoint provides **fixture/schedule data**, not results
- Scores are `null` because these are upcoming/future matches or the API doesn't provide results in this format
- Use case: Match schedules, upcoming fixtures, venue information

**Team Matches (with team_id)**: ✅ **WORKING - INCLUDES RESULTS**
- Successfully collected team matches with actual results
- Provides `result` (W/L/D), `gf` (goals for), `ga` (goals against)
- **Key insight**: Must use correct team/league combinations (international teams with international leagues)
- Use case: Match results, team performance analysis

**Implementation Status**:
- ✅ **League matches staging table**: Created and tested successfully (fixtures only)
- ✅ **Team matches staging table**: Created and tested successfully (includes results)
- ✅ **Dual response format handling**: Successfully implemented separate tables for different data structures
- ✅ **Data validation**: Both league and team matches data integrity verified
- ✅ **Cascading integration**: Successfully integrated into `collect_football_data.py`
- ✅ **Performance optimization**: Added duplicate checking to skip existing data and avoid unnecessary API calls

**Key Learning**: 
1. **League matches** provide fixture/schedule data (scores are null)
2. **Team matches** provide actual results with scores and outcomes
3. Team matches work when using international team IDs with international leagues (e.g., England in World Cup 2022)
4. The initial failure was due to testing international team IDs with club leagues
5. **Performance optimization**: Checking for existing data before API calls dramatically improves collection efficiency

**Data Strategy**:
- Use **league matches** for fixture schedules, venue info, and match metadata
- Use **team matches** for actual results, scores, and team performance data
- **Team matches create duplicate data**: Each match is recorded twice (home/away perspectives)
- **Storage impact**: Premier League: 380 unique matches → 760 team match records per season
- **Benefit**: Easy team-centric analysis and complete team match histories

**Integration Success**:
- Successfully collected **3,605 new matches** across **17/48 combinations**
- Skipped existing data efficiently, avoiding unnecessary API calls
- Future fixtures (2025-2026) properly handled with null match_id filtering

---
*Created: 2025-07-31*
*Last Updated: 2025-07-31*
*Status: COMPLETED* 