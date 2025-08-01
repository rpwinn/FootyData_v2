# /league-standings Endpoint Documentation

## Overview
Endpoint to retrieve all standings tables for a given league and season id. This provides current and historical league standings data.

## Endpoint Details
- **URL**: `/league-standings`
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
    "data": [
        {
            "position": 1,
            "team": "Manchester City",
            "team_id": "b8fd03ef",
            "played": 38,
            "won": 28,
            "drawn": 5,
            "lost": 5,
            "goals_for": 94,
            "goals_against": 33,
            "goal_difference": 61,
            "points": 89
        },
        {
            "position": 2,
            "team": "Arsenal",
            "team_id": "18bb7c10",
            "played": 38,
            "won": 26,
            "drawn": 6,
            "lost": 6,
            "goals_for": 88,
            "goals_against": 43,
            "goal_difference": 45,
            "points": 84
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
| `position` | integer | Team's position in the standings | 1, 2, 20 |
| `team` | string | Name of the team | "Manchester City", "Arsenal" |
| `team_id` | string | Football reference team ID | "b8fd03ef", "18bb7c10" |
| `played` | integer | Number of matches played | 38, 30, 22 |
| `won` | integer | Number of matches won | 28, 20, 15 |
| `drawn` | integer | Number of matches drawn | 5, 8, 4 |
| `lost` | integer | Number of matches lost | 5, 10, 3 |
| `goals_for` | integer | Goals scored by the team | 94, 75, 45 |
| `goals_against` | integer | Goals conceded by the team | 33, 42, 25 |
| `goal_difference` | integer | Difference between goals for and against | 61, 33, 20 |
| `points` | integer | Total points earned | 89, 68, 49 |

## Usage Examples

### Get Standings for Specific League and Season
```bash
GET /league-standings?league_id=9&season_id=2023-2024
```

### Get Standings for Most Recent Season
```bash
GET /league-standings?league_id=9
```

### Using curl
```bash
# Get Premier League 2023-2024 standings
curl -H "X-API-Key: YOUR_API_KEY" \
     -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
     "https://fbrapi.com/league-standings/?league_id=9&season_id=2023-2024"

# Get most recent standings for Champions League
curl -H "X-API-Key: YOUR_API_KEY" \
     -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
     "https://fbrapi.com/league-standings/?league_id=8"
```

### Using Python
```python
import requests

headers = {
    'X-API-Key': 'YOUR_API_KEY',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
}

# Get Premier League 2023-2024 standings
response = requests.get('https://fbrapi.com/league-standings/?league_id=9&season_id=2023-2024', headers=headers)
premier_league_standings = response.json()

# Get Champions League standings
response = requests.get('https://fbrapi.com/league-standings/?league_id=8', headers=headers)
champions_league_standings = response.json()
```

### Using JavaScript/Fetch
```javascript
fetch('https://fbrapi.com/league-standings/?league_id=9&season_id=2023-2024', {
    headers: {
        'X-API-Key': 'YOUR_API_KEY',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
})
.then(response => response.json())
.then(data => {
    console.log('Premier League Standings:', data.data);
});
```

## Data Volume
- **Response Size**: Medium (varies by number of teams)
- **Update Frequency**: Dynamic (changes throughout season)
- **Data Availability**: Varies by league and season

## Dependencies
- **Requires**: `/leagues` endpoint (for league_id values)
- **Requires**: `/league-seasons` endpoint (for season_id values)
- **Used by**: Applications needing current standings data

## Notes

Standings data includes:

- **Position**: Team's current position in the league table
- **Team Information**: Team name and unique identifier
- **Match Statistics**: Games played, won, drawn, lost
- **Goal Statistics**: Goals scored, conceded, and goal difference
- **Points**: Total points earned in the competition

### Additional Notes
- Standings are typically ordered by points (highest first)
- Goal difference is used as a tiebreaker
- Some leagues may have additional tiebreaking criteria
- Data availability varies by league and season
- Historical standings may have different data completeness 