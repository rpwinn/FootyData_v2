# FootyData_v2 Project Plan

## Overview
Build a new football data scraper using the FBR API (https://fbrapi.com/documentation) to store data in a PostgreSQL database. Initially using local database for development, with plans to migrate to Railway-hosted PostgreSQL.

## Goals
- Replace web scraping with API-based data collection
- Create a staging database for raw scraped data
- Design a clear database architecture
- Develop ETL processes to transform data into better formats

## Project Structure

### Phase 1: Database Setup
1. **Build staging database** - Local PostgreSQL database for initial development
2. **Design database schema** - Plan tables for raw API data storage
3. **Set up database connection** - Configure local PostgreSQL connection

### Phase 2: API Integration
1. **FBR API setup** - Generate API key and test connectivity
2. **Data extraction** - Extract various data types from FBR API:
   - Countries and leagues metadata
   - League seasons and standings
   - Teams and players
   - Match statistics
   - Player statistics
3. **Rate limiting compliance** - Implement 3-second delays between requests

### Phase 3: ETL Development
1. **Raw data storage** - Store API responses in staging tables
2. **Data transformation** - Clean and structure raw data
3. **Final database schema** - Design normalized tables for analysis
4. **ETL pipeline** - Transform staging data into final format

## Technical Stack
- **API**: FBR API (https://fbrapi.com)
- **Database**: PostgreSQL (local → Railway)
- **Language**: Python
- **Key Libraries**: requests, psycopg2, pandas

## API Endpoints to Target
Based on FBR API documentation:
- `/countries` - Get available countries
- `/leagues` - Get leagues by country
- `/league-seasons` - Get seasons for leagues
- `/league-standings` - Get standings data
- `/teams` - Get team rosters and schedules
- `/players` - Get player metadata
- `/team-season-stats` - Get team statistics
- `/player-season-stats` - Get player statistics
- `/matches` - Get match metadata

## Rate Limiting
- FBR API allows 1 request every 3 seconds
- Must implement proper delays to avoid being blocked
- Consider batch processing for efficiency

## Next Steps
1. Set up local PostgreSQL database
2. Generate FBR API key
3. Create basic API client
4. Design initial database schema
5. Test with small dataset 