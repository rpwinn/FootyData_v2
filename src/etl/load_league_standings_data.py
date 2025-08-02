#!/usr/bin/env python3
"""
Load League Standings Data
Parameterized script for collecting league standings data with optional filtering
Works with international competitions (World Cup, CONCACAF, OFC, AFC)
"""

import os
import sys
import psycopg2
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Add src to path
sys.path.append('src')

from api.fbr_client import FBRClient
from utils.endpoint_blacklist import load_endpoint_blacklist

def get_working_league_combinations() -> List[Dict[str, Any]]:
    """Get working league-season combinations for international competitions"""
    # Working international competitions
    working_combinations = [
        # World Cup (different years)
        {'league_id': 1, 'season_id': '2022', 'description': 'World Cup 2022'},
        {'league_id': 1, 'season_id': '2018', 'description': 'World Cup 2018'},
        {'league_id': 1, 'season_id': '2014', 'description': 'World Cup 2014'},
        
        # CONCACAF Nations League
        {'league_id': 3, 'season_id': None, 'description': 'CONCACAF Nations League'},
        
        # OFC Nations Cup
        {'league_id': 5, 'season_id': None, 'description': 'OFC Nations Cup'},
        
        # AFC Asian Cup Qualifiers
        {'league_id': 7, 'season_id': None, 'description': 'AFC Asian Cup Qualifiers'},
    ]
    
    return working_combinations

def insert_league_standings_data(data: Dict[str, Any], league_id: int, season_id: Optional[str]) -> bool:
    """Insert league standings data into staging table"""
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("❌ DATABASE_URL not found in .env file")
        return False
    
    try:
        with psycopg2.connect(database_url) as conn:
            with conn.cursor() as cur:
                # Extract data from API response
                standings_data = data.get('data', [])
                
                if not standings_data:
                    print(f"      ⚠️  No standings data found for league_id={league_id}, season_id={season_id}")
                    return True  # Not an error, just no data
                
                # Insert each group's standings
                for group_standing in standings_data:
                    standings_type = group_standing.get('standings_type')
                    team_standings = group_standing.get('standings', [])
                    
                    for team_standing in team_standings:
                        # Handle empty strings and convert to proper types
                        def safe_int(value):
                            if value == "" or value is None:
                                return None
                            try:
                                return int(value)
                            except (ValueError, TypeError):
                                return None
                        
                        insert_data = {
                            'league_id': league_id,
                            'season_id': season_id,
                            'standings_type': standings_type,
                            'position': safe_int(team_standing.get('rk')),  # API uses 'rk' for rank
                            'team_id': team_standing.get('team_id'),
                            'team_name': team_standing.get('team_name'),
                            'played': safe_int(team_standing.get('mp')),
                            'won': safe_int(team_standing.get('w')),
                            'drawn': safe_int(team_standing.get('d')),
                            'lost': safe_int(team_standing.get('l')),
                            'goals_for': safe_int(team_standing.get('gf')),
                            'goals_against': safe_int(team_standing.get('ga')),
                            'goal_difference': team_standing.get('gd'),  # Keep as string for +/- values
                            'points': safe_int(team_standing.get('pts')),
                            'top_team_scorer': json.dumps(team_standing.get('top_team_scorer')) if team_standing.get('top_team_scorer') else None,
                            'raw_data': json.dumps(team_standing)
                        }
                        
                        # Insert with ON CONFLICT handling
                        cur.execute("""
                            INSERT INTO staging.league_standings 
                            (league_id, season_id, standings_type, position, team_id, team_name,
                             played, won, drawn, lost, goals_for, goals_against, goal_difference,
                             points, top_team_scorer, raw_data)
                            VALUES (%(league_id)s, %(season_id)s, %(standings_type)s, %(position)s,
                                    %(team_id)s, %(team_name)s, %(played)s, %(won)s, %(drawn)s,
                                    %(lost)s, %(goals_for)s, %(goals_against)s, %(goal_difference)s,
                                    %(points)s, %(top_team_scorer)s, %(raw_data)s)
                            ON CONFLICT (league_id, season_id, team_id) 
                            DO UPDATE SET
                                standings_type = EXCLUDED.standings_type,
                                position = EXCLUDED.position,
                                team_name = EXCLUDED.team_name,
                                played = EXCLUDED.played,
                                won = EXCLUDED.won,
                                drawn = EXCLUDED.drawn,
                                lost = EXCLUDED.lost,
                                goals_for = EXCLUDED.goals_for,
                                goals_against = EXCLUDED.goals_against,
                                goal_difference = EXCLUDED.goal_difference,
                                points = EXCLUDED.points,
                                top_team_scorer = EXCLUDED.top_team_scorer,
                                raw_data = EXCLUDED.raw_data,
                                updated_at = CURRENT_TIMESTAMP
                        """, insert_data)
                
                conn.commit()
                return True
                
    except Exception as e:
        print(f"❌ Error inserting data: {e}")
        return False

def load_league_standings_data(league_ids: Optional[List[int]] = None,
                               season_ids: Optional[List[str]] = None,
                               update_only: bool = False,
                               verbose: bool = False) -> bool:
    """
    Load league standings data with optional filtering
    
    Args:
        league_ids: List of league IDs to collect (None for all working leagues)
        season_ids: List of season IDs to collect (None for all seasons)
        update_only: Only update existing records, don't add new ones
        verbose: Enable verbose logging
    
    Returns:
        bool: True if successful, False otherwise
    """
    print(f"🏆 Loading League Standings Data")
    print(f"   League IDs: {league_ids if league_ids else 'All Working International Leagues'}")
    print(f"   Season IDs: {season_ids if season_ids else 'All Seasons'}")
    print(f"   Update Only: {update_only}")
    
    # Initialize FBR client and blacklist
    client = FBRClient()
    blacklist = load_endpoint_blacklist()
    
    # Get combinations to process
    if league_ids or season_ids:
        # Filter working combinations based on parameters
        all_combinations = get_working_league_combinations()
        combinations_to_process = []
        
        for combo in all_combinations:
            if league_ids and combo['league_id'] not in league_ids:
                continue
            if season_ids and combo['season_id'] and combo['season_id'] not in season_ids:
                continue
            combinations_to_process.append(combo)
    else:
        # Use all working combinations
        combinations_to_process = get_working_league_combinations()
    
    if not combinations_to_process:
        print("❌ No league-season combinations found to process")
        return False
    
    print(f"📋 Found {len(combinations_to_process)} combinations to process")
    
    success_count = 0
    error_count = 0
    blacklisted_count = 0
    
    for i, combination in enumerate(combinations_to_process, 1):
        league_id = combination['league_id']
        season_id = combination['season_id']
        description = combination['description']
        
        if verbose:
            print(f"   [{i}/{len(combinations_to_process)}] Processing {description}")
        
        # Check if blacklisted
        if blacklist.is_blacklisted("league-standings", league_id=league_id):
            if verbose:
                print(f"      ⚠️  League {league_id} is blacklisted, skipping")
            blacklisted_count += 1
            continue
        
        try:
            # Make API call
            response = client.get_league_standings(league_id, season_id)
            
            if "error" in response:
                if verbose:
                    print(f"      ❌ API Error: {response['error']}")
                error_count += 1
                continue
            
            # Store data
            if insert_league_standings_data(response, league_id, season_id):
                success_count += 1
                if verbose:
                    print(f"      ✅ Stored successfully")
            else:
                error_count += 1
                if verbose:
                    print(f"      ❌ Failed to store data")
                
        except Exception as e:
            error_count += 1
            if verbose:
                print(f"      ❌ Error: {e}")
    
    # Print summary
    print(f"\n📊 Collection Summary:")
    print(f"   Successful: {success_count}")
    print(f"   Errors: {error_count}")
    print(f"   Blacklisted: {blacklisted_count}")
    print(f"   Total Processed: {len(combinations_to_process)}")
    
    if success_count > 0:
        print(f"✅ League standings collection completed successfully!")
        return True
    else:
        print(f"❌ No data was collected successfully")
        return False

def main():
    """Main CLI function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Load League Standings Data")
    parser.add_argument("--league-ids", help="Comma-separated list of league IDs")
    parser.add_argument("--season-ids", help="Comma-separated list of season IDs")
    parser.add_argument("--update-only", action="store_true", help="Only update existing records")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    # Parse arguments
    league_ids = None
    if args.league_ids:
        league_ids = [int(x.strip()) for x in args.league_ids.split(",")]
    
    season_ids = None
    if args.season_ids:
        season_ids = [x.strip() for x in args.season_ids.split(",")]
    
    # Run collection
    success = load_league_standings_data(
        league_ids=league_ids,
        season_ids=season_ids,
        update_only=args.update_only,
        verbose=args.verbose
    )
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main()) 