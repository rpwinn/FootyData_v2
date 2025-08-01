# /matches Endpoint Documentation

## Overview
Endpoint to retrieve match meta-data for a specific league and season. This provides comprehensive match information including fixtures, results, and match details.

## Endpoint Details
- **URL**: `/matches`
- **Method**: GET
- **Base URL**: https://fbrapi.com

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `league_id` | string | Yes | Integer representing a league's football reference id |
| `season_id` | string | Yes | Football reference season that is either in "%Y" or "%Y-%Y" format, depending on the league |
| `team_id` | string | No | 8-character string representing a team's football reference id (optional filter) |

## Response Structure

### Success Response (200)
```json
{
    "data": [
        {
            "match_id": "cc5b4244",
            "date": "2023-08-11",
            "time": "20:00",
            "home_team": "Manchester City",
            "home_team_id": "b8fd03ef",
            "away_team": "Burnley",
            "away_team_id": "943e8050",
            "home_team_score": 3,
            "away_team_score": 0,
            "venue": "Etihad Stadium",
            "attendance": 53400,
            "referee": "Simon Hooper",
            "round": "Matchweek 1"
        },
        {
            "match_id": "dd6c5355",
            "date": "2023-08-12",
            "time": "15:00",
            "home_team": "Arsenal",
            "home_team_id": "18bb7c10",
            "away_team": "Nottingham Forest",
            "away_team_id": "a5c9f123",
            "home_team_score": 2,
            "away_team_score": 1,
            "venue": "Emirates Stadium",
            "attendance": 60100,
            "referee": "Michael Oliver",
            "round": "Matchweek 1"
        }
    ]
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
| `match_id` | string | Football reference match ID | "cc5b4244" |
| `date` | string | Match date in YYYY-MM-DD format | "2023-08-11" |
| `time` | string | Match time in HH:MM format | "20:00", "15:00" |
| `home_team` | string | Name of home team | "Manchester City" |
| `home_team_id` | string | Football reference home team ID | "b8fd03ef" |
| `away_team` | string | Name of away team | "Burnley" |
| `away_team_id` | string | Football reference away team ID | "943e8050" |
| `home_team_score` | integer | Goals scored by home team | 3, 2, 0 |
| `away_team_score` | integer | Goals scored by away team | 0, 1, 2 |
| `venue` | string | Match venue | "Etihad Stadium" |
| `attendance` | integer | Match attendance | 53400, 60100 |
| `referee` | string | Match referee | "Simon Hooper" |
| `round` | string | Competition round or matchweek | "Matchweek 1" |

## Usage Examples

### Get All Matches for League and Season
```bash
GET /matches?league_id=9&season_id=2023-2024
```

### Get Matches for Specific Team
```bash
GET /matches?league_id=9&season_id=2023-2024&team_id=b8fd03ef
```

### Using curl
```bash
# Get all Premier League 2023-2024 matches
curl -H "X-API-Key: YOUR_API_KEY" \
     -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
     "https://fbrapi.com/matches/?league_id=9&season_id=2023-2024"

# Get Manchester City matches only
curl -H "X-API-Key: YOUR_API_KEY" \
     -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
     "https://fbrapi.com/matches/?league_id=9&season_id=2023-2024&team_id=b8fd03ef"
```

### Using Python
```python
import requests

headers = {
    'X-API-Key': 'YOUR_API_KEY',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
}

# Get all Premier League 2023-2024 matches
response = requests.get('https://fbrapi.com/matches/?league_id=9&season_id=2023-2024', headers=headers)
premier_league_matches = response.json()

# Get Manchester City matches only
response = requests.get('https://fbrapi.com/matches/?league_id=9&season_id=2023-2024&team_id=b8fd03ef', headers=headers)
man_city_matches = response.json()
```

### Using JavaScript/Fetch
```javascript
fetch('https://fbrapi.com/matches/?league_id=9&season_id=2023-2024', {
    headers: {
        'X-API-Key': 'YOUR_API_KEY',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
})
.then(response => response.json())
.then(data => {
    console.log('Premier League Matches:', data.data);
});
```

## Data Volume
- **Response Size**: Large (varies by number of matches)
- **Update Frequency**: Dynamic (new fixtures, results updates)
- **Data Availability**: Varies by league and season

## Dependencies
- **Requires**: League ID and season ID from other endpoints
- **Used by**: Applications needing match data and fixtures
- **Related**: `/teams` endpoint for team-specific match data

## Notes

Match data includes:

- **Fixture Information**: Date, time, venue, referee
- **Team Information**: Home and away teams with IDs
- **Result Data**: Scores for completed matches
- **Competition Context**: Round information and attendance

### Additional Notes
- Match IDs are 8-character alphanumeric strings
- Team IDs correspond to teams from `/teams` endpoint
- Scores may be null for upcoming matches
- Attendance data may not be available for all matches
- Some matches may have limited data availability 