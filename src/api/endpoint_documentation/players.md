# /players Endpoint Documentation

## Overview
Endpoint to retrieve player meta-data for a specific player. This provides comprehensive player information including personal details, career statistics, and current status.

## Endpoint Details
- **URL**: `/players`
- **Method**: GET
- **Base URL**: https://fbrapi.com

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `player_id` | string | Yes | 8-character string representing a player's football reference id |

## Response Structure

### Success Response (200)
```json
{
    "data": {
        "player_id": "8b04d6c1",
        "player_name": "Erling Haaland",
        "full_name": "Erling Braut Haaland",
        "date_of_birth": "2000-07-21",
        "age": 23,
        "height": 195,
        "nationality": "NOR",
        "position": "FW",
        "current_team": "Manchester City",
        "current_team_id": "b8fd03ef",
        "current_league": "Premier League",
        "current_league_id": 9,
        "career_stats": {
            "total_appearances": 245,
            "total_goals": 198,
            "total_assists": 45,
            "clubs_played_for": 4
        }
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
| `player_id` | string | Football reference player ID | "8b04d6c1" |
| `player_name` | string | Common name of the player | "Erling Haaland" |
| `full_name` | string | Complete name of the player | "Erling Braut Haaland" |
| `date_of_birth` | string | Birth date in YYYY-MM-DD format | "2000-07-21" |
| `age` | integer | Current age of the player | 23, 28, 19 |
| `height` | integer | Height in centimeters | 195, 180, 175 |
| `nationality` | string | 3-letter country code | "NOR", "ENG", "BRA" |
| `position` | string | Primary playing position | "FW", "MF", "DF", "GK" |
| `current_team` | string | Name of current team | "Manchester City" |
| `current_team_id` | string | Football reference team ID | "b8fd03ef" |
| `current_league` | string | Name of current league | "Premier League" |
| `current_league_id` | integer | Football reference league ID | 9, 12, 8 |

### Career Stats Object
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `total_appearances` | integer | Total career appearances | 245, 180, 320 |
| `total_goals` | integer | Total career goals scored | 198, 45, 120 |
| `total_assists` | integer | Total career assists | 45, 23, 67 |
| `clubs_played_for` | integer | Number of clubs played for | 4, 2, 6 |

## Usage Examples

### Get Player Data
```bash
GET /players?player_id=8b04d6c1
```

### Using curl
```bash
# Get Erling Haaland data
curl -H "X-API-Key: YOUR_API_KEY" \
     -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
     "https://fbrapi.com/players/?player_id=8b04d6c1"

# Get Kevin De Bruyne data
curl -H "X-API-Key: YOUR_API_KEY" \
     -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
     "https://fbrapi.com/players/?player_id=7c0e6d8a"
```

### Using Python
```python
import requests

headers = {
    'X-API-Key': 'YOUR_API_KEY',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
}

# Get Erling Haaland data
response = requests.get('https://fbrapi.com/players/?player_id=8b04d6c1', headers=headers)
haaland_data = response.json()

# Get Kevin De Bruyne data
response = requests.get('https://fbrapi.com/players/?player_id=7c0e6d8a', headers=headers)
de_bruyne_data = response.json()
```

### Using JavaScript/Fetch
```javascript
fetch('https://fbrapi.com/players/?player_id=8b04d6c1', {
    headers: {
        'X-API-Key': 'YOUR_API_KEY',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
})
.then(response => response.json())
.then(data => {
    console.log('Haaland Data:', data.data);
});
```

## Data Volume
- **Response Size**: Small to medium (varies by player)
- **Update Frequency**: Static (personal info) to dynamic (current team)
- **Data Availability**: Varies by player and data completeness

## Dependencies
- **Requires**: Player ID from other endpoints or data sources
- **Used by**: Applications needing detailed player information
- **Related**: `/teams` endpoint for team roster data

## Notes

Player data includes:

- **Personal Information**: Name, birth date, nationality, height
- **Current Status**: Team, league, position
- **Career Statistics**: Appearances, goals, assists
- **Career History**: Number of clubs played for

### Additional Notes
- Player IDs are 8-character alphanumeric strings
- Height is provided in centimeters
- Position abbreviations follow standard football conventions
- Career stats may not be complete for all players
- Some players may have limited data availability 