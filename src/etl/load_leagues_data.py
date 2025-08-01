#!/usr/bin/env python3
"""
Load Leagues Data from FBR API to Staging Table
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

def load_leagues_data(country_codes: Optional[List[str]] = None, config: Optional[Dict[str, Any]] = None) -> bool:
    """
    Load leagues data from API to staging table
    
    Args:
        country_codes: Optional list of country codes to filter by. If None, loads all countries.
        config: Optional configuration dictionary for additional settings
    
    Returns:
        bool: True if successful, False otherwise
    """
    
    print("📡 Loading Leagues Data from API")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("❌ DATABASE_URL not found in .env file")
        return False
    
    # If no country codes specified, get all countries from database
    if not country_codes:
        try:
            with psycopg2.connect(database_url) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT DISTINCT country_code FROM staging.countries ORDER BY country_code")
                    country_codes = [row[0] for row in cur.fetchall()]
            print(f"📊 Using all {len(country_codes)} countries from database")
        except Exception as e:
            print(f"❌ Error getting countries from database: {e}")
            return False
    
    print(f"📊 Processing {len(country_codes)} countries: {', '.join(country_codes)}")
    
    try:
        # Initialize FBR client
        client = FBRClient()
        print("✅ FBR Client initialized")
        
        # Connect to database
        with psycopg2.connect(database_url) as conn:
            with conn.cursor() as cur:
                
                # Clear existing data for specified countries
                placeholders = ','.join(['%s'] * len(country_codes))
                cur.execute(f"DELETE FROM staging.leagues WHERE country_code IN ({placeholders})", country_codes)
                print(f"🗑️ Cleared existing data for {len(country_codes)} countries")
                
                total_leagues = 0
                failed_countries = []
                
                for country_code in country_codes:
                    print(f"\n📡 Fetching leagues for {country_code}...")
                    
                    try:
                        # Get leagues data for this country
                        leagues_response = client.get_leagues(country_code)
                        
                        if "error" in leagues_response:
                            print(f"❌ API call failed for {country_code}: {leagues_response['error']}")
                            failed_countries.append(country_code)
                            continue
                        
                        data = leagues_response.get('data', [])
                        country_leagues = 0
                        
                        # Process each league type
                        for league_type_obj in data:
                            league_type = league_type_obj.get('league_type', 'unknown')
                            leagues = league_type_obj.get('leagues', [])
                            
                            # Insert each league
                            for league in leagues:
                                cur.execute("""
                                    INSERT INTO staging.leagues (
                                        country_code, league_type, league_id, competition_name,
                                        gender, first_season, last_season, tier, raw_data
                                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                                    ON CONFLICT (country_code, league_id) DO UPDATE SET
                                        league_type = EXCLUDED.league_type,
                                        competition_name = EXCLUDED.competition_name,
                                        gender = EXCLUDED.gender,
                                        first_season = EXCLUDED.first_season,
                                        last_season = EXCLUDED.last_season,
                                        tier = EXCLUDED.tier,
                                        raw_data = EXCLUDED.raw_data,
                                        updated_at = CURRENT_TIMESTAMP
                                """, (
                                    country_code,
                                    league_type,
                                    league.get('league_id'),
                                    league.get('competition_name'),
                                    league.get('gender'),
                                    league.get('first_season'),
                                    league.get('last_season'),
                                    league.get('tier'),
                                    json.dumps(league)  # Store individual league object
                                ))
                                country_leagues += 1
                        
                        print(f"✅ Inserted {country_leagues} leagues for {country_code}")
                        total_leagues += country_leagues
                        
                    except Exception as e:
                        print(f"❌ Error processing {country_code}: {e}")
                        failed_countries.append(country_code)
                
                print(f"\n📊 Total leagues inserted: {total_leagues}")
                
                if failed_countries:
                    print(f"⚠️ Failed countries: {', '.join(failed_countries)}")
                
                # Verify data was inserted
                placeholders = ','.join(['%s'] * len(country_codes))
                cur.execute(f"SELECT COUNT(*) FROM staging.leagues WHERE country_code IN ({placeholders})", country_codes)
                count = cur.fetchone()[0]
                print(f"📊 Verified {count} leagues in staging table")
                
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
        # Get fresh data from API for sample countries
        client = FBRClient()
        
        # Use provided country codes or sample from database
        if not country_codes:
            with psycopg2.connect(database_url) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT DISTINCT country_code FROM staging.countries ORDER BY country_code LIMIT 5")
                    country_codes = [row[0] for row in cur.fetchall()]
        
        print(f"📊 Verifying {len(country_codes)} countries: {', '.join(country_codes)}")
        
        total_api_leagues = 0
        total_db_leagues = 0
        
        for country_code in country_codes:
            print(f"\n📋 Verifying {country_code}...")
            
            # Get fresh API data
            api_response = client.get_leagues(country_code)
            api_data = api_response.get('data', [])
            
            # Count leagues in API response
            api_league_count = 0
            for league_type_obj in api_data:
                api_league_count += len(league_type_obj.get('leagues', []))
            
            # Get data from database
            with psycopg2.connect(database_url) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT COUNT(*) FROM staging.leagues 
                        WHERE country_code = %s
                    """, (country_code,))
                    db_league_count = cur.fetchone()[0]
            
            print(f"  API leagues: {api_league_count}")
            print(f"  DB leagues: {db_league_count}")
            
            if api_league_count == db_league_count:
                print(f"  ✅ League count matches for {country_code}")
            else:
                print(f"  ❌ League count mismatch for {country_code}")
                return False
            
            total_api_leagues += api_league_count
            total_db_leagues += db_league_count
        
        print(f"\n📊 Total API leagues: {total_api_leagues}")
        print(f"📊 Total DB leagues: {total_db_leagues}")
        
        if total_api_leagues == total_db_leagues:
            print("✅ All league counts match!")
            return True
        else:
            print("❌ Total league count mismatch!")
            return False
        
    except Exception as e:
        print(f"❌ Error verifying data: {e}")
        return False

def main():
    """Main execution function for backward compatibility"""
    
    print("🚀 Starting Leagues Data Loading (Parameterized Version)")
    print("=" * 60)
    
    # Load all leagues (backward compatibility)
    success = load_leagues_data()
    
    if success:
        # Verify data integrity
        verify_data_integrity()
        print("\n🎉 Leagues data loading completed successfully!")
    else:
        print("\n❌ Leagues data loading failed!")
    
    return success

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1) 