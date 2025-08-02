#!/usr/bin/env python3
"""
Test script for matches staging tables
Tests both league matches (no team_id) and team matches (with team_id) formats
"""

import os
import json
import psycopg2
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from dotenv import load_dotenv

# Import FBR client
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from api.fbr_client import FBRClient

def get_test_league_season_combinations() -> List[Tuple[int, str]]:
    """Get test league-season combinations from database or use fallbacks"""
    try:
        load_dotenv()
        conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        cur = conn.cursor()
        
        # Query existing league seasons
        cur.execute("""
            SELECT league_id, season_id 
            FROM staging.league_seasons 
            ORDER BY league_id, season_id 
            LIMIT 3
        """)
        
        combinations = cur.fetchall()
        cur.close()
        conn.close()
        
        if combinations:
            print(f"✅ Found {len(combinations)} league-season combinations from database")
            return combinations
        else:
            print("⚠️ No league seasons found in database, using fallback combinations")
            return [(9, "2023-2024"), (8, "2023-2024"), (1, "2022")]
            
    except Exception as e:
        print(f"⚠️ Error querying database: {e}, using fallback combinations")
        return [(9, "2023-2024"), (8, "2023-2024"), (1, "2022")]

def get_test_team_ids() -> List[str]:
    """Get test team IDs from database or use fallbacks"""
    try:
        load_dotenv()
        conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        cur = conn.cursor()
        
        # Query existing team IDs from league standings, prefer well-known teams
        cur.execute("""
            SELECT DISTINCT team_id, team_name 
            FROM staging.league_standings 
            WHERE team_id IS NOT NULL 
            AND team_name IN ('England', 'United States', 'France', 'Brazil', 'Argentina')
            LIMIT 5
        """)
        
        results = cur.fetchall()
        if results:
            team_ids = [row[0] for row in results]
            print(f"✅ Found {len(team_ids)} well-known team IDs from database")
            return team_ids
        else:
            # Fallback to any team IDs
            cur.execute("""
                SELECT DISTINCT team_id 
                FROM staging.league_standings 
                WHERE team_id IS NOT NULL 
                LIMIT 3
            """)
            team_ids = [row[0] for row in cur.fetchall()]
            cur.close()
            conn.close()
            
            if team_ids:
                print(f"✅ Found {len(team_ids)} team IDs from database")
                return team_ids
            else:
                print("⚠️ No team IDs found in database, using fallback team IDs")
                return ["1862c019", "0f66725b", "b1b36dcd"]  # England, USA, France
                
    except Exception as e:
        print(f"⚠️ Error querying database: {e}, using fallback team IDs")
        return ["1862c019", "0f66725b", "b1b36dcd"]  # England, USA, France

def insert_league_matches_data(data: Dict[str, Any], league_id: int, season_id: str) -> bool:
    """Insert league matches data into staging table"""
    try:
        load_dotenv()
        conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        cur = conn.cursor()
        
        matches_data = data.get('data', [])
        inserted_count = 0
        
        for match in matches_data:
            # Handle empty strings and convert to proper types
            def safe_int(value):
                if value == "" or value is None:
                    return None
                try:
                    return int(value)
                except (ValueError, TypeError):
                    return None
            
            # Convert date string to date object
            match_date = None
            if match.get('date'):
                try:
                    match_date = datetime.strptime(match['date'], '%Y-%m-%d').date()
                except ValueError:
                    match_date = None
            
            # Convert time string to time object
            match_time = None
            if match.get('time'):
                try:
                    match_time = datetime.strptime(match['time'], '%H:%M').time()
                except ValueError:
                    match_time = None
            
            insert_data = {
                'match_id': match.get('match_id'),
                'league_id': league_id,
                'season_id': season_id,
                'match_date': match_date,
                'match_time': match_time,
                'round': match.get('round'),
                'wk': match.get('wk'),
                'home_team': match.get('home'),
                'home_team_id': match.get('home_team_id'),
                'away_team': match.get('away'),
                'away_team_id': match.get('away_team_id'),
                'home_team_score': safe_int(match.get('home_team_score')),
                'away_team_score': safe_int(match.get('away_team_score')),
                'venue': match.get('venue'),
                'attendance': match.get('attendance'),
                'referee': match.get('referee'),
                'raw_data': json.dumps(match)
            }
            
            # Insert with upsert
            cur.execute("""
                INSERT INTO staging.league_matches (
                    match_id, league_id, season_id, match_date, match_time, round, wk,
                    home_team, home_team_id, away_team, away_team_id,
                    home_team_score, away_team_score, venue, attendance, referee, raw_data
                ) VALUES (
                    %(match_id)s, %(league_id)s, %(season_id)s, %(match_date)s, %(match_time)s, 
                    %(round)s, %(wk)s, %(home_team)s, %(home_team_id)s, %(away_team)s, %(away_team_id)s,
                    %(home_team_score)s, %(away_team_score)s, %(venue)s, %(attendance)s, %(referee)s, %(raw_data)s
                ) ON CONFLICT (league_id, season_id, match_id) 
                DO UPDATE SET
                    match_date = EXCLUDED.match_date,
                    match_time = EXCLUDED.match_time,
                    round = EXCLUDED.round,
                    wk = EXCLUDED.wk,
                    home_team = EXCLUDED.home_team,
                    home_team_id = EXCLUDED.home_team_id,
                    away_team = EXCLUDED.away_team,
                    away_team_id = EXCLUDED.away_team_id,
                    home_team_score = EXCLUDED.home_team_score,
                    away_team_score = EXCLUDED.away_team_score,
                    venue = EXCLUDED.venue,
                    attendance = EXCLUDED.attendance,
                    referee = EXCLUDED.referee,
                    raw_data = EXCLUDED.raw_data,
                    updated_at = CURRENT_TIMESTAMP
            """, insert_data)
            
            inserted_count += 1
        
        conn.commit()
        cur.close()
        conn.close()
        
        print(f"✅ Inserted {inserted_count} league matches for league {league_id}, season {season_id}")
        return True
        
    except Exception as e:
        print(f"❌ Error inserting league matches data: {e}")
        return False

def insert_team_matches_data(data: Dict[str, Any], league_id: int, season_id: str, team_id: str) -> bool:
    """Insert team matches data into staging table"""
    try:
        load_dotenv()
        conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        cur = conn.cursor()
        
        matches_data = data.get('data', [])
        inserted_count = 0
        
        for match in matches_data:
            # Handle empty strings and convert to proper types
            def safe_int(value):
                if value == "" or value is None:
                    return None
                try:
                    return int(value)
                except (ValueError, TypeError):
                    return None
            
            # Convert date string to date object
            match_date = None
            if match.get('date'):
                try:
                    match_date = datetime.strptime(match['date'], '%Y-%m-%d').date()
                except ValueError:
                    match_date = None
            
            # Convert time string to time object
            match_time = None
            if match.get('time'):
                try:
                    match_time = datetime.strptime(match['time'], '%H:%M').time()
                except ValueError:
                    match_time = None
            
            insert_data = {
                'match_id': match.get('match_id'),
                'league_id': league_id,
                'season_id': season_id,
                'team_id': team_id,
                'match_date': match_date,
                'match_time': match_time,
                'round': match.get('round'),
                'home_away': match.get('home_away'),
                'opponent': match.get('opponent'),
                'opponent_id': match.get('opponent_id'),
                'result': match.get('result'),
                'goals_for': safe_int(match.get('gf')),
                'goals_against': safe_int(match.get('ga')),
                'formation': match.get('formation'),
                'captain': match.get('captain'),
                'attendance': match.get('attendance'),
                'referee': match.get('referee'),
                'raw_data': json.dumps(match)
            }
            
            # Insert with upsert
            cur.execute("""
                INSERT INTO staging.team_matches (
                    match_id, league_id, season_id, team_id, match_date, match_time, round,
                    home_away, opponent, opponent_id, result, goals_for, goals_against,
                    formation, captain, attendance, referee, raw_data
                ) VALUES (
                    %(match_id)s, %(league_id)s, %(season_id)s, %(team_id)s, %(match_date)s, %(match_time)s, 
                    %(round)s, %(home_away)s, %(opponent)s, %(opponent_id)s, %(result)s, %(goals_for)s, %(goals_against)s,
                    %(formation)s, %(captain)s, %(attendance)s, %(referee)s, %(raw_data)s
                ) ON CONFLICT (league_id, season_id, match_id, team_id) 
                DO UPDATE SET
                    match_date = EXCLUDED.match_date,
                    match_time = EXCLUDED.match_time,
                    round = EXCLUDED.round,
                    home_away = EXCLUDED.home_away,
                    opponent = EXCLUDED.opponent,
                    opponent_id = EXCLUDED.opponent_id,
                    result = EXCLUDED.result,
                    goals_for = EXCLUDED.goals_for,
                    goals_against = EXCLUDED.goals_against,
                    formation = EXCLUDED.formation,
                    captain = EXCLUDED.captain,
                    attendance = EXCLUDED.attendance,
                    referee = EXCLUDED.referee,
                    raw_data = EXCLUDED.raw_data,
                    updated_at = CURRENT_TIMESTAMP
            """, insert_data)
            
            inserted_count += 1
        
        conn.commit()
        cur.close()
        conn.close()
        
        print(f"✅ Inserted {inserted_count} team matches for team {team_id}, league {league_id}, season {season_id}")
        return True
        
    except Exception as e:
        print(f"❌ Error inserting team matches data: {e}")
        return False

def verify_stored_data() -> bool:
    """Verify that stored data matches original API responses"""
    try:
        load_dotenv()
        conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        cur = conn.cursor()
        
        # Check league matches count
        cur.execute("SELECT COUNT(*) FROM staging.league_matches")
        league_matches_count = cur.fetchone()[0]
        
        # Check team matches count
        cur.execute("SELECT COUNT(*) FROM staging.team_matches")
        team_matches_count = cur.fetchone()[0]
        
        # Get sample data for verification
        cur.execute("""
            SELECT match_id, league_id, season_id, home_team, away_team, home_team_score, away_team_score
            FROM staging.league_matches 
            LIMIT 3
        """)
        league_samples = cur.fetchall()
        
        cur.execute("""
            SELECT match_id, league_id, season_id, team_id, opponent, result, goals_for, goals_against
            FROM staging.team_matches 
            LIMIT 3
        """)
        team_samples = cur.fetchall()
        
        cur.close()
        conn.close()
        
        print(f"✅ Verification complete:")
        print(f"   - League matches stored: {league_matches_count}")
        print(f"   - Team matches stored: {team_matches_count}")
        
        if league_samples:
            print(f"   - Sample league match: {league_samples[0]}")
        if team_samples:
            print(f"   - Sample team match: {team_samples[0]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error verifying stored data: {e}")
        return False

def print_stored_data_summary():
    """Print summary of stored data"""
    try:
        load_dotenv()
        conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        cur = conn.cursor()
        
        # League matches summary
        cur.execute("""
            SELECT league_id, season_id, COUNT(*) as match_count
            FROM staging.league_matches 
            GROUP BY league_id, season_id 
            ORDER BY league_id, season_id
        """)
        league_summary = cur.fetchall()
        
        # Team matches summary
        cur.execute("""
            SELECT league_id, season_id, team_id, COUNT(*) as match_count
            FROM staging.team_matches 
            GROUP BY league_id, season_id, team_id 
            ORDER BY league_id, season_id, team_id
        """)
        team_summary = cur.fetchall()
        
        cur.close()
        conn.close()
        
        print("\n📊 Stored Data Summary:")
        print("League Matches:")
        for row in league_summary:
            print(f"   League {row[0]} Season {row[1]}: {row[2]} matches")
        
        print("Team Matches:")
        for row in team_summary:
            print(f"   League {row[0]} Season {row[1]} Team {row[2]}: {row[3]} matches")
        
    except Exception as e:
        print(f"❌ Error printing data summary: {e}")

def main():
    """Main test function"""
    print("🧪 Testing Matches Staging Tables")
    print("=" * 50)
    
    # Initialize FBR client
    client = FBRClient()
    
    # Get test combinations
    league_combinations = get_test_league_season_combinations()
    team_ids = get_test_team_ids()
    
    print(f"\n📋 Test Combinations:")
    print(f"   League combinations: {league_combinations}")
    print(f"   Team IDs: {team_ids}")
    
    # Test league matches (no team_id)
    print(f"\n🏆 Testing League Matches (no team_id):")
    for league_id, season_id in league_combinations[:2]:  # Test first 2 combinations
        print(f"\n   Testing league {league_id}, season {season_id}...")
        
        try:
            # Make API call
            response = client.get_matches(str(league_id), season_id)
            
            if 'error' in response:
                print(f"   ❌ API Error: {response['error']}")
                continue
            
            # Insert data
            if insert_league_matches_data(response, league_id, season_id):
                print(f"   ✅ Successfully processed league matches")
            else:
                print(f"   ❌ Failed to insert league matches data")
                
        except Exception as e:
            print(f"   ❌ Error testing league matches: {e}")
    
    # Test team matches (with team_id)
    print(f"\n👥 Testing Team Matches (with team_id):")
    for team_id in team_ids[:2]:  # Test first 2 team IDs
        print(f"\n   Testing team {team_id}...")
        
        try:
            # Use international league for team tests (World Cup 2022)
            league_id, season_id = 1, "2022"
            
            # Make API call
            response = client.get_matches(str(league_id), season_id, team_id)
            
            if 'error' in response:
                print(f"   ❌ API Error: {response['error']}")
                continue
            
            # Insert data
            if insert_team_matches_data(response, league_id, season_id, team_id):
                print(f"   ✅ Successfully processed team matches")
            else:
                print(f"   ❌ Failed to insert team matches data")
                
        except Exception as e:
            print(f"   ❌ Error testing team matches: {e}")
    
    # Verify stored data
    print(f"\n🔍 Verifying Stored Data:")
    if verify_stored_data():
        print("   ✅ Data verification successful")
    else:
        print("   ❌ Data verification failed")
    
    # Print summary
    print_stored_data_summary()
    
    print(f"\n✅ Matches staging table test completed!")

if __name__ == "__main__":
    main() 