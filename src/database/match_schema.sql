-- Match Data Database Schema
-- Based on FBR API match data structure

-- =====================================================
-- MATCH METADATA TABLES
-- =====================================================

-- Staging table for raw match metadata
CREATE TABLE IF NOT EXISTS staging.matches (
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
);

-- =====================================================
-- PLAYER METADATA TABLES
-- =====================================================

-- Staging table for player metadata
CREATE TABLE IF NOT EXISTS staging.players (
    id SERIAL PRIMARY KEY,
    player_id VARCHAR(20) UNIQUE,
    player_name VARCHAR(100),
    player_country_code VARCHAR(3),
    player_number VARCHAR(10),
    age INTEGER,
    raw_data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- PLAYER STATS TABLES
-- =====================================================

-- Staging table for player summary stats
CREATE TABLE IF NOT EXISTS staging.player_summary_stats (
    id SERIAL PRIMARY KEY,
    match_id VARCHAR(20),
    player_id VARCHAR(20),
    positions TEXT[], -- Array of positions
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
);

-- Staging table for player passing stats
CREATE TABLE IF NOT EXISTS staging.player_passing_stats (
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
);

-- Staging table for player passing types
CREATE TABLE IF NOT EXISTS staging.player_passing_types (
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
);

-- Staging table for player defense stats
CREATE TABLE IF NOT EXISTS staging.player_defense_stats (
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
);

-- Staging table for player possession stats
CREATE TABLE IF NOT EXISTS staging.player_possession_stats (
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
);

-- Staging table for player misc stats
CREATE TABLE IF NOT EXISTS staging.player_misc_stats (
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
);

-- =====================================================
-- GOALKEEPER STATS TABLES
-- =====================================================

-- Staging table for goalkeeper stats
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
);

-- =====================================================
-- INDEXES FOR PERFORMANCE
-- =====================================================

-- Indexes on match_id for fast lookups
CREATE INDEX IF NOT EXISTS idx_matches_match_id ON staging.matches(match_id);
CREATE INDEX IF NOT EXISTS idx_matches_date ON staging.matches(date);
CREATE INDEX IF NOT EXISTS idx_matches_league_season ON staging.matches(league_id, season_id);

-- Indexes on player_id for fast lookups
CREATE INDEX IF NOT EXISTS idx_players_player_id ON staging.players(player_id);

-- Indexes on match_id and player_id for stats tables
CREATE INDEX IF NOT EXISTS idx_player_summary_match_player ON staging.player_summary_stats(match_id, player_id);
CREATE INDEX IF NOT EXISTS idx_player_passing_match_player ON staging.player_passing_stats(match_id, player_id);
CREATE INDEX IF NOT EXISTS idx_player_passing_types_match_player ON staging.player_passing_types(match_id, player_id);
CREATE INDEX IF NOT EXISTS idx_player_defense_match_player ON staging.player_defense_stats(match_id, player_id);
CREATE INDEX IF NOT EXISTS idx_player_possession_match_player ON staging.player_possession_stats(match_id, player_id);
CREATE INDEX IF NOT EXISTS idx_player_misc_match_player ON staging.player_misc_stats(match_id, player_id);
CREATE INDEX IF NOT EXISTS idx_goalkeeper_match_player ON staging.goalkeeper_stats(match_id, player_id);

-- =====================================================
-- FINAL SCHEMA TABLES (for transformed data)
-- =====================================================

-- Final matches table (transformed from staging)
CREATE TABLE IF NOT EXISTS football.matches (
    id SERIAL PRIMARY KEY,
    match_id VARCHAR(20) UNIQUE,
    date DATE,
    time TIME,
    week INTEGER,
    home_team_id VARCHAR(20),
    away_team_id VARCHAR(20),
    home_team_name VARCHAR(100),
    away_team_name VARCHAR(100),
    home_score INTEGER,
    away_score INTEGER,
    venue VARCHAR(200),
    attendance INTEGER,
    referee VARCHAR(100),
    league_id INTEGER,
    season_id VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Final players table (transformed from staging)
CREATE TABLE IF NOT EXISTS football.players (
    id SERIAL PRIMARY KEY,
    player_id VARCHAR(20) UNIQUE,
    player_name VARCHAR(100),
    country_code VARCHAR(3),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Final player match performances table (aggregated stats)
CREATE TABLE IF NOT EXISTS football.player_match_performances (
    id SERIAL PRIMARY KEY,
    match_id VARCHAR(20),
    player_id VARCHAR(20),
    team_id VARCHAR(20),
    positions TEXT[],
    minutes_played INTEGER,
    goals INTEGER,
    assists INTEGER,
    xg NUMERIC(5,3),
    xa NUMERIC(5,3),
    shots INTEGER,
    shots_on_target INTEGER,
    passes_completed INTEGER,
    passes_attempted INTEGER,
    pass_completion_pct NUMERIC(5,2),
    progressive_passes INTEGER,
    progressive_carries INTEGER,
    touches INTEGER,
    tackles INTEGER,
    interceptions INTEGER,
    blocks INTEGER,
    yellow_cards INTEGER,
    red_cards INTEGER,
    fouls_committed INTEGER,
    fouls_drawn INTEGER,
    offsides INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(match_id, player_id)
);

-- Final goalkeeper performances table
CREATE TABLE IF NOT EXISTS football.goalkeeper_performances (
    id SERIAL PRIMARY KEY,
    match_id VARCHAR(20),
    player_id VARCHAR(20),
    team_id VARCHAR(20),
    goals_against INTEGER,
    saves INTEGER,
    save_percentage NUMERIC(5,2),
    clean_sheet BOOLEAN,
    crosses_faced INTEGER,
    crosses_stopped INTEGER,
    crosses_stopped_pct NUMERIC(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(match_id, player_id)
);

-- =====================================================
-- INDEXES FOR FINAL TABLES
-- =====================================================

CREATE INDEX IF NOT EXISTS idx_football_matches_match_id ON football.matches(match_id);
CREATE INDEX IF NOT EXISTS idx_football_matches_date ON football.matches(date);
CREATE INDEX IF NOT EXISTS idx_football_matches_league_season ON football.matches(league_id, season_id);

CREATE INDEX IF NOT EXISTS idx_football_players_player_id ON football.players(player_id);

CREATE INDEX IF NOT EXISTS idx_football_performances_match_player ON football.player_match_performances(match_id, player_id);
CREATE INDEX IF NOT EXISTS idx_football_performances_player ON football.player_match_performances(player_id);
CREATE INDEX IF NOT EXISTS idx_football_performances_team ON football.player_match_performances(team_id);

CREATE INDEX IF NOT EXISTS idx_football_goalkeeper_match_player ON football.goalkeeper_performances(match_id, player_id);
CREATE INDEX IF NOT EXISTS idx_football_goalkeeper_player ON football.goalkeeper_performances(player_id);
CREATE INDEX IF NOT EXISTS idx_football_goalkeeper_team ON football.goalkeeper_performances(team_id); 