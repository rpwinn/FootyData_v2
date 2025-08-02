#!/usr/bin/env python3
"""
Load League Season Details Data
Parameterized script for collecting league season details data with optional filtering
"""

import os
import sys
import psycopg2
import json
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from dotenv import load_dotenv

# Add src to path
sys.path.append('src')

from api.fbr_client import FBRClient
from utils.endpoint_blacklist import load_endpoint_blacklist

def get_league_season_combinations(league_ids: Optional[List[int]] = None, 
                                  season_ids: Optional[List[str]] = None,
                                  time_period: Optional[str] = None) -> List[Dict[str, Any]]:
    """Get league-season combinations from the database"""
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        raise ValueError("DATABASE_URL not found in .env file")
    
    try:
        with psycopg2.connect(database_url) as conn:
            with conn.cursor() as cur:
                # Build query based on parameters
                query = "SELECT league_id, season_id FROM staging.league_seasons WHERE 1=1"
                params = []
                
                if league_ids:
                    placeholders = ','.join(['%s'] * len(league_ids))
                    query += f" AND league_id IN ({placeholders})"
                    params.extend(league_ids)
                
                if season_ids:
                    placeholders = ','.join(['%s'] * len(season_ids))
                    query += f" AND season_id IN ({placeholders})"
                    params.extend(season_ids)
                
                if time_period:
                    # Add time period filtering logic here if needed
                    # For now, we'll use the season_ids parameter
                    pass
                
                query += " ORDER BY league_id, season_id"
                
                cur.execute(query, params)
                
                combinations = []
                for row in cur.fetchall():
                    combinations.append({
                        'league_id': row[0],
                        'season_id': row[1]
                    })
                
                return combinations
                
    except Exception as e:
        print(f"❌ Error getting league-season combinations: {e}")
        return []

def insert_league_season_details_data(data: Dict[str, Any]) -> bool:
    """Insert league season details data into staging table"""
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("❌ DATABASE_URL not found in .env file")
        return False
    
    try:
        with psycopg2.connect(database_url) as conn:
            with conn.cursor() as cur:
                # Extract data from API response
                api_data = data.get('data', {})
                
                # Handle invalid date values
                league_start = api_data.get('league_start')
                league_end = api_data.get('league_end')
                
                # Convert invalid date strings to None
                if league_start == 'Date' or league_start == '':
                    league_start = None
                if league_end == 'Date' or league_end == '':
                    league_end = None
                
                # Prepare data for insertion
                insert_data = {
                    'league_id': api_data.get('lg_id'),  # API returns lg_id, we store as league_id
                    'season_id': api_data.get('season_id'),
                    'league_start': league_start,
                    'league_end': league_end,
                    'league_type': api_data.get('league_type'),
                    'has_adv_stats': api_data.get('has_adv_stats'),
                    'rounds': json.dumps(api_data.get('rounds', [])),
                    'raw_data': json.dumps(data)
                }
                
                # Insert with ON CONFLICT handling
                cur.execute("""
                    INSERT INTO staging.league_season_details 
                    (league_id, season_id, league_start, league_end, league_type, has_adv_stats, rounds, raw_data)
                    VALUES (%(league_id)s, %(season_id)s, %(league_start)s, %(league_end)s, 
                            %(league_type)s, %(has_adv_stats)s, %(rounds)s, %(raw_data)s)
                    ON CONFLICT (league_id, season_id) 
                    DO UPDATE SET
                        league_start = EXCLUDED.league_start,
                        league_end = EXCLUDED.league_end,
                        league_type = EXCLUDED.league_type,
                        has_adv_stats = EXCLUDED.has_adv_stats,
                        rounds = EXCLUDED.rounds,
                        raw_data = EXCLUDED.raw_data,
                        updated_at = CURRENT_TIMESTAMP
                """, insert_data)
                
                conn.commit()
                return True
                
    except Exception as e:
        print(f"❌ Error inserting data: {e}")
        return False

def load_league_season_details_data(league_ids: Optional[List[int]] = None,
                                   season_ids: Optional[List[str]] = None,
                                   time_period: Optional[str] = None,
                                   update_only: bool = False,
                                   verbose: bool = False) -> bool:
    """
    Load league season details data with optional filtering
    
    Args:
        league_ids: List of league IDs to collect (None for all)
        season_ids: List of season IDs to collect (None for all)
        time_period: Time period filter (e.g., "2024", "2020s")
        update_only: Only update existing records, don't add new ones
        verbose: Enable verbose logging
    
    Returns:
        bool: True if successful, False otherwise
    """
    print(f"🏈 Loading League Season Details Data")
    print(f"   League IDs: {league_ids if league_ids else 'All'}")
    print(f"   Season IDs: {season_ids if season_ids else 'All'}")
    print(f"   Time Period: {time_period if time_period else 'All'}")
    print(f"   Update Only: {update_only}")
    
    # Initialize FBR client and blacklist
    client = FBRClient()
    blacklist = load_endpoint_blacklist()
    
    # Get league-season combinations
    combinations = get_league_season_combinations(league_ids, season_ids, time_period)
    
    if not combinations:
        print("❌ No league-season combinations found")
        return False
    
    print(f"📋 Found {len(combinations)} league-season combinations to process")
    
    success_count = 0
    error_count = 0
    blacklisted_count = 0
    
    for i, combo in enumerate(combinations, 1):
        league_id = combo['league_id']
        season_id = combo['season_id']
        
        if verbose:
            print(f"   [{i}/{len(combinations)}] Processing League {league_id}, Season {season_id}")
        
        # Check if blacklisted
        if blacklist.is_blacklisted("league-season-details", league_id=league_id):
            if verbose:
                print(f"      ⚠️  League {league_id} is blacklisted, skipping")
            blacklisted_count += 1
            continue
        
        try:
            # Make API call
            response = client.get_league_season_details(league_id, season_id)
            
            if "error" in response:
                if verbose:
                    print(f"      ❌ API Error: {response['error']}")
                error_count += 1
                continue
            
            # Store data
            if insert_league_season_details_data(response):
                success_count += 1
                if verbose:
                    print(f"      ✅ Stored successfully")
            else:
                error_count += 1
                if verbose:
                    print(f"      ❌ Failed to store data")
                
        except Exception as e:
            error_count += 1
            if verbose:
                print(f"      ❌ Error: {e}")
    
    # Print summary
    print(f"\n📊 Collection Summary:")
    print(f"   Successful: {success_count}")
    print(f"   Errors: {error_count}")
    print(f"   Blacklisted: {blacklisted_count}")
    print(f"   Total Processed: {len(combinations)}")
    
    if success_count > 0:
        print(f"✅ League season details collection completed successfully!")
        return True
    else:
        print(f"❌ No data was collected successfully")
        return False

def main():
    """Main CLI function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Load League Season Details Data")
    parser.add_argument("--league-ids", help="Comma-separated list of league IDs")
    parser.add_argument("--season-ids", help="Comma-separated list of season IDs")
    parser.add_argument("--time-period", help="Time period filter (e.g., 2024, 2020s)")
    parser.add_argument("--update-only", action="store_true", help="Only update existing records")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    # Parse arguments
    league_ids = None
    if args.league_ids:
        league_ids = [int(x.strip()) for x in args.league_ids.split(",")]
    
    season_ids = None
    if args.season_ids:
        season_ids = [x.strip() for x in args.season_ids.split(",")]
    
    # Run collection
    success = load_league_season_details_data(
        league_ids=league_ids,
        season_ids=season_ids,
        time_period=args.time_period,
        update_only=args.update_only,
        verbose=args.verbose
    )
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main()) 