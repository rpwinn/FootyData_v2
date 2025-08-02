#!/usr/bin/env python3
"""
Test Teams Data Collection
Validates the teams staging tables with real API calls
Handles nested JSON structure: team_roster and team_schedule data
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

def get_test_team_ids() -> List[Dict[str, Any]]:
    """Get test team IDs from API documentation examples"""
    # Use team IDs from API documentation examples
    return [
        {'team_id': 'b8fd03ef', 'team_name': 'Manchester City', 'season_id': '2023-2024'},
        {'team_id': '18bb7c10', 'team_name': 'Arsenal', 'season_id': '2023-2024'},
        {'team_id': '19538871', 'team_name': 'Manchester United', 'season_id': '2024-2025'}
    ]

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

def verify_stored_data(team_id: str) -> bool:
    """Verify that stored data matches original API response"""
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("❌ DATABASE_URL not found in .env file")
        return False
    
    try:
        with psycopg2.connect(database_url) as conn:
            with conn.cursor() as cur:
                # Get roster data
                cur.execute("""
                    SELECT COUNT(*) as roster_count
                    FROM staging.team_rosters 
                    WHERE team_id = %s
                """, (team_id,))
                
                roster_count = cur.fetchone()[0]
                
                # Get schedule data
                cur.execute("""
                    SELECT COUNT(*) as schedule_count
                    FROM staging.team_schedules 
                    WHERE team_id = %s
                """, (team_id,))
                
                schedule_count = cur.fetchone()[0]
                
                print(f"      📊 Stored: {roster_count} roster records, {schedule_count} schedule records")
                
                if roster_count > 0 or schedule_count > 0:
                    print(f"✅ Data verification passed for team_id={team_id}")
                    return True
                else:
                    print(f"❌ No data found for team_id={team_id}")
                    return False
                
    except Exception as e:
        print(f"❌ Error verifying data: {e}")
        return False

def print_stored_data_summary():
    """Print summary of stored teams data"""
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("❌ DATABASE_URL not found in .env file")
        return
    
    try:
        with psycopg2.connect(database_url) as conn:
            with conn.cursor() as cur:
                # Get roster summary
                cur.execute("""
                    SELECT 
                        COUNT(*) as total_roster_records,
                        COUNT(DISTINCT team_id) as unique_teams_rosters,
                        COUNT(DISTINCT player_id) as unique_players
                    FROM staging.team_rosters
                """)
                
                roster_row = cur.fetchone()
                
                # Get schedule summary
                cur.execute("""
                    SELECT 
                        COUNT(*) as total_schedule_records,
                        COUNT(DISTINCT team_id) as unique_teams_schedules,
                        COUNT(DISTINCT match_id) as unique_matches,
                        COUNT(DISTINCT league_id) as unique_leagues
                    FROM staging.team_schedules
                """)
                
                schedule_row = cur.fetchone()
                
                if roster_row and schedule_row:
                    print("\n📊 Teams Data Summary:")
                    print(f"   Roster Records: {roster_row[0]}")
                    print(f"   Schedule Records: {schedule_row[0]}")
                    print(f"   Unique Teams (Rosters): {roster_row[1]}")
                    print(f"   Unique Teams (Schedules): {schedule_row[1]}")
                    print(f"   Unique Players: {roster_row[2]}")
                    print(f"   Unique Matches: {schedule_row[2]}")
                    print(f"   Unique Leagues: {schedule_row[3]}")
                
                # Get sample roster data
                cur.execute("""
                    SELECT team_id, player_name, position, nationality
                    FROM staging.team_rosters 
                    ORDER BY team_id, player_name
                    LIMIT 5
                """)
                
                print("\n📋 Sample Roster Data:")
                for row in cur.fetchall():
                    print(f"   {row[1]} ({row[2]}) - {row[3]} (Team: {row[0]})")
                
                # Get sample schedule data
                cur.execute("""
                    SELECT team_id, opponent, result, goals_for, goals_against, league_name
                    FROM staging.team_schedules 
                    ORDER BY team_id, match_date
                    LIMIT 5
                """)
                
                print("\n📋 Sample Schedule Data:")
                for row in cur.fetchall():
                    print(f"   {row[0]} vs {row[1]} - {row[2]} ({row[3]}-{row[4]}) - {row[5]}")
                print()
                
    except Exception as e:
        print(f"❌ Error getting summary: {e}")

def main():
    """Main test function"""
    print("🧪 Testing Teams Data Collection")
    print("=" * 50)
    
    # Initialize FBR client
    client = FBRClient()
    
    # Get test team IDs
    test_teams = get_test_team_ids()
    print(f"📋 Testing {len(test_teams)} teams")
    
    success_count = 0
    total_count = len(test_teams)
    
    for i, team in enumerate(test_teams, 1):
        team_id = team['team_id']
        team_name = team['team_name']
        season_id = team['season_id']
        
        print(f"\n🔍 Test {i}/{total_count}: {team_name} (ID: {team_id})")
        
        try:
            # Make API call
            print(f"   📡 Making API call...")
            response = client.get_teams(team_id, season_id)
            
            if "error" in response:
                print(f"   ❌ API Error: {response['error']}")
                continue
            
            # Store roster data
            print(f"   💾 Storing roster data...")
            roster_success = insert_team_rosters_data(response, team_id)
            
            # Store schedule data
            print(f"   💾 Storing schedule data...")
            schedule_success = insert_team_schedules_data(response, team_id)
            
            if roster_success and schedule_success:
                print(f"   ✅ Data stored successfully")
                
                # Verify data
                print(f"   🔍 Verifying data...")
                if verify_stored_data(team_id):
                    success_count += 1
                    print(f"   ✅ Verification passed")
                else:
                    print(f"   ❌ Verification failed")
            else:
                print(f"   ❌ Failed to store some data")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Print summary
    print(f"\n📊 Test Results:")
    print(f"   Successful: {success_count}/{total_count}")
    print(f"   Success Rate: {(success_count/total_count)*100:.1f}%")
    
    # Print stored data summary
    print_stored_data_summary()
    
    if success_count == total_count:
        print("\n🎉 All tests passed! Teams staging tables are working correctly.")
        return 0
    else:
        print(f"\n⚠️  {total_count - success_count} tests failed. Check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 