# FootyData_v2

A football data collection system using the FBR API to gather comprehensive football statistics and store them in a PostgreSQL database.

## Overview

This project replaces web scraping with API-based data collection using the FBR API (https://fbrapi.com/documentation) to gather football data from fbref.com. The system stores raw data in a staging database and provides ETL processes to transform it into analysis-ready formats.

## Features

- **API-based data collection** - Uses FBR API instead of web scraping
- **Rate limiting compliance** - Respects API limits (1 request per 3 seconds)
- **Staging database** - Raw data storage for initial processing
- **ETL pipeline** - Transform raw data into analysis-ready formats
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

## Project Structure

```
FootyData_v2/
├── src/
│   ├── api/           # FBR API client
│   ├── database/      # Database models and connections
│   ├── etl/           # ETL processes
│   └── utils/         # Utility functions
├── config/            # Configuration files
├── data/              # Data storage
└── tests/             # Test files
```

## Usage

1. Set up the database schema
2. Generate FBR API key
3. Run data collection scripts
4. Execute ETL processes

## Rate Limiting

The FBR API enforces a 3-second delay between requests. All API calls automatically include this delay to ensure compliance and avoid being blocked.

## License

MIT 