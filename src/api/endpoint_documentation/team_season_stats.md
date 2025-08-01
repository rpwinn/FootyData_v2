# /team-season-stats Endpoint Documentation

## Overview
Endpoint to retrieve season-level team statistical data for a specified league and season. This provides comprehensive team performance statistics aggregated over the entire season.

## Endpoint Details
- **URL**: `/team-season-stats`
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
            "team": "Manchester City",
            "team_id": "b8fd03ef",
            "position": 1,
            "played": 38,
            "won": 28,
            "drawn": 5,
            "lost": 5,
            "goals_for": 94,
            "goals_against": 33,
            "goal_difference": 61,
            "points": 89,
            "expected_goals": 78.5,
            "expected_goals_against": 45.2,
            "clean_sheets": 15,
            "failed_to_score": 3
        },
        {
            "team": "Arsenal",
            "team_id": "18bb7c10",
            "position": 2,
            "played": 38,
            "won": 26,
            "drawn": 6,
            "lost": 6,
            "goals_for": 88,
            "goals_against": 43,
            "goal_difference": 45,
            "points": 84,
            "expected_goals": 72.1,
            "expected_goals_against": 48.7,
            "clean_sheets": 12,
            "failed_to_score": 5
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
| `team` | string | Name of the team | "Manchester City" |
| `team_id` | string | Football reference team ID | "b8fd03ef" |
| `position` | integer | Final league position | 1, 2, 20 |
| `played` | integer | Number of matches played | 38, 30, 22 |
| `won` | integer | Number of matches won | 28, 20, 15 |
| `drawn` | integer | Number of matches drawn | 5, 8, 4 |
| `lost` | integer | Number of matches lost | 5, 10, 3 |
| `goals_for` | integer | Goals scored by the team | 94, 75, 45 |
| `goals_against` | integer | Goals conceded by the team | 33, 42, 25 |
| `goal_difference` | integer | Difference between goals for and against | 61, 33, 20 |
| `points` | integer | Total points earned | 89, 68, 49 |
| `expected_goals` | float | Expected goals based on shot quality | 78.5, 65.2 |
| `expected_goals_against` | float | Expected goals against based on shot quality | 45.2, 48.7 |
| `clean_sheets` | integer | Number of matches without conceding | 15, 12, 8 |
| `failed_to_score` | integer | Number of matches without scoring | 3, 5, 7 |

## Usage Examples

### Get Team Stats for Specific League and Season
```bash
GET /team-season-stats?league_id=9&season_id=2023-2024
```

### Get Team Stats for Most Recent Season
```bash
GET /team-season-stats?league_id=9
```

### Using curl
```bash
# Get Premier League 2023-2024 team stats
curl -H "X-API-Key: YOUR_API_KEY" \
     -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
     "https://fbrapi.com/team-season-stats/?league_id=9&season_id=2023-2024"

# Get Champions League team stats
curl -H "X-API-Key: YOUR_API_KEY" \
     -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
     "https://fbrapi.com/team-season-stats/?league_id=8"
```

### Using Python
```python
import requests

headers = {
    'X-API-Key': 'YOUR_API_KEY',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
}

# Get Premier League 2023-2024 team stats
response = requests.get('https://fbrapi.com/team-season-stats/?league_id=9&season_id=2023-2024', headers=headers)
premier_league_stats = response.json()

# Get Champions League team stats
response = requests.get('https://fbrapi.com/team-season-stats/?league_id=8', headers=headers)
champions_league_stats = response.json()
```

### Using JavaScript/Fetch
```javascript
fetch('https://fbrapi.com/team-season-stats/?league_id=9&season_id=2023-2024', {
    headers: {
        'X-API-Key': 'YOUR_API_KEY',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
})
.then(response => response.json())
.then(data => {
    console.log('Premier League Team Stats:', data.data);
});
```

## Data Volume
- **Response Size**: Medium (varies by number of teams)
- **Update Frequency**: Static (season completed) to dynamic (ongoing season)
- **Data Availability**: Varies by league and season

## Dependencies
- **Requires**: League ID and season ID from other endpoints
- **Used by**: Applications needing team performance analysis
- **Related**: `/league-standings` endpoint for position data

## Notes

Team season stats include:

- **Basic Statistics**: Matches played, won, drawn, lost
- **Goal Statistics**: Goals scored, conceded, goal difference
- **Advanced Metrics**: Expected goals, clean sheets, failed to score
- **Performance Indicators**: Points earned and final position

### Additional Notes
- Data represents complete season statistics
- Expected goals provide advanced performance metrics
- Clean sheets and failed to score indicate defensive/offensive consistency
- Some advanced metrics may not be available for all leagues 