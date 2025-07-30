"""
Data Collector for FootyData_v2

Collects data from the FBR API and stores it in the staging database.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import psycopg2
import json
from typing import Dict, Any, List
from api.fbr_client import FBRClient
from database.setup import DatabaseSetup
import yaml

class DataCollector:
    """Collects data from FBR API and stores in staging database"""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        """Initialize data collector"""
        self.client = FBRClient(config_path)
        
        # Load configuration
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.leagues = self.config['leagues']
        self.seasons = self.config['seasons']
        
        # Database connection
        import os
        from dotenv import load_dotenv
        load_dotenv()
        
        self.database_url = os.getenv("DATABASE_URL")
        if not self.database_url:
            raise ValueError("DATABASE_URL environment variable not set")
        
        self.staging_schema = self.config['database']['staging_schema']
    
    def store_countries(self):
        """Collect and store countries data"""
        print("Collecting countries data...")
        
        countries = self.client.get_countries()
        if "error" in countries:
            print(f"Failed to get countries: {countries['error']}")
            return False
        
        with psycopg2.connect(self.database_url) as conn:
            with conn.cursor() as cur:
                for country_data in countries.get('data', []):
                    cur.execute(f"""
                        INSERT INTO {self.staging_schema}.countries 
                        (country, country_code, governing_body, num_clubs, num_players, national_teams, raw_data)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (country_code) DO NOTHING
                    """, (
                        country_data.get('country'),
                        country_data.get('country_code'),
                        country_data.get('governing_body'),
                        country_data.get('#_clubs'),
                        country_data.get('#_players'),
                        country_data.get('national_teams'),
                        json.dumps(country_data)
                    ))
        
        print(f"✅ Stored {len(countries.get('data', []))} countries")
        return True
    
    def store_leagues(self):
        """Collect and store leagues data for configured countries"""
        print("Collecting leagues data...")
        
        for league_config in self.leagues:
            country_code = league_config['country_code']
            print(f"Collecting leagues for {country_code}...")
            
            leagues = self.client.get_leagues(country_code)
            if "error" in leagues:
                print(f"Failed to get leagues for {country_code}: {leagues['error']}")
                continue
            
            with psycopg2.connect(self.database_url) as conn:
                with conn.cursor() as cur:
                    # The API returns leagues nested in a 'leagues' array
                    leagues_data = leagues.get('data', {}).get('leagues', [])
                    for league_data in leagues_data:
                        cur.execute(f"""
                            INSERT INTO {self.staging_schema}.leagues 
                            (league_id, competition_name, league_type, gender, first_season, last_season, tier, country_code, raw_data)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                            ON CONFLICT (league_id) DO NOTHING
                        """, (
                            int(league_data.get('league_id')),
                            league_data.get('competition_name'),
                            leagues.get('data', {}).get('league_type'),
                            league_data.get('gender'),
                            league_data.get('first_season'),
                            league_data.get('last_season'),
                            league_data.get('tier'),
                            country_code,
                            json.dumps(league_data)
                        ))
            
            print(f"✅ Stored {len(leagues.get('data', []))} leagues for {country_code}")
        
        return True
    
    def store_league_seasons(self):
        """Collect and store league seasons data"""
        print("Collecting league seasons data...")
        
        for league_config in self.leagues:
            league_id = league_config['league_id']
            print(f"Collecting seasons for league {league_id}...")
            
            seasons = self.client.get_league_seasons(league_id)
            if "error" in seasons:
                print(f"Failed to get seasons for league {league_id}: {seasons['error']}")
                continue
            
            with psycopg2.connect(self.database_url) as conn:
                with conn.cursor() as cur:
                    for season_data in seasons.get('data', []):
                        cur.execute(f"""
                            INSERT INTO {self.staging_schema}.league_seasons 
                            (league_id, season_id, raw_data)
                            VALUES (%s, %s, %s)
                            ON CONFLICT (league_id, season_id) DO NOTHING
                        """, (
                            int(league_id),
                            season_data.get('season_id'),
                            json.dumps(season_data)
                        ))
            
            print(f"✅ Stored {len(seasons.get('data', []))} seasons for league {league_id}")
        
        return True
    
    def collect_all_data(self):
        """Collect all available data"""
        print("Starting data collection...")
        
        # Test API connection first
        if not self.client.test_connection():
            print("❌ API connection failed!")
            return False
        
        # Collect data in order
        success = True
        success &= self.store_countries()
        success &= self.store_leagues()
        success &= self.store_league_seasons()
        
        if success:
            print("✅ Data collection completed successfully!")
        else:
            print("❌ Data collection completed with errors!")
        
        return success

def main():
    """Main data collection function"""
    try:
        collector = DataCollector()
        collector.collect_all_data()
    except Exception as e:
        print(f"Data collection failed: {e}")

if __name__ == "__main__":
    main() 