#!/usr/bin/env python3
"""
Load Countries Data from FBR API to Staging Table
Parameterized version for cascading collection framework
"""

import os
import sys
import psycopg2
import json
from datetime import datetime
from dotenv import load_dotenv
from typing import List, Optional, Dict, Any

# Add src to path
sys.path.append('src')

from api.fbr_client import FBRClient

def load_countries_data(country_codes: Optional[List[str]] = None, config: Optional[Dict[str, Any]] = None) -> bool:
    """
    Load countries data from API to staging table
    
    Args:
        country_codes: Optional list of country codes to filter by. If None, loads all countries.
        config: Optional configuration dictionary for additional settings
    
    Returns:
        bool: True if successful, False otherwise
    """
    
    print("📡 Loading Countries Data from API")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("❌ DATABASE_URL not found in .env file")
        return False
    
    try:
        # Initialize FBR client
        client = FBRClient()
        print("✅ FBR Client initialized")
        
        # Get all countries data
        print("📡 Fetching countries data...")
        countries_response = client.get_countries()
        
        if "error" in countries_response:
            print(f"❌ API call failed: {countries_response['error']}")
            return False
        
        all_countries_data = countries_response.get('data', [])
        print(f"✅ Retrieved {len(all_countries_data)} total countries from API")
        
        # Filter by country codes if specified
        if country_codes:
            filtered_countries = [
                country for country in all_countries_data 
                if country.get('country_code') in country_codes
            ]
            print(f"📊 Filtered to {len(filtered_countries)} countries: {', '.join(country_codes)}")
        else:
            filtered_countries = all_countries_data
            print(f"📊 Loading all {len(filtered_countries)} countries")
        
        # Connect to database and insert data
        with psycopg2.connect(database_url) as conn:
            with conn.cursor() as cur:
                
                # Clear existing data for specified countries (or all if none specified)
                if country_codes:
                    placeholders = ','.join(['%s'] * len(country_codes))
                    cur.execute(f"DELETE FROM staging.countries WHERE country_code IN ({placeholders})", country_codes)
                    print(f"🗑️ Cleared existing data for {len(country_codes)} countries")
                else:
                    cur.execute("DELETE FROM staging.countries")
                    print("🗑️ Cleared all existing data")
                
                # Insert new data
                for country in filtered_countries:
                    cur.execute("""
                        INSERT INTO staging.countries (
                            country_name, country_code, governing_body, 
                            num_clubs, num_players, national_teams, raw_data
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (country_code) DO UPDATE SET
                            country_name = EXCLUDED.country_name,
                            governing_body = EXCLUDED.governing_body,
                            num_clubs = EXCLUDED.num_clubs,
                            num_players = EXCLUDED.num_players,
                            national_teams = EXCLUDED.national_teams,
                            raw_data = EXCLUDED.raw_data,
                            updated_at = CURRENT_TIMESTAMP
                    """, (
                        country.get('country'),
                        country.get('country_code'),
                        country.get('governing_body'),
                        country.get('#_clubs', 0),
                        country.get('#_players', 0),
                        country.get('national_teams', []),
                        json.dumps(country)  # Store individual country object
                    ))
                
                print(f"✅ Inserted {len(filtered_countries)} countries into staging table")
                
                # Verify data was inserted
                if country_codes:
                    placeholders = ','.join(['%s'] * len(country_codes))
                    cur.execute(f"SELECT COUNT(*) FROM staging.countries WHERE country_code IN ({placeholders})", country_codes)
                else:
                    cur.execute("SELECT COUNT(*) FROM staging.countries")
                count = cur.fetchone()[0]
                print(f"📊 Verified {count} countries in staging table")
                
                return True
                
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return False

def verify_data_integrity(country_codes: Optional[List[str]] = None) -> bool:
    """
    Verify that stored data matches original API response
    
    Args:
        country_codes: Optional list of country codes to verify. If None, verifies all.
    
    Returns:
        bool: True if verification passes, False otherwise
    """
    
    print("\n🔍 Verifying Data Integrity")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("❌ DATABASE_URL not found in .env file")
        return False
    
    try:
        # Get fresh data from API
        client = FBRClient()
        api_response = client.get_countries()
        api_data = api_response.get('data', [])
        
        # Filter API data if country codes specified
        if country_codes:
            api_data = [country for country in api_data if country.get('country_code') in country_codes]
        
        # Get data from database
        with psycopg2.connect(database_url) as conn:
            with conn.cursor() as cur:
                if country_codes:
                    placeholders = ','.join(['%s'] * len(country_codes))
                    cur.execute(f"""
                        SELECT country_name, country_code, governing_body, 
                               num_clubs, num_players, national_teams, raw_data
                        FROM staging.countries 
                        WHERE country_code IN ({placeholders})
                        ORDER BY country_code
                    """, country_codes)
                else:
                    cur.execute("""
                        SELECT country_name, country_code, governing_body, 
                               num_clubs, num_players, national_teams, raw_data
                        FROM staging.countries 
                        ORDER BY country_code
                    """)
                db_data = cur.fetchall()
        
        print(f"📊 API data: {len(api_data)} countries")
        print(f"📊 DB data: {len(db_data)} countries")
        
        # Compare data
        if len(api_data) != len(db_data):
            print("❌ Data count mismatch!")
            return False
        
        print("✅ Data count matches")
        
        # Create lookup dictionaries for comparison
        api_lookup = {country['country_code']: country for country in api_data}
        db_lookup = {row[1]: row for row in db_data}  # country_code is at index 1
        
        # Check a few sample records
        print("\n📋 Sample verification:")
        sample_countries = country_codes[:5] if country_codes else ['AFG', 'ENG', 'USA', 'BRA', 'GER']
        
        for i, country_code in enumerate(sample_countries):
            if country_code in api_lookup and country_code in db_lookup:
                api_country = api_lookup[country_code]
                db_country = db_lookup[country_code]
                
                print(f"  {i+1}. {api_country.get('country')} ({country_code})")
                
                # Compare key fields
                api_name = api_country.get('country')
                db_name = db_country[0]
                if api_name == db_name:
                    print(f"     ✅ Name: {api_name}")
                else:
                    print(f"     ❌ Name: API='{api_name}' vs DB='{db_name}'")
                    return False
                
                api_code = api_country.get('country_code')
                db_code = db_country[1]
                if api_code == db_code:
                    print(f"     ✅ Code: {api_code}")
                else:
                    print(f"     ❌ Code: API='{api_code}' vs DB='{db_code}'")
                    return False
        
        print("\n✅ Data integrity verification completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error verifying data: {e}")
        return False

def main():
    """Main execution function for backward compatibility"""
    
    print("🚀 Starting Countries Data Loading (Parameterized Version)")
    print("=" * 60)
    
    # Load all countries (backward compatibility)
    success = load_countries_data()
    
    if success:
        # Verify data integrity
        verify_data_integrity()
        print("\n🎉 Countries data loading completed successfully!")
    else:
        print("\n❌ Countries data loading failed!")
    
    return success

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1) 