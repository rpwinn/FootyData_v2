# /league-seasons Endpoint Documentation

## Overview
Endpoint to retrieve meta-data for all season ids tracked by football reference, given a football reference league id. The season_id retrieved by this endpoint can be used to retrieve data in the league-seasons, league-season-details, league-standings and other endpoints.

## Endpoint Details
- **URL**: `/league-seasons`
- **Method**: GET
- **Base URL**: https://fbrapi.com

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `league_id` | integer | Yes | Integer representing a league's football reference id |

## Response Structure

### Success Response (200)
```json
{
    "data": [
        {
            "season_id": "2023-2024",
            "competition_name": "Premier League",
            "#_squads": 20,
            "champion": "Manchester City",
            "top_scorer": {
                "player": "Erling Haaland",
                "goals_scored": 27
            }
        },
        {
            "season_id": "2022-2023",
            "competition_name": "Premier League",
            "#_squads": 20,
            "champion": "Manchester City",
            "top_scorer": {
                "player": "Erling Haaland",
                "goals_scored": 36
            }
        },
        {
            "season_id": "2021-2022",
            "competition_name": "Premier League",
            "#_squads": 20,
            "champion": "Manchester City",
            "top_scorer": {
                "player": [
                    "Son Heung min",
                    "Mohamed Salah"
                ],
                "goals_scored": 23
            }
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
| `season_id` | string | Football reference season in "%Y" or "%Y-%Y" format | "2023-2024", "2024" |
| `competition_name` | string | Name of the league (typically consistent across seasons) | "Premier League" |
| `#_squads` | integer | Number of teams that competed in the league-season | 20, 18, 22 |
| `champion` | string | Name of the team that won the competition | "Manchester City" |
| `top_scorer` | object | Dictionary containing top scorer information | See below |

### Top Scorer Object Fields
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `player` | string/array | Name of top scorer(s) - can be single player or array for ties | "Erling Haaland" or ["Son Heung min", "Mohamed Salah"] |
| `goals_scored` | integer | Number of goals scored by top scorer | 27, 36, 23 |

## Season ID Formats
- **European Leagues**: Typically "%Y-%Y" format (e.g., "2023-2024")
- **Other Leagues**: May use "%Y" format (e.g., "2024")
- **Historical Seasons**: May use different formats for older seasons

## Usage Examples

### Get All Seasons for Premier League
```bash
GET /league-seasons?league_id=9
```

### Get All Seasons for La Liga
```bash
GET /league-seasons?league_id=12
```

### Using curl
```bash
curl -H "X-API-Key: YOUR_API_KEY" \
     -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
     "https://fbrapi.com/league-seasons/?league_id=9"
```

### Using Python
```python
import requests

headers = {
    'X-API-Key': 'YOUR_API_KEY',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
}

# Get all seasons for Premier League
response = requests.get('https://fbrapi.com/league-seasons/?league_id=9', headers=headers)
premier_league_seasons = response.json()

# Get all seasons for La Liga
response = requests.get('https://fbrapi.com/league-seasons/?league_id=12', headers=headers)
la_liga_seasons = response.json()
```

### Using JavaScript/Fetch
```javascript
fetch('https://fbrapi.com/league-seasons/?league_id=9', {
    headers: {
        'X-API-Key': 'YOUR_API_KEY',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
})
.then(response => response.json())
.then(data => {
    console.log('Premier League Seasons:', data.data);
});
```

### Get All Seasons for Bundesliga
```bash
GET /league-seasons?league_id=20
```

## Data Volume
- **Seasons per League**: Varies by league (typically 10-50 seasons)
- **Update Frequency**: Static (seasons don't change, new ones added)
- **Data Size**: Small to medium (few KB per request)

## Dependencies
- **Requires**: `/leagues` endpoint (for league_id values)
- **Used by**: Multiple endpoints that need season_id parameter

## Notes

Meta-data, when available, includes:

- **season_id (str)**: Football reference season that is either in "%Y" or "%Y-%Y" format, depending on the league.
- **competition_name (str)**: Name of the league; typically consistent across seasons, although it does change on rare occasions.
- **#_squads (int)**: Number of teams that competed in the league-season.
- **champion (str)**: Name of the team that won the competition for the specified league-season.
- **top_scorer (dict)**: Dictionary containing player(s) name (str) and number of goals scored (int) by the top scorer for the specified league-season.

### Additional Notes
- League IDs are unique across the entire FBR system
- Season formats vary by league and region
- Some leagues may have incomplete data for older seasons
- Top scorer can be a tie (array of players) or single player
- Champion field may be empty for ongoing seasons
- Number of squads can vary between seasons for the same league 