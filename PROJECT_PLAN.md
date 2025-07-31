# FootyData_v2 Project Plan

## 🎯 Project Overview

Build a football data collection system using the FBR API (https://fbrapi.com/documentation) to store data in a PostgreSQL database with a proper data warehouse architecture. The system implements a three-schema approach: staging (raw data), dimensions (reference data), and facts (event data).

### Goals
- Replace web scraping with API-based data collection
- Implement proper data warehouse architecture (staging → dim/fact)
- Handle denormalized API data correctly through ETL
- Create scalable, performant database design
- Develop comprehensive ETL processes

## 🏗️ Three-Schema Architecture

### **Staging Schema** (`staging.*`)
**Purpose**: Raw API data storage for validation and debugging

```sql
-- Raw API responses with denormalized data
staging.matches          -- Raw match data (includes team names)
staging.players          -- Raw player data
staging.countries        -- Raw country data
staging.leagues          -- Raw league data
staging.teams            -- Raw team data
staging.league_seasons   -- Raw season data
```

**Characteristics**:
- ✅ **Preserves denormalized data** (e.g., team names in match records)
- ✅ **JSONB storage** for full API responses
- ✅ **Validation source** for debugging and data quality checks
- ✅ **Temporary storage** before processing

### **Dimension Schema** (`dim.*`)
**Purpose**: Reference data with proper normalization

```sql
-- Reference data with proper normalization
dim.countries            -- Country reference data
dim.leagues              -- League reference data
dim.seasons              -- Season reference data
dim.teams                -- Team reference data (SCD Type 2)
dim.players               -- Player reference data (SCD Type 2)
```

**Characteristics**:
- ✅ **Denormalized** for fast lookups
- ✅ **SCD Type 2** tracks changes over time
- ✅ **Small tables** optimized for filtering
- ✅ **Descriptive attributes** (names, codes, metadata)

### **Fact Schema** (`fact.*`)
**Purpose**: Event data optimized for analytics

```sql
-- Event data optimized for analytics
fact.matches             -- Match events (normalized, team IDs only)
fact.player_match_performances  -- Player performance facts
fact.goalkeeper_performances    -- Goalkeeper performance facts
fact.team_rosters        -- Team composition facts
fact.team_schedules      -- Team fixture facts
```

**Characteristics**:
- ✅ **Normalized** with proper foreign keys
- ✅ **High volume** data (many rows)
- ✅ **Optimized for aggregations**
- ✅ **Partitioned** for performance

## 🔄 ETL Strategy

### **The Challenge**
The FBR API returns denormalized data:
```json
{
  "match_id": "cc5b4244",
  "home": "Manchester Utd",        // ❌ Denormalized team name
  "home_team_id": "19538871",     // ✅ Team ID
  "away": "Fulham",               // ❌ Denormalized team name
  "away_team_id": "fd962109",     // ✅ Team ID
  "home_team_score": null,
  "away_team_score": null
}
```

### **Our Solution**

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

## 🎯 Critical API Insights

### **Matches API Behavior**

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

## 📊 Data Categories

### **Raw Facts Data** (5 endpoints)
- **Volume**: High (380+ matches/season, 8,360+ player stats/season)
- **Update Frequency**: Daily during season
- **Storage**: Normalized fact tables with partitioning

| Endpoint | Status | Volume | Characteristics |
|----------|--------|--------|----------------|
| `/matches` | ✅ Working | Large (380/season) | Match events, scores, venues |
| `/all-players-match-stats` | ✅ Working | Very Large (8,360/season) | Player performance per match |
| `/team-match-stats` | ✅ Working | Medium (380/season) | Match-level team statistics |
| `/player-match-stats` | ✅ Working | Large (8,360/season) | Individual player match data |
| `/league-standings` | ❌ Failing | Small (20/league) | Current standings |

### **Dimensional Data** (6 endpoints)
- **Volume**: Small to medium (225 countries, 500+ players/team)
- **Update Frequency**: Static to seasonal
- **Storage**: Denormalized dimension tables with SCD Type 2

| Endpoint | Status | Volume | Characteristics |
|----------|--------|--------|----------------|
| `/countries` | ✅ Working | Small (225) | Country metadata |
| `/leagues` | ✅ Working | Small | League definitions |
| `/league-seasons` | ✅ Working | Small (127) | Season definitions |
| `/league-season-details` | ✅ Working | Small | League-season metadata |
| `/teams` | ✅ Working | Medium (20/league) | Team reference data |
| `/players` | ✅ Working | Medium (500+/team) | Player metadata |

### **Aggregated Data** (2 endpoints)
- **Volume**: Medium (20 teams/league, 500+ players/team)
- **Update Frequency**: Weekly
- **Storage**: Aggregate tables with materialized views

| Endpoint | Status | Volume | Characteristics |
|----------|--------|--------|----------------|
| `/team-season-stats` | ✅ Working | Medium (20/league) | Team performance summaries |
| `/player-season-stats` | ✅ Working | Large (500+/team) | Player performance summaries |

## 📋 Complete API Endpoints Status

### **Utility Endpoints (2)**
1. **`/documentation`** - GET method to view FBR API documentation
2. **`/generate_api_key`** - POST method to generate a new API key

### **Data Extraction Endpoints (13)**

#### ✅ **Working Endpoints (12/13)**
1. **`/countries`** - Returns 225 countries with metadata
2. **`/leagues`** - Returns leagues organized by type and country
3. **`/league-seasons`** - Returns all seasons for a specific league
4. **`/league-season-details`** - Returns metadata for specific league and season
5. **`/teams`** - Returns team roster and schedule data
6. **`/players`** - Returns detailed player metadata
7. **`/matches`** - Returns match data (380 matches per season)
8. **`/team-season-stats`** - Returns comprehensive team statistics
9. **`/team-match-stats`** - Returns match-level team statistical data
10. **`/player-season-stats`** - Returns comprehensive player statistics
11. **`/player-match-stats`** - Returns matchlog data for a given player-league-season
12. **`/all-players-match-stats`** - Returns detailed player stats per match

#### ❌ **Failing Endpoints (1/13)**
13. **`/league-standings`** - Returns 500 Server Error (server-side issue)

## 📊 Endpoint Implementation Progress

### **4-Step Process for Each Endpoint**
For each API endpoint, we follow this systematic approach:
1. **📋 API Documentation** - Document endpoint structure, parameters, response format
2. **🧪 Pull Test Data** - Collect sample data and validate quality
3. **🗄️ Create Staging Table** - Design staging table schema with JSONB preservation
4. **💾 Insert Data** - Implement data collection and insertion with error handling

### **Progress Tracking Table**

| Endpoint | Priority | API Documentation | Pull Test Data | Create Staging Table | Insert Test Data | Full Extraction | Status |
|----------|----------|-------------------|-----------------|---------------------|-------------|----------------|---------|
| `/countries` | 1 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ **Complete** |
| `/leagues` | 1 | ✅ | ✅ | ✅ | ✅ | ❌ | ⚠️ **API Broken** |
| `/league-seasons` | 1 | ❌ | ❌ | ❌ | ❌ | ❌ | 🔄 **Next** |
| `/league-season-details` | 1 | ❌ | ❌ | ❌ | ❌ | ❌ | 📋 Planned |
| `/teams` | 1 | ❌ | ❌ | ❌ | ❌ | ❌ | 📋 Planned |
| `/players` | 1 | ❌ | ❌ | ❌ | ❌ | ❌ | 📋 Planned |
| `/matches` | 2 | ❌ | ❌ | ❌ | ❌ | ❌ | 📋 Planned |
| `/all-players-match-stats` | 2 | ❌ | ❌ | ❌ | ❌ | ❌ | 📋 Planned |
| `/team-season-stats` | 2 | ❌ | ❌ | ❌ | ❌ | ❌ | 📋 Planned |
| `/team-match-stats` | 2 | ❌ | ❌ | ❌ | ❌ | ❌ | 📋 Planned |
| `/player-season-stats` | 2 | ❌ | ❌ | ❌ | ❌ | ❌ | 📋 Planned |
| `/player-match-stats` | 2 | ❌ | ❌ | ❌ | ❌ | ❌ | 📋 Planned |
| `/league-standings` | 3 | ❌ | ❌ | ❌ | ❌ | ❌ | ⚠️ **Failing** |

**Legend:**
- ✅ **Complete** - Step finished
- 🔄 **In Progress** - Currently working on this step
- ❌ **Not Started** - Step not yet begun
- ⚠️ **Failing** - Endpoint has API issues

**Columns:**
- **API Documentation** - Document endpoint structure, parameters, response format
- **Pull Test Data** - Collect sample data and validate quality
- **Create Staging Table** - Design staging table schema with JSONB preservation
- **Insert Data** - Implement data collection and insertion with error handling
- **Full Extraction** - Complete data extraction for all countries/leagues (not just test data)

### **Implementation Priority**

#### **Priority 1: Dimensional Data (Foundation)**
1. **`/countries`** - Small, static data, good starting point
2. **`/leagues`** - Small, static data, foundation for other endpoints
3. **`/league-seasons`** - Small, seasonal data, needed for team/player data
4. **`/league-season-details`** - Small, metadata for specific league/season combinations
5. **`/teams`** - Medium volume, needed for match data
6. **`/players`** - Medium volume, needed for performance data

#### **Priority 2: Fact Data (Core Analytics)**
7. **`/matches`** - High volume, core match events
8. **`/all-players-match-stats`** - Very high volume, detailed performance
9. **`/team-season-stats`** - Medium volume, team summaries
10. **`/team-match-stats`** - Medium volume, match-level team data
11. **`/player-season-stats`** - High volume, player summaries
12. **`/player-match-stats`** - High volume, individual player match data

#### **Priority 3: Additional Data**
13. **`/league-standings`** - Currently failing, investigate later

## 🎯 Benefits of This Architecture

### **1. Data Quality**
- ✅ **Foreign key constraints** ensure referential integrity
- ✅ **SCD Type 2** tracks changes over time
- ✅ **Staging layer** preserves original data for validation
- ✅ **Proper normalization** removes redundancy

### **2. Performance**
- ✅ **Dimension tables**: Small, fast lookups
- ✅ **Fact tables**: Optimized for aggregations
- ✅ **Partitioning**: High-volume tables partitioned by date
- ✅ **Indexing**: Proper indexes for common query patterns

### **3. Maintainability**
- ✅ **Clear separation** of concerns (staging vs dim vs fact)
- ✅ **ETL processes** handle denormalized API data correctly
- ✅ **Scalable architecture** as data grows
- ✅ **Easy debugging** with staging layer

### **4. Analytics**
- ✅ **Star schema** for easy joins
- ✅ **Optimized queries** for dashboard and reporting
- ✅ **Materialized views** for common aggregations
- ✅ **Time-series analysis** support

## 📊 Data Structure Analysis

### **Match Data Structure**
- **Match metadata**: 13 fields (match_id, date, teams, scores, venue, etc.)
- **Player metadata**: 5 fields per player (player_id, name, country, number, age)
- **Player stats**: 5 categories with 84 total fields
  - Summary: 26 fields (goals, assists, shots, etc.)
  - Passing: 16 fields (pass completion, progressive passes, etc.)
  - Passing Types: 13 fields (live passes, dead balls, crosses, etc.)
  - Defense: 11 fields (tackles, interceptions, blocks, etc.)
  - Possession: 17 fields (touches, carries, take-ons, etc.)
  - Misc: 11 fields (fouls, cards, offsides, etc.)
- **Goalkeeper stats**: 22 fields per goalkeeper
- **Total unique fields**: ~140+ different data points per match

## 🔧 Technical Stack
- **API**: FBR API (https://fbrapi.com)
- **Database**: PostgreSQL (local → Railway)
- **Language**: Python
- **Key Libraries**: requests, psycopg2, pandas
- **Architecture**: Three-schema data warehouse

## 📋 Current Progress

### ✅ Completed
- [x] FBR API integration and testing (12/13 data endpoints working)
- [x] Data categorization analysis (raw facts, dimensional, aggregated)
- [x] Three-schema architecture design
- [x] ETL strategy for denormalized data
- [x] API endpoint configuration and documentation
- [x] Cleaned up old database creation scripts (starting fresh)
- [x] Local PostgreSQL database setup (`fbref`)
- [x] Database connection testing and verification

### 🔄 In Progress
- [ ] Endpoint-by-endpoint implementation (Phase 2)
- [ ] Starting with `/countries` endpoint

### 📋 Planned
- [ ] Complete all endpoint implementations
- [ ] Transformation layer development
- [ ] Performance optimization (partitioning, materialized views)
- [ ] Automated ETL scheduling
- [ ] Analytics dashboard
- [ ] Data quality monitoring

## 🎯 Next Steps

1. **Start with `/countries` endpoint**:
   - Document API structure
   - Pull test data
   - Create staging table
   - Insert data
2. **Continue with remaining endpoints** in priority order
3. **Implement transformation layer** once all staging is complete
4. **Add foreign key constraints** and data validation
5. **Test query performance** and optimize
6. **Implement automated ETL scheduling**
7. **Create analytics dashboard**

## ⚡ Rate Limiting
- FBR API allows 1 request every 3 seconds
- Implemented proper delays to avoid being blocked
- Consider batch processing for efficiency

## 🎉 Summary

This revised approach provides a **structured, manageable path** to building the football data analytics system by:

1. **Breaking down the work** into endpoint-by-endpoint implementation
2. **Ensuring quality** through proper documentation and testing at each step
3. **Building incrementally** with staging tables first, then transformations
4. **Maintaining focus** on one endpoint at a time
5. **Creating a solid foundation** before moving to complex transformations

The system is designed to **evolve systematically** as we complete each endpoint and **scale** as data volumes grow. 