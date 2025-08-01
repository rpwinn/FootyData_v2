#!/usr/bin/env python3
"""
Verify Countries Data by Comparing Database to Fresh API Call
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

def verify_countries_data():
    """Compare database data with fresh API call"""
    
    print("🔍 Verifying Countries Data: Database vs API")
    print("=" * 60)
    
    # Load environment variables
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("❌ DATABASE_URL not found in .env file")
        return False
    
    try:
        # Get fresh data from API
        print("📡 Fetching fresh data from API...")
        client = FBRClient()
        api_response = client.get_countries()
        api_data = api_response.get('data', [])
        print(f"✅ Retrieved {len(api_data)} countries from API")
        
        # Get data from database
        print("🗄️ Fetching data from database...")
        with psycopg2.connect(database_url) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT country_name, country_code, governing_body, 
                           num_clubs, num_players, national_teams, raw_data
                    FROM staging.countries 
                    ORDER BY country_code
                """)
                db_data = cur.fetchall()
        print(f"✅ Retrieved {len(db_data)} countries from database")
        
        # Compare counts
        if len(api_data) != len(db_data):
            print(f"❌ COUNT MISMATCH: API has {len(api_data)} countries, DB has {len(db_data)} countries")
            return False
        else:
            print(f"✅ Count match: {len(api_data)} countries")
        
        # Create lookup dictionaries
        api_lookup = {country['country_code']: country for country in api_data}
        db_lookup = {row[1]: row for row in db_data}  # country_code is at index 1
        
        # Check for missing countries
        api_codes = set(api_lookup.keys())
        db_codes = set(db_lookup.keys())
        
        missing_in_db = api_codes - db_codes
        extra_in_db = db_codes - api_codes
        
        if missing_in_db:
            print(f"❌ Missing in DB: {missing_in_db}")
        if extra_in_db:
            print(f"❌ Extra in DB: {extra_in_db}")
        
        if not missing_in_db and not extra_in_db:
            print("✅ All country codes match between API and DB")
        
        # Compare specific countries
        print("\n📋 Detailed Comparison of Sample Countries:")
        sample_countries = ['ENG', 'USA', 'BRA', 'GER', 'FRA', 'ESP', 'ITA']
        
        mismatches = 0
        for country_code in sample_countries:
            if country_code in api_lookup and country_code in db_lookup:
                api_country = api_lookup[country_code]
                db_country = db_lookup[country_code]
                
                print(f"\n  {api_country.get('country')} ({country_code}):")
                
                # Compare each field
                api_name = api_country.get('country')
                db_name = db_country[0]
                if api_name == db_name:
                    print(f"    ✅ Name: {api_name}")
                else:
                    print(f"    ❌ Name: API='{api_name}' vs DB='{db_name}'")
                    mismatches += 1
                
                api_code = api_country.get('country_code')
                db_code = db_country[1]
                if api_code == db_code:
                    print(f"    ✅ Code: {api_code}")
                else:
                    print(f"    ❌ Code: API='{api_code}' vs DB='{db_code}'")
                    mismatches += 1
                
                api_body = api_country.get('governing_body')
                db_body = db_country[2]
                if api_body == db_body:
                    print(f"    ✅ Governing Body: {api_body}")
                else:
                    print(f"    ❌ Governing Body: API='{api_body}' vs DB='{db_body}'")
                    mismatches += 1
                
                api_clubs = api_country.get('#_clubs', 0)
                db_clubs = db_country[3]
                if api_clubs == db_clubs:
                    print(f"    ✅ Clubs: {api_clubs}")
                else:
                    print(f"    ❌ Clubs: API={api_clubs} vs DB={db_clubs}")
                    mismatches += 1
                
                api_players = api_country.get('#_players', 0)
                db_players = db_country[4]
                if api_players == db_players:
                    print(f"    ✅ Players: {api_players}")
                else:
                    print(f"    ❌ Players: API={api_players} vs DB={db_players}")
                    mismatches += 1
                
                api_teams = api_country.get('national_teams', [])
                db_teams = db_country[5]
                if api_teams == db_teams:
                    print(f"    ✅ National Teams: {api_teams}")
                else:
                    print(f"    ❌ National Teams: API={api_teams} vs DB={db_teams}")
                    mismatches += 1
            else:
                print(f"  ❌ Country code {country_code} not found in both API and DB")
                mismatches += 1
        
        # Check raw_data integrity
        print("\n🔍 Checking raw_data integrity...")
        raw_data_mismatches = 0
        for country_code in sample_countries:
            if country_code in db_lookup:
                db_country = db_lookup[country_code]
                raw_data = db_country[6]  # raw_data is at index 6
                
                # Check if raw_data contains the individual country object
                if isinstance(raw_data, dict) and 'country' in raw_data:
                    raw_country_name = raw_data.get('country')
                    db_country_name = db_country[0]
                    
                    if raw_country_name == db_country_name:
                        print(f"    ✅ Raw data for {country_code}: {raw_country_name}")
                    else:
                        print(f"    ❌ Raw data mismatch for {country_code}: raw='{raw_country_name}' vs db='{db_country_name}'")
                        raw_data_mismatches += 1
                else:
                    print(f"    ❌ Raw data for {country_code} is not a valid country object")
                    raw_data_mismatches += 1
        
        # Summary
        print(f"\n📊 Verification Summary:")
        print(f"  Total countries: {len(api_data)}")
        print(f"  Field mismatches: {mismatches}")
        print(f"  Raw data mismatches: {raw_data_mismatches}")
        
        if mismatches == 0 and raw_data_mismatches == 0:
            print("✅ All data matches perfectly between API and database!")
            return True
        else:
            print("❌ Found mismatches between API and database data")
            return False
        
    except Exception as e:
        print(f"❌ Error during verification: {e}")
        return False

if __name__ == "__main__":
    success = verify_countries_data()
    if success:
        print("\n🎉 Countries data verification completed successfully!")
    else:
        print("\n❌ Countries data verification failed!")
        sys.exit(1) 