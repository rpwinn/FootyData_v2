# /teams Endpoint Documentation

## Overview
Endpoint to retrieve team roster and schedule data for a specific team. This provides comprehensive team information including players, fixtures, and team metadata.

## Endpoint Details
- **URL**: `/teams`
- **Method**: GET
- **Base URL**: https://fbrapi.com

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `team_id` | string | Yes | 8-character string representing a team's football reference id |
| `season_id` | string | No | Football reference season that is either in "%Y" or "%Y-%Y" format, depending on the league. If not provided, endpoint retrieves data for most recent season for provided team_id |

## Response Structure

### Success Response (200)
```json
{
    "data": {
        "team_info": {
            "team_id": "b8fd03ef",
            "team_name": "Manchester City",
            "league_id": 9,
            "league_name": "Premier League",
            "season_id": "2023-2024"
        },
        "roster": [
            {
                "player_id": "8b04d6c1",
                "player_name": "Erling Haaland",
                "position": "FW",
                "age": 23,
                "nationality": "NOR",
                "appearances": 35,
                "minutes_played": 3150
            }
        ],
        "schedule": [
            {
                "match_id": "cc5b4244",
                "date": "2023-08-11",
                "home_away": "Home",
                "opponent": "Burnley",
                "opponent_id": "943e8050",
                "result": "W",
                "score": "3-0",
                "venue": "Etihad Stadium"
            }
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

### Team Info Object
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `team_id` | string | Football reference team ID | "b8fd03ef" |
| `team_name` | string | Name of the team | "Manchester City" |
| `league_id` | integer | League ID the team competes in | 9, 12, 8 |
| `league_name` | string | Name of the league | "Premier League" |
| `season_id` | string | Season ID | "2023-2024" |

### Roster Array Objects
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `player_id` | string | Football reference player ID | "8b04d6c1" |
| `player_name` | string | Name of the player | "Erling Haaland" |
| `position` | string | Player position | "FW", "MF", "DF", "GK" |
| `age` | integer | Player age | 23, 28, 19 |
| `nationality` | string | 3-letter country code | "NOR", "ENG", "BRA" |
| `appearances` | integer | Number of appearances | 35, 22, 8 |
| `minutes_played` | integer | Total minutes played | 3150, 1980, 720 |

### Schedule Array Objects
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `match_id` | string | Football reference match ID | "cc5b4244" |
| `date` | string | Match date in YYYY-MM-DD format | "2023-08-11" |
| `home_away` | string | Whether team played home/away | "Home", "Away" |
| `opponent` | string | Name of opponent team | "Burnley" |
| `opponent_id` | string | Football reference opponent team ID | "943e8050" |
| `result` | string | Match result from team's perspective | "W", "L", "D" |
| `score` | string | Match score | "3-0", "1-2", "2-2" |
| `venue` | string | Match venue | "Etihad Stadium" |

## Usage Examples

### Get Team Data for Specific Season
```bash
GET /teams?team_id=b8fd03ef&season_id=2023-2024
```

### Get Team Data for Most Recent Season
```bash
GET /teams?team_id=b8fd03ef
```

### Using curl
```bash
# Get Manchester City 2023-2024 data
curl -H "X-API-Key: YOUR_API_KEY" \
     -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
     "https://fbrapi.com/teams/?team_id=b8fd03ef&season_id=2023-2024"

# Get Arsenal most recent season data
curl -H "X-API-Key: YOUR_API_KEY" \
     -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
     "https://fbrapi.com/teams/?team_id=18bb7c10"
```

### Using Python
```python
import requests

headers = {
    'X-API-Key': 'YOUR_API_KEY',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
}

# Get Manchester City 2023-2024 data
response = requests.get('https://fbrapi.com/teams/?team_id=b8fd03ef&season_id=2023-2024', headers=headers)
man_city_data = response.json()

# Get Arsenal data
response = requests.get('https://fbrapi.com/teams/?team_id=18bb7c10', headers=headers)
arsenal_data = response.json()
```

### Using JavaScript/Fetch
```javascript
fetch('https://fbrapi.com/teams/?team_id=b8fd03ef&season_id=2023-2024', {
    headers: {
        'X-API-Key': 'YOUR_API_KEY',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
})
.then(response => response.json())
.then(data => {
    console.log('Manchester City Data:', data.data);
});
```

## Data Volume
- **Response Size**: Large (includes roster and schedule data)
- **Update Frequency**: Dynamic (roster changes, new matches)
- **Data Availability**: Varies by team and season

## Dependencies
- **Requires**: Team ID from other endpoints or data sources
- **Used by**: Applications needing detailed team information
- **Related**: `/players` endpoint for individual player data

## Notes

Team data includes:

- **Team Information**: Basic team metadata and identification
- **Roster Data**: Complete list of players with statistics
- **Schedule Data**: All matches for the team in the season
- **Player Statistics**: Individual player performance data

### Additional Notes
- Team IDs are 8-character alphanumeric strings
- Roster data includes current squad members
- Schedule data includes both completed and upcoming matches
- Player positions follow standard football abbreviations
- Some teams may have incomplete roster or schedule data 