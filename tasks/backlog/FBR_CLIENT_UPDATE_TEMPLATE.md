# FBR Client Update Template for Backlog Tasks

## 📋 Tasks That Need FBR Client Updates:

### TASK-002-03: League Seasons
- **Client Method**: `FBRClient.get_league_seasons(league_id: str)`
- **Parameters**: `league_id` (required string)
- **Dependencies**: Leagues staging table

### TASK-002-04: League Season Details
- **Client Method**: `FBRClient.get_league_season_details(league_id: int, season_id: Optional[str] = None)`
- **Parameters**: `league_id` (required int), `season_id` (optional string)
- **Dependencies**: League seasons staging table

### TASK-002-05: League Standings
- **Client Method**: `FBRClient.get_league_standings(league_id: int, season_id: Optional[str] = None)`
- **Parameters**: `league_id` (required int), `season_id` (optional string)
- **Dependencies**: League seasons staging table

### TASK-002-06: Teams
- **Client Method**: `FBRClient.get_teams(team_id: str, season_id: Optional[str] = None)`
- **Parameters**: `team_id` (required string), `season_id` (optional string)
- **Dependencies**: None (independent)

### TASK-002-07: Players
- **Client Method**: `FBRClient.get_players(player_id: str)`
- **Parameters**: `player_id` (required string)
- **Dependencies**: None (independent)

### TASK-002-08: Matches
- **Client Method**: `FBRClient.get_matches(league_id: str, season_id: str, team_id: Optional[str] = None)`
- **Parameters**: `league_id` (required string), `season_id` (required string), `team_id` (optional string)
- **Dependencies**: League seasons staging table

### TASK-002-09: Team Season Stats
- **Client Method**: `FBRClient.get_team_season_stats(league_id: int, season_id: Optional[str] = None)`
- **Parameters**: `league_id` (required int), `season_id` (optional string)
- **Dependencies**: League seasons staging table

### TASK-002-10: Team Match Stats
- **Client Method**: `FBRClient.get_team_match_stats()` (needs to be implemented)
- **Parameters**: `team_id`, `league_id`, `season_id` (all required)
- **Dependencies**: Teams + League seasons staging tables

### TASK-002-11: Player Season Stats
- **Client Method**: `FBRClient.get_player_season_stats(team_id: str, league_id: int, season_id: Optional[str] = None)`
- **Parameters**: `team_id` (required string), `league_id` (required int), `season_id` (optional string)
- **Dependencies**: Teams + League seasons staging tables

### TASK-002-12: Player Match Stats
- **Client Method**: `FBRClient.get_match_stats(match_id: str)` (for all players) or needs new method
- **Parameters**: `match_id` (required string)
- **Dependencies**: Matches staging table

### TASK-002-13: All Players Match Stats
- **Client Method**: `FBRClient.get_match_stats(match_id: str)` (same as above)
- **Parameters**: `league_id` (required int), `season_id` (required string)
- **Dependencies**: League seasons staging table

## 🔧 Implementation Steps for Each Task:

1. **Add FBR Client Setup Section**:
   ```
   4. **FBR Client Setup and Verification**
      - [ ] Verify `FBRClient.[method_name]()` method exists and works correctly
      - [ ] Test client method with real API calls
      - [ ] Validate response structure matches API documentation
      - [ ] Confirm rate limiting is enforced (6-second delay between calls)
      - [ ] Test error handling with invalid parameters
   ```

2. **Update Implementation Steps**:
   ```
   5. **Implement and Test**
      - [ ] Execute SQL script and verify table structure
      - [ ] Create test script `src/etl/test_[table_name]_data.py`
      - [ ] Use `FBRClient.[method_name]()` to make API calls
      - [ ] Store API responses in staging table
      - [ ] Write SQL query to retrieve stored data
      - [ ] Compare original API responses with SQL query results
      - [ ] Verify data integrity and field mapping accuracy
   ```

3. **Add FBR Client Method Details**:
   ```
   ### FBR Client Method:
   - **Method**: `FBRClient.[method_name](parameters)`
   - **Parameters**: [list parameters with types]
   - **Returns**: `Dict[str, Any]` with [endpoint] data
   - **Rate Limiting**: 6-second delay between calls
   - **Error Handling**: Returns `{"error": str(e)}` on failure
   ```

4. **Update Dependencies**:
   ```
   - FBR API client configuration (`src/api/fbr_client.py`)
   ```

## ⚠️ Missing Client Methods:
- **TASK-002-10**: Team Match Stats - needs new method
- **TASK-002-12**: Player Match Stats - may need new method
- **TASK-002-13**: All Players Match Stats - may need new method

## 📝 Notes:
- All existing methods in `FBRClient` should be tested before use
- Rate limiting (6-second delay) must be verified
- Error handling should be tested with invalid parameters
- Response structure validation is critical 