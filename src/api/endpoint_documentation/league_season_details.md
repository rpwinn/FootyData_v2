# /league-season-details Endpoint Documentation

## Overview
Endpoint to retrieve meta-data for a specific league id and season id.

## Endpoint Details
- **URL**: `/league-season-details`
- **Method**: GET
- **Base URL**: https://fbrapi.com

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `league_id` | integer | Yes | Integer representing a league's football reference id |
| `season_id` | string | No | Football reference season that is either in "%Y" or "%Y-%Y" format, depending on the league. If not provided, endpoint retrieves data for most recent season for provided league_id |

## Response Structure

### Success Response (200)
```json
{
    "data": {
        "lg_id": 8,
        "season_id": "2018-2019",
        "league_start": "2018-09-18",
        "league_end": "2019-05-29",
        "league_type": "cup",
        "has_adv_stats": "yes",
        "rounds": [
            "Round of 16",
            "Final",
            "Quarter-finals",
            "Semi-finals",
            "Group stage"
        ]
    }
}
```

### Error Response (4xx/5xx)
```json
{
    "error": "Error message description"
}
```

## Field Descriptions

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `lg_id` | integer | League ID (same as input parameter) | 8, 9, 12 |
| `season_id` | string | Season ID (same as input parameter) | "2018-2019", "2024" |
| `league_start` | string | String date in '%Y-%m-%d' format representing the first match date for the given league-season | "2018-09-18" |
| `league_end` | string | String date in '%Y-%m-%d' format representing the last match date for the given league-season | "2019-05-29" |
| `league_type` | string | Either 'cup' or 'league' | "cup", "league" |
| `has_adv_stats` | string | Either 'yes' or 'no'; identifies whether advanced stats are available for the specific league-season | "yes", "no" |
| `rounds` | array | List of names of rounds if a league has a multiple round format | ["Round of 16", "Final"] |

## Season ID Formats
- **European Leagues**: Typically "%Y-%Y" format (e.g., "2018-2019")
- **Other Leagues**: May use "%Y" format (e.g., "2024")
- **Historical Seasons**: May use different formats for older seasons

## Usage Examples

### Get Details for Specific League and Season
```bash
GET /league-season-details?league_id=8&season_id=2018-2019
```

### Get Details for Most Recent Season
```bash
GET /league-season-details?league_id=9
```

### Get Details for Premier League 2023-2024
```bash
GET /league-season-details?league_id=9&season_id=2023-2024
```

### Using curl
```bash
# Get Champions League 2023-2024 details
curl -H "X-API-Key: YOUR_API_KEY" \
     -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
     "https://fbrapi.com/league-season-details/?league_id=8&season_id=2023-2024"

# Get most recent season for Premier League (returns 500 error)
curl -H "X-API-Key: YOUR_API_KEY" \
     -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
     "https://fbrapi.com/league-season-details/?league_id=9"
```

### Using Python
```python
import requests

headers = {
    'X-API-Key': 'YOUR_API_KEY',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
}

# Get Champions League 2023-2024 details (working endpoint)
response = requests.get('https://fbrapi.com/league-season-details/?league_id=8&season_id=2023-2024', headers=headers)
champions_league_details = response.json()

# Get Premier League details (broken endpoint - returns 500 error)
response = requests.get('https://fbrapi.com/league-season-details/?league_id=9', headers=headers)
premier_league_details = response.json()  # Will contain error
```

### Using JavaScript/Fetch
```javascript
fetch('https://fbrapi.com/league-season-details/?league_id=8&season_id=2023-2024', {
    headers: {
        'X-API-Key': 'YOUR_API_KEY',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
})
.then(response => response.json())
.then(data => {
    console.log('Champions League Details:', data.data);
});
```

## Data Volume
- **Response Size**: Small (few KB per request)
- **Update Frequency**: Static (season metadata doesn't change)
- **Data Availability**: Varies by league and season

## Dependencies
- **Requires**: `/leagues` endpoint (for league_id values)
- **Requires**: `/league-seasons` endpoint (for season_id values)
- **Used by**: Multiple endpoints that need league-season metadata

## Notes

Meta-data, when available, includes:

- **league_start (str)**: String date in '%Y-%m-%d' format representing the first match date for the given league-season.
- **league_end (str)**: String date in '%Y-%m-%d' format representing the last match date for the given league-season. Note: If the season has a round format and is still in progress, the actual last match date may be inaccurate due to the currently unknown final match date.
- **league_type (str)**: Either 'cup' or 'league'.
- **has_adv_stats (str)**: Either 'yes' or 'no'; identifies whether advanced stats are available for the specific league-season.
- **rounds (list of str)**: List of names of rounds if a league has a multiple round format.

### Additional Notes
- If season_id is not provided, returns data for the most recent season for the given league_id
- League end dates may be inaccurate for ongoing cup competitions
- Advanced stats availability varies by league and season
- Round information is only available for cup competitions with multiple rounds
- League start/end dates are in UTC timezone 