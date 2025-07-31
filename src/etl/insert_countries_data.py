#!/usr/bin/env python3
"""
Insert countries data into staging table
Step 4: Insert Data
"""

import os
import sys
import json
import time
import psycopg2
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from api.fbr_client import FBRClient

def insert_countries_data():
    """Collect and insert countries data into staging table"""
    
    print("💾 Inserting Countries Data")
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
        
        print("📡 Collecting countries data from API...")
        start_time = time.time()
        
        # Get countries data
        response = client.get_countries()
        
        api_time = time.time() - start_time
        print(f"⏱️  API request completed in {api_time:.2f} seconds")
        
        if "error" in response:
            print(f"❌ API Error: {response['error']}")
            return False
        
        countries_data = response.get('data', [])
        print(f"✅ Retrieved {len(countries_data)} countries from API")
        
        # Insert data into staging table
        print("\n🗄️ Inserting data into staging.countries...")
        insert_start_time = time.time()
        
        with psycopg2.connect(database_url) as conn:
            with conn.cursor() as cur:
                
                # Clear existing data (for fresh start)
                cur.execute("DELETE FROM staging.countries")
                print("✅ Cleared existing data")
                
                # Insert new data
                inserted_count = 0
                errors = []
                
                for country in countries_data:
                    try:
                        cur.execute("""
                            INSERT INTO staging.countries 
                            (country, country_code, governing_body, num_clubs, num_players, national_teams, raw_data)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """, (
                            country.get('country'),
                            country.get('country_code'),
                            country.get('governing_body'),
                            country.get('#_clubs', 0),
                            country.get('#_players', 0),
                            country.get('national_teams', []),
                            json.dumps(country)
                        ))
                        
                        inserted_count += 1
                        
                    except Exception as e:
                        errors.append({
                            'country': country.get('country', 'Unknown'),
                            'error': str(e)
                        })
                
                # Commit the transaction
                conn.commit()
                
                insert_time = time.time() - insert_start_time
                print(f"⏱️  Database insertion completed in {insert_time:.2f} seconds")
                
                # Report results
                print(f"\n📊 Insertion Results:")
                print(f"   • Successfully inserted: {inserted_count} countries")
                print(f"   • Errors encountered: {len(errors)}")
                
                if errors:
                    print("\n❌ Errors:")
                    for error in errors[:5]:  # Show first 5 errors
                        print(f"   • {error['country']}: {error['error']}")
                    if len(errors) > 5:
                        print(f"   • ... and {len(errors) - 5} more errors")
                
                # Verify the data
                print("\n🔍 Verifying inserted data...")
                
                # Check total count
                cur.execute("SELECT COUNT(*) FROM staging.countries")
                total_count = cur.fetchone()[0]
                print(f"   • Total records in table: {total_count}")
                
                # Check for duplicates
                cur.execute("""
                    SELECT country_code, COUNT(*) 
                    FROM staging.countries 
                    GROUP BY country_code 
                    HAVING COUNT(*) > 1
                """)
                duplicates = cur.fetchall()
                
                if duplicates:
                    print(f"   ⚠️  Found {len(duplicates)} duplicate country codes")
                else:
                    print("   ✅ No duplicate country codes found")
                
                # Sample verification
                cur.execute("""
                    SELECT country, country_code, governing_body, num_clubs, num_players
                    FROM staging.countries 
                    ORDER BY country 
                    LIMIT 5
                """)
                
                sample_data = cur.fetchall()
                
                print("\n📋 Sample Inserted Data:")
                for row in sample_data:
                    country, code, body, clubs, players = row
                    print(f"   • {country} ({code}) - {body} - {clubs} clubs, {players} players")
                
                # Governing body distribution
                cur.execute("""
                    SELECT governing_body, COUNT(*) 
                    FROM staging.countries 
                    GROUP BY governing_body 
                    ORDER BY COUNT(*) DESC
                """)
                
                governing_bodies = cur.fetchall()
                
                print("\n🌍 Governing Body Distribution:")
                for body, count in governing_bodies:
                    print(f"   • {body}: {count} countries")
                
                # Data quality summary
                cur.execute("""
                    SELECT 
                        SUM(num_clubs) as total_clubs,
                        SUM(num_players) as total_players,
                        COUNT(*) as total_countries
                    FROM staging.countries
                """)
                
                summary = cur.fetchone()
                total_clubs, total_players, total_countries = summary
                
                print(f"\n📈 Data Summary:")
                print(f"   • Total countries: {total_countries}")
                print(f"   • Total clubs: {total_clubs:,}")
                print(f"   • Total players: {total_players:,}")
                print(f"   • Average clubs per country: {total_clubs/total_countries:.1f}")
                print(f"   • Average players per country: {total_players/total_countries:.1f}")
                
                return True
                
    except Exception as e:
        print(f"❌ Failed to insert countries data: {e}")
        return False

if __name__ == "__main__":
    success = insert_countries_data()
    
    if success:
        print("\n🎉 Countries data insertion completed successfully!")
        print("✅ /countries endpoint implementation complete!")
        print("✅ Ready to move to next endpoint: /leagues")
    else:
        print("\n❌ Failed to insert countries data") 