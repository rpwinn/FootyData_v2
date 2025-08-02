#!/usr/bin/env python3
"""
Load Teams Data
Parameterized script for collecting teams data with optional filtering
Handles nested JSON structure: team_roster and team_schedule data
"""

import os
import sys
import psycopg2
import json
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from dotenv import load_dotenv

# Add src to path
sys.path.append('src')

from api.fbr_client import FBRClient
from utils.endpoint_blacklist import load_endpoint_blacklist

def get_team_ids_from_database(league_ids: Optional[List[int]] = None, 
                               season_ids: Optional[List[str]] = None) -> List[str]:
    """Get team IDs from the database based on filters"""
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        raise ValueError("DATABASE_URL not found in .env file")
    
    try:
        with psycopg2.connect(database_url) as conn:
            with conn.cursor() as cur:
                # Build query based on parameters
                query = "SELECT DISTINCT team_id FROM staging.team_schedules WHERE 1=1"
                params = []
                
                if league_ids:
                    placeholders = ','.join(['%s'] * len(league_ids))
                    query += f" AND league_id IN ({placeholders})"
                    params.extend(league_ids)
                
                query += " ORDER BY team_id"
                
                cur.execute(query, params)
                
                team_ids = [row[0] for row in cur.fetchall()]
                return team_ids
                
    except Exception as e:
        print(f"❌ Error getting team IDs from database: {e}")
        return []

def insert_team_rosters_data(data: Dict[str, Any], team_id: str) -> bool:
    """Insert team roster data into staging.team_rosters table"""
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("❌ DATABASE_URL not found in .env file")
        return False
    
    try:
        with psycopg2.connect(database_url) as conn:
            with conn.cursor() as cur:
                # Extract roster data from API response
                roster_data = data.get('team_roster', {}).get('data', [])
                
                if not roster_data:
                    print(f"      ⚠️  No roster data found for team {team_id}")
                    return True  # Not an error, just no data
                
                # Insert each player in the roster
                for player in roster_data:
                    insert_data = {
                        'team_id': team_id,
                        'player_id': player.get('player_id'),
                        'player_name': player.get('player'),
                        'nationality': player.get('nationality'),
                        'position': player.get('position'),
                        'age': player.get('age'),
                        'matches_played': player.get('mp'),
                        'starts': player.get('starts'),
                        'raw_data': json.dumps(player)
                    }
                    
                    # Insert with ON CONFLICT handling
                    cur.execute("""
                        INSERT INTO staging.team_rosters 
                        (team_id, player_id, player_name, nationality, position, age, 
                         matches_played, starts, raw_data)
                        VALUES (%(team_id)s, %(player_id)s, %(player_name)s, %(nationality)s, 
                                %(position)s, %(age)s, %(matches_played)s, %(starts)s, %(raw_data)s)
                        ON CONFLICT (team_id, player_id) 
                        DO UPDATE SET
                            player_name = EXCLUDED.player_name,
                            nationality = EXCLUDED.nationality,
                            position = EXCLUDED.position,
                            age = EXCLUDED.age,
                            matches_played = EXCLUDED.matches_played,
                            starts = EXCLUDED.starts,
                            raw_data = EXCLUDED.raw_data,
                            updated_at = CURRENT_TIMESTAMP
                    """, insert_data)
                
                conn.commit()
                return True
                
    except Exception as e:
        print(f"❌ Error inserting roster data: {e}")
        return False

def insert_team_schedules_data(data: Dict[str, Any], team_id: str) -> bool:
    """Insert team schedule data into staging.team_schedules table"""
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("❌ DATABASE_URL not found in .env file")
        return False
    
    try:
        with psycopg2.connect(database_url) as conn:
            with conn.cursor() as cur:
                # Extract schedule data from API response
                schedule_data = data.get('team_schedule', {}).get('data', [])
                
                if not schedule_data:
                    print(f"      ⚠️  No schedule data found for team {team_id}")
                    return True  # Not an error, just no data
                
                # Insert each match in the schedule
                for match in schedule_data:
                    # Handle date conversion
                    match_date = None
                    if match.get('date'):
                        try:
                            match_date = datetime.strptime(match['date'], '%Y-%m-%d').date()
                        except ValueError:
                            match_date = None
                    
                    # Handle time conversion
                    match_time = None
                    if match.get('time'):
                        try:
                            match_time = datetime.strptime(match['time'], '%H:%M').time()
                        except ValueError:
                            match_time = None
                    
                    insert_data = {
                        'team_id': team_id,
                        'match_id': match.get('match_id'),
                        'match_date': match_date,
                        'match_time': match_time,
                        'league_name': match.get('league_name'),
                        'league_id': match.get('league_id'),
                        'opponent': match.get('opponent'),
                        'opponent_id': match.get('opponent_id'),
                        'home_away': match.get('home_away'),
                        'result': match.get('result'),
                        'goals_for': match.get('gf'),
                        'goals_against': match.get('ga'),
                        'attendance': match.get('attendance'),
                        'captain': match.get('captain'),
                        'formation': match.get('formation'),
                        'referee': match.get('referee'),
                        'raw_data': json.dumps(match)
                    }
                    
                    # Insert with ON CONFLICT handling
                    cur.execute("""
                        INSERT INTO staging.team_schedules 
                        (team_id, match_id, match_date, match_time, league_name, league_id,
                         opponent, opponent_id, home_away, result, goals_for, goals_against,
                         attendance, captain, formation, referee, raw_data)
                        VALUES (%(team_id)s, %(match_id)s, %(match_date)s, %(match_time)s,
                                %(league_name)s, %(league_id)s, %(opponent)s, %(opponent_id)s,
                                %(home_away)s, %(result)s, %(goals_for)s, %(goals_against)s,
                                %(attendance)s, %(captain)s, %(formation)s, %(referee)s, %(raw_data)s)
                        ON CONFLICT (team_id, match_id) 
                        DO UPDATE SET
                            match_date = EXCLUDED.match_date,
                            match_time = EXCLUDED.match_time,
                            league_name = EXCLUDED.league_name,
                            league_id = EXCLUDED.league_id,
                            opponent = EXCLUDED.opponent,
                            opponent_id = EXCLUDED.opponent_id,
                            home_away = EXCLUDED.home_away,
                            result = EXCLUDED.result,
                            goals_for = EXCLUDED.goals_for,
                            goals_against = EXCLUDED.goals_against,
                            attendance = EXCLUDED.attendance,
                            captain = EXCLUDED.captain,
                            formation = EXCLUDED.formation,
                            referee = EXCLUDED.referee,
                            raw_data = EXCLUDED.raw_data,
                            updated_at = CURRENT_TIMESTAMP
                    """, insert_data)
                
                conn.commit()
                return True
                
    except Exception as e:
        print(f"❌ Error inserting schedule data: {e}")
        return False

def load_teams_data(team_ids: Optional[List[str]] = None,
                    season_ids: Optional[List[str]] = None,
                    update_only: bool = False,
                    verbose: bool = False) -> bool:
    """
    Load teams data with optional filtering
    
    Args:
        team_ids: List of team IDs to collect (None for all)
        season_ids: List of season IDs to collect (None for all)
        update_only: Only update existing records, don't add new ones
        verbose: Enable verbose logging
    
    Returns:
        bool: True if successful, False otherwise
    """
    print(f"🏈 Loading Teams Data")
    print(f"   Team IDs: {team_ids if team_ids else 'All'}")
    print(f"   Season IDs: {season_ids if season_ids else 'All'}")
    print(f"   Update Only: {update_only}")
    
    # Initialize FBR client and blacklist
    client = FBRClient()
    blacklist = load_endpoint_blacklist()
    
    # Get team IDs to process
    if team_ids:
        teams_to_process = team_ids
    else:
        # Get team IDs from database
        teams_to_process = get_team_ids_from_database(season_ids=season_ids)
    
    if not teams_to_process:
        print("❌ No team IDs found to process")
        return False
    
    print(f"📋 Found {len(teams_to_process)} teams to process")
    
    success_count = 0
    error_count = 0
    blacklisted_count = 0
    
    for i, team_id in enumerate(teams_to_process, 1):
        if verbose:
            print(f"   [{i}/{len(teams_to_process)}] Processing Team {team_id}")
        
        # Check if blacklisted
        if blacklist.is_blacklisted("teams", team_id=team_id):
            if verbose:
                print(f"      ⚠️  Team {team_id} is blacklisted, skipping")
            blacklisted_count += 1
            continue
        
        try:
            # Make API call (no season_id for teams endpoint)
            response = client.get_teams(team_id)
            
            if "error" in response:
                if verbose:
                    print(f"      ❌ API Error: {response['error']}")
                error_count += 1
                continue
            
            # Store roster data
            roster_success = insert_team_rosters_data(response, team_id)
            
            # Store schedule data
            schedule_success = insert_team_schedules_data(response, team_id)
            
            if roster_success and schedule_success:
                success_count += 1
                if verbose:
                    print(f"      ✅ Stored roster and schedule data successfully")
            else:
                error_count += 1
                if verbose:
                    print(f"      ❌ Failed to store some data")
                
        except Exception as e:
            error_count += 1
            if verbose:
                print(f"      ❌ Error: {e}")
    
    # Print summary
    print(f"\n📊 Collection Summary:")
    print(f"   Successful: {success_count}")
    print(f"   Errors: {error_count}")
    print(f"   Blacklisted: {blacklisted_count}")
    print(f"   Total Processed: {len(teams_to_process)}")
    
    if success_count > 0:
        print(f"✅ Teams collection completed successfully!")
        return True
    else:
        print(f"❌ No data was collected successfully")
        return False

def main():
    """Main CLI function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Load Teams Data")
    parser.add_argument("--team-ids", help="Comma-separated list of team IDs")
    parser.add_argument("--season-ids", help="Comma-separated list of season IDs")
    parser.add_argument("--update-only", action="store_true", help="Only update existing records")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    # Parse arguments
    team_ids = None
    if args.team_ids:
        team_ids = [x.strip() for x in args.team_ids.split(",")]
    
    season_ids = None
    if args.season_ids:
        season_ids = [x.strip() for x in args.season_ids.split(",")]
    
    # Run collection
    success = load_teams_data(
        team_ids=team_ids,
        season_ids=season_ids,
        update_only=args.update_only,
        verbose=args.verbose
    )
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main()) 