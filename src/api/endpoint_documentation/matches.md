# /matches Endpoint Documentation

## Overview
Endpoint to retrieve match meta-data from Football Reference. There are two distinct match data returned by this endpoint:

1. **Team Match Data** - When a `team_id` is passed, this retrieves match meta-data for a specific team
2. **League Match Data** - When a `team_id` is not passed but a `league_id` is, this retrieves match meta-data for a specific league

## Endpoint Details
- **URL**: `/matches`
- **Method**: GET
- **Base URL**: https://fbrapi.com

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `team_id` | string | No | 8-character string representing a team's football reference id |
| `league_id` | integer | Yes | Integer representing a league's football reference id |
| `season_id` | string | No | Football reference season that is either in "%Y" or "%Y-%Y" format, depending on the league. If not provided, endpoint retrieves data for most recent season for provided league_id |

## Response Structure

### Team Match Data Response (when team_id is provided)
```json
{
    "data": [
        {
            "match_id": "09d8a999",
            "date": "2022-08-06",
            "time": "15:00",
            "round": "Matchweek 1",
            "league_id": 9,
            "home_away": "Home",
            "opponent": "Southampton",
            "opponent_id": "33c895d4",
            "result": "W",
            "gf": 4,
            "ga": 1,
            "formation": "3-4-3",
            "attendance": "61,732",
            "captain": "Hugo Lloris",
            "referee": "Andre Marriner"
        }
    ]
}
```

### League Match Data Response (when team_id is not provided)
```json
{
    "data": [
        {
            "match_id": "089c98e2",
            "date": "2022-07-30",
            "time": "15:00",
            "round": "Regular season",
            "wk": "1",
            "home": "Wycombe",
            "home_team_id": "43c2583e",
            "away": "Burton Albion",
            "away_team_id": "b09787c5",
            "home_team_score": null,
            "away_team_score": null,
            "venue": "Adams Park",
            "attendance": "5,772",
            "referee": "Gavin Ward"
        }
    ]
}
```

## Field Descriptions

### Team Match Data Fields (when team_id is provided)

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `match_id` | string | 8-character football reference match identification | "09d8a999" |
| `date` | string | Date of match in %Y-%m-%d format | "2022-08-06" |
| `time` | string | Time in %H:%M format | "15:00" |
| `round` | string | Name of round or matchweek number | "Matchweek 1" |
| `league_id` | integer | Football reference league identification | 9 |
| `home_away` | string | Whether team played at home, neutral or away | "Home", "Away" |
| `opponent` | string | Name of opposing team | "Southampton" |
| `opponent_id` | string | 8-character football reference identification of opposing team | "33c895d4" |
| `result` | string | Result of match (W = win, L = loss, D = draw) | "W", "L", "D" |
| `gf` | integer | Number of goals scored by team in match | 4 |
| `ga` | integer | Number of goals conceded by team in match | 1 |
| `formation` | string | Formation played by team | "3-4-3" |
| `attendance` | string | Number of people in attendance | "61,732" |
| `captain` | string | Name of team captain for match | "Hugo Lloris" |
| `referee` | string | Name of referee for match | "Andre Marriner" |

### League Match Data Fields (when team_id is not provided)

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `match_id` | string | 8-character football reference match identification | "089c98e2" |
| `date` | string | Date of match in %Y-%m-%d format | "2022-07-30" |
| `time` | string | Time in %H:%M format | "15:00" |
| `wk` | string | Name of matchweek if applicable | "1" |
| `round` | string | Name of round if applicable | "Regular season" |
| `home` | string | Name of home team | "Wycombe" |
| `home_team_id` | string | 8-character football reference identification of home team | "43c2583e" |
| `away` | string | Name of away team | "Burton Albion" |
| `away_team_id` | string | 8-character football reference identification of away team | "b09787c5" |
| `home_team_score` | integer | Number of goals scored by home team in match | null |
| `away_team_score` | integer | Number of goals scored by away team in match | null |
| `venue` | string | Name of venue played at | "Adams Park" |
| `attendance` | string | Number of people in attendance | "5,772" |
| `referee` | string | Name of referee for match | "Gavin Ward" |

## Usage Examples

### Get League Matches (no team_id)
```bash
GET /matches?league_id=9&season_id=2023-2024
```

### Get Team Matches (with team_id)
```bash
GET /matches?team_id=b8fd03ef&league_id=9&season_id=2023-2024
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
     "https://fbrapi.com/matches/?team_id=b8fd03ef&league_id=9&season_id=2023-2024"
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
league_matches = response.json()

# Get Manchester City matches only
response = requests.get('https://fbrapi.com/matches/?team_id=b8fd03ef&league_id=9&season_id=2023-2024', headers=headers)
team_matches = response.json()
```

## Data Volume
- **Response Size**: Large (varies by number of matches)
- **Update Frequency**: Dynamic (new fixtures, results updates)
- **Data Availability**: Varies by league and season

## Dependencies
- **Requires**: League ID and season ID from other endpoints
- **Used by**: Applications needing match data and fixtures
- **Related**: `/all-players-match-stats` endpoint for detailed player statistics

## Notes

### Team Match Data (when team_id is provided):
- Provides team-centric view of matches
- Includes formation, captain, and team-specific statistics
- Shows home/away status and opponent information
- Result field indicates win/loss/draw for the team

### League Match Data (when team_id is not provided):
- Provides league-wide view of all matches
- Includes both home and away team information
- Shows venue and attendance for each match
- Scores may be null for upcoming matches

### Additional Notes
- Match IDs are 8-character alphanumeric strings
- Team IDs correspond to teams from `/teams` endpoint
- Scores may be null for upcoming matches
- Attendance data may not be available for all matches
- Some matches may have limited data availability
- The `match_id` retrieved by this endpoint can be used to retrieve data in the `/all-players-match-stats` endpoint 