#!/usr/bin/env python3
"""
Match data collector for FootyData_v2

Collects match data from FBR API and stores in staging database.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import json
import psycopg2
from datetime import datetime
from typing import Dict, Any, List, Optional
from api.fbr_client import FBRClient
from dotenv import load_dotenv
import yaml

load_dotenv()

class MatchDataCollector:
    """Collect match data from FBR API"""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        """Initialize match data collector"""
        self.database_url = os.getenv("DATABASE_URL")
        if not self.database_url:
            raise ValueError("DATABASE_URL environment variable not set")
        
        # Load configuration
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.staging_schema = self.config['database']['staging_schema']
        self.client = FBRClient()
    
    def store_match_metadata(self, match_data: Dict[str, Any], league_id: int, season_id: str):
        """Store match metadata in staging database"""
        with psycopg2.connect(self.database_url) as conn:
            with conn.cursor() as cur:
                cur.execute(f"""
                    INSERT INTO {self.staging_schema}.matches
                    (match_id, date, time, wk, home, home_team_id, away, away_team_id,
                     home_team_score, away_team_score, venue, attendance, referee,
                     league_id, season_id, raw_data)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (match_id) DO NOTHING
                """, (
                    match_data.get('match_id'),
                    match_data.get('date'),
                    match_data.get('time'),
                    match_data.get('wk'),
                    match_data.get('home'),
                    match_data.get('home_team_id'),
                    match_data.get('away'),
                    match_data.get('away_team_id'),
                    match_data.get('home_team_score'),
                    match_data.get('away_team_score'),
                    match_data.get('venue'),
                    match_data.get('attendance'),
                    match_data.get('referee'),
                    league_id,
                    season_id,
                    json.dumps(match_data)
                ))
            conn.commit()
    
    def store_player_metadata(self, player_data: Dict[str, Any]):
        """Store player metadata in staging database"""
        with psycopg2.connect(self.database_url) as conn:
            with conn.cursor() as cur:
                cur.execute(f"""
                    INSERT INTO {self.staging_schema}.players
                    (player_id, player_name, player_country_code, player_number, age, raw_data)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (player_id) DO NOTHING
                """, (
                    player_data.get('player_id'),
                    player_data.get('player_name'),
                    player_data.get('player_country_code'),
                    player_data.get('player_number'),
                    int(player_data.get('age')) if player_data.get('age') else None,
                    json.dumps(player_data)
                ))
            conn.commit()
    
    def store_player_summary_stats(self, match_id: str, player_data: Dict[str, Any]):
        """Store player summary stats in staging database"""
        with psycopg2.connect(self.database_url) as conn:
            with conn.cursor() as cur:
                stats = player_data.get('stats', {}).get('summary', {})
                
                # Handle positions array
                positions = stats.get('positions')
                if isinstance(positions, str):
                    positions = [positions]
                elif not positions:
                    positions = []
                
                cur.execute(f"""
                    INSERT INTO {self.staging_schema}.player_summary_stats
                    (match_id, player_id, positions, min, gls, sh, sot, xg, non_pen_xg,
                     ast, xag, pass_cmp, pass_att, pct_pass_cmp, pass_prog, sca, gca,
                     touches, carries, carries_prog, take_on_att, take_on_suc, tkl, int,
                     blocks, yellow_cards, red_cards, pk_made, pk_att, raw_data)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (match_id, player_id) DO NOTHING
                """, (
                    match_id,
                    player_data.get('meta_data', {}).get('player_id'),
                    positions,
                    int(stats.get('min', 0)) if stats.get('min') else 0,
                    stats.get('gls', 0),
                    stats.get('sh', 0),
                    stats.get('sot', 0),
                    stats.get('xg', 0),
                    stats.get('non_pen_xg', 0),
                    stats.get('ast', 0),
                    stats.get('xag', 0),
                    stats.get('pass_cmp', 0),
                    stats.get('pass_att', 0),
                    stats.get('pct_pass_cmp', 0),
                    stats.get('pass_prog', 0),
                    stats.get('sca', 0),
                    stats.get('gca', 0),
                    stats.get('touches', 0),
                    stats.get('carries', 0),
                    stats.get('carries_prog', 0),
                    stats.get('take_on_att', 0),
                    stats.get('take_on_suc', 0),
                    stats.get('tkl', 0),
                    stats.get('int', 0),
                    stats.get('blocks', 0),
                    stats.get('yellow_cards', 0),
                    stats.get('red_cards', 0),
                    stats.get('pk_made', 0),
                    stats.get('pk_att', 0),
                    json.dumps(player_data)
                ))
            conn.commit()
    
    def store_player_passing_stats(self, match_id: str, player_data: Dict[str, Any]):
        """Store player passing stats in staging database"""
        with psycopg2.connect(self.database_url) as conn:
            with conn.cursor() as cur:
                stats = player_data.get('stats', {}).get('passing', {})
                
                cur.execute(f"""
                    INSERT INTO {self.staging_schema}.player_passing_stats
                    (match_id, player_id, pass_ttl_dist, pass_prog_ttl_dist, pass_cmp_s,
                     pass_att_s, pct_pass_cmp_s, pass_cmp_m, pass_att_m, pct_pass_cmp_m,
                     pass_cmp_l, pass_att_l, pct_pass_cmp_l, xa, key_passes, pass_fthird,
                     pass_opp_box, cross_opp_box, raw_data)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (match_id, player_id) DO NOTHING
                """, (
                    match_id,
                    player_data.get('meta_data', {}).get('player_id'),
                    stats.get('pass_ttl_dist', 0),
                    stats.get('pass_prog_ttl_dist', 0),
                    stats.get('pass_cmp_s', 0),
                    stats.get('pass_att_s', 0),
                    stats.get('pct_pass_cmp_s', 0),
                    stats.get('pass_cmp_m', 0),
                    stats.get('pass_att_m', 0),
                    stats.get('pct_pass_cmp_m', 0),
                    stats.get('pass_cmp_l', 0),
                    stats.get('pass_att_l', 0),
                    stats.get('pct_pass_cmp_l', 0),
                    stats.get('xa', 0),
                    stats.get('key_passes', 0),
                    stats.get('pass_fthird', 0),
                    stats.get('pass_opp_box', 0),
                    stats.get('cross_opp_box', 0),
                    json.dumps(player_data)
                ))
            conn.commit()
    
    def store_player_passing_types(self, match_id: str, player_data: Dict[str, Any]):
        """Store player passing types in staging database"""
        with psycopg2.connect(self.database_url) as conn:
            with conn.cursor() as cur:
                stats = player_data.get('stats', {}).get('passing_types', {})
                
                cur.execute(f"""
                    INSERT INTO {self.staging_schema}.player_passing_types
                    (match_id, player_id, pass_live, pass_dead, pass_fk, through_balls,
                     switches, crosses, pass_offside, pass_blocked, throw_ins, ck,
                     ck_in_swinger, ck_out_swinger, ck_straight, raw_data)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (match_id, player_id) DO NOTHING
                """, (
                    match_id,
                    player_data.get('meta_data', {}).get('player_id'),
                    stats.get('pass_live', 0),
                    stats.get('pass_dead', 0),
                    stats.get('pass_fk', 0),
                    stats.get('through_balls', 0),
                    stats.get('switches', 0),
                    stats.get('crosses', 0),
                    stats.get('pass_offside', 0),
                    stats.get('pass_blocked', 0),
                    stats.get('throw_ins', 0),
                    stats.get('ck', 0),
                    stats.get('ck_in_swinger', 0),
                    stats.get('ck_out_swinger', 0),
                    stats.get('ck_straight', 0),
                    json.dumps(player_data)
                ))
            conn.commit()
    
    def store_player_defense_stats(self, match_id: str, player_data: Dict[str, Any]):
        """Store player defense stats in staging database"""
        with psycopg2.connect(self.database_url) as conn:
            with conn.cursor() as cur:
                stats = player_data.get('stats', {}).get('defense', {})
                
                cur.execute(f"""
                    INSERT INTO {self.staging_schema}.player_defense_stats
                    (match_id, player_id, tkl_won, tkl_def_third, tkl_mid_third,
                     tkl_att_third, tkl_drb, tkl_drb_att, pct_tkl_drb_suc, sh_blocked,
                     tkl_plus_int, clearances, def_error, raw_data)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (match_id, player_id) DO NOTHING
                """, (
                    match_id,
                    player_data.get('meta_data', {}).get('player_id'),
                    stats.get('tkl_won', 0),
                    stats.get('tkl_def_third', 0),
                    stats.get('tkl_mid_third', 0),
                    stats.get('tkl_att_third', 0),
                    stats.get('tkl_drb', 0),
                    stats.get('tkl_drb_att', 0),
                    stats.get('pct_tkl_drb_suc', 0),
                    stats.get('sh_blocked', 0),
                    stats.get('tkl_plus_int', 0),
                    stats.get('clearances', 0),
                    stats.get('def_error', 0),
                    json.dumps(player_data)
                ))
            conn.commit()
    
    def store_player_possession_stats(self, match_id: str, player_data: Dict[str, Any]):
        """Store player possession stats in staging database"""
        with psycopg2.connect(self.database_url) as conn:
            with conn.cursor() as cur:
                stats = player_data.get('stats', {}).get('possession', {})
                
                cur.execute(f"""
                    INSERT INTO {self.staging_schema}.player_possession_stats
                    (match_id, player_id, touch_def_box, touch_def_third, touch_mid_third,
                     touch_fthird, touch_opp_box, touch_live, pct_take_on_suc, take_on_tkld,
                     pct_take_on_tkld, ttl_carries_dist, ttl_carries_prog_dist,
                     carries_fthird, carries_opp_box, carries_miscontrolled,
                     carries_dispossessed, pass_recvd, pass_prog_rcvd, raw_data)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (match_id, player_id) DO NOTHING
                """, (
                    match_id,
                    player_data.get('meta_data', {}).get('player_id'),
                    stats.get('touch_def_box', 0),
                    stats.get('touch_def_third', 0),
                    stats.get('touch_mid_third', 0),
                    stats.get('touch_fthird', 0),
                    stats.get('touch_opp_box', 0),
                    stats.get('touch_live', 0),
                    stats.get('pct_take_on_suc', 0),
                    stats.get('take_on_tkld', 0),
                    stats.get('pct_take_on_tkld', 0),
                    stats.get('ttl_carries_dist', 0),
                    stats.get('ttl_carries_prog_dist', 0),
                    stats.get('carries_fthird', 0),
                    stats.get('carries_opp_box', 0),
                    stats.get('carries_miscontrolled', 0),
                    stats.get('carries_dispossessed', 0),
                    stats.get('pass_recvd', 0),
                    stats.get('pass_prog_rcvd', 0),
                    json.dumps(player_data)
                ))
            conn.commit()
    
    def store_player_misc_stats(self, match_id: str, player_data: Dict[str, Any]):
        """Store player misc stats in staging database"""
        with psycopg2.connect(self.database_url) as conn:
            with conn.cursor() as cur:
                stats = player_data.get('stats', {}).get('misc', {})
                
                cur.execute(f"""
                    INSERT INTO {self.staging_schema}.player_misc_stats
                    (match_id, player_id, second_yellow_cards, fls_com, fls_drawn,
                     offside, pk_won, pk_conceded, og, ball_recov, air_dual_won,
                     air_dual_lost, pct_air_dual_won, raw_data)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (match_id, player_id) DO NOTHING
                """, (
                    match_id,
                    player_data.get('meta_data', {}).get('player_id'),
                    stats.get('second_yellow_cards', 0),
                    stats.get('fls_com', 0),
                    stats.get('fls_drawn', 0),
                    stats.get('offside', 0),
                    stats.get('pk_won', 0),
                    stats.get('pk_conceded', 0),
                    stats.get('og', 0),
                    stats.get('ball_recov', 0),
                    stats.get('air_dual_won', 0),
                    stats.get('air_dual_lost', 0),
                    stats.get('pct_air_dual_won', 0),
                    json.dumps(player_data)
                ))
            conn.commit()
    
    def store_goalkeeper_stats(self, match_id: str, keeper_data: Dict[str, Any]):
        """Store goalkeeper stats in staging database"""
        with psycopg2.connect(self.database_url) as conn:
            with conn.cursor() as cur:
                cur.execute(f"""
                    INSERT INTO {self.staging_schema}.goalkeeper_stats
                    (match_id, player_id, gls_ag, sot_ag, saves, save_pct, psxg,
                     launched_pass_cmp, launched_pass_att, pct_launched_pass_cmp,
                     pass_att, throws_att, pct_passes_launched, avg_pass_len, gk_att,
                     pct_gk_launch, avg_gk_len, crosses_faced, crosses_stopped,
                     pct_crosses_stopped, def_action_outside_box,
                     avg_dist_def_action_outside_box, raw_data)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (match_id, player_id) DO NOTHING
                """, (
                    match_id,
                    keeper_data.get('player_id'),
                    keeper_data.get('gls_ag', 0),
                    keeper_data.get('sot_ag', 0),
                    int(keeper_data.get('saves', 0)) if keeper_data.get('saves') else 0,
                    keeper_data.get('save_pct', 0),
                    float(keeper_data.get('psxg', 0)) if keeper_data.get('psxg') else 0,
                    keeper_data.get('launched_pass_cmp', 0),
                    keeper_data.get('launched_pass_att', 0),
                    keeper_data.get('pct_launched_pass_cmp', 0),
                    keeper_data.get('pass_att', 0),
                    keeper_data.get('throws_att', 0),
                    keeper_data.get('pct_passes_launched', 0),
                    keeper_data.get('avg_pass_len', 0),
                    keeper_data.get('gk_att', 0),
                    keeper_data.get('pct_gk_launch', 0),
                    keeper_data.get('avg_gk_len', 0),
                    keeper_data.get('crosses_faced', 0),
                    keeper_data.get('crosses_stopped', 0),
                    keeper_data.get('pct_crosses_stopped', 0),
                    keeper_data.get('def_action_outside_box', 0),
                    keeper_data.get('avg_dist_def_action_outside_box', 0),
                    json.dumps(keeper_data)
                ))
            conn.commit()
    
    def collect_match_data(self, league_id: int, season_id: str, max_matches: Optional[int] = None):
        """Collect match data for a specific league and season"""
        print(f"Collecting match data for league {league_id}, season {season_id}")
        
        # Get matches
        matches_response = self.client.get_matches(league_id, season_id)
        if "error" in matches_response:
            print(f"Error getting matches: {matches_response['error']}")
            return
        
        matches = matches_response.get('data', [])
        if max_matches:
            matches = matches[:max_matches]
        
        print(f"Found {len(matches)} matches")
        
        for i, match in enumerate(matches):
            print(f"Processing match {i+1}/{len(matches)}: {match.get('home')} vs {match.get('away')}")
            
            # Store match metadata
            self.store_match_metadata(match, league_id, season_id)
            
            # Get match stats
            match_id = match.get('match_id')
            match_stats = self.client.get_match_stats(match_id)
            
            if "error" in match_stats:
                print(f"Error getting match stats for {match_id}: {match_stats['error']}")
                continue
            
            # Store player data
            teams = match_stats.get('data', [])
            for team in teams:
                players = team.get('players', [])
                for player in players:
                    # Store player metadata
                    meta_data = player.get('meta_data', {})
                    self.store_player_metadata(meta_data)
                    
                    # Store player stats
                    self.store_player_summary_stats(match_id, player)
                    self.store_player_passing_stats(match_id, player)
                    self.store_player_passing_types(match_id, player)
                    self.store_player_defense_stats(match_id, player)
                    self.store_player_possession_stats(match_id, player)
                    self.store_player_misc_stats(match_id, player)
            
            # Store goalkeeper data
            keepers = match_stats.get('keepers', [])
            for keeper in keepers:
                self.store_goalkeeper_stats(match_id, keeper)
            
            print(f"✅ Processed match {match_id}")
        
        print(f"✅ Completed collecting match data for {len(matches)} matches")

def main():
    """Main function for testing"""
    collector = MatchDataCollector()
    
    # Test with a small sample
    collector.collect_match_data(9, "2024-2025", max_matches=2)

if __name__ == "__main__":
    main() 