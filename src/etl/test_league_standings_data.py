#!/usr/bin/env python3
"""
Test League Standings Data Collection
Validates the league standings staging table with real API calls
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

def get_test_league_season_combinations() -> List[Dict[str, Any]]:
    """Get test league_id + season_id combinations from database"""
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("❌ DATABASE_URL not found in .env file")
        return []
    
    try:
        with psycopg2.connect(database_url) as conn:
            with conn.cursor() as cur:
                # Get some league-season combinations from the database
                cur.execute("""
                    SELECT league_id, season_id 
                    FROM staging.league_seasons 
                    WHERE league_id IN (9, 8, 12)  -- Premier League, Champions League, La Liga
                    ORDER BY league_id, season_id
                    LIMIT 3
                """)
                
                combinations = []
                for row in cur.fetchall():
                    combinations.append({
                        'league_id': row[0],
                        'season_id': row[1]
                    })
                
                return combinations
                
    except Exception as e:
        print(f"❌ Error getting league-season combinations: {e}")
        # Fallback to hardcoded combinations
        return [
            {'league_id': 9, 'season_id': '2023-2024'},  # Premier League
            {'league_id': 8, 'season_id': '2023-2024'},  # Champions League
            {'league_id': 12, 'season_id': '2023-2024'}  # La Liga
        ]

def insert_league_standings_data(data: Dict[str, Any], league_id: int, season_id: str) -> bool:
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
                standings_type = data.get('standings_type')
                standings_data = data.get('data', [])
                
                if not standings_data:
                    print(f"      ⚠️  No standings data found for league_id={league_id}, season_id={season_id}")
                    return True  # Not an error, just no data
                
                # Insert each team's standings
                for team_standing in standings_data:
                    insert_data = {
                        'league_id': league_id,
                        'season_id': season_id,
                        'standings_type': standings_type,
                        'position': team_standing.get('position'),
                        'team_id': team_standing.get('team_id'),
                        'team_name': team_standing.get('team'),
                        'played': team_standing.get('played'),
                        'won': team_standing.get('won'),
                        'drawn': team_standing.get('drawn'),
                        'lost': team_standing.get('lost'),
                        'goals_for': team_standing.get('goals_for'),
                        'goals_against': team_standing.get('goals_against'),
                        'goal_difference': team_standing.get('goal_difference'),
                        'points': team_standing.get('points'),
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

def verify_stored_data(league_id: int, season_id: str) -> bool:
    """Verify that stored data matches original API response"""
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("❌ DATABASE_URL not found in .env file")
        return False
    
    try:
        with psycopg2.connect(database_url) as conn:
            with conn.cursor() as cur:
                # Get stored data count
                cur.execute("""
                    SELECT COUNT(*) as standings_count
                    FROM staging.league_standings 
                    WHERE league_id = %s AND season_id = %s
                """, (league_id, season_id))
                
                standings_count = cur.fetchone()[0]
                
                print(f"      📊 Stored: {standings_count} standings records")
                
                if standings_count > 0:
                    print(f"✅ Data verification passed for league_id={league_id}, season_id={season_id}")
                    return True
                else:
                    print(f"❌ No data found for league_id={league_id}, season_id={season_id}")
                    return False
                
    except Exception as e:
        print(f"❌ Error verifying data: {e}")
        return False

def print_stored_data_summary():
    """Print summary of stored league standings data"""
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("❌ DATABASE_URL not found in .env file")
        return
    
    try:
        with psycopg2.connect(database_url) as conn:
            with conn.cursor() as cur:
                # Get summary statistics
                cur.execute("""
                    SELECT 
                        COUNT(*) as total_records,
                        COUNT(DISTINCT league_id) as unique_leagues,
                        COUNT(DISTINCT season_id) as unique_seasons,
                        COUNT(DISTINCT team_id) as unique_teams
                    FROM staging.league_standings
                """)
                
                row = cur.fetchone()
                if row:
                    print("\n📊 League Standings Data Summary:")
                    print(f"   Total Records: {row[0]}")
                    print(f"   Unique Leagues: {row[1]}")
                    print(f"   Unique Seasons: {row[2]}")
                    print(f"   Unique Teams: {row[3]}")
                
                # Get sample data
                cur.execute("""
                    SELECT league_id, season_id, team_name, position, points
                    FROM staging.league_standings 
                    ORDER BY league_id, season_id, position
                    LIMIT 10
                """)
                
                print("\n📋 Sample Data:")
                for row in cur.fetchall():
                    print(f"   League {row[0]} Season {row[1]}: {row[2]} - Position {row[3]} ({row[4]} pts)")
                print()
                
    except Exception as e:
        print(f"❌ Error getting summary: {e}")

def main():
    """Main test function"""
    print("🧪 Testing League Standings Data Collection")
    print("=" * 50)
    
    # Initialize FBR client
    client = FBRClient()
    
    # Get test league-season combinations
    test_combinations = get_test_league_season_combinations()
    print(f"📋 Testing {len(test_combinations)} league-season combinations")
    
    success_count = 0
    total_count = len(test_combinations)
    
    for i, combination in enumerate(test_combinations, 1):
        league_id = combination['league_id']
        season_id = combination['season_id']
        
        print(f"\n🔍 Test {i}/{total_count}: League {league_id} Season {season_id}")
        
        try:
            # Make API call
            print(f"   📡 Making API call...")
            response = client.get_league_standings(league_id, season_id)
            
            if "error" in response:
                print(f"   ❌ API Error: {response['error']}")
                continue
            
            # Store data
            print(f"   💾 Storing data...")
            if insert_league_standings_data(response, league_id, season_id):
                print(f"   ✅ Data stored successfully")
                
                # Verify data
                print(f"   🔍 Verifying data...")
                if verify_stored_data(league_id, season_id):
                    success_count += 1
                    print(f"   ✅ Verification passed")
                else:
                    print(f"   ❌ Verification failed")
            else:
                print(f"   ❌ Failed to store data")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Print summary
    print(f"\n📊 Test Results:")
    print(f"   Successful: {success_count}/{total_count}")
    print(f"   Success Rate: {(success_count/total_count)*100:.1f}%")
    
    # Print stored data summary
    print_stored_data_summary()
    
    if success_count == total_count:
        print("\n🎉 All tests passed! League standings staging table is working correctly.")
        return 0
    else:
        print(f"\n⚠️  {total_count - success_count} tests failed. Check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 