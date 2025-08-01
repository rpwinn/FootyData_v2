#!/usr/bin/env python3
"""
Smart Cascading Data Collection System
Checks database freshness before making API calls
"""

import os
import sys
import psycopg2
import json
from datetime import datetime
from dotenv import load_dotenv
from typing import List, Optional, Dict, Any, Tuple

# Add src to path
sys.path.append('src')

from api.fbr_client import FBRClient
from utils.collection_config import load_collection_config

class SmartCascadingCollector:
    """Smart cascading data collector that checks database freshness"""
    
    def __init__(self):
        """Initialize the collector"""
        load_dotenv()
        self.database_url = os.getenv("DATABASE_URL")
        self.client = FBRClient()
        
        if not self.database_url:
            raise ValueError("DATABASE_URL not found in .env file")
    
    def check_countries_freshness(self, country_codes: List[str]) -> Tuple[bool, List[str]]:
        """
        Check if countries data is fresh
        
        Returns:
            Tuple[bool, List[str]]: (is_fresh, missing_countries)
        """
        print("🔍 Checking countries freshness...")
        
        try:
            with psycopg2.connect(self.database_url) as conn:
                with conn.cursor() as cur:
                    # Check if all required countries exist
                    placeholders = ','.join(['%s'] * len(country_codes))
                    cur.execute(f"""
                        SELECT country_code, country_name, governing_body 
                        FROM staging.countries 
                        WHERE country_code IN ({placeholders})
                    """, country_codes)
                    
                    existing_countries = {row[0]: (row[1], row[2]) for row in cur.fetchall()}
                    
                    missing_countries = [code for code in country_codes if code not in existing_countries]
                    
                    if missing_countries:
                        print(f"❌ Missing countries: {missing_countries}")
                        return False, missing_countries
                    else:
                        print(f"✅ All {len(country_codes)} countries exist in database")
                        return True, []
                        
        except Exception as e:
            print(f"❌ Error checking countries: {e}")
            return False, country_codes
    
    def check_leagues_freshness(self, country_codes: List[str]) -> Tuple[bool, List[Dict]]:
        """
        Check if leagues data is fresh by comparing last_season field
        
        Returns:
            Tuple[bool, List[Dict]]: (is_fresh, leagues_needing_update)
        """
        print("🔍 Checking leagues freshness...")
        
        try:
            with psycopg2.connect(self.database_url) as conn:
                with conn.cursor() as cur:
                    # Get existing leagues from database
                    placeholders = ','.join(['%s'] * len(country_codes))
                    cur.execute(f"""
                        SELECT league_id, country_code, competition_name, last_season
                        FROM staging.leagues 
                        WHERE country_code IN ({placeholders})
                    """, country_codes)
                    
                    db_leagues = {row[0]: (row[1], row[2], row[3]) for row in cur.fetchall()}
                    
                    leagues_needing_update = []
                    
                    # Check each country's leagues against API
                    for country_code in country_codes:
                        print(f"  📋 Checking {country_code} leagues...")
                        
                        try:
                            # Get fresh API data for this country
                            api_response = self.client.get_leagues(country_code)
                            
                            if "error" in api_response:
                                print(f"    ❌ API call failed for {country_code}")
                                continue
                            
                            api_data = api_response.get('data', [])
                            
                            # Process each league type
                            for league_type_obj in api_data:
                                leagues = league_type_obj.get('leagues', [])
                                
                                for league in leagues:
                                    league_id = league.get('league_id')
                                    api_last_season = league.get('last_season')
                                    
                                    if league_id in db_leagues:
                                        db_last_season = db_leagues[league_id][2]
                                        
                                        if db_last_season != api_last_season:
                                            print(f"    ⚠️ League {league_id} ({league.get('competition_name')}) needs update")
                                            print(f"      DB last_season: {db_last_season}")
                                            print(f"      API last_season: {api_last_season}")
                                            leagues_needing_update.append({
                                                'league_id': league_id,
                                                'country_code': country_code,
                                                'competition_name': league.get('competition_name'),
                                                'db_last_season': db_last_season,
                                                'api_last_season': api_last_season
                                            })
                                    else:
                                        # New league found
                                        print(f"    ➕ New league found: {league.get('competition_name')} (ID: {league_id})")
                                        leagues_needing_update.append({
                                            'league_id': league_id,
                                            'country_code': country_code,
                                            'competition_name': league.get('competition_name'),
                                            'db_last_season': None,
                                            'api_last_season': api_last_season
                                        })
                        
                        except Exception as e:
                            print(f"    ❌ Error checking {country_code}: {e}")
                    
                    if leagues_needing_update:
                        print(f"❌ {len(leagues_needing_update)} leagues need update")
                        return False, leagues_needing_update
                    else:
                        print(f"✅ All leagues are fresh")
                        return True, []
                        
        except Exception as e:
            print(f"❌ Error checking leagues: {e}")
            return False, []
    
    def collect_european_majors(self) -> bool:
        """
        Collect European majors data using smart cascading approach
        """
        print("🚀 Starting Smart European Majors Collection")
        print("=" * 50)
        
        # Load configuration
        config = load_collection_config()
        scope = config.get_scope('european_majors')
        
        if not scope:
            print("❌ European majors scope not found!")
            return False
        
        print(f"📋 Scope: {scope.name}")
        print(f"🌍 Countries: {', '.join(scope.countries)}")
        print(f"⏰ Time Period: {scope.time_period.description if scope.time_period else 'All time periods'}")
        
        # Step 1: Check countries freshness
        countries_fresh, missing_countries = self.check_countries_freshness(scope.countries)
        
        if not countries_fresh:
            print(f"\n📡 Loading missing countries: {missing_countries}")
            # TODO: Call countries loading function
            # load_countries_data(country_codes=missing_countries)
        
        # Step 2: Check leagues freshness
        leagues_fresh, leagues_needing_update = self.check_leagues_freshness(scope.countries)
        
        if not leagues_fresh:
            print(f"\n📡 Updating {len(leagues_needing_update)} leagues...")
            # TODO: Call leagues loading function
            # load_leagues_data(country_codes=scope.countries)
        
        # Step 3: Check if league seasons need refresh
        if not leagues_fresh:
            print(f"\n📡 League seasons may need refresh due to league updates...")
            # TODO: Call league seasons loading function
            # load_league_seasons_data(league_ids=[l['league_id'] for l in leagues_needing_update])
        else:
            print(f"\n✅ League seasons are fresh (no league updates needed)")
        
        print(f"\n🎉 Smart collection analysis complete!")
        return True

def main():
    """Main execution function"""
    try:
        collector = SmartCascadingCollector()
        collector.collect_european_majors()
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1) 