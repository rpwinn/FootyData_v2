#!/usr/bin/env python3
"""
Parameterized Team Matches Data Loader
Loads team matches data from /matches endpoint (with team_id)
Uses team IDs extracted from league_matches table

⚠️  DESIGN NOTE: This creates duplicate match data
Each match is recorded twice - once from each team's perspective.
This allows for easy team-centric analysis but doubles storage.
For Premier League: 380 unique matches → 760 team match records per season.
"""

import os
import json
import psycopg2
import re
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from dotenv import load_dotenv

# Import FBR client
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from api.fbr_client import FBRClient
from utils.endpoint_blacklist import load_endpoint_blacklist

def get_database_connection():
    """Get database connection"""
    load_dotenv()
    return psycopg2.connect(os.getenv('DATABASE_URL'))

def get_team_ids_from_league_matches(league_ids: Optional[List[int]] = None, 
                                    season_ids: Optional[List[str]] = None,
                                    time_period: Optional[str] = None) -> List[Tuple[int, str, str]]:
    """
    Extract unique team_id combinations from league_matches table
    
    Returns:
        List of tuples: (league_id, season_id, team_id)
    """
    try:
        conn = get_database_connection()
        cur = conn.cursor()
        
        # Build query to get unique team combinations
        # Only include matches that have already happened + 2 days buffer for data entry
        query = """
            SELECT DISTINCT league_id, season_id, team_id
            FROM (
                SELECT league_id, season_id, home_team_id as team_id
                FROM staging.league_matches 
                WHERE home_team_id IS NOT NULL
                  AND match_date + INTERVAL '2 days' < CURRENT_DATE
                UNION
                SELECT league_id, season_id, away_team_id as team_id
                FROM staging.league_matches 
                WHERE away_team_id IS NOT NULL
                  AND match_date + INTERVAL '2 days' < CURRENT_DATE
            ) team_combinations
            WHERE 1=1
        """
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
            # Filter by time period using the same logic as league matches
            if time_period == "2024":
                # Match 2024 or 2024-2025
                query += " AND season_id ~ '^(2024|2024-2025)$'"
            elif time_period == "default_2024":
                # Match 2024 or 2024-2025 (default 2024 pattern)
                query += " AND season_id ~ '^(2024|2024-2025)$'"
            elif time_period == "2020s":
                # Match the full 2020s pattern
                query += " AND season_id ~ '^(2020|2020-2021|2021|2021-2022|2022|2022-2023|2023|2023-2024|2024|2024-2025|2025|2025-2026)$'"
            elif time_period == "recent_seasons":
                # Match last 5 years
                current_year = datetime.now().year
                patterns = []
                for year in range(current_year-4, current_year+1):
                    patterns.append(f"^{year}")
                pattern = '|'.join(patterns)
                query += f" AND season_id ~ '({pattern})'"
            else:
                # Default: match exact pattern
                query += f" AND season_id ~ '{time_period}'"
        
        query += " ORDER BY league_id, season_id, team_id"
        
        cur.execute(query, params)
        combinations = cur.fetchall()
        cur.close()
        conn.close()
        
        if combinations:
            print(f"✅ Found {len(combinations)} unique team combinations from league_matches")
            return combinations
        else:
            print("⚠️ No team combinations found in league_matches table")
            return []
            
    except Exception as e:
        print(f"⚠️ Error querying team combinations: {e}")
        return []

def insert_team_matches_data(data: Dict[str, Any], league_id: int, season_id: str, team_id: str) -> bool:
    """Insert team matches data into staging table"""
    try:
        conn = get_database_connection()
        cur = conn.cursor()
        
        matches_data = data.get('data', [])
        
        # Check for existing matches to avoid duplicates
        existing_match_ids = set()
        cur.execute(
            "SELECT match_id FROM staging.team_matches WHERE league_id = %s AND season_id = %s AND team_id = %s",
            (league_id, season_id, team_id)
        )
        for row in cur.fetchall():
            if row[0]:  # Only add non-null match_ids
                existing_match_ids.add(row[0])
        
        if existing_match_ids:
            print(f"   ℹ️  Found {len(existing_match_ids)} existing matches, will skip duplicates")
        
        inserted_count = 0
        skipped_count = 0
        
        for match in matches_data:
            # Skip matches without match_id
            if not match.get('match_id'):
                print(f"   ⏭️  Skipping match without match_id: {match.get('opponent', 'Unknown')}")
                continue
            
            # Skip matches that already exist in database
            if match.get('match_id') in existing_match_ids:
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
                'team_id': team_id,
                'match_date': match_date,
                'match_time': match_time,
                'round': match.get('round'),
                'home_away': match.get('home_away'),
                'opponent': match.get('opponent'),
                'opponent_id': match.get('opponent_id'),
                'result': match.get('result'),
                'goals_for': safe_int(match.get('gf')),
                'goals_against': safe_int(match.get('ga')),
                'formation': match.get('formation'),
                'captain': match.get('captain'),
                'attendance': match.get('attendance'),
                'referee': match.get('referee'),
                'raw_data': json.dumps(match)
            }
            
            # Insert with upsert - handle both matches with IDs and future matches
            if match.get('match_id'):
                # Match has ID - use the match_id unique constraint
                cur.execute("""
                    INSERT INTO staging.team_matches (
                        match_id, league_id, season_id, team_id, match_date, match_time, round,
                        home_away, opponent, opponent_id, result, goals_for, goals_against,
                        formation, captain, attendance, referee, raw_data
                    ) VALUES (
                        %(match_id)s, %(league_id)s, %(season_id)s, %(team_id)s, %(match_date)s, %(match_time)s, 
                        %(round)s, %(home_away)s, %(opponent)s, %(opponent_id)s, %(result)s, %(goals_for)s, %(goals_against)s,
                        %(formation)s, %(captain)s, %(attendance)s, %(referee)s, %(raw_data)s
                    ) ON CONFLICT ON CONSTRAINT uk_team_matches_match_id
                    DO UPDATE SET
                        match_date = EXCLUDED.match_date,
                        match_time = EXCLUDED.match_time,
                        round = EXCLUDED.round,
                        home_away = EXCLUDED.home_away,
                        opponent = EXCLUDED.opponent,
                        opponent_id = EXCLUDED.opponent_id,
                        result = EXCLUDED.result,
                        goals_for = EXCLUDED.goals_for,
                        goals_against = EXCLUDED.goals_against,
                        formation = EXCLUDED.formation,
                        captain = EXCLUDED.captain,
                        attendance = EXCLUDED.attendance,
                        referee = EXCLUDED.referee,
                        raw_data = EXCLUDED.raw_data,
                        updated_at = CURRENT_TIMESTAMP
                """, insert_data)
            else:
                # Future match without ID - use the future match unique constraint
                cur.execute("""
                    INSERT INTO staging.team_matches (
                        match_id, league_id, season_id, team_id, match_date, match_time, round,
                        home_away, opponent, opponent_id, result, goals_for, goals_against,
                        formation, captain, attendance, referee, raw_data
                    ) VALUES (
                        %(match_id)s, %(league_id)s, %(season_id)s, %(team_id)s, %(match_date)s, %(match_time)s, 
                        %(round)s, %(home_away)s, %(opponent)s, %(opponent_id)s, %(result)s, %(goals_for)s, %(goals_against)s,
                        %(formation)s, %(captain)s, %(attendance)s, %(referee)s, %(raw_data)s
                    ) ON CONFLICT ON CONSTRAINT uk_team_matches_future
                    DO UPDATE SET
                        match_time = EXCLUDED.match_time,
                        round = EXCLUDED.round,
                        home_away = EXCLUDED.home_away,
                        opponent_id = EXCLUDED.opponent_id,
                        result = EXCLUDED.result,
                        goals_for = EXCLUDED.goals_for,
                        goals_against = EXCLUDED.goals_against,
                        formation = EXCLUDED.formation,
                        captain = EXCLUDED.captain,
                        attendance = EXCLUDED.attendance,
                        referee = EXCLUDED.referee,
                        raw_data = EXCLUDED.raw_data,
                        updated_at = CURRENT_TIMESTAMP
                """, insert_data)
            
            inserted_count += 1
        
        conn.commit()
        cur.close()
        conn.close()
        
        print(f"✅ Inserted {inserted_count} team matches for league {league_id}, season {season_id}, team {team_id}")
        if skipped_count > 0:
            print(f"   ⏭️  Skipped {skipped_count} existing matches")
        return True
        
    except Exception as e:
        print(f"❌ Error inserting team matches data: {e}")
        return False

def load_team_matches_data(league_ids: Optional[List[int]] = None, 
                          season_ids: Optional[List[str]] = None,
                          time_period: Optional[str] = None,
                          update_only: bool = False) -> bool:
    """
    Load team matches data from API using team IDs from league_matches table
    
    ⚠️  IMPORTANT: This creates duplicate match data
    Each match is recorded twice - once from each team's perspective.
    For example, Arsenal vs Chelsea creates two records:
    - Arsenal's perspective (home team)
    - Chelsea's perspective (away team)
    
    This design allows for easy team-centric analysis but doubles storage.
    For Premier League: 380 unique matches → 760 team match records per season.
    
    Args:
        league_ids: List of league IDs to collect (None = all available)
        season_ids: List of season IDs to collect (None = all available)
        time_period: Time period filter (e.g., "2024", "2020s")
        update_only: If True, only update existing records
    
    Returns:
        bool: True if successful, False otherwise
    """
    print("🏆 Loading Team Matches Data")
    print("=" * 50)
    
    # Check blacklist
    blacklist = load_endpoint_blacklist()
    if blacklist.is_blacklisted("matches"):
        print("❌ Matches endpoint is blacklisted, skipping collection")
        return False
    
    # Get team combinations from league_matches table
    team_combinations = get_team_ids_from_league_matches(league_ids, season_ids, time_period)
    
    if not team_combinations:
        print("❌ No team combinations found")
        return False
    
    # Initialize FBR client
    client = FBRClient()
    
    # Collect data for each combination
    total_matches = 0
    successful_combinations = 0
    data_available_combinations = 0
    
    for league_id, season_id, team_id in team_combinations:
        print(f"\n📊 Processing League {league_id}, Season {season_id}, Team {team_id}...")
        
        try:
            # Check if we already have data for this combination
            try:
                conn = get_database_connection()
                cur = conn.cursor()
                cur.execute("""
                    SELECT COUNT(*) FROM staging.team_matches 
                    WHERE league_id = %s AND season_id = %s AND team_id = %s
                """, (league_id, season_id, team_id))
                existing_count = cur.fetchone()[0]
                cur.close()
                conn.close()
                
                if existing_count > 0:
                    print(f"   ℹ️  Found {existing_count} existing matches, skipping API call")
                    data_available_combinations += 1
                    continue
            except Exception as e:
                print(f"   ⚠️  Error checking existing data: {e}")
            
            # Make API call with team_id
            response = client.get_matches(str(league_id), season_id, team_id)
            
            if 'error' in response:
                print(f"   ❌ API Error: {response['error']}")
                continue
            
            # Insert data
            if insert_team_matches_data(response, league_id, season_id, team_id):
                match_count = len(response.get('data', []))
                total_matches += match_count
                successful_combinations += 1
                data_available_combinations += 1
                print(f"   ✅ Successfully processed {match_count} matches")
            else:
                print(f"   ❌ Failed to insert team matches data")
                
        except Exception as e:
            print(f"   ❌ Error processing league {league_id}, season {season_id}, team {team_id}: {e}")
    
    # Summary
    print(f"\n📊 Collection Summary:")
    print(f"   - Successful combinations: {successful_combinations}/{len(team_combinations)}")
    print(f"   - Data available combinations: {data_available_combinations}/{len(team_combinations)}")
    print(f"   - Total matches collected: {total_matches}")
    
    # Return True if we have data for any combination (either existing or newly collected)
    if data_available_combinations > 0:
        print("✅ Team matches data collection completed successfully!")
        return True
    else:
        print("❌ No team matches data was collected")
        return False

if __name__ == "__main__":
    # Test the function
    success = load_team_matches_data()
    if success:
        print("\n🎉 Test completed successfully!")
    else:
        print("\n❌ Test failed!") 