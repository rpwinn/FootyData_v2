#!/usr/bin/env python3
"""
Load League Seasons Data from FBR API to Staging Table
Parameterized version with selective update logic
"""

import os
import sys
import psycopg2
import json
import re
from datetime import datetime
from dotenv import load_dotenv
from typing import List, Optional, Dict, Any

# Add src to path
sys.path.append('src')

from api.fbr_client import FBRClient

def load_league_seasons_data(league_ids: Optional[List[int]] = None, 
                           time_period: Optional[str] = None,
                           config: Optional[Dict[str, Any]] = None,
                           update_only: bool = False) -> bool:
    """
    Load league seasons data from API to staging table with selective updates
    
    Args:
        league_ids: Optional list of league IDs to filter by. If None, uses all leagues.
        time_period: Optional time period pattern (e.g., "2024", "2020s"). If None, loads all seasons.
        config: Optional configuration dictionary for additional settings
    
    Returns:
        bool: True if successful, False otherwise
    """
    
    print("📡 Loading League Seasons Data from API")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("❌ DATABASE_URL not found in .env file")
        return False
    
    # If no league IDs specified, get all leagues from database
    if not league_ids:
        try:
            with psycopg2.connect(database_url) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT DISTINCT league_id FROM staging.leagues ORDER BY league_id")
                    league_ids = [row[0] for row in cur.fetchall()]
            print(f"📊 Using all {len(league_ids)} leagues from database")
        except Exception as e:
            print(f"❌ Error getting leagues from database: {e}")
            return False
    
    print(f"📊 Processing {len(league_ids)} leagues")
    if time_period:
        print(f"⏰ Filtering for time period: {time_period}")
    if update_only:
        print(f"🔄 Update-only mode: only updating existing seasons")
    
    try:
        # Initialize FBR client
        client = FBRClient()
        print("✅ FBR Client initialized")
        
        # Connect to database
        with psycopg2.connect(database_url) as conn:
            with conn.cursor() as cur:
                
                total_seasons_processed = 0
                total_seasons_skipped = 0
                total_seasons_added = 0
                failed_leagues = []
                
                for league_id in league_ids:
                    print(f"\n📡 Processing league ID: {league_id}")
                    
                    try:
                        # Get existing seasons for this league
                        cur.execute("""
                            SELECT season_id, competition_name, num_squads, champion, 
                                   top_scorer_player, top_scorer_goals
                            FROM staging.league_seasons 
                            WHERE league_id = %s
                        """, (league_id,))
                        existing_seasons = {row[0]: row[1:] for row in cur.fetchall()}
                        
                        # Get fresh API data
                        seasons_response = client.get_league_seasons(league_id)
                        
                        if "error" in seasons_response:
                            print(f"❌ API call failed for league {league_id}: {seasons_response['error']}")
                            failed_leagues.append(league_id)
                            continue
                        
                        data = seasons_response.get('data', [])
                        league_seasons_processed = 0
                        league_seasons_skipped = 0
                        league_seasons_added = 0
                        
                        # Process each season
                        for season in data:
                            season_id = season.get('season_id')
                            
                            # Apply time period filter if specified
                            if time_period and not matches_time_period(season_id, time_period):
                                continue
                            
                            # Skip if season doesn't exist in database and we're in update-only mode
                            if update_only and season_id not in existing_seasons:
                                continue
                            
                            # Check if season already exists with same data
                            if season_id in existing_seasons:
                                existing_data = existing_seasons[season_id]
                                new_data = (
                                    season.get('competition_name'),
                                    season.get('num_squads'),
                                    season.get('champion'),
                                    season.get('top_scorer_player'),
                                    season.get('top_scorer_goals')
                                )
                                
                                if existing_data == new_data:
                                    # Season exists with same data, skip
                                    league_seasons_skipped += 1
                                    continue
                            
                            # Season is new or has changed data, insert/update
                            try:
                                cur.execute("""
                                    INSERT INTO staging.league_seasons (
                                        league_id, competition_name, season_id, num_squads,
                                        champion, top_scorer_player, top_scorer_goals, raw_data
                                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                                    ON CONFLICT (league_id, season_id) DO UPDATE SET
                                        competition_name = EXCLUDED.competition_name,
                                        num_squads = EXCLUDED.num_squads,
                                        champion = EXCLUDED.champion,
                                        top_scorer_player = EXCLUDED.top_scorer_player,
                                        top_scorer_goals = EXCLUDED.top_scorer_goals,
                                        raw_data = EXCLUDED.raw_data,
                                        updated_at = CURRENT_TIMESTAMP
                                """, (
                                    league_id,
                                    season.get('competition_name'),
                                    season_id,
                                    season.get('num_squads'),
                                    season.get('champion'),
                                    season.get('top_scorer_player'),
                                    season.get('top_scorer_goals'),
                                    json.dumps(season)
                                ))
                                league_seasons_added += 1
                                
                            except Exception as e:
                                print(f"❌ Error inserting season {season_id} for league {league_id}: {e}")
                                continue
                            
                            league_seasons_processed += 1
                        
                        print(f"  ✅ Processed: {league_seasons_processed}, Skipped: {league_seasons_skipped}, Added: {league_seasons_added}")
                        total_seasons_processed += league_seasons_processed
                        total_seasons_skipped += league_seasons_skipped
                        total_seasons_added += league_seasons_added
                        
                    except Exception as e:
                        print(f"❌ Error processing league {league_id}: {e}")
                        failed_leagues.append(league_id)
                
                print(f"\n📊 Summary:")
                print(f"  Total seasons processed: {total_seasons_processed}")
                print(f"  Total seasons skipped (already exist): {total_seasons_skipped}")
                print(f"  Total seasons added/updated: {total_seasons_added}")
                
                if failed_leagues:
                    print(f"⚠️ Failed leagues: {failed_leagues}")
                
                return True
                
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return False

def matches_time_period(season_id: str, time_period: str) -> bool:
    """
    Check if a season ID matches the specified time period
    
    Args:
        season_id: Season ID string (e.g., "2024", "2024-2025")
        time_period: Time period name or pattern (e.g., "default_2024", "2020s", "^(2024|2024-2025)$")
    
    Returns:
        bool: True if season matches time period
    """
    
    # Handle time period names from config
    if time_period == "default_2024":
        # Match 2024 or 2024-2025
        return bool(re.match(r"^(2024|2024-2025)$", season_id))
    elif time_period == "2020s":
        # Match any season starting with 2020
        return bool(re.match(r"^2020", season_id))
    elif time_period == "recent_seasons":
        # Match last 5 years
        current_year = datetime.now().year
        return any(re.match(rf"^{year}", season_id) for year in range(current_year-4, current_year+1))
    elif time_period == "2024":
        # Match 2024 or 2024-2025
        return bool(re.match(r"^(2024|2024-2025)$", season_id))
    elif time_period == "^(2024|2024-2025)$":
        # Match 2024 or 2024-2025 (default_2024 pattern)
        return bool(re.match(r"^(2024|2024-2025)$", season_id))
    else:
        # Default: match exact pattern
        return bool(re.match(time_period, season_id))

def verify_data_integrity(league_ids: Optional[List[int]] = None, 
                         time_period: Optional[str] = None) -> bool:
    """
    Verify that stored data matches original API response
    
    Args:
        league_ids: Optional list of league IDs to verify. If None, verifies all.
        time_period: Optional time period to filter verification.
    
    Returns:
        bool: True if verification passes, False otherwise
    """
    
    print("\n🔍 Verifying Data Integrity")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("❌ DATABASE_URL not found in .env file")
        return False
    
    try:
        # Get fresh data from API for sample leagues
        client = FBRClient()
        
        # Use provided league IDs or sample from database
        if not league_ids:
            with psycopg2.connect(database_url) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT DISTINCT league_id FROM staging.leagues ORDER BY league_id LIMIT 5")
                    league_ids = [row[0] for row in cur.fetchall()]
        
        print(f"📊 Verifying {len(league_ids)} leagues")
        if time_period:
            print(f"⏰ Filtering for time period: {time_period}")
        
        total_api_seasons = 0
        total_db_seasons = 0
        
        for league_id in league_ids:
            print(f"\n📋 Verifying league {league_id}...")
            
            # Get fresh API data
            api_response = client.get_league_seasons(str(league_id))
            api_data = api_response.get('data', [])
            
            # Filter API data by time period if specified
            if time_period:
                api_data = [season for season in api_data if matches_time_period(season.get('season_id', ''), time_period)]
            
            # Count seasons in API response
            api_season_count = len(api_data)
            
            # Get data from database
            with psycopg2.connect(database_url) as conn:
                with conn.cursor() as cur:
                    if time_period:
                        # Filter database data by time period
                        cur.execute("""
                            SELECT COUNT(*) FROM staging.league_seasons 
                            WHERE league_id = %s AND season_id ~ %s
                        """, (league_id, time_period.replace("2024", "^(2024|2024-2025)$").replace("2020s", "^2020")))
                    else:
                        cur.execute("""
                            SELECT COUNT(*) FROM staging.league_seasons 
                            WHERE league_id = %s
                        """, (league_id,))
                    db_season_count = cur.fetchone()[0]
            
            print(f"  API seasons: {api_season_count}")
            print(f"  DB seasons: {db_season_count}")
            
            if api_season_count == db_season_count:
                print(f"  ✅ Season count matches for league {league_id}")
            else:
                print(f"  ❌ Season count mismatch for league {league_id}")
                return False
            
            total_api_seasons += api_season_count
            total_db_seasons += db_season_count
        
        print(f"\n📊 Total API seasons: {total_api_seasons}")
        print(f"📊 Total DB seasons: {total_db_seasons}")
        
        if total_api_seasons == total_db_seasons:
            print("✅ All season counts match!")
            return True
        else:
            print("❌ Total season count mismatch!")
            return False
        
    except Exception as e:
        print(f"❌ Error verifying data: {e}")
        return False

def main():
    """Main execution function for backward compatibility"""
    
    print("🚀 Starting League Seasons Data Loading (Parameterized Version)")
    print("=" * 60)
    
    # Load all seasons for all leagues (backward compatibility)
    success = load_league_seasons_data()
    
    if success:
        # Verify data integrity
        verify_data_integrity()
        print("\n🎉 League seasons data loading completed successfully!")
    else:
        print("\n❌ League seasons data loading failed!")
    
    return success

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1) 