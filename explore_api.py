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

def explore_league_standings(client, league_id="9", season_id="2022-2023"):
    """Explore league standings endpoint"""
    print(f"\n=== LEAGUE STANDINGS ENDPOINT (League {league_id}, Season {season_id}) ===")
    standings = client.get_league_standings(league_id, season_id)
    if "error" not in standings and standings.get('data'):
        print(f"Found {len(standings['data'])} teams in standings")
        print("Sample standings data:")
        sample_standings = standings['data'][0]
        print(json.dumps(sample_standings, indent=2))
        return True
    else:
        print(f"Error: {standings.get('error', 'Unknown error')}")
        return False

def explore_teams(client, league_id="9", season_id="2022-2023"):
    """Explore teams endpoint"""
    print(f"\n=== TEAMS ENDPOINT (League {league_id}, Season {season_id}) ===")
    teams = client.get_teams(league_id, season_id)
    if "error" not in teams and teams.get('data'):
        print(f"Found {len(teams['data'])} teams")
        print("Sample team data:")
        sample_team = teams['data'][0]
        print(json.dumps(sample_team, indent=2))
        return True
    else:
        print(f"Error: {teams.get('error', 'Unknown error')}")
        return False

def explore_players(client, team_id, league_id="9", season_id="2022-2023"):
    """Explore players endpoint"""
    print(f"\n=== PLAYERS ENDPOINT (Team {team_id}, League {league_id}, Season {season_id}) ===")
    players = client.get_players(team_id, league_id, season_id)
    if "error" not in players and players.get('data'):
        print(f"Found {len(players['data'])} players")
        print("Sample player data:")
        sample_player = players['data'][0]
        print(json.dumps(sample_player, indent=2))
        return True
    else:
        print(f"Error: {players.get('error', 'Unknown error')}")
        return False

def explore_team_season_stats(client, team_id, league_id="9", season_id="2022-2023"):
    """Explore team season stats endpoint"""
    print(f"\n=== TEAM SEASON STATS ENDPOINT (Team {team_id}, League {league_id}, Season {season_id}) ===")
    team_stats = client.get_team_season_stats(team_id, league_id, season_id)
    if "error" not in team_stats and team_stats.get('data'):
        print("Found team season stats")
        print("Sample team stats data:")
        print(json.dumps(team_stats['data'][0], indent=2))
        return True
    else:
        print(f"Error: {team_stats.get('error', 'Unknown error')}")
        return False

def explore_player_season_stats(client, team_id, league_id="9", season_id="2022-2023"):
    """Explore player season stats endpoint"""
    print(f"\n=== PLAYER SEASON STATS ENDPOINT (Team {team_id}, League {league_id}, Season {season_id}) ===")
    player_stats = client.get_player_season_stats(team_id, league_id, season_id)
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
    
    # Note: These require a valid team_id, so we'll skip them for now
    print("\n=== SKIPPING TEAM-DEPENDENT ENDPOINTS ===")
    print("The following endpoints require a valid team_id from the teams endpoint:")
    print("- Players")
    print("- Team Season Stats") 
    print("- Player Season Stats")
    print("- Matches")
    print("Run with --endpoint teams first to get a team_id, then test others.")

def main():
    """Main function with command line arguments"""
    parser = argparse.ArgumentParser(description='Explore FBR API endpoints')
    parser.add_argument('--endpoint', choices=[
        'countries', 'leagues', 'league-seasons', 'league-standings', 
        'teams', 'players', 'team-stats', 'player-stats', 'matches', 'match-stats', 'all'
    ], default='all', help='Endpoint to explore')
    parser.add_argument('--country', default='ENG', help='Country code for leagues endpoint')
    parser.add_argument('--league-id', default='9', help='League ID for various endpoints')
    parser.add_argument('--season-id', default='2022-2023', help='Season ID for various endpoints')
    parser.add_argument('--team-id', help='Team ID for team-dependent endpoints')
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
        explore_league_standings(client, args.league_id, args.season_id)
    elif args.endpoint == 'teams':
        explore_teams(client, args.league_id, args.season_id)
    elif args.endpoint == 'players':
        if not args.team_id:
            print("Error: --team-id is required for players endpoint")
            return
        explore_players(client, args.team_id, args.league_id, args.season_id)
    elif args.endpoint == 'team-stats':
        if not args.team_id:
            print("Error: --team-id is required for team-stats endpoint")
            return
        explore_team_season_stats(client, args.team_id, args.league_id, args.season_id)
    elif args.endpoint == 'player-stats':
        if not args.team_id:
            print("Error: --team-id is required for player-stats endpoint")
            return
        explore_player_season_stats(client, args.team_id, args.league_id, args.season_id)
    elif args.endpoint == 'matches':
        explore_matches(client, args.league_id, args.season_id, args.team_id)
    elif args.endpoint == 'match-stats':
        if not args.match_id:
            print("Error: --match-id is required for match-stats endpoint")
            return
        explore_match_stats(client, args.match_id)

if __name__ == "__main__":
    main() 