"""
Database setup for FootyData_v2

Creates the staging database schema for storing raw API data.
"""

import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv
import yaml

load_dotenv()

class DatabaseSetup:
    """Database setup and management"""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        """Initialize database setup"""
        self.database_url = os.getenv("DATABASE_URL")
        if not self.database_url:
            raise ValueError("DATABASE_URL environment variable not set")
        
        # Load configuration
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.staging_schema = self.config['database']['staging_schema']
        self.final_schema = self.config['database']['final_schema']
    
    def create_schemas(self):
        """Create staging and final schemas"""
        with psycopg2.connect(self.database_url) as conn:
            with conn.cursor() as cur:
                # Create staging schema
                cur.execute(f"CREATE SCHEMA IF NOT EXISTS {self.staging_schema}")
                print(f"✅ Created schema: {self.staging_schema}")
                
                # Create final schema
                cur.execute(f"CREATE SCHEMA IF NOT EXISTS {self.final_schema}")
                print(f"✅ Created schema: {self.final_schema}")
    
    def create_staging_tables(self):
        """Create staging tables for raw API data"""
        with psycopg2.connect(self.database_url) as conn:
            with conn.cursor() as cur:
                
                # Countries table
                cur.execute(f"""
                    CREATE TABLE IF NOT EXISTS {self.staging_schema}.countries (
                        id SERIAL PRIMARY KEY,
                        country VARCHAR(100),
                        country_code VARCHAR(3) UNIQUE,
                        governing_body VARCHAR(10),
                        num_clubs INTEGER,
                        num_players INTEGER,
                        national_teams TEXT[],
                        raw_data JSONB,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Leagues table
                cur.execute(f"""
                    CREATE TABLE IF NOT EXISTS {self.staging_schema}.leagues (
                        id SERIAL PRIMARY KEY,
                        league_id INTEGER UNIQUE,
                        competition_name VARCHAR(100),
                        league_type VARCHAR(50),
                        gender VARCHAR(1),
                        first_season VARCHAR(20),
                        last_season VARCHAR(20),
                        tier VARCHAR(10),
                        country_code VARCHAR(3),
                        raw_data JSONB,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # League seasons table
                cur.execute(f"""
                    CREATE TABLE IF NOT EXISTS {self.staging_schema}.league_seasons (
                        id SERIAL PRIMARY KEY,
                        league_id INTEGER,
                        season_id VARCHAR(20),
                        raw_data JSONB,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(league_id, season_id)
                    )
                """)
                
                # League standings table
                cur.execute(f"""
                    CREATE TABLE IF NOT EXISTS {self.staging_schema}.league_standings (
                        id SERIAL PRIMARY KEY,
                        league_id INTEGER,
                        season_id VARCHAR(20),
                        raw_data JSONB,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Teams table
                cur.execute(f"""
                    CREATE TABLE IF NOT EXISTS {self.staging_schema}.teams (
                        id SERIAL PRIMARY KEY,
                        team_id VARCHAR(20),
                        team_name VARCHAR(100),
                        league_id INTEGER,
                        season_id VARCHAR(20),
                        raw_data JSONB,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Players table
                cur.execute(f"""
                    CREATE TABLE IF NOT EXISTS {self.staging_schema}.players (
                        id SERIAL PRIMARY KEY,
                        player_id VARCHAR(20),
                        player_name VARCHAR(100),
                        team_id VARCHAR(20),
                        league_id INTEGER,
                        season_id VARCHAR(20),
                        raw_data JSONB,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Team season stats table
                cur.execute(f"""
                    CREATE TABLE IF NOT EXISTS {self.staging_schema}.team_season_stats (
                        id SERIAL PRIMARY KEY,
                        team_id VARCHAR(20),
                        league_id INTEGER,
                        season_id VARCHAR(20),
                        raw_data JSONB,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Player season stats table
                cur.execute(f"""
                    CREATE TABLE IF NOT EXISTS {self.staging_schema}.player_season_stats (
                        id SERIAL PRIMARY KEY,
                        player_id VARCHAR(20),
                        team_id VARCHAR(20),
                        league_id INTEGER,
                        season_id VARCHAR(20),
                        raw_data JSONB,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Matches table
                cur.execute(f"""
                    CREATE TABLE IF NOT EXISTS {self.staging_schema}.matches (
                        id SERIAL PRIMARY KEY,
                        match_id VARCHAR(20),
                        team_id VARCHAR(20),
                        league_id INTEGER,
                        season_id VARCHAR(20),
                        raw_data JSONB,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                print("✅ Created all staging tables")
    
    def setup_database(self):
        """Complete database setup"""
        print("Setting up FootyData_v2 database...")
        
        try:
            self.create_schemas()
            self.create_staging_tables()
            print("✅ Database setup complete!")
            return True
        except Exception as e:
            print(f"❌ Database setup failed: {e}")
            return False

def main():
    """Main setup function"""
    try:
        setup = DatabaseSetup()
        setup.setup_database()
    except Exception as e:
        print(f"Setup failed: {e}")

if __name__ == "__main__":
    main() 