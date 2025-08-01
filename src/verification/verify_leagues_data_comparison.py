#!/usr/bin/env python3
"""
Verify Leagues Data by Comparing Database to Fresh API Call
This script ensures the data in our database exactly matches what the API returns
"""

import os
import sys
import psycopg2
import json
from dotenv import load_dotenv

# Add src to path
sys.path.append('src')

from api.fbr_client import FBRClient

def verify_leagues_data():
    """Compare database data with fresh API call"""
    
    print("🔍 Verifying Leagues Data: Database vs API")
    print("=" * 60)
    
    # Load environment variables
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("❌ DATABASE_URL not found in .env file")
        return False
    
    try:
        # Test countries
        test_countries = ['ENG', 'USA', 'BRA']
        
        # Get fresh data from API
        client = FBRClient()
        
        total_mismatches = 0
        
        for country_code in test_countries:
            print(f"\n📋 Verifying {country_code}...")
            
            # Get fresh API data
            api_response = client.get_leagues(country_code)
            api_data = api_response.get('data', [])
            
            # Get data from database
            with psycopg2.connect(database_url) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT league_id, competition_name, gender, first_season, 
                               last_season, tier, league_type, raw_data
                        FROM staging.leagues 
                        WHERE country_code = %s
                        ORDER BY league_id
                    """, (country_code,))
                    db_data = cur.fetchall()
            
            # Count leagues in API response
            api_league_count = 0
            api_leagues = []
            for league_type_obj in api_data:
                league_type = league_type_obj.get('league_type', 'unknown')
                leagues = league_type_obj.get('leagues', [])
                api_league_count += len(leagues)
                
                # Flatten leagues with league_type
                for league in leagues:
                    league['league_type'] = league_type
                    api_leagues.append(league)
            
            db_league_count = len(db_data)
            
            print(f"  API leagues: {api_league_count}")
            print(f"  DB leagues: {db_league_count}")
            
            if api_league_count != db_league_count:
                print(f"  ❌ League count mismatch for {country_code}")
                total_mismatches += 1
                continue
            
            # Compare individual leagues
            print(f"  📊 Comparing {api_league_count} leagues...")
            
            # Create lookup for API leagues
            api_lookup = {league['league_id']: league for league in api_leagues}
            db_lookup = {row[0]: row for row in db_data}  # league_id is at index 0
            
            country_mismatches = 0
            
            for league_id in api_lookup:
                if league_id in db_lookup:
                    api_league = api_lookup[league_id]
                    db_league = db_lookup[league_id]
                    
                    # Compare fields
                    if (api_league.get('competition_name') != db_league[1] or
                        api_league.get('gender') != db_league[2] or
                        api_league.get('first_season') != db_league[3] or
                        api_league.get('last_season') != db_league[4] or
                        api_league.get('tier') != db_league[5] or
                        api_league.get('league_type') != db_league[6]):
                        country_mismatches += 1
                        print(f"    ❌ Mismatch for league {league_id}: {api_league.get('competition_name')}")
            
            if country_mismatches == 0:
                print(f"  ✅ All {api_league_count} leagues match perfectly for {country_code}")
            else:
                print(f"  ❌ Found {country_mismatches} mismatches for {country_code}")
                total_mismatches += country_mismatches
        
        # Summary
        print(f"\n📊 Verification Summary:")
        print(f"  Countries tested: {len(test_countries)}")
        print(f"  Total mismatches: {total_mismatches}")
        
        if total_mismatches == 0:
            print("✅ All data matches perfectly between API and database!")
            return True
        else:
            print("❌ Found mismatches between API and database data")
            return False
        
    except Exception as e:
        print(f"❌ Error during verification: {e}")
        return False

if __name__ == "__main__":
    success = verify_leagues_data()
    if success:
        print("\n🎉 Leagues data verification completed successfully!")
    else:
        print("\n❌ Leagues data verification failed!")
        sys.exit(1) 