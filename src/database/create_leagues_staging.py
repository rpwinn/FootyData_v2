#!/usr/bin/env python3
"""
Create staging table for leagues data
Step 3: Create Staging Table
"""

import os
import psycopg2
from dotenv import load_dotenv

def create_leagues_staging_table():
    """Create the staging table for leagues data"""
    
    print("🗄️ Creating Leagues Staging Table")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("❌ DATABASE_URL not found in .env file")
        return False
    
    try:
        # Connect to database
        with psycopg2.connect(database_url) as conn:
            with conn.cursor() as cur:
                
                # Create staging schema if it doesn't exist
                cur.execute("CREATE SCHEMA IF NOT EXISTS staging")
                print("✅ Created staging schema")
                
                # Create leagues staging table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS staging.leagues (
                        id SERIAL PRIMARY KEY,
                        country_code VARCHAR(3) NOT NULL,
                        league_type VARCHAR(50) NOT NULL,
                        league_id INTEGER NOT NULL,
                        competition_name VARCHAR(200) NOT NULL,
                        gender VARCHAR(1) NOT NULL,
                        first_season VARCHAR(20),
                        last_season VARCHAR(20),
                        tier VARCHAR(10),
                        raw_data JSONB NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(country_code, league_id)
                    )
                """)
                
                print("✅ Created staging.leagues table")
                
                # Create indexes for performance
                cur.execute("""
                    CREATE INDEX IF NOT EXISTS idx_leagues_country_code 
                    ON staging.leagues(country_code)
                """)
                
                cur.execute("""
                    CREATE INDEX IF NOT EXISTS idx_leagues_league_id 
                    ON staging.leagues(league_id)
                """)
                
                cur.execute("""
                    CREATE INDEX IF NOT EXISTS idx_leagues_league_type 
                    ON staging.leagues(league_type)
                """)
                
                cur.execute("""
                    CREATE INDEX IF NOT EXISTS idx_leagues_gender 
                    ON staging.leagues(gender)
                """)
                
                cur.execute("""
                    CREATE INDEX IF NOT EXISTS idx_leagues_raw_data 
                    ON staging.leagues USING GIN(raw_data)
                """)
                
                print("✅ Created indexes for performance")
                
                # Add comments for documentation
                cur.execute("""
                    COMMENT ON TABLE staging.leagues IS 
                    'Staging table for leagues data from FBR API /leagues endpoint'
                """)
                
                cur.execute("""
                    COMMENT ON COLUMN staging.leagues.country_code IS 
                    'Three-letter country code (e.g., JPN, ENG)'
                """)
                
                cur.execute("""
                    COMMENT ON COLUMN staging.leagues.league_type IS 
                    'Type of league (domestic_leagues, domestic_cups, international_competitions, national_team_competitions)'
                """)
                
                cur.execute("""
                    COMMENT ON COLUMN staging.leagues.league_id IS 
                    'Unique Football Reference league ID number'
                """)
                
                cur.execute("""
                    COMMENT ON COLUMN staging.leagues.competition_name IS 
                    'Name of the league (e.g., J1 League, Premier League)'
                """)
                
                cur.execute("""
                    COMMENT ON COLUMN staging.leagues.gender IS 
                    'Gender classification (M=Male, F=Female)'
                """)
                
                cur.execute("""
                    COMMENT ON COLUMN staging.leagues.first_season IS 
                    'Season ID for earliest tracked season (e.g., 2014, 2021-2022)'
                """)
                
                cur.execute("""
                    COMMENT ON COLUMN staging.leagues.last_season IS 
                    'Season ID for latest tracked season (e.g., 2025, 2025-2026)'
                """)
                
                cur.execute("""
                    COMMENT ON COLUMN staging.leagues.tier IS 
                    'Level in country football pyramid (1st, 2nd, 3rd, 4th)'
                """)
                
                cur.execute("""
                    COMMENT ON COLUMN staging.leagues.raw_data IS 
                    'Complete JSON response from API for debugging and validation'
                """)
                
                print("✅ Added table and column comments")
                
                # Verify table structure
                cur.execute("""
                    SELECT column_name, data_type, is_nullable, column_default
                    FROM information_schema.columns 
                    WHERE table_schema = 'staging' 
                    AND table_name = 'leagues'
                    ORDER BY ordinal_position
                """)
                
                columns = cur.fetchall()
                
                print("\n📋 Table Structure:")
                print("   Column Name         | Data Type    | Nullable | Default")
                print("   --------------------|--------------|----------|---------")
                
                for col in columns:
                    col_name = col[0].ljust(18)
                    data_type = col[1].ljust(12)
                    nullable = col[2].ljust(8)
                    default = col[3] if col[3] else 'NULL'
                    print(f"   {col_name} | {data_type} | {nullable} | {default}")
                
                # Check if table is empty
                cur.execute("SELECT COUNT(*) FROM staging.leagues")
                count = cur.fetchone()[0]
                
                print(f"\n📊 Current Status:")
                print(f"   • Records in table: {count}")
                print(f"   • Table ready for data insertion")
                
                return True
                
    except Exception as e:
        print(f"❌ Failed to create staging table: {e}")
        return False

if __name__ == "__main__":
    success = create_leagues_staging_table()
    
    if success:
        print("\n🎉 Leagues staging table created successfully!")
        print("✅ Ready for Step 4: Insert Data")
    else:
        print("\n❌ Failed to create leagues staging table") 