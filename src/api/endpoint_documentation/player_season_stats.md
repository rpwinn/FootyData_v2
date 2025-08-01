# /player-season-stats Endpoint Documentation

## Overview
Endpoint to retrieve aggregate season stats for all players for a team-league-season. This provides comprehensive player performance statistics aggregated over the entire season.

## Endpoint Details
- **URL**: `/player-season-stats`
- **Method**: GET
- **Base URL**: https://fbrapi.com

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `team_id` | string | Yes | 8-character string representing a team's football reference id |
| `league_id` | integer | Yes | Integer representing a league's football reference id |
| `season_id` | string | No | Football reference season that is either in "%Y" or "%Y-%Y" format, depending on the league. If not provided, endpoint retrieves data for most recent season for provided league_id |

## Response Structure

### Success Response (200)
```json
{
    "players": [
        {
            "meta_data": {
                "player_id": "8b04d6c1",
                "player_name": "Pierre Højbjerg",
                "player_country_code": "DEN",
                "age": 24
            },
            "stats": {
                "stats": {
                    "positions": "MF",
                    "matches_played": 38,
                    "starts": 38,
                    "min": 3420,
                    "gls": 2,
                    "ast": 4,
                    "gls_and_ast": 6,
                    "non_pen_gls": 2,
                    "xg": 1.1,
                    "non_pen_xg": 1.1,
                    "xag": 1.6,
                    "pk_made": 0,
                    "pk_att": 0,
                    "yellow_cards": 9,
                    "red_cards": 0,
                    "carries_prog": 36,
                    "passes_prog": 218,
                    "per90_gls": 0.05,
                    "per90_ast": 0.11,
                    "per90_non_pen_gls": 0.05,
                    "per90_xg": 0.03,
                    "per90_xag": 0.04,
                    "per90_non_pen_xg": 0.03
                },
                "shooting": {
                    "sh": 14,
                    "sot": 7,
                    "pct_sot": 50.0,
                    "per90_sh": 0.37,
                    "per90_sot": 0.18,
                    "gls_per_sh": 0.14,
                    "gls_per_sot": 0.29,
                    "avg_sh_dist": 24.0,
                    "fk_sh": 0,
                    "npxg_per_sh": 0.08,
                    "gls_xg_diff": 0.9,
                    "non_pen_gls_xg_diff": 0.9
                },
                "passing": {
                    "pass_cmp": 2455,
                    "pass_att": 2783,
                    "pct_pass_cmp": 88.2,
                    "pass_ttl_dist": 40417,
                    "pass_cmp_s": 1161,
                    "pass_att_s": 1263,
                    "pct_pass_cmp_s": 91.9,
                    "pass_cmp_m": 1033,
                    "pass_att_m": 1129,
                    "pct_pass_cmp_m": 91.5,
                    "pass_cmp_l": 173,
                    "pass_att_l": 257,
                    "pct_pass_cmp_l": 67.3,
                    "xa": 1.3,
                    "ast_xag_diff": 2.4,
                    "pass_prog": 218,
                    "pass_prog_ttl_dist": 12152,
                    "key_passes": 16,
                    "pass_fthird": 208,
                    "pass_opp_box": 17,
                    "cross_opp_box": 1
                },
                "defense": {
                    "tkl": 98,
                    "tkl_won": 51,
                    "tkl_def_third": 45,
                    "tkl_mid_third": 42,
                    "tkl_att_third": 11,
                    "tkl_drb": 54,
                    "tkl_drb_att": 129,
                    "pct_tkl_drb_suc": 41.9,
                    "blocks": 51,
                    "sh_blocked": 9,
                    "int": 48,
                    "tkl_plus_int": 146,
                    "clearances": 66,
                    "def_error": 0
                },
                "possession": {
                    "touches": 3116,
                    "touch_def_box": 120,
                    "touch_def_third": 712,
                    "touch_mid_third": 2126,
                    "touch_fthird": 308,
                    "touch_opp_box": 20,
                    "touch_live": 3116,
                    "take_on_att": 32,
                    "take_on_suc": 23,
                    "pct_take_on_suc": 71.9,
                    "take_on_tkld": 9,
                    "pct_take_on_tkld": 28.1,
                    "carries": 1794,
                    "ttl_carries_dist": 8521,
                    "ttl_carries_prog_dist": 4176,
                    "carries_fthird": 33,
                    "carries_opp_box": 2,
                    "carries_miscontrolled": 37,
                    "carries_dispossessed": 20,
                    "pass_recvd": 2224,
                    "pass_prog_rcvd": 26
                },
                "playingtime": {
                    "min_per_match_played": 90.0,
                    "pct_squad_min": 100.0,
                    "avg_min_starter": 90.0,
                    "subs": 0,
                    "avg_min_sub": null,
                    "unused_sub": 0,
                    "team_gls_on_pitch": 68,
                    "team_gls_ag_on_pitch": 45,
                    "per90_plus_minus": "+0.61",
                    "per90_on_off": "",
                    "team_xg_on_pitch": 53.1,
                    "team_xg_ag_on_pitch": 49.1,
                    "per90_x_plus_minus": "+0.10",
                    "per90_x_on_off": ""
                },
                "misc": {
                    "second_yellow_cards": 0,
                    "fls_com": 69,
                    "fls_drawn": 53,
                    "offside": 0,
                    "pk_won": 0,
                    "pk_conceded": 1,
                    "og": 0,
                    "ball_recov": 296,
                    "air_dual_won": 43,
                    "air_dual_lost": 36,
                    "pct_air_dual_won": 54.4
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
| `player_id` | string | Football reference player ID | "8b04d6c1" |
| `player_name` | string | Name of the player | "Pierre Højbjerg" |
| `player_country_code` | string | 3-letter country code | "DEN" |
| `age` | integer | Player age | 24 |

### Stats Object Categories
The stats object contains multiple statistical categories:

- **stats**: Basic statistics (goals, assists, minutes, cards)
- **shooting**: Shot statistics (shots, goals, expected goals)
- **passing**: Passing statistics (completions, assists, key passes)
- **defense**: Defensive statistics (tackles, blocks, interceptions)
- **possession**: Possession statistics (touches, carries, take-ons)
- **playingtime**: Playing time statistics (minutes, substitutions)
- **misc**: Miscellaneous statistics (fouls, offsides, penalties)

## Usage Examples

### Get Player Season Stats for Team, League and Season
```bash
GET /player-season-stats?team_id=b8fd03ef&league_id=9&season_id=2023-2024
```

### Get Player Season Stats for Most Recent Season
```bash
GET /player-season-stats?team_id=b8fd03ef&league_id=9
```

### Using curl
```bash
# Get Manchester City player stats for Premier League 2023-2024
curl -H "X-API-Key: YOUR_API_KEY" \
     -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
     "https://fbrapi.com/player-season-stats/?team_id=b8fd03ef&league_id=9&season_id=2023-2024"

# Get Arsenal player stats for Champions League 2023-2024
curl -H "X-API-Key: YOUR_API_KEY" \
     -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
     "https://fbrapi.com/player-season-stats/?team_id=18bb7c10&league_id=8&season_id=2023-2024"
```

### Using Python
```python
import requests

headers = {
    'X-API-Key': 'YOUR_API_KEY',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
}

# Get Manchester City player stats
response = requests.get('https://fbrapi.com/player-season-stats/?team_id=b8fd03ef&league_id=9&season_id=2023-2024', headers=headers)
man_city_player_stats = response.json()

# Get Arsenal player stats
response = requests.get('https://fbrapi.com/player-season-stats/?team_id=18bb7c10&league_id=8&season_id=2023-2024', headers=headers)
arsenal_player_stats = response.json()
```

### Using JavaScript/Fetch
```javascript
fetch('https://fbrapi.com/player-season-stats/?team_id=b8fd03ef&league_id=9&season_id=2023-2024', {
    headers: {
        'X-API-Key': 'YOUR_API_KEY',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
})
.then(response => response.json())
.then(data => {
    console.log('Manchester City Player Stats:', data.players);
});
```

## Data Volume
- **Response Size**: Very large (detailed stats for all players)
- **Update Frequency**: Static (season completed) to dynamic (ongoing season)
- **Data Availability**: Varies by team, league and season

## Dependencies
- **Requires**: Team ID and league ID from other endpoints
- **Used by**: Applications needing detailed player performance analysis
- **Related**: `/players` endpoint for individual player metadata

## Notes

Player season stats include:

- **Basic Statistics**: Goals, assists, minutes, appearances
- **Advanced Metrics**: Expected goals, key passes, tackles
- **Performance Indicators**: Per-90 statistics, team impact
- **Detailed Categories**: Shooting, passing, defense, possession

### Additional Notes
- Data represents complete season statistics for all players
- Per-90 statistics provide normalized performance metrics
- Advanced metrics may not be available for all players
- Some statistical categories may have limited data availability 