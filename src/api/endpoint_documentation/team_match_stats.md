# /team-match-stats Endpoint Documentation

## Overview
Endpoint to retrieve match-level team statistical data for a specified team, league and season. This provides detailed team performance statistics for individual matches.

## Endpoint Details
- **URL**: `/team-match-stats`
- **Method**: GET
- **Base URL**: https://fbrapi.com

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `team_id` | string | Yes | 8-character string representing a team's football reference id |
| `league_id` | integer | Yes | Integer representing a league's football reference id |
| `season_id` | string | Yes | Football reference season that is either in "%Y" or "%Y-%Y" format, depending on the league |

## Response Structure

### Success Response (200)
```json
{
    "data": [
        {
            "meta_data": {
                "match_id": "404ee5d3",
                "date": "2019-08-10",
                "round": "Matchweek 1",
                "home_away": "Away",
                "opponent": "Tottenham",
                "opponent_id": "361ca564"
            },
            "stats": {
                "schedule": {
                    "time": "17:30",
                    "result": "L",
                    "gls": 1,
                    "gls_ag": 3,
                    "xg": 0.7,
                    "xga": 2.4,
                    "poss": 30,
                    "attendance": "60,407",
                    "captain": "Jack Grealish",
                    "formation": "4-1-4-1",
                    "referee": "Chris Kavanagh"
                },
                "keeper": {
                    "sot_ag": 6,
                    "saves": 3,
                    "save_pct": 50.0,
                    "clean_sheets": 0,
                    "psxg": 2.0,
                    "psxg_gls_ag_diff": -1.0
                },
                "shooting": {
                    "sh": 7,
                    "sot": 4,
                    "pct_sot": 57.1,
                    "gls_per_sh": 0.14,
                    "gls_per_sot": 0.25,
                    "avg_sh_dist": 19.8,
                    "fk_sh": 0,
                    "pk_made": 0,
                    "non_pen_xg": 0.7,
                    "npxg_per_sh": 0.09,
                    "gls_xg_diff": 0.3,
                    "non_pen_gls_xg_diff": 0.3
                },
                "passing": {
                    "pass_cmp": 214,
                    "pct_pass_cmp": 77.3,
                    "pass_ttl_dist": 4137,
                    "pass_prog_ttl_dist": 1842,
                    "ast": 1,
                    "xag": 0.7,
                    "xa": 0.2,
                    "pass_prog": 17,
                    "key_passes": 7,
                    "pass_fthird": 17,
                    "pass_opp_box": 4,
                    "cross_opp_box": 2
                },
                "defense": {
                    "tkl": 29,
                    "tkl_won": 13,
                    "tkl_def_third": 18,
                    "tkl_mid_third": 8,
                    "tkl_att_third": 3,
                    "tkl_drb": 14,
                    "tkl_drb_att": 25,
                    "pct_tkl_drb_suc": 56.0,
                    "blocks": 18,
                    "sh_blocked": 11,
                    "int": 9,
                    "tkl_plus_int": 38,
                    "clearances": 46,
                    "def_error": 1
                },
                "possession": {
                    "touches": 422,
                    "touch_def_box": 104,
                    "touch_def_third": 220,
                    "touch_mid_third": 152,
                    "touch_fthird": 55,
                    "touch_opp_box": 8,
                    "touch_live": 422,
                    "take_on_att": 8,
                    "take_on_suc": 4,
                    "pct_take_on_suc": 50.0,
                    "take_on_tkld": 4,
                    "pct_take_on_tkld": 50.0,
                    "carries": 183,
                    "ttl_carries_dist": 1063,
                    "ttl_carries_prog_dist": 557,
                    "carries_prog": 6,
                    "carries_fthird": 8,
                    "carries_opp_box": 0,
                    "carries_miscontrolled": 13,
                    "carries_dispossessed": 13,
                    "pass_recvd": 213,
                    "pass_prog_rcvd": 17
                },
                "misc": {
                    "yellow_cards": 0,
                    "red_cards": 0,
                    "second_yellow_cards": 0,
                    "fls_com": 9,
                    "fls_drawn": 13,
                    "offside": 0,
                    "pk_won": 0,
                    "pk_conceded": 0,
                    "ball_recov": 39,
                    "air_dual_won": 12,
                    "air_dual_lost": 10,
                    "pct_air_dual_won": 54.5
                }
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

### Meta Data Object
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `match_id` | string | Football reference match ID | "404ee5d3" |
| `date` | string | Match date in YYYY-MM-DD format | "2019-08-10" |
| `round` | string | Competition round | "Matchweek 1" |
| `home_away` | string | Whether team played home/away | "Away", "Home" |
| `opponent` | string | Name of opponent team | "Tottenham" |
| `opponent_id` | string | Football reference opponent team ID | "361ca564" |

### Stats Object Categories
The stats object contains multiple statistical categories:

- **schedule**: Match result, goals, expected goals, possession, attendance
- **keeper**: Goalkeeping statistics (saves, clean sheets, etc.)
- **shooting**: Shot statistics (shots, goals, expected goals, etc.)
- **passing**: Passing statistics (completions, assists, key passes, etc.)
- **defense**: Defensive statistics (tackles, blocks, interceptions, etc.)
- **possession**: Possession statistics (touches, carries, take-ons, etc.)
- **misc**: Miscellaneous statistics (cards, fouls, offsides, etc.)

## Usage Examples

### Get Team Match Stats for Specific Team, League and Season
```bash
GET /team-match-stats?team_id=b8fd03ef&league_id=9&season_id=2023-2024
```

### Using curl
```bash
# Get Manchester City match stats for Premier League 2023-2024
curl -H "X-API-Key: YOUR_API_KEY" \
     -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
     "https://fbrapi.com/team-match-stats/?team_id=b8fd03ef&league_id=9&season_id=2023-2024"

# Get Arsenal match stats for Champions League 2023-2024
curl -H "X-API-Key: YOUR_API_KEY" \
     -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
     "https://fbrapi.com/team-match-stats/?team_id=18bb7c10&league_id=8&season_id=2023-2024"
```

### Using Python
```python
import requests

headers = {
    'X-API-Key': 'YOUR_API_KEY',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
}

# Get Manchester City match stats
response = requests.get('https://fbrapi.com/team-match-stats/?team_id=b8fd03ef&league_id=9&season_id=2023-2024', headers=headers)
man_city_match_stats = response.json()

# Get Arsenal match stats
response = requests.get('https://fbrapi.com/team-match-stats/?team_id=18bb7c10&league_id=8&season_id=2023-2024', headers=headers)
arsenal_match_stats = response.json()
```

### Using JavaScript/Fetch
```javascript
fetch('https://fbrapi.com/team-match-stats/?team_id=b8fd03ef&league_id=9&season_id=2023-2024', {
    headers: {
        'X-API-Key': 'YOUR_API_KEY',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
})
.then(response => response.json())
.then(data => {
    console.log('Manchester City Match Stats:', data.data);
});
```

## Data Volume
- **Response Size**: Large (detailed stats for each match)
- **Update Frequency**: Dynamic (after each match)
- **Data Availability**: Varies by team, league and season

## Dependencies
- **Requires**: Team ID, league ID and season ID from other endpoints
- **Used by**: Applications needing detailed match-level team analysis
- **Related**: `/matches` endpoint for basic match information

## Notes

Team match stats include:

- **Match Context**: Date, opponent, venue, result
- **Performance Metrics**: Goals, expected goals, possession
- **Detailed Statistics**: Passing, shooting, defense, possession
- **Advanced Metrics**: Expected goals, key passes, tackles

### Additional Notes
- All three parameters (team_id, league_id, season_id) are required
- Data includes both basic and advanced statistical categories
- Some statistical categories may not be available for all matches
- Advanced metrics provide deeper performance analysis 