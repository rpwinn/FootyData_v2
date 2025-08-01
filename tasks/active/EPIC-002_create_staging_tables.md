# EPIC-002: Create Staging Tables for API Data

## Epic Overview
- **Epic ID**: EPIC-002
- **Created**: 2025-07-31
- **Status**: IN_PROGRESS
- **Priority**: HIGH
- **Type**: EPIC

## 🎯 Objective
Create PostgreSQL staging tables for each major data area from the FBR API to establish the foundation for data collection and storage. Each staging table should match the structure of its corresponding API endpoint data.

## 📋 Acceptance Criteria
- [ ] Staging table created for each of the 13 major data areas
- [ ] Table schemas match API response structures
- [ ] All tables include standard audit fields (created_at, updated_at)
- [ ] Primary keys and appropriate indexes defined
- [ ] Tables created in `staging` schema
- [ ] SQL scripts documented and reusable
- [ ] Integration with existing database structure

## 🔍 Context
We now have comprehensive API documentation for all 15 FBR endpoints. We need to create staging tables to store this data before processing it into dimension and fact tables. The staging tables will serve as the landing zone for all API data collection.

## 📊 Endpoint/Staging Table Completion Tracking

- [x] **Countries** - `/countries` endpoint and staging table ✅
- [x] **Leagues** - `/leagues` endpoint and staging table ✅
- [ ] **League Seasons** - `/league-seasons` endpoint and staging table
- [ ] **League Season Details** - `/league-season-details` endpoint and staging table
- [ ] **League Standings** - `/league-standings` endpoint and staging table
- [ ] **Teams** - `/teams` endpoint and staging table
- [ ] **Players** - `/players` endpoint and staging table
- [ ] **Matches** - `/matches` endpoint and staging table
- [ ] **Team Season Stats** - `/team-season-stats` endpoint and staging table
- [ ] **Team Match Stats** - `/team-match-stats` endpoint and staging table
- [ ] **Player Season Stats** - `/player-season-stats` endpoint and staging table
- [ ] **Player Match Stats** - `/player-match-stats` endpoint and staging table
- [ ] **All Players Match Stats** - `/all-players-match-stats` endpoint and staging table

## 📋 Task Execution Order & Dependencies

### Phase 1: Independent Endpoints
- **TASK-002-01**: Countries ✅ (no dependencies)
- **TASK-002-06**: Teams (requires `team_id` - can use known team IDs)
- **TASK-002-07**: Players (requires `player_id` - can use known player IDs)

### Phase 2: Country-Dependent Endpoints
- **TASK-002-02**: Leagues ✅ (requires `country_code` from Countries)
- **TASK-002-03**: League Seasons (requires `league_id` from Leagues)

### Phase 3: League-Season-Dependent Endpoints
- **TASK-002-04**: League Season Details (requires `league_id` + `season_id`)
- **TASK-002-05**: League Standings (requires `league_id` + `season_id`)
- **TASK-002-08**: Matches (requires `league_id` + `season_id`)
- **TASK-002-09**: Team Season Stats (requires `league_id` + `season_id`)
- **TASK-002-13**: All Players Match Stats (requires `league_id` + `season_id`)

### Phase 4: Team-Dependent Endpoints
- **TASK-002-10**: Team Match Stats (requires `team_id` + `league_id` + `season_id`)
- **TASK-002-11**: Player Season Stats (requires `team_id` + `league_id` + `season_id`)

### Phase 5: Match-Dependent Endpoints
- **TASK-002-12**: Player Match Stats (requires `match_id` from Matches)

## 🎯 Recommended Execution Order

1. **TASK-002-01**: Countries ✅ (independent)
2. **TASK-002-06**: Teams (independent - use known team IDs)
3. **TASK-002-07**: Players (independent - use known player IDs)
4. **TASK-002-02**: Leagues ✅ (depends on Countries)
5. **TASK-002-03**: League Seasons (depends on Leagues)
6. **TASK-002-04**: League Season Details (depends on League Seasons)
7. **TASK-002-05**: League Standings (depends on League Seasons)
8. **TASK-002-08**: Matches (depends on League Seasons)
9. **TASK-002-09**: Team Season Stats (depends on League Seasons)
10. **TASK-002-13**: All Players Match Stats (depends on League Seasons)
11. **TASK-002-10**: Team Match Stats (depends on Teams + League Seasons)
12. **TASK-002-11**: Player Season Stats (depends on Teams + League Seasons)
13. **TASK-002-12**: Player Match Stats (depends on Matches)

## 📊 Dependency Map

```
Countries (01) ✅
    ↓
Leagues (02) ✅
    ↓
League Seasons (03)
    ↓
├── League Season Details (04)
├── League Standings (05)
├── Matches (08)
├── Team Season Stats (09)
└── All Players Match Stats (13)
    ↓
├── Team Match Stats (10) ← Teams (06)
└── Player Season Stats (11) ← Teams (06)
    ↓
Player Match Stats (12) ← Matches (08)

Teams (06) ──┘
Players (07) ──┘ (independent)
```

## 💡 Execution Notes

- **Independent tasks** can be done in parallel after the first one
- **Dependent tasks** must wait for their prerequisites
- **Test data** for independent tasks can use known IDs from API documentation
- **Complex dependencies** (like Team Match Stats) require multiple previous tasks

## 📝 Implementation Steps

1. **Start with Countries API and Staging Table**
   - [ ] Review `/countries` endpoint documentation
   - [ ] Analyze API response structure and field types
   - [ ] Design staging table schema for countries data
   - [ ] Create `src/database/create_countries_staging.sql`
   - [ ] Execute SQL script and verify table structure
   - [ ] Create test script `src/etl/test_countries_data.py` (make 2-3 API calls, store data)
   - [ ] Execute test script and store API responses
   - [ ] Write SQL query to retrieve stored data and compare with original API responses
   - [ ] Verify data integrity and field mapping accuracy

2. **Continue with Leagues API and Staging Table**
   - [ ] Review `/leagues` endpoint documentation
   - [ ] Analyze API response structure and field types
   - [ ] Design staging table schema for leagues data
   - [ ] Create `src/database/create_leagues_staging.sql`
   - [ ] Execute SQL script and verify table structure
   - [ ] Create test script `src/etl/test_leagues_data.py` (make 2-3 API calls, store data)
   - [ ] Execute test script and store API responses
   - [ ] Write SQL query to retrieve stored data and compare with original API responses
   - [ ] Verify data integrity and field mapping accuracy

3. **Continue with League Seasons API and Staging Table**
   - [ ] Review `/league-seasons` endpoint documentation
   - [ ] Analyze API response structure and field types
   - [ ] Design staging table schema for league seasons data
   - [ ] Create `src/database/create_league_seasons_staging.sql`
   - [ ] Execute SQL script and verify table structure
   - [ ] Create test script `src/etl/test_league_seasons_data.py` (make 2-3 API calls, store data)
   - [ ] Execute test script and store API responses
   - [ ] Write SQL query to retrieve stored data and compare with original API responses
   - [ ] Verify data integrity and field mapping accuracy

4. **Continue with League Season Details API and Staging Table**
   - [ ] Review `/league-season-details` endpoint documentation
   - [ ] Analyze API response structure and field types
   - [ ] Design staging table schema for league season details data
   - [ ] Create `src/database/create_league_season_details_staging.sql`
   - [ ] Execute SQL script and verify table structure
   - [ ] Create test script `src/etl/test_league_season_details_data.py` (make 2-3 API calls, store data)
   - [ ] Execute test script and store API responses
   - [ ] Write SQL query to retrieve stored data and compare with original API responses
   - [ ] Verify data integrity and field mapping accuracy

5. **Continue with League Standings API and Staging Table**
   - [ ] Review `/league-standings` endpoint documentation
   - [ ] Analyze API response structure and field types
   - [ ] Design staging table schema for league standings data
   - [ ] Create `src/database/create_league_standings_staging.sql`
   - [ ] Execute SQL script and verify table structure
   - [ ] Create test script `src/etl/test_league_standings_data.py` (make 2-3 API calls, store data)
   - [ ] Execute test script and store API responses
   - [ ] Write SQL query to retrieve stored data and compare with original API responses
   - [ ] Verify data integrity and field mapping accuracy

6. **Continue with Teams API and Staging Table**
   - [ ] Review `/teams` endpoint documentation
   - [ ] Analyze API response structure and field types
   - [ ] Design staging table schema for teams data
   - [ ] Create `src/database/create_teams_staging.sql`
   - [ ] Execute SQL script and verify table structure
   - [ ] Create test script `src/etl/test_teams_data.py` (make 2-3 API calls, store data)
   - [ ] Execute test script and store API responses
   - [ ] Write SQL query to retrieve stored data and compare with original API responses
   - [ ] Verify data integrity and field mapping accuracy

7. **Continue with Players API and Staging Table**
   - [ ] Review `/players` endpoint documentation
   - [ ] Analyze API response structure and field types
   - [ ] Design staging table schema for players data
   - [ ] Create `src/database/create_players_staging.sql`
   - [ ] Execute SQL script and verify table structure
   - [ ] Create test script `src/etl/test_players_data.py` (make 2-3 API calls, store data)
   - [ ] Execute test script and store API responses
   - [ ] Write SQL query to retrieve stored data and compare with original API responses
   - [ ] Verify data integrity and field mapping accuracy

8. **Continue with Matches API and Staging Table**
   - [ ] Review `/matches` endpoint documentation
   - [ ] Analyze API response structure and field types
   - [ ] Design staging table schema for matches data
   - [ ] Create `src/database/create_matches_staging.sql`
   - [ ] Execute SQL script and verify table structure
   - [ ] Create test script `src/etl/test_matches_data.py` (make 2-3 API calls, store data)
   - [ ] Execute test script and store API responses
   - [ ] Write SQL query to retrieve stored data and compare with original API responses
   - [ ] Verify data integrity and field mapping accuracy

9. **Continue with Team Season Stats API and Staging Table**
   - [ ] Review `/team-season-stats` endpoint documentation
   - [ ] Analyze API response structure and field types
   - [ ] Design staging table schema for team season stats data
   - [ ] Create `src/database/create_team_season_stats_staging.sql`
   - [ ] Execute SQL script and verify table structure
   - [ ] Create test script `src/etl/test_team_season_stats_data.py` (make 2-3 API calls, store data)
   - [ ] Execute test script and store API responses
   - [ ] Write SQL query to retrieve stored data and compare with original API responses
   - [ ] Verify data integrity and field mapping accuracy

10. **Continue with Team Match Stats API and Staging Table**
    - [ ] Review `/team-match-stats` endpoint documentation
    - [ ] Analyze API response structure and field types
    - [ ] Design staging table schema for team match stats data
    - [ ] Create `src/database/create_team_match_stats_staging.sql`
    - [ ] Execute SQL script and verify table structure
    - [ ] Create test script `src/etl/test_team_match_stats_data.py` (make 2-3 API calls, store data)
    - [ ] Execute test script and store API responses
    - [ ] Write SQL query to retrieve stored data and compare with original API responses
    - [ ] Verify data integrity and field mapping accuracy

11. **Continue with Player Season Stats API and Staging Table**
    - [ ] Review `/player-season-stats` endpoint documentation
    - [ ] Analyze API response structure and field types
    - [ ] Design staging table schema for player season stats data
    - [ ] Create `src/database/create_player_season_stats_staging.sql`
    - [ ] Execute SQL script and verify table structure
    - [ ] Create test script `src/etl/test_player_season_stats_data.py` (make 2-3 API calls, store data)
    - [ ] Execute test script and store API responses
    - [ ] Write SQL query to retrieve stored data and compare with original API responses
    - [ ] Verify data integrity and field mapping accuracy

12. **Continue with Player Match Stats API and Staging Table**
    - [ ] Review `/player-match-stats` endpoint documentation
    - [ ] Analyze API response structure and field types
    - [ ] Design staging table schema for player match stats data
    - [ ] Create `src/database/create_player_match_stats_staging.sql`
    - [ ] Execute SQL script and verify table structure
    - [ ] Create test script `src/etl/test_player_match_stats_data.py` (make 2-3 API calls, store data)
    - [ ] Execute test script and store API responses
    - [ ] Write SQL query to retrieve stored data and compare with original API responses
    - [ ] Verify data integrity and field mapping accuracy

13. **Finish with All Players Match Stats API and Staging Table**
    - [ ] Review `/all-players-match-stats` endpoint documentation
    - [ ] Analyze API response structure and field types
    - [ ] Design staging table schema for all players match stats data
    - [ ] Create `src/database/create_all_players_match_stats_staging.sql`
    - [ ] Execute SQL script and verify table structure
    - [ ] Create test script `src/etl/test_all_players_match_stats_data.py` (make 2-3 API calls, store data)
    - [ ] Execute test script and store API responses
    - [ ] Write SQL query to retrieve stored data and compare with original API responses
    - [ ] Verify data integrity and field mapping accuracy

## 🛠️ Technical Details

### Data Areas to Cover:
1. **Countries** - `/countries` endpoint
2. **Leagues** - `/leagues` endpoint  
3. **League Seasons** - `/league-seasons` endpoint
4. **League Season Details** - `/league-season-details` endpoint
5. **League Standings** - `/league-standings` endpoint
6. **Teams** - `/teams` endpoint
7. **Players** - `/players` endpoint
8. **Matches** - `/matches` endpoint
9. **Team Season Stats** - `/team-season-stats` endpoint
10. **Team Match Stats** - `/team-match-stats` endpoint
11. **Player Season Stats** - `/player-season-stats` endpoint
12. **Player Match Stats** - `/player-match-stats` endpoint
13. **All Players Match Stats** - `/all-players-match-stats` endpoint

### Files to Create:
**Database Scripts:**
- `src/database/create_countries_staging.sql`
- `src/database/create_leagues_staging.sql`
- `src/database/create_league_seasons_staging.sql`
- `src/database/create_league_season_details_staging.sql`
- `src/database/create_league_standings_staging.sql`
- `src/database/create_teams_staging.sql`
- `src/database/create_players_staging.sql`
- `src/database/create_matches_staging.sql`
- `src/database/create_team_season_stats_staging.sql`
- `src/database/create_team_match_stats_staging.sql`
- `src/database/create_player_season_stats_staging.sql`
- `src/database/create_player_match_stats_staging.sql`
- `src/database/create_all_players_match_stats_staging.sql`

**Test Scripts:**
- `src/etl/test_countries_data.py`
- `src/etl/test_leagues_data.py`
- `src/etl/test_league_seasons_data.py`
- `src/etl/test_league_season_details_data.py`
- `src/etl/test_league_standings_data.py`
- `src/etl/test_teams_data.py`
- `src/etl/test_players_data.py`
- `src/etl/test_matches_data.py`
- `src/etl/test_team_season_stats_data.py`
- `src/etl/test_team_match_stats_data.py`
- `src/etl/test_player_season_stats_data.py`
- `src/etl/test_player_match_stats_data.py`
- `src/etl/test_all_players_match_stats_data.py`

### Database Configuration:
- **Database**: PostgreSQL (via `DATABASE_URL` environment variable)
- **Schema**: `staging` (as defined in `config/config.yaml`)
- **Connection**: Using `psycopg2` with environment variables from `.env`
- **Tables**: All staging tables follow pattern `staging.[table_name]`
- **Standard Fields**: All tables include `created_at`, `updated_at`, and `raw_data JSONB`

### Dependencies:
- PostgreSQL database access via `DATABASE_URL`
- API documentation from TASK-001
- FBR API client configuration (`src/api/fbr_client.py`)
- Environment variables loaded from `.env` file

### FBR Client Setup Requirements:
Each task must include proper FBR client setup and verification:

1. **Client Method Implementation**: Ensure the corresponding method exists in `FBRClient` class
2. **Endpoint Configuration**: Verify endpoint is properly configured in `src/api/endpoint_config.py`
3. **Client Testing**: Test the client method with real API calls before proceeding
4. **Error Handling**: Validate that the client handles API errors appropriately
5. **Rate Limiting**: Confirm rate limiting is working correctly (6-second delay)

### Client Verification Steps:
- [ ] Verify `FBRClient` method exists and accepts correct parameters
- [ ] Test client method with known working parameters
- [ ] Validate response structure matches API documentation
- [ ] Confirm rate limiting is enforced
- [ ] Test error handling with invalid parameters

### Missing Client Methods to Implement:
- **TASK-002-10**: `FBRClient.get_team_match_stats(team_id, league_id, season_id)` - needs implementation
- **TASK-002-13**: `FBRClient.get_all_players_match_stats(league_id, season_id)` - needs implementation

## 📚 Resources
- [API Endpoint Documentation](src/api/endpoint_documentation/)
- [Existing database scripts](src/database/)
- [PostgreSQL documentation](https://www.postgresql.org/docs/)

## 🚧 Blockers
- None currently identified

## 💡 Notes
This task establishes the data storage foundation. The staging tables will be the landing zone for all API data before it's processed into the data warehouse. We should design these tables to be flexible enough to handle variations in API responses while maintaining data integrity.

### Data Verification Requirements:
- **SQL queries should retrieve the exact same data** that was originally received from the API
- **Compare field-by-field** to ensure no data loss or transformation errors
- **Verify data types** are correctly mapped (strings, integers, dates, etc.)
- **Check for null values** and ensure they're handled properly
- **Validate JSON fields** are stored correctly (arrays, objects, nested data)
- **Confirm audit fields** (created_at, updated_at) are populated correctly

### Example Verification Workflow:
```python
# 1. Make API call
api_response = client.get_countries()

# 2. Store in database
insert_countries_data(api_response)

# 3. Write SQL query to retrieve
sql_result = """
SELECT * FROM staging.countries 
WHERE country_code IN ('ENG', 'ESP', 'GER')
ORDER BY country_code;
"""

# 4. Compare api_response vs sql_result
# 5. Verify field mapping, data types, null handling, etc.
```

---
*Created: 2025-07-31*
*Last Updated: 2025-07-31*
*Status: TODO* 