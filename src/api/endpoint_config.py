"""
FBR API Endpoint Configuration
Stores proper formats, parameters, and examples for all API endpoints
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

class EndpointStatus(Enum):
    WORKING = "✅ WORKING"
    FAILING = "❌ FAILING"
    PARTIAL = "⚠️ PARTIAL"
    UNTESTED = "❓ UNTESTED"

@dataclass
class EndpointConfig:
    """Configuration for a single API endpoint"""
    name: str
    path: str
    status: EndpointStatus
    required_params: Dict[str, str]  # param_name: param_type
    optional_params: Dict[str, str]  # param_name: param_type
    description: str
    example_request: Dict[str, Any]
    example_response: Dict[str, Any]
    notes: str = ""

# FBR API Endpoint Configurations
ENDPOINT_CONFIGS = {
    "countries": EndpointConfig(
        name="Countries",
        path="/countries",
        status=EndpointStatus.WORKING,
        required_params={},
        optional_params={"country": "string"},
        description="Returns list of all countries with metadata",
        example_request={},
        example_response={
            "country": "Afghanistan",
            "country_code": "AFG",
            "governing_body": "AFC",
            "#_clubs": 0,
            "#_players": 215,
            "national_teams": ["M", "F"]
        },
        notes="Returns 225 countries"
    ),
    
    "leagues": EndpointConfig(
        name="Leagues",
        path="/leagues",
        status=EndpointStatus.WORKING,
        required_params={},
        optional_params={"country_code": "string"},
        description="Returns leagues organized by type",
        example_request={"country_code": "ENG"},
        example_response={
            "league_type": "domestic_leagues",
            "leagues": [
                {
                    "league_id": 9,
                    "competition_name": "Premier League",
                    "gender": "M",
                    "first_season": "1888-1889",
                    "last_season": "2025-2026",
                    "tier": "1st"
                }
            ]
        },
        notes="Returns leagues by country code"
    ),
    
    "league_seasons": EndpointConfig(
        name="League Seasons",
        path="/league-seasons",
        status=EndpointStatus.WORKING,
        required_params={"league_id": "string"},
        optional_params={},
        description="Returns all seasons for a specific league",
        example_request={"league_id": "9"},
        example_response={
            "season_id": "2025-2026",
            "competition_name": "Premier League",
            "#_squads": 20,
            "champion": "",
            "top_scorer": {
                "player": "",
                "goals_scored": None
            }
        },
        notes="Returns 127 seasons for Premier League"
    ),
    
    "league_standings": EndpointConfig(
        name="League Standings",
        path="/league-standings",
        status=EndpointStatus.FAILING,
        required_params={"league_id": "int"},
        optional_params={"season_id": "string"},
        description="Returns league standings table",
        example_request={"league_id": 9, "season_id": "2024-2025"},
        example_response={"error": "500 Server Error"},
        notes="Consistently returns 500 Server Error - server-side issue"
    ),
    
    "teams": EndpointConfig(
        name="Teams",
        path="/teams",
        status=EndpointStatus.WORKING,
        required_params={"team_id": "string"},
        optional_params={"season_id": "string"},
        description="Returns team roster and schedule data",
        example_request={"team_id": "19538871", "season_id": "2024-2025"},
        example_response={
            "team_roster": [{"player_id": "abc123", "name": "Player Name"}],
            "team_schedule": [{"match_id": "xyz789", "date": "2024-08-16"}]
        },
        notes="Returns team roster (71 players) and schedule (67 matches)"
    ),
    
    "players": EndpointConfig(
        name="Players",
        path="/players",
        status=EndpointStatus.WORKING,
        required_params={"player_id": "string"},
        optional_params={},
        description="Returns detailed player metadata",
        example_request={"player_id": "4d224fe8"},
        example_response={
            "player_id": "4d224fe8",
            "full_name": "Casemiro",
            "positions": ["MF", "CM", "DM"],
            "footed": "Right",
            "date_of_birth": "1992-02-23",
            "birth_city": "São José dos Campos",
            "nationality": "Brazil",
            "wages": "350000 Weekly",
            "height": 184.0,
            "weight": 79.0
        },
        notes="Returns detailed player metadata including positions, nationality, wages"
    ),
    
    "team_season_stats": EndpointConfig(
        name="Team Season Stats",
        path="/team-season-stats",
        status=EndpointStatus.WORKING,
        required_params={"league_id": "int"},
        optional_params={"season_id": "string"},
        description="Returns comprehensive team statistics for all teams in league",
        example_request={"league_id": 9, "season_id": "2024-2025"},
        example_response={
            "meta_data": {"team_id": "18bb7c10", "team_name": "Arsenal"},
            "stats": {
                "stats": {"roster_size": 25, "matches_played": 38},
                "shooting": {"ttl_sh": 544, "ttl_sot": 178},
                "passing": {"ttl_pass_cmp": 17066, "pct_pass_cmp": 84.3}
            }
        },
        notes="Returns comprehensive team statistics including shooting, passing, defense, possession, goalkeeping"
    ),
    
    "player_season_stats": EndpointConfig(
        name="Player Season Stats",
        path="/player-season-stats",
        status=EndpointStatus.WORKING,
        required_params={"team_id": "string", "league_id": "int"},
        optional_params={"season_id": "string"},
        description="Returns comprehensive player statistics for all players in team",
        example_request={"team_id": "19538871", "league_id": 9, "season_id": "2024-2025"},
        example_response={
            "outfield": [{"meta_data": {"player_id": "abc123"}, "stats": {}}],
            "keepers": [{"meta_data": {"player_id": "def456"}, "stats": {}}]
        },
        notes="Returns detailed stats including shooting, passing, defense, possession, goalkeeping"
    ),
    
    "matches": EndpointConfig(
        name="Matches",
        path="/matches",
        status=EndpointStatus.WORKING,
        required_params={"league_id": "string", "season_id": "string"},
        optional_params={"team_id": "string"},
        description="Returns all matches for a league and season",
        example_request={"league_id": "9", "season_id": "2024-2025"},
        example_response={
            "match_id": "cc5b4244",
            "date": "2024-08-16",
            "time": "20:00",
            "wk": "1",
            "home": "Manchester Utd",
            "home_team_id": "19538871",
            "away": "Fulham",
            "away_team_id": "fd962109",
            "home_team_score": None,
            "away_team_score": None,
            "venue": "Old Trafford",
            "attendance": "73,297",
            "referee": "Robert Jones"
        },
        notes="Returns 380 matches per season"
    ),
    
    "all_players_match_stats": EndpointConfig(
        name="All Players Match Stats",
        path="/all-players-match-stats",
        status=EndpointStatus.WORKING,
        required_params={"match_id": "string"},
        optional_params={},
        description="Returns comprehensive player statistics for all players in a match",
        example_request={"match_id": "cc5b4244"},
        example_response={
            "summary": [{"player_id": "abc123", "name": "Player Name"}],
            "passing": [{"player_id": "abc123", "passes": 45}],
            "defense": [{"player_id": "abc123", "tackles": 3}],
            "possession": [{"player_id": "abc123", "touches": 67}],
            "misc": [{"player_id": "abc123", "fouls": 1}],
            "keepers": [{"player_id": "def456", "saves": 4}]
        },
        notes="Returns comprehensive player statistics across multiple categories"
    )
}

def get_endpoint_config(endpoint_name: str) -> Optional[EndpointConfig]:
    """Get configuration for a specific endpoint"""
    return ENDPOINT_CONFIGS.get(endpoint_name)

def get_working_endpoints() -> List[EndpointConfig]:
    """Get all working endpoints"""
    return [config for config in ENDPOINT_CONFIGS.values() if config.status == EndpointStatus.WORKING]

def get_failing_endpoints() -> List[EndpointConfig]:
    """Get all failing endpoints"""
    return [config for config in ENDPOINT_CONFIGS.values() if config.status == EndpointStatus.FAILING]

def get_endpoint_status_summary() -> Dict[str, int]:
    """Get summary of endpoint statuses"""
    summary = {}
    for status in EndpointStatus:
        count = len([config for config in ENDPOINT_CONFIGS.values() if config.status == status])
        summary[status.value] = count
    return summary

def format_api_call(endpoint_name: str, params: Dict[str, Any]) -> str:
    """Format an API call for the given endpoint"""
    config = get_endpoint_config(endpoint_name)
    if not config:
        return f"Unknown endpoint: {endpoint_name}"
    
    # Build URL with parameters
    url = f"GET {config.path}"
    if params:
        param_str = "&".join([f"{k}={v}" for k, v in params.items()])
        url += f"?{param_str}"
    
    return url

# Example usage functions
def get_example_calls() -> Dict[str, str]:
    """Get example API calls for all endpoints"""
    examples = {}
    for name, config in ENDPOINT_CONFIGS.items():
        if config.example_request:
            examples[name] = format_api_call(name, config.example_request)
        else:
            examples[name] = format_api_call(name, {})
    return examples 