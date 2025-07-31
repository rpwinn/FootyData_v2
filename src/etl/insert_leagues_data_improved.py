#!/usr/bin/env python3
"""
Insert leagues data into staging table (Improved version)
Step 4: Insert Data
"""

import os
import json
import time
import psycopg2
import logging
from datetime import datetime
from dotenv import load_dotenv

# Add src to path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from api.fbr_client import FBRClient

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('leagues_extraction.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def insert_leagues_data():
    """Collect and insert leagues data into staging table"""
    
    logger.info("💾 Starting Leagues Data Extraction")
    logger.info("=" * 50)
    
    # Load environment variables
    load_dotenv()
    api_key = os.getenv("FBR_API_KEY")
    database_url = os.getenv("DATABASE_URL")
    
    if not api_key:
        logger.error("❌ FBR_API_KEY not found in .env file")
        return False
    
    if not database_url:
        logger.error("❌ DATABASE_URL not found in .env file")
        return False
    
    try:
        # Initialize API client
        client = FBRClient()
        
        # Get countries from our staging table to iterate through
        logger.info("📡 Getting countries from staging table...")
        
        with psycopg2.connect(database_url) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT country_code FROM staging.countries ORDER BY country_code")
                countries = [row[0] for row in cur.fetchall()]
        
        logger.info(f"✅ Found {len(countries)} countries to process")
        
        # Don't clear existing data - continue from where we left off
        logger.info("🔄 Continuing from existing data (not clearing)")
        
        # Process countries
        total_inserted = 0
        total_errors = 0
        processed_countries = 0
        start_time = datetime.now()
        
        for i, country_code in enumerate(countries, 1):
            logger.info(f"\n📡 Processing {country_code} ({i}/{len(countries)})...")
            
            try:
                # Get leagues for this country
                api_start_time = time.time()
                response = client.get_leagues(country_code)
                api_time = time.time() - api_start_time
                
                if "error" in response:
                    logger.error(f"   ❌ API Error for {country_code}: {response['error']}")
                    total_errors += 1
                    continue
                
                leagues_data = response.get('data', [])
                
                if not leagues_data:
                    logger.warning(f"   ⚠️  No leagues found for {country_code}")
                    continue
                
                # Insert leagues data
                insert_start_time = time.time()
                
                with psycopg2.connect(database_url) as conn:
                    with conn.cursor() as cur:
                        
                        inserted_count = 0
                        country_errors = 0
                        
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
                                    logger.error(f"   ❌ Error inserting league {league.get('league_id', 'Unknown')}: {e}")
                                    country_errors += 1
                                    total_errors += 1
                        
                        conn.commit()
                        
                        insert_time = time.time() - insert_start_time
                        total_inserted += inserted_count
                        processed_countries += 1
                        
                        logger.info(f"   ✅ {country_code}: {inserted_count} leagues inserted in {insert_time:.2f}s (API: {api_time:.2f}s)")
                        
                        if country_errors > 0:
                            logger.warning(f"   ⚠️  {country_errors} errors for {country_code}")
                
                # Rate limiting - wait 6 seconds between requests
                logger.info(f"   ⏱️  Waiting 6 seconds before next request...")
                time.sleep(6)
                
                # Progress update every 10 countries
                if i % 10 == 0:
                    elapsed = datetime.now() - start_time
                    avg_time_per_country = elapsed.total_seconds() / i
                    remaining_countries = len(countries) - i
                    estimated_remaining = remaining_countries * avg_time_per_country
                    
                    logger.info(f"\n📊 Progress Update ({i}/{len(countries)}):")
                    logger.info(f"   • Countries processed: {processed_countries}")
                    logger.info(f"   • Total leagues inserted: {total_inserted}")
                    logger.info(f"   • Total errors: {total_errors}")
                    logger.info(f"   • Estimated time remaining: {estimated_remaining/60:.1f} minutes")
                
            except Exception as e:
                logger.error(f"   ❌ Failed to process {country_code}: {e}")
                total_errors += 1
                continue
        
        # Final verification and summary
        elapsed = datetime.now() - start_time
        logger.info(f"\n📊 Final Results:")
        logger.info(f"   • Total time: {elapsed}")
        logger.info(f"   • Countries processed: {processed_countries}")
        logger.info(f"   • Total leagues inserted: {total_inserted}")
        logger.info(f"   • Total errors: {total_errors}")
        
        # Verify the data
        logger.info(f"\n🔍 Verifying inserted data...")
        
        with psycopg2.connect(database_url) as conn:
            with conn.cursor() as cur:
                
                # Check total count
                cur.execute("SELECT COUNT(*) FROM staging.leagues")
                total_count = cur.fetchone()[0]
                logger.info(f"   • Total records in table: {total_count}")
                
                # Check for duplicates
                cur.execute("""
                    SELECT country_code, league_id, COUNT(*) 
                    FROM staging.leagues 
                    GROUP BY country_code, league_id 
                    HAVING COUNT(*) > 1
                """)
                duplicates = cur.fetchall()
                
                if duplicates:
                    logger.warning(f"   ⚠️  Found {len(duplicates)} duplicate league entries")
                else:
                    logger.info("   ✅ No duplicate league entries found")
                
                # League type distribution
                cur.execute("""
                    SELECT league_type, COUNT(*) 
                    FROM staging.leagues 
                    GROUP BY league_type 
                    ORDER BY COUNT(*) DESC
                """)
                
                league_types = cur.fetchall()
                
                logger.info(f"\n🏆 League Type Distribution:")
                for league_type, count in league_types:
                    logger.info(f"   • {league_type}: {count} leagues")
                
                # Countries with most leagues
                cur.execute("""
                    SELECT country_code, COUNT(*) as league_count
                    FROM staging.leagues 
                    GROUP BY country_code 
                    ORDER BY COUNT(*) DESC 
                    LIMIT 10
                """)
                
                top_countries = cur.fetchall()
                
                logger.info(f"\n🌍 Top Countries by League Count:")
                for country, count in top_countries:
                    logger.info(f"   • {country}: {count} leagues")
                
                return True
                
    except Exception as e:
        logger.error(f"❌ Failed to insert leagues data: {e}")
        return False

if __name__ == "__main__":
    success = insert_leagues_data()
    
    if success:
        logger.info("\n🎉 Leagues data insertion completed successfully!")
        logger.info("✅ /leagues endpoint implementation complete!")
        logger.info("✅ Ready to move to next endpoint: /league-seasons")
    else:
        logger.error("\n❌ Failed to insert leagues data") 