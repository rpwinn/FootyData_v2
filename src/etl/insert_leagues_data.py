#!/usr/bin/env python3
"""
Insert leagues data into staging table
Step 4: Insert Data
"""

import os
import json
import time
import psycopg2
from dotenv import load_dotenv

# Add src to path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from api.fbr_client import FBRClient

def insert_leagues_data():
    """Collect and insert leagues data into staging table"""
    
    print("💾 Inserting Leagues Data")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    api_key = os.getenv("FBR_API_KEY")
    database_url = os.getenv("DATABASE_URL")
    
    if not api_key:
        print("❌ FBR_API_KEY not found in .env file")
        return False
    
    if not database_url:
        print("❌ DATABASE_URL not found in .env file")
        return False
    
    try:
        # Initialize API client
        client = FBRClient()
        
        # Get countries from our staging table to iterate through
        print("📡 Getting countries from staging table...")
        
        with psycopg2.connect(database_url) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT country_code FROM staging.countries ORDER BY country_code")
                countries = [row[0] for row in cur.fetchall()]
        
        print(f"✅ Found {len(countries)} countries to process")
        
        # Clear existing leagues data
        with psycopg2.connect(database_url) as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM staging.leagues")
                print("✅ Cleared existing leagues data")
        
        # Process countries
        total_inserted = 0
        total_errors = 0
        processed_countries = 0
        
        for country_code in countries:
            print(f"\n📡 Processing {country_code}...")
            
            try:
                # Get leagues for this country
                start_time = time.time()
                response = client.get_leagues(country_code)
                api_time = time.time() - start_time
                
                if "error" in response:
                    print(f"   ❌ API Error for {country_code}: {response['error']}")
                    total_errors += 1
                    continue
                
                leagues_data = response.get('data', [])
                
                if not leagues_data:
                    print(f"   ⚠️  No leagues found for {country_code}")
                    continue
                
                # Insert leagues data
                insert_start_time = time.time()
                
                with psycopg2.connect(database_url) as conn:
                    with conn.cursor() as cur:
                        
                        inserted_count = 0
                        
                        for league_type_obj in leagues_data:
                            league_type = league_type_obj.get('league_type', 'Unknown')
                            leagues = league_type_obj.get('leagues', [])
                            
                            for league in leagues:
                                try:
                                    cur.execute("""
                                        INSERT INTO staging.leagues 
                                        (country_code, league_type, league_id, competition_name, 
                                         gender, first_season, last_season, tier, raw_data)
                                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
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
                                        json.dumps(league)
                                    ))
                                    
                                    inserted_count += 1
                                    
                                except Exception as e:
                                    print(f"   ❌ Error inserting league {league.get('league_id', 'Unknown')}: {e}")
                                    total_errors += 1
                        
                        conn.commit()
                        
                        insert_time = time.time() - insert_start_time
                        total_inserted += inserted_count
                        processed_countries += 1
                        
                        print(f"   ✅ {country_code}: {inserted_count} leagues inserted in {insert_time:.2f}s")
                
                # Rate limiting - wait 3 seconds between requests
                time.sleep(3)
                
            except Exception as e:
                print(f"   ❌ Failed to process {country_code}: {e}")
                total_errors += 1
                continue
        
        # Final verification and summary
        print(f"\n📊 Final Results:")
        print(f"   • Countries processed: {processed_countries}")
        print(f"   • Total leagues inserted: {total_inserted}")
        print(f"   • Total errors: {total_errors}")
        
        # Verify the data
        print(f"\n🔍 Verifying inserted data...")
        
        with psycopg2.connect(database_url) as conn:
            with conn.cursor() as cur:
                
                # Check total count
                cur.execute("SELECT COUNT(*) FROM staging.leagues")
                total_count = cur.fetchone()[0]
                print(f"   • Total records in table: {total_count}")
                
                # Check for duplicates
                cur.execute("""
                    SELECT country_code, league_id, COUNT(*) 
                    FROM staging.leagues 
                    GROUP BY country_code, league_id 
                    HAVING COUNT(*) > 1
                """)
                duplicates = cur.fetchall()
                
                if duplicates:
                    print(f"   ⚠️  Found {len(duplicates)} duplicate league entries")
                else:
                    print("   ✅ No duplicate league entries found")
                
                # Sample verification
                cur.execute("""
                    SELECT country_code, league_type, competition_name, gender, tier
                    FROM staging.leagues 
                    ORDER BY country_code, league_type
                    LIMIT 10
                """)
                
                sample_data = cur.fetchall()
                
                print(f"\n📋 Sample Inserted Data:")
                for row in sample_data:
                    country, league_type, name, gender, tier = row
                    print(f"   • {country} - {league_type} - {name} ({gender}) - {tier}")
                
                # League type distribution
                cur.execute("""
                    SELECT league_type, COUNT(*) 
                    FROM staging.leagues 
                    GROUP BY league_type 
                    ORDER BY COUNT(*) DESC
                """)
                
                league_types = cur.fetchall()
                
                print(f"\n🏆 League Type Distribution:")
                for league_type, count in league_types:
                    print(f"   • {league_type}: {count} leagues")
                
                # Gender distribution
                cur.execute("""
                    SELECT gender, COUNT(*) 
                    FROM staging.leagues 
                    GROUP BY gender 
                    ORDER BY COUNT(*) DESC
                """)
                
                gender_dist = cur.fetchall()
                
                print(f"\n👥 Gender Distribution:")
                for gender, count in gender_dist:
                    print(f"   • {gender}: {count} leagues")
                
                # Countries with most leagues
                cur.execute("""
                    SELECT country_code, COUNT(*) as league_count
                    FROM staging.leagues 
                    GROUP BY country_code 
                    ORDER BY COUNT(*) DESC 
                    LIMIT 10
                """)
                
                top_countries = cur.fetchall()
                
                print(f"\n🌍 Top Countries by League Count:")
                for country, count in top_countries:
                    print(f"   • {country}: {count} leagues")
                
                return True
                
    except Exception as e:
        print(f"❌ Failed to insert leagues data: {e}")
        return False

if __name__ == "__main__":
    success = insert_leagues_data()
    
    if success:
        print("\n🎉 Leagues data insertion completed successfully!")
        print("✅ /leagues endpoint implementation complete!")
        print("✅ Ready to move to next endpoint: /league-seasons")
    else:
        print("\n❌ Failed to insert leagues data") 