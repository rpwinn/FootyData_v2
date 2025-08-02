# FootyData_v2

A football data collection system using the FBR API to gather comprehensive football statistics and store them in a PostgreSQL database with a proper data warehouse architecture.

## ⚠️ Important Setup Notes

### Python Version
- **Always use `python3`** instead of `python` for running scripts
- The `python` command may not be available or may point to Python 2
- Example: `python3 src/etl/test_league_seasons_data.py`

### Database Connection
- **DATABASE_URL environment variable only works with `python3`**
- The `psycopg2` library requires Python 3 for proper environment variable handling
- Always run database scripts with `python3` to ensure proper connection

### Example Usage
```bash
# ✅ Correct way
python3 src/etl/test_league_seasons_data.py

# ❌ May not work
python src/etl/test_league_seasons_data.py
```

## Overview

This project replaces web scraping with API-based data collection using the FBR API (https://fbrapi.com/documentation) to gather football data from fbref.com. The system implements a three-schema data warehouse architecture:

- **Staging Schema**: Raw API data storage for validation and debugging
- **Dimension Schema**: Reference data (countries, leagues, teams, players) with proper normalization
- **Fact Schema**: Event data (matches, player performances) optimized for analytics

## Architecture

### 🏗️ Three-Schema Data Warehouse

#### **Staging Schema** (`staging.*`)
```sql
-- Raw API responses with denormalized data
staging.countries        -- Raw country data ✅
staging.leagues          -- Raw league data ✅
staging.league_seasons   -- Raw league seasons data ✅
staging.matches          -- Raw match data (includes team names)
staging.players          -- Raw player data
staging.teams            -- Raw team data
```

**Purpose**: Store raw, unprocessed data exactly as it comes from the FBR API
**Characteristics**: 
- Contains JSONB columns with full API responses
- Preserves denormalized data (e.g., team names in match records)
- Used for data validation and debugging
- Temporary storage before processing

#### **Dimension Schema** (`dim.*`)
```sql
-- Reference data with proper normalization
dim.countries            -- Country reference data
dim.leagues              -- League reference data
dim.seasons              -- Season reference data
dim.teams                -- Team reference data (SCD Type 2)
dim.players               -- Player reference data (SCD Type 2)
```

**Note**: Team entities are dimension data, but team-related events (rosters, schedules) are fact data.

**Purpose**: Store dimensional data - the "who, what, where, when" reference information
**Characteristics**:
- **Denormalized** (contains all related data in one table)
- **Slowly Changing Dimensions** (SCD) - tracks changes over time
- Used for **lookups** and **filtering**
- Contains **descriptive attributes** (names, codes, metadata)

#### **Fact Schema** (`fact.*`)
```sql
-- Event data optimized for analytics
fact.matches             -- Match events (normalized, team IDs only)
fact.player_match_performances  -- Player performance facts
fact.goalkeeper_performances    -- Goalkeeper performance facts
fact.team_rosters        -- Team composition facts
fact.team_schedules      -- Team fixture facts
```

**Purpose**: Store factual data - the "what happened" events and measurements
**Characteristics**:
- **Normalized** (minimal redundancy, proper foreign keys)
- Contains **measurements** and **metrics**
- **High volume** (many rows)
- Used for **analytics** and **reporting**

### 📊 Data Collection Summary

#### **Completed Collections**
- **Countries**: All countries from `/countries` endpoint ✅
- **Leagues**: All leagues from `/leagues` endpoint (by country) ✅
- **League Seasons**: 1,740 seasons from 107 leagues via `/league-seasons` endpoint ✅

### 🏗️ **Nested JSON Handling**

The FBR API often returns nested JSON structures that require proper normalization into separate staging tables:

#### **Example: `/teams` Endpoint**
        ```json
        {
          "team_roster": {
            "data": [
              {
                "player": "Rodri",
                "player_id": "6434f10d",
                "nationality": "ESP",
                "position": "MF",
                "age": 27,
                "mp": 34,
                "starts": 34
              }
            ]
          },
          "team_schedule": {
            "data": [
              {
                "date": "2023-08-06",
                "match_id": "10e5c045",
                "league_name": "Community Shield",
                "league_id": 602,
                "opponent": "Arsenal",
                "result": "D",
                "gf": 1,
                "ga": 1
              }
            ]
          }
        }
        ```

        **Solution**: Create separate staging tables:
        - `staging.team_rosters` - For player roster data
        - `staging.team_schedules` - For match schedule data

#### **Example: `/matches` Endpoint**
        The matches endpoint has **two distinct response formats** based on parameters:

        **League Matches (no team_id)**:
        ```json
        {
          "data": [
            {
              "match_id": "089c98e2",
              "date": "2022-07-30",
              "home": "Wycombe",
              "home_team_id": "43c2583e",
              "away": "Burton Albion",
              "away_team_id": "b09787c5",
              "venue": "Adams Park",
              "attendance": "5,772"
            }
          ]
        }
        ```

        **Team Matches (with team_id)**:
        ```json
        {
          "data": [
            {
              "match_id": "09d8a999",
              "date": "2022-08-06",
              "home_away": "Home",
              "opponent": "Southampton",
              "opponent_id": "33c895d4",
              "result": "W",
              "gf": 4,
              "ga": 1,
              "formation": "3-4-3",
              "captain": "Hugo Lloris"
            }
          ]
        }
        ```

        **Solution**: Create separate staging tables:
        - `staging.league_matches` - For league-wide match data
        - `staging.team_matches` - For team-specific match data

#### **Design Pattern**
        When encountering nested JSON structures or parameter-based response formats:
        1. **Identify distinct data entities** within the response
        2. **Create separate staging tables** for each entity type
        3. **Maintain referential integrity** through shared keys (e.g., `team_id`, `match_id`)
        4. **Preserve raw data** in JSONB columns for debugging
        5. **Document the relationship** between the tables
        6. **Handle parameter-based responses** by creating separate tables for different API call patterns

This pattern ensures proper normalization while maintaining data integrity and debugging capabilities.

#### **Collection Statistics**
- **Countries**: 195 countries collected
- **Leagues**: 1,234 league entries (including international competitions across multiple countries)
- **League Seasons**: 1,740 seasons across 107 unique leagues
- **Top League**: Premier League (ENG) with 127 seasons

### 🔄 ETL Strategy

The FBR API returns denormalized data (e.g., team names included in match responses). Our ETL process handles this properly:

#### **Step 1: Extract & Stage**
```python
# Store raw API response in staging (preserves denormalized data)
staging.matches:
- match_id, date, home_team_id, away_team_id
- home_team_name, away_team_name  # Denormalized from API
- home_score, away_score, venue
- raw_data JSONB  # Full API response
```

#### **Step 2: Transform Dimensions**
```python
# Extract team data from staging and load into dim.teams
# Handles SCD Type 2 for team name changes over time
dim.teams:
- team_id, team_name, league_id, country_code
- valid_from, valid_to, is_current
```

#### **Step 3: Transform Facts**
```python
# Load normalized facts (remove denormalized names)
fact.matches:
- match_id, date, home_team_id, away_team_id  # Only IDs
- home_score, away_score, venue
- FOREIGN KEY (home_team_id) REFERENCES dim.teams(team_id)
```

## Features

- **API-based data collection** - Uses FBR API instead of web scraping
- **Rate limiting compliance** - Respects API limits (1 request per 3 seconds)
- **Three-schema architecture** - Staging, dimension, and fact schemas
- **Proper normalization** - Handles denormalized API data correctly
- **Data quality** - Foreign key constraints and validation
- **Performance optimization** - Partitioning and indexing strategies
- **PostgreSQL support** - Local development with Railway deployment ready

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up local PostgreSQL database**

3. **Generate FBR API key**:
   ```bash
   curl -X POST https://fbrapi.com/generate_api_key
   ```

4. **Configure environment**:
   Create `.env` file with:
   ```
   FBR_API_KEY=your_api_key_here
   DATABASE_URL=postgresql://username:password@localhost:5432/footydata_v2
   ```

5. **Set up database schemas**:
   ```bash
   python3 setup_dimension_schema.py
   ```

## Project Structure

```
FootyData_v2/
├── src/
│   ├── api/           # FBR API client and endpoint configuration
│   ├── database/      # Database schemas and connections
│   ├── etl/           # ETL processes for staging → dim/fact
│   └── utils/         # Utility functions
├── config/            # Configuration files
├── data/              # Data storage
├── tests/             # Test files
└── docs/              # Documentation and analysis
```

## Usage

1. **Set up the database schemas**:
   ```bash
   python3 setup_dimension_schema.py
   ```

2. **Populate dimension tables**:
   ```bash
   python3 test_dimension_collection.py
   ```

3. **Run data collection**:
   ```bash
   python3 src/etl/dimension_data_collector.py
   ```

4. **Execute ETL processes** to transform staging → dim/fact

## Data Flow

```
FBR API → Staging (Raw) → Dimensions + Facts → Analytics
     ↓           ↓              ↓              ↓
Raw API    Denormalized   Normalized    Dashboard
Response   Data Storage   Data Model    Queries
```

## Rate Limiting

The FBR API enforces a 3-second delay between requests. All API calls automatically include this delay to ensure compliance and avoid being blocked.

## API Insights

### 🎯 **Critical Matches API Behavior**

The `/matches` endpoint has **two distinct data modes**:

**League Match Data** (no `team_id`):
```json
{
  "home_team_score": null,  // No scores available
  "away_team_score": null,  // No scores available
  "home": "Manchester Utd",
  "away": "Fulham"
}
```

**Team Match Data** (with `team_id`):
```json
{
  "result": "W",           // Team's result (W/L/D)
  "gf": 2,                 // Goals For (team's goals)
  "ga": 1,                 // Goals Against (opponent's goals)
  "opponent": "Fulham",    // Opponent team
  "home_away": "Home"      // Team's perspective
}
```

**Solution**: Collect team-specific match data to get actual scores!

## Data Categories

Based on our analysis of FBR API endpoints:

### 📊 **Raw Facts Data** (3 endpoints)
- `/matches` - Match events, scores, venues
  - **CRITICAL**: Use `team_id` parameter to get actual scores
  - League matches (no `team_id`) return `None` scores
  - Team matches (with `team_id`) return `gf`/`ga` scores
- `/all-players-match-stats` - Player performance per match
- `/league-standings` - Current standings

## Complete FBR API Endpoints (15 total)

### ✅ **Working Endpoints (10)**
1. **`/countries`** - GET method to retrieve football-related meta-data for all available countries
2. **`/leagues`** - GET method to retrieve meta-data for all unique leagues associated with a specified country
3. **`/league-seasons`** - GET method to retrieve all season ids for a specific league id
4. **`/teams`** - GET method to retrieve team roster and schedule data
5. **`/players`** - GET method to retrieve player meta-data
6. **`/matches`** - GET method to retrieve match meta-data
7. **`/team-season-stats`** - GET method to retrieve season-level team statistical data for a specified league and season
8. **`/player-season-stats`** - GET method to retrieve aggregate season stats for all players for a team-league-season
9. **`/all-players-match-stats`** - GET method to retrieve match stats for all players in a match

### ❌ **Failing Endpoints (1)**
10. **`/league-standings`** - GET method to retrieve all standings tables for a given league and season id (500 Server Error)

### 🔧 **Missing Endpoints (3)**
11. **`/league-season-details`** - GET method to retrieve meta-data for a specific league id and season id
12. **`/team-match-stats`** - GET method to retrieve match-level team statistical data for a specified team, league and season
13. **`/player-match-stats`** - GET method to retrieve matchlog data for a given player-league-season

### 🛠️ **Utility Endpoints (2)**
14. **`/documentation`** - GET method to view FBR API documentation
15. **`/generate_api_key`** - POST method to generate a new API key

### 📋 **Dimensional Data** (5 endpoints)
- `/countries` - Country metadata
- `/leagues` - League definitions
- `/league-seasons` - Season definitions
- `/teams` - Team reference data (entities)
- `/players` - Player metadata

### 📈 **Aggregated Data** (2 endpoints)
- `/team-season-stats` - Team performance summaries
- `/player-season-stats` - Player performance summaries

## Data Completeness Issues

### Current Known Issues

#### ISSUE-001: League Season Details API Endpoint Failures
- **Status**: Open (API Provider Issue)
- **Severity**: High
- **Impact**: 54% failure rate for league season details collection
- **Details**: The `/league-season-details` endpoint returns 500 Internal Server Errors for major domestic leagues (Premier League, La Liga, Serie A, Bundesliga, Ligue 1)
- **Workaround**: Focus on international competitions and smaller leagues that work properly
- **Documentation**: See `data_issues/ISSUE-001_league_season_details_missing_data.md`

### Data Collection Success Rates
- **Countries**: 100% (195/195 countries)
- **Leagues**: 100% (1,234 league entries)
- **League Seasons**: 100% (1,740 seasons collected)
- **League Season Details**: 46% (800/1,740 combinations successful)

### Monitoring
All data completeness issues are tracked in the `data_issues/` directory with detailed investigation reports and resolution plans.

## 🛠️ Common Issues

### Database Connection
- **DATABASE_URL environment variable only works with `python3`**
- The `psycopg2` library requires Python 3 for proper environment variable handling
- Always run database scripts with `python3` to ensure proper connection

## License

MIT 