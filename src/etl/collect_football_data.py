#!/usr/bin/env python3
"""
Master Football Data Collection Orchestrator
Integrates all parameterized scripts for cascading data collection
"""

import os
import sys
import argparse
import psycopg2
import json
from datetime import datetime
from typing import List, Optional, Dict, Any, Tuple
from dotenv import load_dotenv

# Add src to path
sys.path.append('src')

from api.fbr_client import FBRClient
from utils.collection_config import load_collection_config
from etl.load_countries_data import load_countries_data
from etl.load_leagues_data import load_leagues_data
from etl.load_league_seasons_data import load_league_seasons_data

class FootballDataCollector:
    """Master orchestrator for football data collection"""
    
    def __init__(self, dry_run: bool = False, verbose: bool = False):
        """Initialize the collector"""
        load_dotenv()
        self.database_url = os.getenv("DATABASE_URL")
        self.client = FBRClient()
        self.dry_run = dry_run
        self.verbose = verbose
        
        if not self.database_url:
            raise ValueError("DATABASE_URL not found in .env file")
    
    def log(self, message: str, level: str = "INFO"):
        """Log messages with level and dry run indication"""
        prefix = "[DRY RUN] " if self.dry_run else ""
        print(f"{prefix}{level}: {message}")
    
    def check_countries_freshness(self, country_codes: List[str]) -> Tuple[bool, List[str]]:
        """Check if countries data is fresh"""
        self.log("Checking countries freshness...")
        
        try:
            with psycopg2.connect(self.database_url) as conn:
                with conn.cursor() as cur:
                    placeholders = ','.join(['%s'] * len(country_codes))
                    cur.execute(f"""
                        SELECT country_code FROM staging.countries 
                        WHERE country_code IN ({placeholders})
                    """, country_codes)
                    
                    existing_countries = {row[0] for row in cur.fetchall()}
                    missing_countries = [code for code in country_codes if code not in existing_countries]
                    
                    if missing_countries:
                        self.log(f"Missing countries: {missing_countries}", "WARN")
                        return False, missing_countries
                    else:
                        self.log(f"All {len(country_codes)} countries exist in database", "INFO")
                        return True, []
                        
        except Exception as e:
            self.log(f"Error checking countries: {e}", "ERROR")
            return False, country_codes
    
    def check_leagues_freshness(self, country_codes: List[str]) -> Tuple[bool, List[Dict]]:
        """Check if leagues data is fresh by comparing last_season field"""
        self.log("Checking leagues freshness...")
        
        try:
            with psycopg2.connect(self.database_url) as conn:
                with conn.cursor() as cur:
                    placeholders = ','.join(['%s'] * len(country_codes))
                    cur.execute(f"""
                        SELECT league_id, country_code, competition_name, last_season
                        FROM staging.leagues 
                        WHERE country_code IN ({placeholders})
                    """, country_codes)
                    
                    db_leagues = {row[0]: (row[1], row[2], row[3]) for row in cur.fetchall()}
                    leagues_needing_update = []
                    
                    for country_code in country_codes:
                        if self.verbose:
                            self.log(f"Checking {country_code} leagues...")
                        
                        try:
                            api_response = self.client.get_leagues(country_code)
                            
                            if "error" in api_response:
                                self.log(f"API call failed for {country_code}: {api_response['error']}", "ERROR")
                                continue
                            
                            api_data = api_response.get('data', [])
                            
                            for league_type_obj in api_data:
                                leagues = league_type_obj.get('leagues', [])
                                
                                for league in leagues:
                                    league_id = league.get('league_id')
                                    api_last_season = league.get('last_season')
                                    
                                    if league_id in db_leagues:
                                        db_last_season = db_leagues[league_id][2]
                                        
                                        if db_last_season != api_last_season:
                                            if self.verbose:
                                                self.log(f"League {league_id} ({league.get('competition_name')}) needs update", "WARN")
                                            leagues_needing_update.append({
                                                'league_id': league_id,
                                                'country_code': country_code,
                                                'competition_name': league.get('competition_name'),
                                                'db_last_season': db_last_season,
                                                'api_last_season': api_last_season
                                            })
                                    else:
                                        if self.verbose:
                                            self.log(f"New league found: {league.get('competition_name')} (ID: {league_id})", "INFO")
                                        leagues_needing_update.append({
                                            'league_id': league_id,
                                            'country_code': country_code,
                                            'competition_name': league.get('competition_name'),
                                            'db_last_season': None,
                                            'api_last_season': api_last_season
                                        })
                        
                        except Exception as e:
                            self.log(f"Error checking {country_code}: {e}", "ERROR")
                    
                    if leagues_needing_update:
                        self.log(f"{len(leagues_needing_update)} leagues need update", "WARN")
                        return False, leagues_needing_update
                    else:
                        self.log("All leagues are fresh", "INFO")
                        return True, []
                        
        except Exception as e:
            self.log(f"Error checking leagues: {e}", "ERROR")
            return False, []
    
    def check_league_seasons_freshness(self, league_ids: List[int], time_period: Optional[str] = None) -> Tuple[bool, List[int]]:
        """Check if league seasons data is fresh for the specified time period"""
        self.log("Checking league seasons freshness...")
        
        if not time_period:
            self.log("No time period specified, assuming fresh", "INFO")
            return True, []
        
        try:
            with psycopg2.connect(self.database_url) as conn:
                with conn.cursor() as cur:
                    # Get existing seasons for these leagues
                    placeholders = ','.join(['%s'] * len(league_ids))
                    cur.execute(f"""
                        SELECT league_id, season_id 
                        FROM staging.league_seasons 
                        WHERE league_id IN ({placeholders})
                    """, league_ids)
                    
                    existing_seasons = {}
                    for row in cur.fetchall():
                        league_id, season_id = row
                        if league_id not in existing_seasons:
                            existing_seasons[league_id] = set()
                        existing_seasons[league_id].add(season_id)
                    
                    # Check what seasons we should have for the time period
                    config = load_collection_config()
                    time_period_config = config.get_time_period(time_period)
                    
                    if not time_period_config:
                        self.log(f"Time period '{time_period}' not found, assuming fresh", "WARN")
                        return True, []
                    
                    # Get expected seasons for this time period
                    expected_seasons = self._get_expected_seasons_for_time_period(time_period_config)
                    
                    if self.verbose:
                        self.log(f"Expected seasons for time period '{time_period}': {sorted(expected_seasons)}", "INFO")
                    
                    leagues_needing_seasons = []
                    
                    for league_id in league_ids:
                        if league_id not in existing_seasons:
                            # No seasons at all for this league
                            if self.verbose:
                                self.log(f"League {league_id}: No seasons found in database", "WARN")
                            leagues_needing_seasons.append(league_id)
                            continue
                        
                        # Check if we have all expected seasons
                        missing_seasons = expected_seasons - existing_seasons[league_id]
                        existing_count = len(existing_seasons[league_id])
                        expected_count = len(expected_seasons)
                        
                        if self.verbose:
                            self.log(f"League {league_id}: {existing_count} existing seasons, {expected_count} expected seasons", "INFO")
                            if missing_seasons:
                                self.log(f"League {league_id} missing seasons: {sorted(missing_seasons)}", "WARN")
                            else:
                                self.log(f"League {league_id}: All expected seasons present", "INFO")
                        
                        if missing_seasons:
                            leagues_needing_seasons.append(league_id)
                    
                    if leagues_needing_seasons:
                        self.log(f"{len(leagues_needing_seasons)} leagues need season updates", "WARN")
                        return False, leagues_needing_seasons
                    else:
                        self.log("All league seasons are fresh for time period", "INFO")
                        return True, []
                        
        except Exception as e:
            self.log(f"Error checking league seasons: {e}", "ERROR")
            return False, league_ids
    
    def _get_expected_seasons_for_time_period(self, time_period_config) -> set:
        """Get expected seasons for a time period configuration"""
        import re
        
        pattern = time_period_config.pattern
        expected_seasons = set()
        
        # For 2020s, generate all seasons from 2020 onwards
        if pattern == "2020|2020-2021|2021|2021-2022|2022|2022-2023|2023|2023-2024|2024|2024-2025|2025|2025-2026":
            for year in range(2020, 2027):
                expected_seasons.add(str(year))
                expected_seasons.add(f"{year}-{year+1}")
        # For default_2024, just 2024 and 2024-2025
        elif pattern == "^(2024|2024-2025)$":
            expected_seasons.add("2024")
            expected_seasons.add("2024-2025")
        else:
            # For other patterns, try to parse them
            seasons = pattern.split("|")
            for season in seasons:
                season = season.strip()
                if season:
                    expected_seasons.add(season)
        
        return expected_seasons
    
    def collect_countries(self, country_codes: List[str]) -> bool:
        """Collect countries data"""
        self.log(f"Collecting countries data for {len(country_codes)} countries...")
        
        if self.dry_run:
            self.log("DRY RUN: Would collect countries data", "INFO")
            return True
        
        try:
            self.log(f"Calling load_countries_data with country_codes: {country_codes}", "DEBUG")
            success = load_countries_data(country_codes=country_codes)
            self.log(f"load_countries_data returned: {success}", "DEBUG")
            if success:
                self.log("Countries data collection completed", "INFO")
            else:
                self.log("Countries data collection failed", "ERROR")
            return success
        except Exception as e:
            self.log(f"Error collecting countries: {e}", "ERROR")
            return False
    
    def collect_leagues(self, country_codes: List[str]) -> bool:
        """Collect leagues data"""
        self.log(f"Collecting leagues data for {len(country_codes)} countries...")
        
        if self.dry_run:
            self.log("DRY RUN: Would collect leagues data", "INFO")
            return True
        
        try:
            success = load_leagues_data(country_codes=country_codes)
            if success:
                self.log("Leagues data collection completed", "INFO")
            else:
                self.log("Leagues data collection failed", "ERROR")
            return success
        except Exception as e:
            self.log(f"Error collecting leagues: {e}", "ERROR")
            return False
    
    def collect_league_seasons(self, league_ids: List[int], time_period: Optional[str] = None) -> bool:
        """Collect league seasons data"""
        self.log(f"Collecting league seasons data for {len(league_ids)} leagues...")
        if time_period:
            self.log(f"Filtering for time period: {time_period}")
        
        if self.dry_run:
            self.log("DRY RUN: Would collect league seasons data", "INFO")
            return True
        
        try:
            self.log(f"Calling load_league_seasons_data with league_ids: {league_ids[:5]}... (showing first 5)", "DEBUG")
            self.log(f"Calling load_league_seasons_data with time_period: {time_period}", "DEBUG")
            success = load_league_seasons_data(
                league_ids=league_ids,
                time_period=time_period,
                update_only=False  # Allow new seasons to be added
            )
            self.log(f"load_league_seasons_data returned: {success}", "DEBUG")
            if success:
                self.log("League seasons data collection completed", "INFO")
            else:
                self.log("League seasons data collection failed", "ERROR")
            return success
        except Exception as e:
            self.log(f"Error collecting league seasons: {e}", "ERROR")
            return False
    
    def get_league_ids_for_countries(self, country_codes: List[str]) -> List[int]:
        """Get league IDs for specified countries"""
        try:
            with psycopg2.connect(self.database_url) as conn:
                with conn.cursor() as cur:
                    placeholders = ','.join(['%s'] * len(country_codes))
                    cur.execute(f"""
                        SELECT DISTINCT league_id 
                        FROM staging.leagues 
                        WHERE country_code IN ({placeholders})
                        AND league_type IN ('domestic_leagues', 'domestic_cups')
                        ORDER BY league_id
                    """, country_codes)
                    
                    return [row[0] for row in cur.fetchall()]
        except Exception as e:
            self.log(f"Error getting league IDs: {e}", "ERROR")
            return []
    
    def collect_scope(self, scope_name: str, time_period: Optional[str] = None, force_refresh: bool = False) -> bool:
        """Collect data for a specific scope"""
        self.log(f"Starting collection for scope: {scope_name}")
        
        # Load configuration
        config = load_collection_config()
        scope = config.get_scope(scope_name)
        
        if not scope:
            self.log(f"Scope '{scope_name}' not found!", "ERROR")
            return False
        
        self.log(f"Scope: {scope.name}")
        self.log(f"Description: {scope.description}")
        self.log(f"Countries: {', '.join(scope.countries)}")
        if scope.time_period:
            self.log(f"Time Period: {scope.time_period.description}")
        
        # Step 1: Check and collect countries
        countries_fresh, missing_countries = self.check_countries_freshness(scope.countries)
        
        if not countries_fresh or force_refresh:
            if not self.collect_countries(scope.countries):
                self.log("Failed to collect countries data", "ERROR")
                return False
        else:
            self.log("Countries data is fresh, skipping collection", "INFO")
        
        # Step 2: Check and collect leagues
        leagues_fresh, leagues_needing_update = self.check_leagues_freshness(scope.countries)
        
        if not leagues_fresh or force_refresh:
            if not self.collect_leagues(scope.countries):
                self.log("Failed to collect leagues data", "ERROR")
                return False
        else:
            self.log("Leagues data is fresh, skipping collection", "INFO")
        
        # Step 3: Check and collect league seasons
        league_ids = self.get_league_ids_for_countries(scope.countries)
        
        if league_ids:
            # Use scope's time period if available, otherwise use CLI argument
            # For scopes, we need to find the time period name from the pattern
            scope_time_period = None
            if scope.time_period:
                # Find the time period name that matches this pattern
                config = load_collection_config()
                time_periods = config.config.get('time_periods', {})
                for tp_name, tp_config in time_periods.items():
                    if tp_config.get('pattern') == scope.time_period.pattern:
                        scope_time_period = tp_name
                        break
                if not scope_time_period:
                    scope_time_period = scope.time_period.pattern  # Fallback to pattern
            else:
                scope_time_period = time_period
            
            # Check if league seasons are fresh for the time period
            seasons_fresh, leagues_needing_seasons = self.check_league_seasons_freshness(league_ids, scope_time_period)
            
            if not seasons_fresh or force_refresh:
                self.log("League seasons need updating, collecting...")
                if not self.collect_league_seasons(league_ids, scope_time_period):
                    self.log("Failed to collect league seasons data", "ERROR")
                    return False
            else:
                self.log("League seasons are fresh for time period, skipping collection", "INFO")
        else:
            self.log("No leagues found for countries, skipping league seasons", "WARN")
        
        self.log(f"Collection for scope '{scope_name}' completed successfully!", "INFO")
        return True
    
    def collect_custom_countries(self, country_codes: List[str], time_period: Optional[str] = None, force_refresh: bool = False) -> bool:
        """Collect data for custom country selection"""
        self.log(f"Starting collection for custom countries: {', '.join(country_codes)}")
        
        # Step 1: Check and collect countries
        countries_fresh, missing_countries = self.check_countries_freshness(country_codes)
        
        if not countries_fresh or force_refresh:
            if not self.collect_countries(country_codes):
                self.log("Failed to collect countries data", "ERROR")
                return False
        else:
            self.log("Countries data is fresh, skipping collection", "INFO")
        
        # Step 2: Check and collect leagues
        leagues_fresh, leagues_needing_update = self.check_leagues_freshness(country_codes)
        
        if not leagues_fresh or force_refresh:
            if not self.collect_leagues(country_codes):
                self.log("Failed to collect leagues data", "ERROR")
                return False
        else:
            self.log("Leagues data is fresh, skipping collection", "INFO")
        
        # Step 3: Check and collect league seasons
        league_ids = self.get_league_ids_for_countries(country_codes)
        
        if league_ids:
            # Check if league seasons are fresh for the time period
            seasons_fresh, leagues_needing_seasons = self.check_league_seasons_freshness(league_ids, time_period)
            
            if not seasons_fresh or force_refresh:
                self.log("League seasons need updating, collecting...")
                if not self.collect_league_seasons(league_ids, time_period):
                    self.log("Failed to collect league seasons data", "ERROR")
                    return False
            else:
                self.log("League seasons are fresh for time period, skipping collection", "INFO")
        else:
            self.log("No leagues found for countries, skipping league seasons", "WARN")
        
        self.log(f"Collection for custom countries completed successfully!", "INFO")
        return True

def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(description="Football Data Collection Orchestrator")
    parser.add_argument("--scope", help="Predefined scope name (e.g., european_majors)")
    parser.add_argument("--countries", help="Comma-separated country codes (e.g., ENG,GER,FRA)")
    parser.add_argument("--time-period", help="Time period filter (e.g., 2024, 2020s)")
    parser.add_argument("--dry-run", action="store_true", help="Test without making changes")
    parser.add_argument("--force", action="store_true", help="Force refresh ignoring freshness checks")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    if not args.scope and not args.countries:
        parser.error("Must specify either --scope or --countries")
    
    try:
        collector = FootballDataCollector(dry_run=args.dry_run, verbose=args.verbose)
        
        if args.scope:
            # Use predefined scope
            success = collector.collect_scope(args.scope, args.time_period, args.force)
        else:
            # Use custom country selection
            country_codes = [code.strip() for code in args.countries.split(",")]
            success = collector.collect_custom_countries(country_codes, args.time_period, args.force)
        
        if success:
            print("\n🎉 Collection completed successfully!")
            return 0
        else:
            print("\n❌ Collection failed!")
            return 1
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 