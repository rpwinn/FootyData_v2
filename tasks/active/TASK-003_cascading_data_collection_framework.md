# TASK-003: Cascading Data Collection Framework

## Task Overview
- **Task ID**: TASK-003
- **Created**: 2025-07-31
- **Status**: IN_PROGRESS
- **Priority**: HIGH
- **Epic**: EPIC-002 (Create Staging Tables for API Data)
- **Dependencies**: TASK-002-01, TASK-002-02, TASK-002-03 (Completed staging tables)

## 🎯 Objective
Create a flexible, configuration-driven data collection framework that allows cascading collection of football data based on country/league scope and time periods. This will enable efficient, targeted data collection for any subset of the football world.

## 📋 Acceptance Criteria
- [x] Refactor core ETL scripts to accept optional filters (countries, leagues, league seasons)
- [ ] Refactor remaining ETL scripts (10 more scripts)
- [x] Create configuration system for collection scopes
- [x] Implement smart cascading collector with database freshness checking
- [ ] Implement master collection orchestrator script
- [x] Create predefined collection scopes (european_majors, etc.)
- [ ] Add command-line interface for custom collection requests
- [x] Implement proper dependency resolution (countries → leagues → seasons)
- [ ] Add progress tracking and error recovery for cascading collections

## 🔍 Context
Currently, we have separate scripts for countries, leagues, and league seasons that work independently. We need a unified framework that can orchestrate cascading collection based on user-defined scopes and time periods.

## 📝 Implementation Steps

### Phase 1: Refactor Existing Scripts
1. **Parameterize Countries Script** ✅ **COMPLETE**
   - [x] Create `load_countries_data.py` with `country_codes=None` parameter
   - [x] Add filtering logic for specific countries vs. all countries
   - [x] Maintain backward compatibility
   - [x] Add ON CONFLICT handling for upserts

2. **Parameterize Leagues Script** ✅ **COMPLETE**
   - [x] Create `load_leagues_data.py` with `country_codes=None` parameter
   - [x] Add logic to query countries table for league collection
   - [x] Implement country-to-league dependency resolution
   - [x] Add ON CONFLICT handling for upserts

3. **Parameterize League Seasons Script** ✅ **COMPLETE**
   - [x] Create `load_league_seasons_data.py` with `league_ids=None` parameter
   - [x] Add logic to query leagues table for season collection
   - [x] Implement league-to-season dependency resolution
   - [x] Add time period filtering (2024, 2020s, etc.)
   - [x] Add selective update logic with `update_only` parameter
   - [x] Add ON CONFLICT handling for upserts

4. **Parameterize League Season Details Script**
   - [ ] Create `load_league_season_details_data.py` with `league_ids=None` and `season_ids=None` parameters
   - [ ] Add logic to query league_seasons table for details collection
   - [ ] Implement league-season-to-details dependency resolution
   - [ ] Add time period filtering
   - [ ] Add selective update logic

5. **Parameterize League Standings Script**
   - [ ] Create `load_league_standings_data.py` with `league_ids=None` and `season_ids=None` parameters
   - [ ] Add logic to query league_seasons table for standings collection
   - [ ] Implement league-season-to-standings dependency resolution
   - [ ] Add time period filtering
   - [ ] Add selective update logic

6. **Parameterize Teams Script**
   - [ ] Create `load_teams_data.py` with `team_ids=None` parameter
   - [ ] Add logic to query leagues table for team collection
   - [ ] Implement league-to-teams dependency resolution
   - [ ] Add selective update logic

7. **Parameterize Players Script**
   - [ ] Create `load_players_data.py` with `player_ids=None` parameter
   - [ ] Add logic to query teams table for player collection
   - [ ] Implement team-to-players dependency resolution
   - [ ] Add selective update logic

8. **Parameterize Matches Script**
   - [ ] Create `load_matches_data.py` with `league_ids=None` and `season_ids=None` parameters
   - [ ] Add logic to query league_seasons table for matches collection
   - [ ] Implement league-season-to-matches dependency resolution
   - [ ] Add time period filtering
   - [ ] Add selective update logic

9. **Parameterize Team Season Stats Script**
   - [ ] Create `load_team_season_stats_data.py` with `league_ids=None` and `season_ids=None` parameters
   - [ ] Add logic to query league_seasons table for team stats collection
   - [ ] Implement league-season-to-team-stats dependency resolution
   - [ ] Add time period filtering
   - [ ] Add selective update logic

10. **Parameterize Team Match Stats Script**
    - [ ] Create `load_team_match_stats_data.py` with `team_ids=None` and `match_ids=None` parameters
    - [ ] Add logic to query teams and matches tables for team match stats collection
    - [ ] Implement team-match-to-stats dependency resolution
    - [ ] Add selective update logic

11. **Parameterize Player Season Stats Script**
    - [ ] Create `load_player_season_stats_data.py` with `player_ids=None` and `season_ids=None` parameters
    - [ ] Add logic to query players and league_seasons tables for player stats collection
    - [ ] Implement player-season-to-stats dependency resolution
    - [ ] Add time period filtering
    - [ ] Add selective update logic

12. **Parameterize Player Match Stats Script**
    - [ ] Create `load_player_match_stats_data.py` with `match_ids=None` parameter
    - [ ] Add logic to query matches table for player match stats collection
    - [ ] Implement match-to-player-stats dependency resolution
    - [ ] Add selective update logic

13. **Parameterize All Players Match Stats Script**
    - [ ] Create `load_all_players_match_stats_data.py` with `league_ids=None` and `season_ids=None` parameters
    - [ ] Add logic to query league_seasons table for all players stats collection
    - [ ] Implement league-season-to-all-players-stats dependency resolution
    - [ ] Add time period filtering
    - [ ] Add selective update logic

### Phase 2: Configuration System
4. **Create Configuration Structure**
   - [x] Create `config/collection_config.yaml` with predefined scopes
   - [x] Define scope templates (european_majors, english_football, european_cups, premier_league_only)
   - [x] Add time period definitions and validation
   - [x] Add season/year configuration (default_2024, 2020s)
   - [x] Remove worldwide scope as requested
   - [x] Remove Belgium from european_majors as requested

5. **Implement Configuration Loader**
   - [x] Create `src/utils/collection_config.py` for config management
   - [x] Add scope validation and dependency checking
   - [x] Implement custom scope creation functionality
   - [x] Add season matching functionality with regex patterns

### Phase 3: Master Collection Script
6. **Create Smart Cascading Collector**
   - [x] Create `src/etl/smart_cascading_collector.py` with database freshness checking
   - [x] Implement countries freshness check (database vs API)
   - [x] Implement leagues freshness check using `last_season` field comparison
   - [x] Add smart dependency resolution (only call APIs when needed)
   - [x] Create European majors collection demonstration

7. **Create Collection Orchestrator** ✅ **PARTIAL - Core Scripts Only**
   - [x] Create `src/etl/collect_football_data.py` master script
   - [x] Implement dependency resolution logic for countries, leagues, league seasons
   - [x] Add progress tracking and error handling
   - [x] Add CLI interface with dry-run, force, and verbose options
   - [ ] **TODO**: Add remaining loading scripts as they are parameterized
   - [ ] **TODO**: Implement dynamic freshness checking for all data types

7. **Add Command-Line Interface**
   - [ ] Create CLI for scope selection and custom parameters
   - [ ] Add dry-run mode for testing
   - [ ] Implement verbose logging and progress reporting

### Phase 4: Testing and Documentation
8. **Create Test Scenarios**
   - [ ] Test worldwide collection (all countries)
   - [ ] Test european_majors scope
   - [ ] Test custom country selection
   - [ ] Test time period filtering

9. **Documentation and Examples**
   - [ ] Create usage examples and documentation
   - [ ] Add configuration examples
   - [ ] Document dependency relationships

## 🛠️ Technical Details

### Configuration Structure:
```yaml
# config/collection_config.yaml
collection_scopes:
  worldwide:
    description: "All countries and leagues"
    countries: null  # All countries
    time_period: null  # All time periods
    
  european_majors:
    description: "Major European leagues"
    countries: ['ENG', 'GER', 'FRA', 'ESP', 'ITA']
    time_period:
      start_season: "2020-2021"
      end_season: "2024-2025"
      
  premier_league_only:
    description: "English Premier League only"
    countries: ['ENG']
    leagues: ['Premier League']
    time_period:
      start_season: "2023-2024"
      end_season: "2024-2025"
```

### Script Function Signatures:
```python
def load_countries_data(country_codes=None, config=None):
    """Load countries with optional filtering"""
    
def load_leagues_data(country_codes=None, config=None):
    """Load leagues with optional country filtering"""
    
def load_league_seasons_data(league_ids=None, time_period=None, config=None):
    """Load seasons with optional league and time filtering"""
    
def collect_football_data(scope_name=None, custom_config=None):
    """Main collection orchestrator"""
```

### CLI Interface:
```bash
# Use predefined scope
python3 src/etl/collect_football_data.py --scope european_majors

# Custom country selection
python3 src/etl/collect_football_data.py --countries ENG,GER,FRA

# Custom scope with time period
python3 src/etl/collect_football_data.py --countries ENG --start-season 2023-2024 --end-season 2024-2025

# Dry run mode
python3 src/etl/collect_football_data.py --scope worldwide --dry-run
```

## 📊 Expected Results

### Success Metrics:
- **Flexibility**: Support any country/league combination
- **Efficiency**: Only collect required data
- **Reliability**: Proper error handling and recovery
- **Usability**: Simple CLI interface for common use cases

### Files to Create:
- `config/collection_config.yaml`
- `src/utils/collection_config.py`
- `src/etl/collect_football_data.py`
- `src/etl/load_countries_data.py` (refactored)
- `src/etl/load_leagues_data.py` (refactored)
- `src/etl/load_league_seasons_data.py` (refactored)

## 📚 Resources
- [Countries API Documentation](src/api/endpoint_documentation/countries.md)
- [Leagues API Documentation](src/api/endpoint_documentation/leagues.md)
- [League Seasons API Documentation](src/api/endpoint_documentation/league_seasons.md)
- [Existing ETL Scripts](src/etl/)

## 🚧 Blockers
- Requires completion of TASK-002-01, TASK-002-02, TASK-002-03
- Need to maintain backward compatibility with existing scripts

## 💡 Notes
This framework will enable efficient data collection for any scope, from worldwide to specific leagues. The configuration-driven approach makes it easy to add new collection scopes and modify existing ones without code changes.

---
*Created: 2025-07-31*
*Last Updated: 2025-07-31*
*Status: IN_PROGRESS* 