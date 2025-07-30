#!/usr/bin/env python3
"""
Simple script to create match tables
"""

import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def create_match_tables():
    """Create match tables"""
    database_url = os.getenv("DATABASE_URL")
    print(f"Connecting to: {database_url}")
    
    with psycopg2.connect(database_url) as conn:
        with conn.cursor() as cur:
            print("Creating match_metadata table...")
            
            # Create match metadata table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS staging.match_metadata (
                    id SERIAL PRIMARY KEY,
                    match_id VARCHAR(20) UNIQUE,
                    date DATE,
                    time TIME,
                    wk VARCHAR(10),
                    home VARCHAR(100),
                    home_team_id VARCHAR(20),
                    away VARCHAR(100),
                    away_team_id VARCHAR(20),
                    home_team_score INTEGER,
                    away_team_score INTEGER,
                    venue VARCHAR(200),
                    attendance VARCHAR(50),
                    referee VARCHAR(100),
                    league_id INTEGER,
                    season_id VARCHAR(20),
                    raw_data JSONB,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            print("✅ Created match_metadata table")
            
            # Commit the transaction
            conn.commit()
            
            # Check if table was created
            cur.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'staging' AND table_name = 'match_metadata';")
            count = cur.fetchone()[0]
            print(f"Table count: {count}")

if __name__ == "__main__":
    create_match_tables() 