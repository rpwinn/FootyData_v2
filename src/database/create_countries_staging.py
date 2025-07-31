#!/usr/bin/env python3
"""
Create staging table for countries data
Step 3: Create Staging Table
"""

import os
import psycopg2
from dotenv import load_dotenv

def create_countries_staging_table():
    """Create the staging table for countries data"""
    
    print("🗄️ Creating Countries Staging Table")
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
                
                # Create countries staging table
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS staging.countries (
                        id SERIAL PRIMARY KEY,
                        country VARCHAR(100) NOT NULL,
                        country_code VARCHAR(3) UNIQUE NOT NULL,
                        governing_body VARCHAR(20) NOT NULL,
                        num_clubs INTEGER DEFAULT 0,
                        num_players INTEGER DEFAULT 0,
                        national_teams TEXT[] DEFAULT '{}',
                        raw_data JSONB NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                print("✅ Created staging.countries table")
                
                # Create indexes for performance
                cur.execute("""
                    CREATE INDEX IF NOT EXISTS idx_countries_country_code 
                    ON staging.countries(country_code)
                """)
                
                cur.execute("""
                    CREATE INDEX IF NOT EXISTS idx_countries_governing_body 
                    ON staging.countries(governing_body)
                """)
                
                cur.execute("""
                    CREATE INDEX IF NOT EXISTS idx_countries_raw_data 
                    ON staging.countries USING GIN(raw_data)
                """)
                
                print("✅ Created indexes for performance")
                
                # Add comments for documentation
                cur.execute("""
                    COMMENT ON TABLE staging.countries IS 
                    'Staging table for countries data from FBR API /countries endpoint'
                """)
                
                cur.execute("""
                    COMMENT ON COLUMN staging.countries.country IS 
                    'Full country name (e.g., Afghanistan)'
                """)
                
                cur.execute("""
                    COMMENT ON COLUMN staging.countries.country_code IS 
                    '3-letter ISO country code (e.g., AFG)'
                """)
                
                cur.execute("""
                    COMMENT ON COLUMN staging.countries.governing_body IS 
                    'Football governing body (e.g., AFC, UEFA, CONCACAF)'
                """)
                
                cur.execute("""
                    COMMENT ON COLUMN staging.countries.num_clubs IS 
                    'Number of clubs in the country'
                """)
                
                cur.execute("""
                    COMMENT ON COLUMN staging.countries.num_players IS 
                    'Number of players tracked in the country'
                """)
                
                cur.execute("""
                    COMMENT ON COLUMN staging.countries.national_teams IS 
                    'Array of national team types (M=Men, F=Women)'
                """)
                
                cur.execute("""
                    COMMENT ON COLUMN staging.countries.raw_data IS 
                    'Complete JSON response from API for debugging and validation'
                """)
                
                print("✅ Added table and column comments")
                
                # Verify table structure
                cur.execute("""
                    SELECT column_name, data_type, is_nullable, column_default
                    FROM information_schema.columns 
                    WHERE table_schema = 'staging' 
                    AND table_name = 'countries'
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
                cur.execute("SELECT COUNT(*) FROM staging.countries")
                count = cur.fetchone()[0]
                
                print(f"\n📊 Current Status:")
                print(f"   • Records in table: {count}")
                print(f"   • Table ready for data insertion")
                
                return True
                
    except Exception as e:
        print(f"❌ Failed to create staging table: {e}")
        return False

if __name__ == "__main__":
    success = create_countries_staging_table()
    
    if success:
        print("\n🎉 Countries staging table created successfully!")
        print("✅ Ready for Step 4: Insert Data")
    else:
        print("\n❌ Failed to create countries staging table") 