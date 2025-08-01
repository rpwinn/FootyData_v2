# /all-players-match-stats Endpoint Documentation

## Overview
Endpoint to retrieve match-level player statistical data for all players across all matches for a specified league and season. This provides comprehensive player performance statistics for every match in a season.

## Endpoint Details
- **URL**: `/all-players-match-stats`
- **Method**: GET
- **Base URL**: https://fbrapi.com

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
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
                "home_team": "Tottenham",
                "home_team_id": "361ca564",
                "away_team": "Manchester City",
                "away_team_id": "b8fd03ef"
            },
            "players": [
                {
                    "meta_data": {
                        "player_id": "8b04d6c1",
                        "player_name": "Pierre Højbjerg",
                        "player_country_code": "DEN",
                        "age": 24,
                        "team": "Tottenham",
                        "team_id": "361ca564",
                        "opponent": "Manchester City",
                        "opponent_id": "b8fd03ef",
                        "formation": "4-1-4-1",
                        "position": "MF",
                        "min": 90
                    },
                    "stats": {
                        "stats": {
                            "gls": 0,
                            "ast": 0,
                            "gls_and_ast": 0,
                            "non_pen_gls": 0,
                            "xg": 0.0,
                            "non_pen_xg": 0.0,
                            "xag": 0.0,
                            "pk_made": 0,
                            "pk_att": 0,
                            "yellow_cards": 0,
                            "red_cards": 0,
                            "carries_prog": 1,
                            "passes_prog": 6
                        },
                        "shooting": {
                            "sh": 0,
                            "sot": 0,
                            "pct_sot": null,
                            "gls_per_sh": null,
                            "gls_per_sot": null,
                            "avg_sh_dist": null,
                            "fk_sh": 0,
                            "npxg_per_sh": null,
                            "gls_xg_diff": 0.0,
                            "non_pen_gls_xg_diff": 0.0
                        },
                        "passing": {
                            "pass_cmp": 45,
                            "pass_att": 52,
                            "pct_pass_cmp": 86.5,
                            "pass_ttl_dist": 789,
                            "pass_cmp_s": 22,
                            "pass_att_s": 24,
                            "pct_pass_cmp_s": 91.7,
                            "pass_cmp_m": 20,
                            "pass_att_m": 22,
                            "pct_pass_cmp_m": 90.9,
                            "pass_cmp_l": 3,
                            "pass_att_l": 6,
                            "pct_pass_cmp_l": 50.0,
                            "xa": 0.0,
                            "ast_xag_diff": 0.0,
                            "pass_prog": 6,
                            "pass_prog_ttl_dist": 234,
                            "key_passes": 0,
                            "pass_fthird": 5,
                            "pass_opp_box": 0,
                            "cross_opp_box": 0
                        },
                        "defense": {
                            "tkl": 3,
                            "tkl_won": 2,
                            "tkl_def_third": 2,
                            "tkl_mid_third": 1,
                            "tkl_att_third": 0,
                            "tkl_drb": 2,
                            "tkl_drb_att": 4,
                            "pct_tkl_drb_suc": 50.0,
                            "blocks": 1,
                            "sh_blocked": 0,
                            "int": 2,
                            "tkl_plus_int": 5,
                            "clearances": 2,
                            "def_error": 0
                        },
                        "possession": {
                            "touches": 67,
                            "touch_def_box": 3,
                            "touch_def_third": 25,
                            "touch_mid_third": 40,
                            "touch_fthird": 2,
                            "touch_opp_box": 0,
                            "touch_live": 67,
                            "take_on_att": 1,
                            "take_on_suc": 1,
                            "pct_take_on_suc": 100.0,
                            "take_on_tkld": 0,
                            "pct_take_on_tkld": 0.0,
                            "carries": 38,
                            "ttl_carries_dist": 180,
                            "ttl_carries_prog_dist": 89,
                            "carries_fthird": 0,
                            "carries_opp_box": 0,
                            "carries_miscontrolled": 2,
                            "carries_dispossessed": 1,
                            "pass_recvd": 42,
                            "pass_prog_rcvd": 0
                        },
                        "misc": {
                            "second_yellow_cards": 0,
                            "fls_com": 2,
                            "fls_drawn": 1,
                            "offside": 0,
                            "pk_won": 0,
                            "pk_conceded": 0,
                            "og": 0,
                            "ball_recov": 8,
                            "air_dual_won": 1,
                            "air_dual_lost": 1,
                            "pct_air_dual_won": 50.0
                        }
                    }
                }
            ]
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

### Match Meta Data Object
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `match_id` | string | Football reference match ID | "404ee5d3" |
| `date` | string | Match date in YYYY-MM-DD format | "2019-08-10" |
| `round` | string | Competition round | "Matchweek 1" |
| `home_team` | string | Name of home team | "Tottenham" |
| `home_team_id` | string | Football reference home team ID | "361ca564" |
| `away_team` | string | Name of away team | "Manchester City" |
| `away_team_id` | string | Football reference away team ID | "b8fd03ef" |

### Player Meta Data Object
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `player_id` | string | Football reference player ID | "8b04d6c1" |
| `player_name` | string | Name of the player | "Pierre Højbjerg" |
| `player_country_code` | string | 3-letter country code | "DEN" |
| `age` | integer | Player age | 24 |
| `team` | string | Name of player's team | "Tottenham" |
| `team_id` | string | Football reference team ID | "361ca564" |
| `opponent` | string | Name of opponent team | "Manchester City" |
| `opponent_id` | string | Football reference opponent team ID | "b8fd03ef" |
| `formation` | string | Team formation | "4-1-4-1" |
| `position` | string | Player position | "MF" |
| `min` | integer | Minutes played | 90, 45, 30 |

### Stats Object Categories
The stats object contains multiple statistical categories:

- **stats**: Basic statistics (goals, assists, cards)
- **shooting**: Shot statistics (shots, goals, expected goals)
- **passing**: Passing statistics (completions, assists, key passes)
- **defense**: Defensive statistics (tackles, blocks, interceptions)
- **possession**: Possession statistics (touches, carries, take-ons)
- **misc**: Miscellaneous statistics (fouls, offsides, penalties)

## Usage Examples

### Get All Players Match Stats for League and Season
```bash
GET /all-players-match-stats?league_id=9&season_id=2023-2024
```

### Using curl
```bash
# Get all player match stats for Premier League 2023-2024
curl -H "X-API-Key: YOUR_API_KEY" \
     -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
     "https://fbrapi.com/all-players-match-stats/?league_id=9&season_id=2023-2024"

# Get all player match stats for Champions League 2023-2024
curl -H "X-API-Key: YOUR_API_KEY" \
     -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
     "https://fbrapi.com/all-players-match-stats/?league_id=8&season_id=2023-2024"
```

### Using Python
```python
import requests

headers = {
    'X-API-Key': 'YOUR_API_KEY',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
}

# Get all player match stats for Premier League 2023-2024
response = requests.get('https://fbrapi.com/all-players-match-stats/?league_id=9&season_id=2023-2024', headers=headers)
premier_league_all_stats = response.json()

# Get all player match stats for Champions League 2023-2024
response = requests.get('https://fbrapi.com/all-players-match-stats/?league_id=8&season_id=2023-2024', headers=headers)
champions_league_all_stats = response.json()
```

### Using JavaScript/Fetch
```javascript
fetch('https://fbrapi.com/all-players-match-stats/?league_id=9&season_id=2023-2024', {
    headers: {
        'X-API-Key': 'YOUR_API_KEY',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
})
.then(response => response.json())
.then(data => {
    console.log('Premier League All Players Match Stats:', data.data);
});
```

## Data Volume
- **Response Size**: Very large (detailed stats for all players in all matches)
- **Update Frequency**: Dynamic (after each match completion)
- **Data Availability**: Varies by league and season

## Dependencies
- **Requires**: League ID and season ID from other endpoints
- **Used by**: Applications needing comprehensive season-wide player analysis
- **Related**: `/matches` endpoint for basic match information

## Notes

All players match stats include:

- **Match Context**: Date, teams, round for each match
- **Player Performance**: Detailed statistics for every player in every match
- **Comprehensive Coverage**: All matches and all players in the season
- **Advanced Metrics**: Expected goals, key passes, tackles for all players

### Additional Notes
- This endpoint provides the most comprehensive player data available
- Data includes statistics for all players who participated in any match
- Some players may have limited data (substitutes, short appearances)
- Advanced metrics may not be available for all players
- This endpoint is ideal for season-wide player analysis and comparisons 