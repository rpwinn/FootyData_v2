"""
FBR API Client for FootyData_v2

Handles API requests to the FBR API with proper rate limiting.
"""

import requests
import time
import yaml
import os
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv
from .endpoint_config import get_endpoint_config, format_api_call

load_dotenv()

class FBRClient:
    """Client for interacting with the FBR API"""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        """Initialize the FBR API client"""
        self.api_key = os.getenv("FBR_API_KEY")
        if not self.api_key:
            raise ValueError("FBR_API_KEY environment variable not set")
        
        # Load configuration
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.base_url = self.config['api']['base_url']
        self.rate_limit_delay = self.config['api']['rate_limit_delay']
        self.timeout = self.config['api']['timeout']
        
        self.session = requests.Session()
        self.session.headers.update({
            'X-API-Key': self.api_key,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        
        self.last_request_time = 0
    
    def _rate_limit(self):
        """Ensure rate limiting compliance"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.rate_limit_delay:
            sleep_time = self.rate_limit_delay - time_since_last
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a rate-limited request to the FBR API"""
        self._rate_limit()
        
        # Add trailing slash to handle redirects properly
        url = f"{self.base_url}/{endpoint}/"
        
        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            return {"error": str(e)}
    
    def get_countries(self, country: Optional[str] = None) -> Dict[str, Any]:
        """Get countries data"""
        params = {"country": country} if country else None
        return self._make_request("countries", params)
    
    def get_leagues(self, country_code: Optional[str] = None) -> Dict[str, Any]:
        """Get leagues for a specific country or all leagues if no country specified"""
        params = {"country_code": country_code} if country_code else None
        return self._make_request("leagues", params)
    
    def get_league_seasons(self, league_id: int) -> Dict[str, Any]:
        """Get seasons for a specific league"""
        params = {"league_id": league_id}
        return self._make_request("league-seasons", params)
    
    def get_league_season_details(self, league_id: int, season_id: Optional[str] = None) -> Dict[str, Any]:
        """Get details for a specific league and season"""
        params = {"league_id": league_id}
        if season_id:
            params["season_id"] = season_id
        return self._make_request("league-season-details", params)
    
    def get_league_standings(self, league_id: int, season_id: Optional[str] = None) -> Dict[str, Any]:
        """Get league standings for a specific league and optionally season"""
        params = {"league_id": league_id}
        if season_id:
            params["season_id"] = season_id
        return self._make_request("league-standings", params)
    
    def get_league_standings_alt(self, league_id: str, season_id: str) -> Dict[str, Any]:
        """Alternative league standings endpoint"""
        params = {
            "league_id": league_id,
            "season_id": season_id
        }
        return self._make_request("standings", params)
    
    def get_league_standings_alt2(self, league_id: str, season_id: str) -> Dict[str, Any]:
        """Alternative league standings endpoint"""
        params = {
            "league_id": league_id,
            "season_id": season_id
        }
        return self._make_request("league-standings", params)
    
    def get_teams(self, team_id: str, season_id: Optional[str] = None) -> Dict[str, Any]:
        """Get team data for a specific team and optionally season"""
        params = {"team_id": team_id}
        if season_id:
            params["season_id"] = season_id
        return self._make_request("teams", params)
    
    def get_teams_by_league(self, league_id: str, season_id: str) -> Dict[str, Any]:
        """Get teams for a specific league and season (if this endpoint exists)"""
        params = {
            "league_id": league_id,
            "season_id": season_id
        }
        return self._make_request("teams", params)
    
    def get_players(self, player_id: str) -> Dict[str, Any]:
        """Get player data for a specific player"""
        params = {"player_id": player_id}
        return self._make_request("players", params)
    
    def get_players_by_team(self, team_id: str, league_id: str, season_id: str) -> Dict[str, Any]:
        """Get players for a specific team, league and season (if this endpoint exists)"""
        params = {
            "team_id": team_id,
            "league_id": league_id,
            "season_id": season_id
        }
        return self._make_request("players", params)
    
    def get_team_season_stats(self, league_id: int, season_id: Optional[str] = None) -> Dict[str, Any]:
        """Get team season statistics for a specific league and optionally season"""
        params = {"league_id": league_id}
        if season_id:
            params["season_id"] = season_id
        return self._make_request("team-season-stats", params)
    
    def get_team_season_stats_by_team(self, team_id: str, league_id: str, season_id: str) -> Dict[str, Any]:
        """Get team season statistics for a specific team (if this endpoint exists)"""
        params = {
            "team_id": team_id,
            "league_id": league_id,
            "season_id": season_id
        }
        return self._make_request("team-season-stats", params)
    
    def get_player_season_stats(self, team_id: str, league_id: int, season_id: Optional[str] = None) -> Dict[str, Any]:
        """Get player season statistics for a specific team, league and optionally season"""
        params = {"team_id": team_id, "league_id": league_id}
        if season_id:
            params["season_id"] = season_id
        return self._make_request("player-season-stats", params)
    
    def get_player_season_stats_by_player(self, player_id: str, league_id: str, season_id: str) -> Dict[str, Any]:
        """Get player season statistics for a specific player (if this endpoint exists)"""
        params = {
            "player_id": player_id,
            "league_id": league_id,
            "season_id": season_id
        }
        return self._make_request("player-season-stats", params)
    
    def get_matches(self, league_id: str, season_id: str, team_id: Optional[str] = None) -> Dict[str, Any]:
        """Get matches for a specific league and season, optionally filtered by team"""
        params = {
            "league_id": league_id,
            "season_id": season_id
        }
        if team_id:
            params["team_id"] = team_id
        return self._make_request("matches", params)
    
    def get_match_stats(self, match_id: str) -> Dict[str, Any]:
        """Get match stats for all players in a specific match"""
        params = {"match_id": match_id}
        return self._make_request("all-players-match-stats", params)
    
    def test_connection(self) -> bool:
        """Test API connection by making a simple request"""
        try:
            result = self.get_countries()
            return "error" not in result
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False 

    def get_endpoint_info(self, endpoint_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific endpoint"""
        config = get_endpoint_config(endpoint_name)
        if not config:
            return None
        
        return {
            "name": config.name,
            "path": config.path,
            "status": config.status.value,
            "required_params": config.required_params,
            "optional_params": config.optional_params,
            "description": config.description,
            "example_request": config.example_request,
            "example_response": config.example_response,
            "notes": config.notes
        }
    
    def format_api_call(self, endpoint_name: str, params: Dict[str, Any]) -> str:
        """Format an API call for the given endpoint"""
        return format_api_call(endpoint_name, params)
    
    def get_working_endpoints(self) -> List[str]:
        """Get list of working endpoint names"""
        from .endpoint_config import get_working_endpoints
        return [config.name for config in get_working_endpoints()]
    
    def get_failing_endpoints(self) -> List[str]:
        """Get list of failing endpoint names"""
        from .endpoint_config import get_failing_endpoints
        return [config.name for config in get_failing_endpoints()] 