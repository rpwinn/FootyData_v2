"""
Match data database setup for FootyData_v2

Creates the match-specific database schema for storing match data.
"""

import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv
import yaml

load_dotenv()

class MatchDatabaseSetup:
    """Match database setup and management"""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        """Initialize database setup"""
        self.database_url = os.getenv("DATABASE_URL")
        if not self.database_url:
            raise ValueError("DATABASE_URL environment variable not set")
        
        # Load configuration
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.staging_schema = self.config['database']['staging_schema']
        self.final_schema = self.config['database']['final_schema']
    
    def create_match_tables(self):
        """Create match-specific staging tables"""
        with psycopg2.connect(self.database_url) as conn:
            with conn.cursor() as cur:
                
                # Match metadata table
                cur.execute(f"""
                    CREATE TABLE IF NOT EXISTS {self.staging_schema}.match_metadata (
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
                
                # Player metadata table
                cur.execute(f"""
                    CREATE TABLE IF NOT EXISTS {self.staging_schema}.player_metadata (
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
                
                # Player summary stats table
                cur.execute(f"""
                    CREATE TABLE IF NOT EXISTS {self.staging_schema}.player_summary_stats (
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
                
                # Player passing stats table
                cur.execute(f"""
                    CREATE TABLE IF NOT EXISTS {self.staging_schema}.player_passing_stats (
                        id SERIAL PRIMARY KEY,
                        match_id VARCHAR(20),
                        player_id VARCHAR(20),
                        pass_ttl_dist INTEGER,
                        pass_prog_ttl_dist INTEGER,
                        pass_cmp_s INTEGER,
                        pass_att_s INTEGER,
                        pct_pass_cmp_s NUMERIC(5,2),
                        pass_cmp_m INTEGER,
                        pass_att_m INTEGER,
                        pct_pass_cmp_m NUMERIC(5,2),
                        pass_cmp_l INTEGER,
                        pass_att_l INTEGER,
                        pct_pass_cmp_l NUMERIC(5,2),
                        xa NUMERIC(5,3),
                        key_passes INTEGER,
                        pass_fthird INTEGER,
                        pass_opp_box INTEGER,
                        cross_opp_box INTEGER,
                        raw_data JSONB,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(match_id, player_id)
                    )
                """)
                
                # Player passing types table
                cur.execute(f"""
                    CREATE TABLE IF NOT EXISTS {self.staging_schema}.player_passing_types (
                        id SERIAL PRIMARY KEY,
                        match_id VARCHAR(20),
                        player_id VARCHAR(20),
                        pass_live INTEGER,
                        pass_dead INTEGER,
                        pass_fk INTEGER,
                        through_balls INTEGER,
                        switches INTEGER,
                        crosses INTEGER,
                        pass_offside INTEGER,
                        pass_blocked INTEGER,
                        throw_ins INTEGER,
                        ck INTEGER,
                        ck_in_swinger INTEGER,
                        ck_out_swinger INTEGER,
                        ck_straight INTEGER,
                        raw_data JSONB,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(match_id, player_id)
                    )
                """)
                
                # Player defense stats table
                cur.execute(f"""
                    CREATE TABLE IF NOT EXISTS {self.staging_schema}.player_defense_stats (
                        id SERIAL PRIMARY KEY,
                        match_id VARCHAR(20),
                        player_id VARCHAR(20),
                        tkl_won INTEGER,
                        tkl_def_third INTEGER,
                        tkl_mid_third INTEGER,
                        tkl_att_third INTEGER,
                        tkl_drb INTEGER,
                        tkl_drb_att INTEGER,
                        pct_tkl_drb_suc NUMERIC(5,2),
                        sh_blocked INTEGER,
                        tkl_plus_int INTEGER,
                        clearances INTEGER,
                        def_error INTEGER,
                        raw_data JSONB,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(match_id, player_id)
                    )
                """)
                
                # Player possession stats table
                cur.execute(f"""
                    CREATE TABLE IF NOT EXISTS {self.staging_schema}.player_possession_stats (
                        id SERIAL PRIMARY KEY,
                        match_id VARCHAR(20),
                        player_id VARCHAR(20),
                        touch_def_box INTEGER,
                        touch_def_third INTEGER,
                        touch_mid_third INTEGER,
                        touch_fthird INTEGER,
                        touch_opp_box INTEGER,
                        touch_live INTEGER,
                        pct_take_on_suc NUMERIC(5,2),
                        take_on_tkld INTEGER,
                        pct_take_on_tkld NUMERIC(5,2),
                        ttl_carries_dist INTEGER,
                        ttl_carries_prog_dist INTEGER,
                        carries_fthird INTEGER,
                        carries_opp_box INTEGER,
                        carries_miscontrolled INTEGER,
                        carries_dispossessed INTEGER,
                        pass_recvd INTEGER,
                        pass_prog_rcvd INTEGER,
                        raw_data JSONB,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(match_id, player_id)
                    )
                """)
                
                # Player misc stats table
                cur.execute(f"""
                    CREATE TABLE IF NOT EXISTS {self.staging_schema}.player_misc_stats (
                        id SERIAL PRIMARY KEY,
                        match_id VARCHAR(20),
                        player_id VARCHAR(20),
                        second_yellow_cards INTEGER,
                        fls_com INTEGER,
                        fls_drawn INTEGER,
                        offside INTEGER,
                        pk_won INTEGER,
                        pk_conceded INTEGER,
                        og INTEGER,
                        ball_recov INTEGER,
                        air_dual_won INTEGER,
                        air_dual_lost INTEGER,
                        pct_air_dual_won NUMERIC(5,2),
                        raw_data JSONB,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(match_id, player_id)
                    )
                """)
                
                # Goalkeeper stats table
                cur.execute(f"""
                    CREATE TABLE IF NOT EXISTS {self.staging_schema}.goalkeeper_stats (
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
                
                # Create indexes for performance
                self.create_match_indexes(cur)
                
                print("✅ Created all match data tables")
    
    def create_match_indexes(self, cur):
        """Create indexes for match data tables"""
        
        # Indexes on match_id for fast lookups
        cur.execute(f"CREATE INDEX IF NOT EXISTS idx_match_metadata_match_id ON {self.staging_schema}.match_metadata(match_id)")
        cur.execute(f"CREATE INDEX IF NOT EXISTS idx_match_metadata_date ON {self.staging_schema}.match_metadata(date)")
        cur.execute(f"CREATE INDEX IF NOT EXISTS idx_match_metadata_league_season ON {self.staging_schema}.match_metadata(league_id, season_id)")
        
        # Indexes on player_id for fast lookups
        cur.execute(f"CREATE INDEX IF NOT EXISTS idx_player_metadata_player_id ON {self.staging_schema}.player_metadata(player_id)")
        
        # Indexes on match_id and player_id for stats tables
        cur.execute(f"CREATE INDEX IF NOT EXISTS idx_player_summary_match_player ON {self.staging_schema}.player_summary_stats(match_id, player_id)")
        cur.execute(f"CREATE INDEX IF NOT EXISTS idx_player_passing_match_player ON {self.staging_schema}.player_passing_stats(match_id, player_id)")
        cur.execute(f"CREATE INDEX IF NOT EXISTS idx_player_passing_types_match_player ON {self.staging_schema}.player_passing_types(match_id, player_id)")
        cur.execute(f"CREATE INDEX IF NOT EXISTS idx_player_defense_match_player ON {self.staging_schema}.player_defense_stats(match_id, player_id)")
        cur.execute(f"CREATE INDEX IF NOT EXISTS idx_player_possession_match_player ON {self.staging_schema}.player_possession_stats(match_id, player_id)")
        cur.execute(f"CREATE INDEX IF NOT EXISTS idx_player_misc_match_player ON {self.staging_schema}.player_misc_stats(match_id, player_id)")
        cur.execute(f"CREATE INDEX IF NOT EXISTS idx_goalkeeper_match_player ON {self.staging_schema}.goalkeeper_stats(match_id, player_id)")
        
        print("✅ Created all match data indexes")
    
    def setup_match_database(self):
        """Complete match database setup"""
        print("Setting up FootyData_v2 match database...")
        
        try:
            self.create_match_tables()
            print("✅ Match database setup complete!")
            return True
        except Exception as e:
            print(f"❌ Match database setup failed: {e}")
            return False

def main():
    """Main setup function"""
    try:
        setup = MatchDatabaseSetup()
        setup.setup_match_database()
    except Exception as e:
        print(f"Match setup failed: {e}")

if __name__ == "__main__":
    main() 