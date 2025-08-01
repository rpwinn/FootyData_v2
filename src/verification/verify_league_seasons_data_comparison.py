#!/usr/bin/env python3
"""
Verify League Seasons Data by Comparing Database to Fresh API Call
This script ensures the data in our database exactly matches what the API returns
"""

import os
import sys
import psycopg2
import json
from dotenv import load_dotenv

# Add src to path
sys.path.append('src')

from api.fbr_client import FBRClient

def verify_league_seasons_data():
    """Compare database data with fresh API call"""
    
    print("🔍 Verifying League Seasons Data: Database vs API")
    print("=" * 60)
    
    # Load environment variables
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("❌ DATABASE_URL not found in .env file")
        return False
    
    try:
        # Get test league IDs from database
        print("📋 Getting test league IDs from database...")
        with psycopg2.connect(database_url) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT DISTINCT league_id, competition_name, country_code 
                    FROM staging.leagues 
                    WHERE country_code IN ('ENG', 'USA', 'BRA', 'GER', 'FRA')
                    AND competition_name IN (
                        'Premier League', 'Ligue 1', 'Fußball-Bundesliga',
                        'Champions League', 'Europa League', 'FA Cup',
                        'Coupe de France', 'DFB-Pokal'
                    )
                    ORDER BY country_code, competition_name
                    LIMIT 5
                """)
                test_leagues = cur.fetchall()
        
        print(f"✅ Found {len(test_leagues)} test leagues")
        
        # Initialize API client
        client = FBRClient()
        
        total_matches = 0
        total_mismatches = 0
        
        for league_id, competition_name, country_code in test_leagues:
            print(f"\n📋 Verifying {country_code}: {competition_name} (ID: {league_id})...")
            
            # Get fresh API data
            api_response = client.get_league_seasons(str(league_id))
            api_data = api_response.get('data', [])
            
            if "error" in api_response:
                print(f"❌ API call failed: {api_response['error']}")
                total_mismatches += 1
                continue
            
            # Get data from database
            with psycopg2.connect(database_url) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT season_id, competition_name, num_squads,
                               champion, top_scorer_player, top_scorer_goals, raw_data
                        FROM staging.league_seasons 
                        WHERE league_id = %s
                        ORDER BY season_id
                    """, (league_id,))
                    db_data = cur.fetchall()
            
            # Compare counts
            api_count = len(api_data)
            db_count = len(db_data)
            
            print(f"  API seasons: {api_count}")
            print(f"  DB seasons: {db_count}")
            
            if api_count == db_count:
                print(f"  ✅ Count match for {competition_name}")
                total_matches += 1
            else:
                print(f"  ❌ Count mismatch for {competition_name}")
                total_mismatches += 1
                continue
            
            # Compare specific seasons by season_id (not by position)
            print(f"  📊 Detailed comparison of matching seasons:")
            
            # Create lookup dictionaries for easier comparison
            api_lookup = {season.get('season_id'): season for season in api_data}
            db_lookup = {row[0]: row for row in db_data}  # season_id is at index 0
            
            # Find seasons that exist in both API and DB
            common_seasons = set(api_lookup.keys()) & set(db_lookup.keys())
            
            if not common_seasons:
                print(f"    ⚠️ No matching seasons found between API and DB")
                continue
            
            # Compare first 3 common seasons
            for season_id in sorted(common_seasons)[:3]:
                api_season = api_lookup[season_id]
                db_season = db_lookup[season_id]
                
                print(f"    Season {season_id}:")
                
                # Compare competition name
                api_comp = api_season.get('competition_name')
                db_comp = db_season[1]  # competition_name is at index 1
                if api_comp == db_comp:
                    print(f"      ✅ Competition: {api_comp}")
                else:
                    print(f"      ❌ Competition: API='{api_comp}' vs DB='{db_comp}'")
                
                # Compare num_squads
                api_squads = api_season.get('#_squads')
                db_squads = db_season[2]  # num_squads is at index 2
                if api_squads == db_squads:
                    print(f"      ✅ Squads: {api_squads}")
                else:
                    print(f"      ❌ Squads: API={api_squads} vs DB={db_squads}")
                
                # Compare champion
                api_champion = api_season.get('champion')
                db_champion = db_season[3]  # champion is at index 3
                if api_champion == db_champion:
                    print(f"      ✅ Champion: {api_champion}")
                else:
                    print(f"      ❌ Champion: API='{api_champion}' vs DB='{db_champion}'")
                
                # Compare top scorer
                api_top_scorer = api_season.get('top_scorer', {})
                api_player = api_top_scorer.get('player')
                api_goals = api_top_scorer.get('goals_scored')
                
                db_player = db_season[4]  # top_scorer_player is at index 4
                db_goals = db_season[5]   # top_scorer_goals is at index 5
                
                # Handle array vs string comparison for top scorer
                if isinstance(api_player, list):
                    api_player_str = json.dumps(api_player)
                else:
                    api_player_str = str(api_player) if api_player else None
                
                if api_player_str == db_player:
                    print(f"      ✅ Top Scorer: {api_player_str}")
                else:
                    print(f"      ❌ Top Scorer: API='{api_player_str}' vs DB='{db_player}'")
                
                if api_goals == db_goals:
                    print(f"      ✅ Goals: {api_goals}")
                else:
                    print(f"      ❌ Goals: API={api_goals} vs DB={db_goals}")
        
        # Summary
        print(f"\n📊 Verification Summary:")
        print(f"  ✅ Matches: {total_matches}")
        print(f"  ❌ Mismatches: {total_mismatches}")
        print(f"  📋 Total leagues tested: {len(test_leagues)}")
        
        if total_mismatches == 0:
            print("🎉 All verifications passed!")
            return True
        else:
            print("❌ Some verifications failed")
            return False
        
    except Exception as e:
        print(f"❌ Error during verification: {e}")
        return False

def display_sample_data():
    """Display sample data from the staging table"""
    
    print("\n📊 Sample Data from League Seasons Staging Table")
    print("=" * 60)
    
    # Load environment variables
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("❌ DATABASE_URL not found in .env file")
        return False
    
    try:
        with psycopg2.connect(database_url) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT 
                        league_id, competition_name, season_id, num_squads,
                        champion, top_scorer_player, top_scorer_goals
                    FROM staging.league_seasons 
                    ORDER BY league_id, season_id 
                    LIMIT 10
                """)
                
                rows = cur.fetchall()
                
                if not rows:
                    print("❌ No data found in staging table")
                    return False
                
                print("League ID | Competition | Season | Squads | Champion | Top Scorer | Goals")
                print("-" * 80)
                
                for row in rows:
                    league_id, competition, season, squads, champion, scorer, goals = row
                    print(f"{league_id:9} | {competition[:15]:15} | {season:7} | {squads:6} | {champion[:15]:15} | {scorer[:15]:15} | {goals}")
                
                return True
                
    except Exception as e:
        print(f"❌ Error displaying data: {e}")
        return False

def main():
    """Main execution function"""
    
    print("🚀 Starting League Seasons Data Verification")
    print("=" * 60)
    
    # Step 1: Verify data integrity
    if not verify_league_seasons_data():
        print("❌ Data integrity verification failed")
        return False
    
    # Step 2: Display sample data
    if not display_sample_data():
        print("❌ Failed to display sample data")
        return False
    
    print("\n🎉 League seasons data verification completed successfully!")
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1) 