#!/usr/bin/env python3
"""
Simple match setup script
"""

import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def create_match_tables():
    """Create match tables one by one"""
    database_url = os.getenv("DATABASE_URL")
    print(f"Connecting to: {database_url}")
    
    with psycopg2.connect(database_url) as conn:
        with conn.cursor() as cur:
            
            # 1. Match metadata table
            print("Creating match_metadata table...")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS staging.match_metadata (
                    id SERIAL PRIMARY KEY,
                    match_id VARCHAR(20) UNIQUE,
                    date DATE,
                    time TIME,
                    wk VARCHAR(10),
                    home VARCHAR(100),
                    home_team_id VARCHAR(20),
                    away VARCHAR(100),
                    away_team_id VARCHAR(20),
                    home_team_score INTEGER,
                    away_team_score INTEGER,
                    venue VARCHAR(200),
                    attendance VARCHAR(50),
                    referee VARCHAR(100),
                    league_id INTEGER,
                    season_id VARCHAR(20),
                    raw_data JSONB,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            print("✅ Created match_metadata table")
            
            # 2. Player metadata table
            print("Creating player_metadata table...")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS staging.player_metadata (
                    id SERIAL PRIMARY KEY,
                    player_id VARCHAR(20) UNIQUE,
                    player_name VARCHAR(100),
                    player_country_code VARCHAR(3),
                    player_number VARCHAR(10),
                    age INTEGER,
                    raw_data JSONB,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            print("✅ Created player_metadata table")
            
            # 3. Player summary stats table
            print("Creating player_summary_stats table...")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS staging.player_summary_stats (
                    id SERIAL PRIMARY KEY,
                    match_id VARCHAR(20),
                    player_id VARCHAR(20),
                    positions TEXT[],
                    min INTEGER,
                    gls INTEGER,
                    sh INTEGER,
                    sot INTEGER,
                    xg NUMERIC(5,3),
                    non_pen_xg NUMERIC(5,3),
                    ast INTEGER,
                    xag NUMERIC(5,3),
                    pass_cmp INTEGER,
                    pass_att INTEGER,
                    pct_pass_cmp NUMERIC(5,2),
                    pass_prog INTEGER,
                    sca INTEGER,
                    gca INTEGER,
                    touches INTEGER,
                    carries INTEGER,
                    carries_prog INTEGER,
                    take_on_att INTEGER,
                    take_on_suc INTEGER,
                    tkl INTEGER,
                    int INTEGER,
                    blocks INTEGER,
                    yellow_cards INTEGER,
                    red_cards INTEGER,
                    pk_made INTEGER,
                    pk_att INTEGER,
                    raw_data JSONB,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(match_id, player_id)
                )
            """)
            conn.commit()
            print("✅ Created player_summary_stats table")
            
            # 4. Goalkeeper stats table
            print("Creating goalkeeper_stats table...")
            cur.execute("""
                CREATE TABLE IF NOT EXISTS staging.goalkeeper_stats (
                    id SERIAL PRIMARY KEY,
                    match_id VARCHAR(20),
                    player_id VARCHAR(20),
                    gls_ag INTEGER,
                    sot_ag INTEGER,
                    saves INTEGER,
                    save_pct NUMERIC(5,2),
                    psxg NUMERIC(5,3),
                    launched_pass_cmp INTEGER,
                    launched_pass_att INTEGER,
                    pct_launched_pass_cmp NUMERIC(5,2),
                    pass_att INTEGER,
                    throws_att INTEGER,
                    pct_passes_launched NUMERIC(5,2),
                    avg_pass_len NUMERIC(5,2),
                    gk_att INTEGER,
                    pct_gk_launch NUMERIC(5,2),
                    avg_gk_len NUMERIC(5,2),
                    crosses_faced INTEGER,
                    crosses_stopped INTEGER,
                    pct_crosses_stopped NUMERIC(5,2),
                    def_action_outside_box INTEGER,
                    avg_dist_def_action_outside_box NUMERIC(5,2),
                    raw_data JSONB,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(match_id, player_id)
                )
            """)
            conn.commit()
            print("✅ Created goalkeeper_stats table")
            
            # Create indexes
            print("Creating indexes...")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_match_metadata_match_id ON staging.match_metadata(match_id)")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_player_metadata_player_id ON staging.player_metadata(player_id)")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_player_summary_match_player ON staging.player_summary_stats(match_id, player_id)")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_goalkeeper_match_player ON staging.goalkeeper_stats(match_id, player_id)")
            conn.commit()
            print("✅ Created indexes")
            
            # Verify tables were created
            cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'staging' ORDER BY table_name;")
            tables = cur.fetchall()
            print(f"✅ Created {len(tables)} tables: {[table[0] for table in tables]}")

if __name__ == "__main__":
    create_match_tables() 