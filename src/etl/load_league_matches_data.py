#!/usr/bin/env python3
"""
Parameterized League Matches Data Loader
Loads league matches data from /matches endpoint (without team_id)
"""

import os
import json
import psycopg2
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from dotenv import load_dotenv

# Import FBR client
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from api.fbr_client import FBRClient
from utils.endpoint_blacklist import load_endpoint_blacklist

def get_league_season_combinations(league_ids: Optional[List[int]] = None, 
                                 season_ids: Optional[List[str]] = None,
                                 time_period: Optional[str] = None) -> List[Tuple[int, str]]:
    """Get league-season combinations from database or use fallbacks"""
    try:
        load_dotenv()
        conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        cur = conn.cursor()
        
        # Build query based on provided filters
        query = """
            SELECT DISTINCT l.league_id, ls.season_id 
            FROM staging.league_seasons ls
            JOIN staging.leagues l ON ls.competition_name = l.competition_name
            WHERE 1=1
        """
        params = []
        
        if league_ids:
            placeholders = ','.join(['%s'] * len(league_ids))
            query += f" AND l.league_id IN ({placeholders})"
            params.extend(league_ids)
        
        if season_ids:
            placeholders = ','.join(['%s'] * len(season_ids))
            query += f" AND ls.season_id IN ({placeholders})"
            params.extend(season_ids)
        
        if time_period:
            # Filter by time period using the same logic as other scripts
            if time_period == "2024":
                # Match 2024 or 2024-2025
                query += " AND ls.season_id ~ '^(2024|2024-2025)$'"
            elif time_period == "default_2024":
                # Match 2024 or 2024-2025 (default 2024 pattern)
                query += " AND ls.season_id ~ '^(2024|2024-2025)$'"
            elif time_period == "2020s":
                # Match the full 2020s pattern
                query += " AND ls.season_id ~ '^(2020|2020-2021|2021|2021-2022|2022|2022-2023|2023|2023-2024|2024|2024-2025|2025|2025-2026)$'"
            elif time_period == "recent_seasons":
                # Match last 5 years
                current_year = datetime.now().year
                patterns = []
                for year in range(current_year-4, current_year+1):
                    patterns.append(f"^{year}")
                pattern = '|'.join(patterns)
                query += f" AND ls.season_id ~ '({pattern})'"
            else:
                # Default: match exact pattern
                query += f" AND ls.season_id ~ '{time_period}'"
        
        query += " ORDER BY l.league_id, ls.season_id"
        
        cur.execute(query, params)
        combinations = cur.fetchall()
        cur.close()
        conn.close()
        
        if combinations:
            print(f"✅ Found {len(combinations)} league-season combinations from database")
            return combinations
        else:
            print("⚠️ No league-season combinations found in database, using fallback")
            return [(9, "2023-2024"), (8, "2023-2024"), (1, "2022")]
            
    except Exception as e:
        print(f"⚠️ Error querying database: {e}, using fallback combinations")
        return [(9, "2023-2024"), (8, "2023-2024"), (1, "2022")]

def insert_league_matches_data(data: Dict[str, Any], league_id: int, season_id: str) -> bool:
    """Insert league matches data into staging table"""
    try:
        load_dotenv()
        conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        cur = conn.cursor()
        
        matches_data = data.get('data', [])
        
        # Check for existing matches to avoid duplicates
        existing_match_ids = set()
        cur.execute(
            "SELECT match_id FROM staging.league_matches WHERE league_id = %s AND season_id = %s",
            (league_id, season_id)
        )
        for row in cur.fetchall():
            if row[0]:  # Only add non-null match_ids
                existing_match_ids.add(row[0])
        
        if existing_match_ids:
            print(f"   ℹ️  Found {len(existing_match_ids)} existing matches, will skip duplicates")
        
        inserted_count = 0
        skipped_count = 0
        
        for match in matches_data:
            # Store matches with or without match_id (including future fixtures)
            match_id = match.get('match_id')
            
            # Skip matches that already exist in database (only for matches with IDs)
            if match_id and match_id in existing_match_ids:
                skipped_count += 1
                continue
            
            # Handle empty strings and convert to proper types
            def safe_int(value):
                if value == "" or value is None:
                    return None
                try:
                    return int(value)
                except (ValueError, TypeError):
                    return None
            
            # Convert date string to date object
            match_date = None
            if match.get('date'):
                try:
                    match_date = datetime.strptime(match['date'], '%Y-%m-%d').date()
                except ValueError:
                    match_date = None
            
            # Convert time string to time object
            match_time = None
            if match.get('time'):
                try:
                    match_time = datetime.strptime(match['time'], '%H:%M').time()
                except ValueError:
                    match_time = None
            
            insert_data = {
                'match_id': match.get('match_id'),
                'league_id': league_id,
                'season_id': season_id,
                'match_date': match_date,
                'match_time': match_time,
                'round': match.get('round'),
                'wk': match.get('wk'),
                'home_team': match.get('home'),
                'home_team_id': match.get('home_team_id'),
                'away_team': match.get('away'),
                'away_team_id': match.get('away_team_id'),
                'home_team_score': safe_int(match.get('home_team_score')),
                'away_team_score': safe_int(match.get('away_team_score')),
                'venue': match.get('venue'),
                'attendance': match.get('attendance'),
                'referee': match.get('referee'),
                'raw_data': json.dumps(match)
            }
            
            # Insert with upsert - handle both matches with IDs and future matches
            if match_id:
                # Match has ID - use the match_id unique constraint
                cur.execute("""
                    INSERT INTO staging.league_matches (
                        match_id, league_id, season_id, match_date, match_time, round, wk,
                        home_team, home_team_id, away_team, away_team_id,
                        home_team_score, away_team_score, venue, attendance, referee, raw_data
                    ) VALUES (
                        %(match_id)s, %(league_id)s, %(season_id)s, %(match_date)s, %(match_time)s, 
                        %(round)s, %(wk)s, %(home_team)s, %(home_team_id)s, %(away_team)s, %(away_team_id)s,
                        %(home_team_score)s, %(away_team_score)s, %(venue)s, %(attendance)s, %(referee)s, %(raw_data)s
                    ) ON CONFLICT ON CONSTRAINT uk_league_matches_match_id
                    DO UPDATE SET
                        match_date = EXCLUDED.match_date,
                        match_time = EXCLUDED.match_time,
                        round = EXCLUDED.round,
                        wk = EXCLUDED.wk,
                        home_team = EXCLUDED.home_team,
                        home_team_id = EXCLUDED.home_team_id,
                        away_team = EXCLUDED.away_team,
                        away_team_id = EXCLUDED.away_team_id,
                        home_team_score = EXCLUDED.home_team_score,
                        away_team_score = EXCLUDED.away_team_score,
                        venue = EXCLUDED.venue,
                        attendance = EXCLUDED.attendance,
                        referee = EXCLUDED.referee,
                        raw_data = EXCLUDED.raw_data,
                        updated_at = CURRENT_TIMESTAMP
                """, insert_data)
            else:
                # Future match without ID - use the future match unique constraint
                cur.execute("""
                    INSERT INTO staging.league_matches (
                        match_id, league_id, season_id, match_date, match_time, round, wk,
                        home_team, home_team_id, away_team, away_team_id,
                        home_team_score, away_team_score, venue, attendance, referee, raw_data
                    ) VALUES (
                        %(match_id)s, %(league_id)s, %(season_id)s, %(match_date)s, %(match_time)s, 
                        %(round)s, %(wk)s, %(home_team)s, %(home_team_id)s, %(away_team)s, %(away_team_id)s,
                        %(home_team_score)s, %(away_team_score)s, %(venue)s, %(attendance)s, %(referee)s, %(raw_data)s
                    ) ON CONFLICT ON CONSTRAINT uk_league_matches_future
                    DO UPDATE SET
                        match_time = EXCLUDED.match_time,
                        round = EXCLUDED.round,
                        wk = EXCLUDED.wk,
                        home_team_id = EXCLUDED.home_team_id,
                        away_team_id = EXCLUDED.away_team_id,
                        venue = EXCLUDED.venue,
                        attendance = EXCLUDED.attendance,
                        referee = EXCLUDED.referee,
                        raw_data = EXCLUDED.raw_data,
                        updated_at = CURRENT_TIMESTAMP
                """, insert_data)
            
            inserted_count += 1
        
        conn.commit()
        cur.close()
        conn.close()
        
        print(f"✅ Inserted {inserted_count} league matches for league {league_id}, season {season_id}")
        if skipped_count > 0:
            print(f"   ⏭️  Skipped {skipped_count} existing matches")
        return True
        
    except Exception as e:
        print(f"❌ Error inserting league matches data: {e}")
        return False

def load_league_matches_data(league_ids: Optional[List[int]] = None, 
                           season_ids: Optional[List[str]] = None,
                           time_period: Optional[str] = None,
                           update_only: bool = False) -> bool:
    """
    Load league matches data from API
    
    Args:
        league_ids: List of league IDs to collect (None = all available)
        season_ids: List of season IDs to collect (None = all available)
        time_period: Time period filter (e.g., "2024", "2020s")
        update_only: If True, only update existing records
    
    Returns:
        bool: True if successful, False otherwise
    """
    print("🏆 Loading League Matches Data")
    print("=" * 50)
    
    # Check blacklist
    blacklist = load_endpoint_blacklist()
    if blacklist.is_blacklisted("matches"):
        print("❌ Matches endpoint is blacklisted, skipping collection")
        return False
    
    # Get league-season combinations
    combinations = get_league_season_combinations(league_ids, season_ids, time_period)
    
    if not combinations:
        print("❌ No league-season combinations found")
        return False
    
    # Initialize FBR client
    client = FBRClient()
    
    # Collect data for each combination
    total_matches = 0
    successful_combinations = 0
    data_available_combinations = 0
    
    for league_id, season_id in combinations:
        print(f"\n📊 Processing League {league_id}, Season {season_id}...")
        
        try:
            # Check if we already have data for this combination
            try:
                load_dotenv()
                conn = psycopg2.connect(os.getenv('DATABASE_URL'))
                cur = conn.cursor()
                cur.execute("""
                    SELECT COUNT(*) FROM staging.league_matches 
                    WHERE league_id = %s AND season_id = %s
                """, (league_id, season_id))
                existing_count = cur.fetchone()[0]
                cur.close()
                conn.close()
                
                if existing_count > 0:
                    print(f"   ℹ️  Found {existing_count} existing matches, skipping API call")
                    data_available_combinations += 1
                    continue
            except Exception as e:
                print(f"   ⚠️  Error checking existing data: {e}")
            
            # Make API call
            response = client.get_matches(str(league_id), season_id)
            
            if 'error' in response:
                print(f"   ❌ API Error: {response['error']}")
                continue
            
            # Insert data
            if insert_league_matches_data(response, league_id, season_id):
                match_count = len(response.get('data', []))
                total_matches += match_count
                successful_combinations += 1
                data_available_combinations += 1
                print(f"   ✅ Successfully processed {match_count} matches")
            else:
                print(f"   ❌ Failed to insert league matches data")
                
        except Exception as e:
            print(f"   ❌ Error processing league {league_id}, season {season_id}: {e}")
    
    # Summary
    print(f"\n📊 Collection Summary:")
    print(f"   - Successful combinations: {successful_combinations}/{len(combinations)}")
    print(f"   - Data available combinations: {data_available_combinations}/{len(combinations)}")
    print(f"   - Total matches collected: {total_matches}")
    
    # Return True if we have data for any combination (either existing or newly collected)
    if data_available_combinations > 0:
        print("✅ League matches data collection completed successfully!")
        return True
    else:
        print("❌ No league matches data was collected")
        return False

if __name__ == "__main__":
    # Test the function
    success = load_league_matches_data()
    if success:
        print("\n🎉 Test completed successfully!")
    else:
        print("\n❌ Test failed!") 