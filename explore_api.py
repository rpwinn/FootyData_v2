#!/usr/bin/env python3
"""
Explore FBR API responses to understand the actual data structure
"""

import sys
import os
import argparse
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import json
from api.fbr_client import FBRClient

def explore_countries(client):
    """Explore countries endpoint"""
    print("\n=== COUNTRIES ENDPOINT ===")
    countries = client.get_countries()
    if "error" not in countries and countries.get('data'):
        print(f"Found {len(countries['data'])} countries")
        print("Sample country data:")
        sample_country = countries['data'][0]
        print(json.dumps(sample_country, indent=2))
        return True
    else:
        print(f"Error: {countries.get('error', 'Unknown error')}")
        return False

def explore_leagues(client, country_code=None):
    """Explore leagues endpoint"""
    if country_code:
        print(f"\n=== LEAGUES ENDPOINT ({country_code}) ===")
    else:
        print(f"\n=== LEAGUES ENDPOINT (No country specified) ===")
    leagues = client.get_leagues(country_code)
    if "error" not in leagues and leagues.get('data'):
        print("Full leagues response structure:")
        print(json.dumps(leagues, indent=2))
        
        # Extract leagues from the nested structure
        if isinstance(leagues.get('data'), list):
            for league_type in leagues['data']:
                print(f"\nLeague Type: {league_type.get('league_type')}")
                leagues_list = league_type.get('leagues', [])
                print(f"Found {len(leagues_list)} leagues")
                if leagues_list:
                    print("Sample league data:")
                    print(json.dumps(leagues_list[0], indent=2))
        return True
    else:
        print(f"Error: {leagues.get('error', 'Unknown error')}")
        return False

def explore_league_seasons(client, league_id="9"):
    """Explore league seasons endpoint"""
    print(f"\n=== LEAGUE SEASONS ENDPOINT (League {league_id}) ===")
    seasons = client.get_league_seasons(league_id)
    if "error" not in seasons and seasons.get('data'):
        print(f"Found {len(seasons['data'])} seasons")
        print("Sample season data:")
        sample_season = seasons['data'][0]
        print(json.dumps(sample_season, indent=2))
        return True
    else:
        print(f"Error: {seasons.get('error', 'Unknown error')}")
        return False

def explore_league_standings(client, league_id=9, season_id=None):
    """Explore league standings endpoint using league_id and season_id"""
    print(f"\n=== LEAGUE STANDINGS ENDPOINT (League {league_id}, Season {season_id or 'current'}) ===")
    standings = client.get_league_standings(league_id, season_id)
    print(f"Full response: {json.dumps(standings, indent=2)}")  # Added for debugging
    if "error" not in standings and standings.get('data'):
        print(f"Found league standings")
        print("Sample standings data:")
        print(json.dumps(standings['data'][0], indent=2))
        return True
    else:
        print(f"Error: {standings.get('error', 'Unknown error')}")
        return False

def explore_league_standings_by_team(client, team_id, league_id="9", season_id="2022-2023"):
    """Explore league standings endpoint using team parameters (if this exists)"""
    print(f"\n=== LEAGUE STANDINGS BY TEAM ENDPOINT (Team {team_id}, League {league_id}, Season {season_id}) ===")
    standings = client.get_league_standings_by_team(team_id, league_id, season_id)
    if "error" not in standings and standings.get('data'):
        print("Found league standings")
        print("Sample standings data:")
        print(json.dumps(standings['data'][0], indent=2))
        return True
    else:
        print(f"Error: {standings.get('error', 'Unknown error')}")
        return False

def explore_teams(client, league_id="9", season_id="2022-2023"):
    """Explore teams endpoint"""
    print(f"\n=== TEAMS ENDPOINT (League {league_id}, Season {season_id}) ===")
    teams = client.get_teams_by_league(league_id, season_id)
    if "error" not in teams and teams.get('data'):
        print(f"Found {len(teams['data'])} teams")
        print("Sample team data:")
        sample_team = teams['data'][0]
        print(json.dumps(sample_team, indent=2))
        return True
    else:
        print(f"Error: {teams.get('error', 'Unknown error')}")
        return False

def explore_team_by_id(client, team_id="19538871", season_id="2024-2025"):
    """Explore team endpoint using team_id"""
    print(f"\n=== TEAM BY ID ENDPOINT (Team {team_id}, Season {season_id}) ===")
    team = client.get_teams(team_id, season_id)
    print(f"Full response: {json.dumps(team, indent=2)}")
    if "error" not in team and team.get('data'):
        print("Found team data")
        print("Sample team data:")
        print(json.dumps(team['data'], indent=2))
        return True
    else:
        print(f"Error: {team.get('error', 'Unknown error')}")
        return False

def explore_players(client, player_id="4d224fe8"):
    """Explore players endpoint using player_id"""
    print(f"\n=== PLAYERS ENDPOINT (Player {player_id}) ===")
    players = client.get_players(player_id)
    print(f"Full response: {json.dumps(players, indent=2)}")
    if "error" not in players and players.get('player_id'):
        print("✅ Found player data")
        print("Sample player data:")
        print(json.dumps(players, indent=2))
        return True
    else:
        print(f"Error: {players.get('error', 'Unknown error')}")
        return False

def explore_players_by_team(client, team_id, league_id="9", season_id="2022-2023"):
    """Explore players endpoint using team parameters (if this exists)"""
    print(f"\n=== PLAYERS BY TEAM ENDPOINT (Team {team_id}, League {league_id}, Season {season_id}) ===")
    players = client.get_players_by_team(team_id, league_id, season_id)
    if "error" not in players and players.get('data'):
        print(f"Found {len(players['data'])} players")
        print("Sample player data:")
        sample_player = players['data'][0]
        print(json.dumps(sample_player, indent=2))
        return True
    else:
        print(f"Error: {players.get('error', 'Unknown error')}")
        return False

def explore_team_season_stats(client, league_id=9, season_id="2024-2025"):
    """Explore team season stats endpoint using league_id and season_id"""
    print(f"\n=== TEAM SEASON STATS ENDPOINT (League {league_id}, Season {season_id}) ===")
    team_stats = client.get_team_season_stats(league_id, season_id)
    if "error" not in team_stats and team_stats.get('data'):
        print(f"Found team season stats")
        print("Sample team stats data:")
        print(json.dumps(team_stats['data'][0], indent=2))
        return True
    else:
        print(f"Error: {team_stats.get('error', 'Unknown error')}")
        return False

def explore_team_season_stats_by_team(client, team_id, league_id="9", season_id="2022-2023"):
    """Explore team season stats endpoint using team parameters (if this exists)"""
    print(f"\n=== TEAM SEASON STATS BY TEAM ENDPOINT (Team {team_id}, League {league_id}, Season {season_id}) ===")
    team_stats = client.get_team_season_stats_by_team(team_id, league_id, season_id)
    if "error" not in team_stats and team_stats.get('data'):
        print("Found team season stats")
        print("Sample team stats data:")
        print(json.dumps(team_stats['data'][0], indent=2))
        return True
    else:
        print(f"Error: {team_stats.get('error', 'Unknown error')}")
        return False

def explore_player_season_stats(client, team_id="19538871", league_id=9, season_id="2024-2025"):
    """Explore player season stats endpoint using team_id, league_id and season_id"""
    print(f"\n=== PLAYER SEASON STATS ENDPOINT (Team {team_id}, League {league_id}, Season {season_id}) ===")
    player_stats = client.get_player_season_stats(team_id, league_id, season_id)
    print(f"Full response: {json.dumps(player_stats, indent=2)}")  # Added for debugging
    if "error" not in player_stats and (player_stats.get('outfield') or player_stats.get('keepers')):
        print(f"Found player season stats")
        print(f"Outfield players: {len(player_stats.get('outfield', []))}")
        print(f"Goalkeepers: {len(player_stats.get('keepers', []))}")
        if player_stats.get('outfield'):
            print("Sample outfield player stats:")
            print(json.dumps(player_stats['outfield'][0], indent=2))
        elif player_stats.get('keepers'):
            print("Sample goalkeeper stats:")
            print(json.dumps(player_stats['keepers'][0], indent=2))
        return True
    else:
        print(f"Error: {player_stats.get('error', 'Unknown error')}")
        return False

def explore_player_season_stats_by_player(client, player_id, league_id="9", season_id="2022-2023"):
    """Explore player season stats endpoint using player parameters (if this exists)"""
    print(f"\n=== PLAYER SEASON STATS BY PLAYER ENDPOINT (Player {player_id}, League {league_id}, Season {season_id}) ===")
    player_stats = client.get_player_season_stats_by_player(player_id, league_id, season_id)
    if "error" not in player_stats and player_stats.get('data'):
        print("Found player season stats")
        print("Sample player stats data:")
        print(json.dumps(player_stats['data'][0], indent=2))
        return True
    else:
        print(f"Error: {player_stats.get('error', 'Unknown error')}")
        return False

def explore_matches(client, league_id="9", season_id="2022-2023", team_id=None):
    """Explore matches endpoint"""
    if team_id:
        print(f"\n=== MATCHES ENDPOINT (League {league_id}, Season {season_id}, Team {team_id}) ===")
    else:
        print(f"\n=== MATCHES ENDPOINT (League {league_id}, Season {season_id}) ===")
    matches = client.get_matches(league_id, season_id, team_id)
    if "error" not in matches and matches.get('data'):
        print(f"Found {len(matches['data'])} matches")
        print("Sample match data:")
        sample_match = matches['data'][0]
        print(json.dumps(sample_match, indent=2))
        return True
    else:
        print(f"Error: {matches.get('error', 'Unknown error')}")
        return False

def explore_match_stats(client, match_id):
    """Explore match stats endpoint"""
    print(f"\n=== MATCH STATS ENDPOINT (Match {match_id}) ===")
    match_stats = client.get_match_stats(match_id)
    if "error" not in match_stats and match_stats.get('data'):
        print(f"Found match stats data")
        print("Sample match stats data:")
        print(json.dumps(match_stats['data'][0], indent=2))
        return True
    else:
        print(f"Error: {match_stats.get('error', 'Unknown error')}")
        return False

def explore_all_endpoints(client):
    """Explore all endpoints"""
    print("🔍 Exploring all FBR API endpoints...")
    print("Note: Each API call has a 3-second delay for rate limiting compliance.")
    
    # Test all endpoints in sequence
    explore_countries(client)
    explore_leagues(client, "ENG")
    explore_leagues(client, "ESP")
    explore_league_seasons(client, "9")
    explore_league_standings(client, "9", "2022-2023")
    explore_teams(client, "9", "2022-2023")
    explore_team_by_id(client, "19538871", "2024-2025") # Test team_id approach
    
    # Note: These require a valid team_id, so we'll skip them for now
    print("\n=== SKIPPING TEAM-DEPENDENT ENDPOINTS ===")
    print("The following endpoints require a valid team_id from the teams endpoint:")
    print("- Players")
    print("- Team Season Stats") 
    print("- Player Season Stats")
    print("- Matches")
    print("Run with --endpoint teams first to get a team_id, then test others.")

def test_parameter_formats(client):
    """Test different parameter formats for failing endpoints"""
    print("\n=== TESTING PARAMETER FORMATS ===")
    
    # Test different league_id formats
    league_formats = ["9", 9, "9", "9"]
    season_formats = ["2024-2025", "2024", "2024-25", "2024/2025"]
    
    print("Testing league-standings with different formats:")
    for i, (league_fmt, season_fmt) in enumerate(zip(league_formats, season_formats)):
        print(f"  Test {i+1}: league_id={league_fmt} ({type(league_fmt)}), season_id={season_fmt}")
        result = client.get_league_standings(str(league_fmt), str(season_fmt))
        if "error" not in result:
            print(f"    ✅ SUCCESS with format {i+1}")
            return True
        else:
            print(f"    ❌ Failed: {result.get('error', 'Unknown error')}")
    
    print("\nTesting teams with different formats:")
    team_formats = ["19538871", 19538871, "19538871", "19538871"]
    for i, (team_fmt, season_fmt) in enumerate(zip(team_formats, season_formats)):
        print(f"  Test {i+1}: team_id={team_fmt} ({type(team_fmt)}), season_id={season_fmt}")
        result = client.get_teams(str(team_fmt), str(season_fmt))
        if "error" not in result:
            print(f"    ✅ SUCCESS with format {i+1}")
            return True
        else:
            print(f"    ❌ Failed: {result.get('error', 'Unknown error')}")
    
    return False

def test_alternative_endpoints(client):
    """Test alternative endpoint names for failing endpoints"""
    print("\n=== TESTING ALTERNATIVE ENDPOINT NAMES ===")
    
    # Test alternative standings endpoints
    print("Testing alternative standings endpoints:")
    alt_endpoints = ["standings", "league-standings", "table", "league-table"]
    
    for endpoint in alt_endpoints:
        print(f"  Testing endpoint: /{endpoint}")
        try:
            # Make direct request to test endpoint
            url = f"{client.base_url}/{endpoint}"
            params = {"league_id": "9", "season_id": "2024-2025"}
            response = client.session.get(url, params=params, timeout=client.timeout)
            if response.status_code == 200:
                print(f"    ✅ SUCCESS with endpoint /{endpoint}")
                return True
            else:
                print(f"    ❌ Failed with status {response.status_code}")
        except Exception as e:
            print(f"    ❌ Error: {e}")
    
    return False

def main():
    """Main function with command line arguments"""
    parser = argparse.ArgumentParser(description='Explore FBR API endpoints')
    parser.add_argument('--endpoint', choices=[
        'countries', 'leagues', 'league-seasons', 'league-standings', 'league-standings-by-team',
        'teams', 'team-by-id', 'players', 'players-by-team', 'team-stats', 'team-stats-by-team', 'player-stats', 'player-stats-by-player', 'matches', 'match-stats', 'test-formats', 'test-alternatives', 'all'
    ], default='all', help='Endpoint to explore')
    parser.add_argument('--country', default='ENG', help='Country code for leagues endpoint')
    parser.add_argument('--league-id', default='9', help='League ID for various endpoints')
    parser.add_argument('--season-id', default=None, help='Season ID for various endpoints')
    parser.add_argument('--team-id', help='Team ID for team-dependent endpoints')
    parser.add_argument('--player-id', help='Player ID for players endpoint')
    parser.add_argument('--match-id', help='Match ID for match-stats endpoint')
    
    args = parser.parse_args()
    
    client = FBRClient()
    
    if args.endpoint == 'all':
        explore_all_endpoints(client)
    elif args.endpoint == 'countries':
        explore_countries(client)
    elif args.endpoint == 'leagues':
        explore_leagues(client, args.country)
    elif args.endpoint == 'league-seasons':
        explore_league_seasons(client, args.league_id)
    elif args.endpoint == 'league-standings':
        # Convert league_id to int and handle optional season_id
        league_id = int(args.league_id)
        season_id = args.season_id if args.season_id else None
        explore_league_standings(client, league_id, season_id)
    elif args.endpoint == 'league-standings-by-team':
        if not args.team_id:
            print("Error: --team-id is required for league-standings-by-team endpoint")
            return
        explore_league_standings_by_team(client, args.team_id, args.league_id, args.season_id)
    elif args.endpoint == 'teams':
        explore_teams(client, args.league_id, args.season_id)
    elif args.endpoint == 'team-by-id':
        if not args.team_id:
            print("Error: --team-id is required for team-by-id endpoint")
            return
        explore_team_by_id(client, args.team_id, args.season_id)
    elif args.endpoint == 'players':
        if not args.player_id:
            print("Error: --player-id is required for players endpoint")
            return
        explore_players(client, args.player_id)
    elif args.endpoint == 'players-by-team':
        if not args.team_id:
            print("Error: --team-id is required for players-by-team endpoint")
            return
        explore_players_by_team(client, args.team_id, args.league_id, args.season_id)
    elif args.endpoint == 'team-stats':
        explore_team_season_stats(client, args.league_id, args.season_id)
    elif args.endpoint == 'team-stats-by-team':
        if not args.team_id:
            print("Error: --team-id is required for team-stats-by-team endpoint")
            return
        explore_team_season_stats_by_team(client, args.team_id, args.league_id, args.season_id)
    elif args.endpoint == 'player-stats':
        # Convert league_id to int and handle optional season_id
        league_id = int(args.league_id)
        season_id = args.season_id if args.season_id else None
        explore_player_season_stats(client, args.team_id, league_id, season_id)
    elif args.endpoint == 'player-stats-by-player':
        if not args.player_id:
            print("Error: --player-id is required for player-stats-by-player endpoint")
            return
        explore_player_season_stats_by_player(client, args.player_id, args.league_id, args.season_id)
    elif args.endpoint == 'matches':
        explore_matches(client, args.league_id, args.season_id, args.team_id)
    elif args.endpoint == 'match-stats':
        if not args.match_id:
            print("Error: --match-id is required for match-stats endpoint")
            return
        explore_match_stats(client, args.match_id)
    elif args.endpoint == 'test-formats':
        test_parameter_formats(client)
    elif args.endpoint == 'test-alternatives':
        test_alternative_endpoints(client)

if __name__ == "__main__":
    main() 