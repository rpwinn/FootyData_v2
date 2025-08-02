#!/usr/bin/env python3
"""
Test League Season Details Data Collection
Validates the league season details staging table with real API calls
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
    """Get test league-season combinations from the database"""
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        raise ValueError("DATABASE_URL not found in .env file")
    
    try:
        with psycopg2.connect(database_url) as conn:
            with conn.cursor() as cur:
                # Get 3 league-season combinations for testing
                cur.execute("""
                    SELECT league_id, season_id 
                    FROM staging.league_seasons 
                    WHERE league_id IN (8, 13)  -- Champions League, Serie A
                    AND season_id IN ('2023-2024', '2024-2025')
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
        print(f"❌ Error getting test combinations: {e}")
        # Fallback to known working combinations
        return [
            {'league_id': 8, 'season_id': '2023-2024'},  # Champions League
            {'league_id': 13, 'season_id': '2023-2024'},  # Serie A
            {'league_id': 8, 'season_id': '2024-2025'}   # Champions League
        ]

def insert_league_season_details_data(data: Dict[str, Any]) -> bool:
    """Insert league season details data into staging table"""
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("❌ DATABASE_URL not found in .env file")
        return False
    
    try:
        with psycopg2.connect(database_url) as conn:
            with conn.cursor() as cur:
                # Extract data from API response
                api_data = data.get('data', {})
                
                # Prepare data for insertion
                # Handle invalid date values
                league_start = api_data.get('league_start')
                league_end = api_data.get('league_end')
                
                # Convert invalid date strings to None
                if league_start == 'Date' or league_start == '':
                    league_start = None
                if league_end == 'Date' or league_end == '':
                    league_end = None
                
                insert_data = {
                    'league_id': api_data.get('lg_id'),  # API returns lg_id, we store as league_id
                    'season_id': api_data.get('season_id'),
                    'league_start': league_start,
                    'league_end': league_end,
                    'league_type': api_data.get('league_type'),
                    'has_adv_stats': api_data.get('has_adv_stats'),
                    'rounds': json.dumps(api_data.get('rounds', [])),
                    'raw_data': json.dumps(data)
                }
                
                # Insert with ON CONFLICT handling
                cur.execute("""
                    INSERT INTO staging.league_season_details 
                    (league_id, season_id, league_start, league_end, league_type, has_adv_stats, rounds, raw_data)
                    VALUES (%(league_id)s, %(season_id)s, %(league_start)s, %(league_end)s, 
                            %(league_type)s, %(has_adv_stats)s, %(rounds)s, %(raw_data)s)
                    ON CONFLICT (league_id, season_id) 
                    DO UPDATE SET
                        league_start = EXCLUDED.league_start,
                        league_end = EXCLUDED.league_end,
                        league_type = EXCLUDED.league_type,
                        has_adv_stats = EXCLUDED.has_adv_stats,
                        rounds = EXCLUDED.rounds,
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
                # Get stored data
                cur.execute("""
                    SELECT league_id, season_id, league_start, league_end, league_type, 
                           has_adv_stats, rounds, raw_data
                    FROM staging.league_season_details 
                    WHERE league_id = %s AND season_id = %s
                """, (league_id, season_id))
                
                row = cur.fetchone()
                if not row:
                    print(f"❌ No data found for league_id={league_id}, season_id={season_id}")
                    return False
                
                # Parse stored data
                stored_data = {
                    'league_id': row[0],
                    'season_id': row[1],
                    'league_start': row[2],
                    'league_end': row[3],
                    'league_type': row[4],
                    'has_adv_stats': row[5],
                    'rounds': row[6] if row[6] else [],
                    'raw_data': row[7] if row[7] else {}
                }
                
                # Get original API data from raw_data
                original_data = stored_data['raw_data'].get('data', {})
                
                # Compare key fields (handle API lg_id vs stored league_id)
                if stored_data.get('league_id') != original_data.get('lg_id'):
                    print(f"❌ Field mismatch for league_id: stored={stored_data.get('league_id')}, original={original_data.get('lg_id')}")
                    return False
                
                if stored_data.get('season_id') != original_data.get('season_id'):
                    print(f"❌ Field mismatch for season_id: stored={stored_data.get('season_id')}, original={original_data.get('season_id')}")
                    return False
                
                if stored_data.get('league_type') != original_data.get('league_type'):
                    print(f"❌ Field mismatch for league_type: stored={stored_data.get('league_type')}, original={original_data.get('league_type')}")
                    return False
                
                if stored_data.get('has_adv_stats') != original_data.get('has_adv_stats'):
                    print(f"❌ Field mismatch for has_adv_stats: stored={stored_data.get('has_adv_stats')}, original={original_data.get('has_adv_stats')}")
                    return False
                
                # Compare dates (handle string vs date object conversion)
                if stored_data.get('league_start'):
                    stored_start = str(stored_data['league_start'])
                    original_start = original_data.get('league_start', '')
                    if stored_start != original_start:
                        print(f"❌ league_start mismatch: stored={stored_start}, original={original_start}")
                        return False
                
                if stored_data.get('league_end'):
                    stored_end = str(stored_data['league_end'])
                    original_end = original_data.get('league_end', '')
                    if stored_end != original_end:
                        print(f"❌ league_end mismatch: stored={stored_end}, original={original_end}")
                        return False
                
                # Compare rounds array
                stored_rounds = stored_data.get('rounds', [])
                original_rounds = original_data.get('rounds', [])
                if stored_rounds != original_rounds:
                    print(f"❌ Rounds mismatch: stored={stored_rounds}, original={original_rounds}")
                    return False
                
                print(f"✅ Data verification passed for league_id={league_id}, season_id={season_id}")
                return True
                
    except Exception as e:
        print(f"❌ Error verifying data: {e}")
        return False

def print_stored_data_summary():
    """Print summary of stored league season details data"""
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
                        COUNT(CASE WHEN league_type = 'cup' THEN 1 END) as cup_competitions,
                        COUNT(CASE WHEN league_type = 'league' THEN 1 END) as league_competitions,
                        COUNT(CASE WHEN has_adv_stats = 'yes' THEN 1 END) as with_adv_stats,
                        COUNT(CASE WHEN has_adv_stats = 'no' THEN 1 END) as without_adv_stats
                    FROM staging.league_season_details
                """)
                
                row = cur.fetchone()
                if row:
                    print("\n📊 League Season Details Data Summary:")
                    print(f"   Total Records: {row[0]}")
                    print(f"   Unique Leagues: {row[1]}")
                    print(f"   Unique Seasons: {row[2]}")
                    print(f"   Cup Competitions: {row[3]}")
                    print(f"   League Competitions: {row[4]}")
                    print(f"   With Advanced Stats: {row[5]}")
                    print(f"   Without Advanced Stats: {row[6]}")
                
                # Get sample data
                cur.execute("""
                    SELECT league_id, season_id, league_type, has_adv_stats, 
                           league_start, league_end, rounds
                    FROM staging.league_season_details 
                    ORDER BY league_id, season_id
                    LIMIT 5
                """)
                
                print("\n📋 Sample Data:")
                for row in cur.fetchall():
                    print(f"   League {row[0]} Season {row[1]}: {row[2]} ({row[3]} adv stats)")
                    print(f"     Period: {row[4]} to {row[5]}")
                    if row[6]:
                        rounds = row[6]
                        print(f"     Rounds: {', '.join(rounds[:3])}{'...' if len(rounds) > 3 else ''}")
                    print()
                
    except Exception as e:
        print(f"❌ Error getting summary: {e}")

def main():
    """Main test function"""
    print("🧪 Testing League Season Details Data Collection")
    print("=" * 50)
    
    # Initialize FBR client
    client = FBRClient()
    
    # Get test combinations
    combinations = get_test_league_season_combinations()
    print(f"📋 Testing {len(combinations)} league-season combinations")
    
    success_count = 0
    total_count = len(combinations)
    
    for i, combo in enumerate(combinations, 1):
        league_id = combo['league_id']
        season_id = combo['season_id']
        
        print(f"\n🔍 Test {i}/{total_count}: League {league_id}, Season {season_id}")
        
        try:
            # Make API call
            print(f"   📡 Making API call...")
            response = client.get_league_season_details(league_id, season_id)
            
            if "error" in response:
                print(f"   ❌ API Error: {response['error']}")
                continue
            
            # Store data
            print(f"   💾 Storing data...")
            if insert_league_season_details_data(response):
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
        print("\n🎉 All tests passed! League season details staging table is working correctly.")
        return 0
    else:
        print(f"\n⚠️  {total_count - success_count} tests failed. Check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 