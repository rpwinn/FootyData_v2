-- Matches Staging Tables
-- Stores match data from /matches endpoint (including future matches without IDs)

-- League Matches Staging Table (when team_id is not provided)
CREATE TABLE IF NOT EXISTS staging.league_matches (
    -- Primary key
    id SERIAL PRIMARY KEY,
    
    -- Match identification (nullable for future matches)
    match_id VARCHAR(20),
    
    -- League and season context
    league_id INTEGER NOT NULL,
    season_id VARCHAR(20) NOT NULL,
    
    -- Match details
    match_date DATE,
    match_time TIME,
    round VARCHAR(200),
    wk VARCHAR(50),
    
    -- Team information
    home_team VARCHAR(200),
    home_team_id VARCHAR(50),
    away_team VARCHAR(200),
    away_team_id VARCHAR(50),
    
    -- Match results
    home_team_score INTEGER,
    away_team_score INTEGER,
    
    -- Match venue and officials
    venue VARCHAR(200),
    attendance VARCHAR(50),
    referee VARCHAR(200),
    
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Raw API response for debugging/backup
    raw_data JSONB
);

-- Team Matches Staging Table (when team_id is provided)
CREATE TABLE IF NOT EXISTS staging.team_matches (
    -- Primary key
    id SERIAL PRIMARY KEY,
    
    -- Match identification (nullable for future matches)
    match_id VARCHAR(20),
    
    -- League and season context
    league_id INTEGER NOT NULL,
    season_id VARCHAR(20) NOT NULL,
    
    -- Team context (the team this data is for)
    team_id VARCHAR(20) NOT NULL,
    
    -- Match details
    match_date DATE,
    match_time TIME,
    round VARCHAR(200),
    
    -- Team match information
    home_away VARCHAR(20),
    opponent VARCHAR(200),
    opponent_id VARCHAR(50),
    result VARCHAR(10),
    goals_for INTEGER,
    goals_against INTEGER,
    
    -- Team-specific details
    formation VARCHAR(50),
    captain VARCHAR(200),
    
    -- Match venue and officials
    attendance VARCHAR(50),
    referee VARCHAR(200),
    
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Raw API response for debugging/backup
    raw_data JSONB
);

-- Add comments for league_matches table
COMMENT ON TABLE staging.league_matches IS 'Staging table for league match data from /matches endpoint (when team_id is not provided)';
COMMENT ON COLUMN staging.league_matches.match_id IS 'Football reference match ID (nullable for future matches)';
COMMENT ON COLUMN staging.league_matches.league_id IS 'Football reference league ID';
COMMENT ON COLUMN staging.league_matches.season_id IS 'Season ID (e.g., 2023-2024)';
COMMENT ON COLUMN staging.league_matches.match_date IS 'Match date';
COMMENT ON COLUMN staging.league_matches.match_time IS 'Match time';
COMMENT ON COLUMN staging.league_matches.round IS 'Competition round or matchweek';
COMMENT ON COLUMN staging.league_matches.wk IS 'Matchweek number';
COMMENT ON COLUMN staging.league_matches.home_team IS 'Name of home team';
COMMENT ON COLUMN staging.league_matches.home_team_id IS 'Football reference home team ID';
COMMENT ON COLUMN staging.league_matches.away_team IS 'Name of away team';
COMMENT ON COLUMN staging.league_matches.away_team_id IS 'Football reference away team ID';
COMMENT ON COLUMN staging.league_matches.home_team_score IS 'Goals scored by home team';
COMMENT ON COLUMN staging.league_matches.away_team_score IS 'Goals scored by away team';
COMMENT ON COLUMN staging.league_matches.venue IS 'Match venue';
COMMENT ON COLUMN staging.league_matches.attendance IS 'Match attendance';
COMMENT ON COLUMN staging.league_matches.referee IS 'Match referee';
COMMENT ON COLUMN staging.league_matches.raw_data IS 'Complete API response JSON for debugging and backup';

-- Add comments for team_matches table
COMMENT ON TABLE staging.team_matches IS 'Staging table for team match data from /matches endpoint (when team_id is provided)';
COMMENT ON COLUMN staging.team_matches.match_id IS 'Football reference match ID (nullable for future matches)';
COMMENT ON COLUMN staging.team_matches.league_id IS 'Football reference league ID';
COMMENT ON COLUMN staging.team_matches.season_id IS 'Season ID (e.g., 2023-2024)';
COMMENT ON COLUMN staging.team_matches.team_id IS 'Football reference team ID (the team this data is for)';
COMMENT ON COLUMN staging.team_matches.match_date IS 'Match date';
COMMENT ON COLUMN staging.team_matches.match_time IS 'Match time';
COMMENT ON COLUMN staging.team_matches.round IS 'Competition round or matchweek';
COMMENT ON COLUMN staging.team_matches.home_away IS 'Whether team played at home, neutral or away';
COMMENT ON COLUMN staging.team_matches.opponent IS 'Name of opposing team';
COMMENT ON COLUMN staging.team_matches.opponent_id IS 'Football reference identification of opposing team';
COMMENT ON COLUMN staging.team_matches.result IS 'Result of match (W = win, L = loss, D = draw)';
COMMENT ON COLUMN staging.team_matches.goals_for IS 'Number of goals scored by team in match';
COMMENT ON COLUMN staging.team_matches.goals_against IS 'Number of goals conceded by team in match';
COMMENT ON COLUMN staging.team_matches.formation IS 'Formation played by team';
COMMENT ON COLUMN staging.team_matches.captain IS 'Name of team captain for match';
COMMENT ON COLUMN staging.team_matches.attendance IS 'Match attendance';
COMMENT ON COLUMN staging.team_matches.referee IS 'Match referee';
COMMENT ON COLUMN staging.team_matches.raw_data IS 'Complete API response JSON for debugging and backup';

-- Create indexes for league_matches table
CREATE INDEX IF NOT EXISTS idx_league_matches_match_id ON staging.league_matches(match_id);
CREATE INDEX IF NOT EXISTS idx_league_matches_league_id ON staging.league_matches(league_id);
CREATE INDEX IF NOT EXISTS idx_league_matches_season_id ON staging.league_matches(season_id);
CREATE INDEX IF NOT EXISTS idx_league_matches_match_date ON staging.league_matches(match_date);
CREATE INDEX IF NOT EXISTS idx_league_matches_home_team_id ON staging.league_matches(home_team_id);
CREATE INDEX IF NOT EXISTS idx_league_matches_away_team_id ON staging.league_matches(away_team_id);

-- Create indexes for team_matches table
CREATE INDEX IF NOT EXISTS idx_team_matches_match_id ON staging.team_matches(match_id);
CREATE INDEX IF NOT EXISTS idx_team_matches_league_id ON staging.team_matches(league_id);
CREATE INDEX IF NOT EXISTS idx_team_matches_season_id ON staging.team_matches(season_id);
CREATE INDEX IF NOT EXISTS idx_team_matches_team_id ON staging.team_matches(team_id);
CREATE INDEX IF NOT EXISTS idx_team_matches_match_date ON staging.team_matches(match_date);
CREATE INDEX IF NOT EXISTS idx_team_matches_opponent_id ON staging.team_matches(opponent_id);

-- Create composite indexes for common queries
CREATE INDEX IF NOT EXISTS idx_league_matches_league_season ON staging.league_matches(league_id, season_id);
CREATE INDEX IF NOT EXISTS idx_league_matches_league_date ON staging.league_matches(league_id, match_date);
CREATE INDEX IF NOT EXISTS idx_team_matches_team_season ON staging.team_matches(team_id, season_id);
CREATE INDEX IF NOT EXISTS idx_team_matches_team_date ON staging.team_matches(team_id, match_date);

-- Create unique constraints for matches with IDs
CREATE UNIQUE INDEX IF NOT EXISTS idx_league_matches_match_id_unique 
ON staging.league_matches(league_id, season_id, match_id) 
WHERE match_id IS NOT NULL;

CREATE UNIQUE INDEX IF NOT EXISTS idx_team_matches_match_id_unique 
ON staging.team_matches(league_id, season_id, match_id, team_id) 
WHERE match_id IS NOT NULL;

-- Create unique constraints for future matches without IDs
CREATE UNIQUE INDEX IF NOT EXISTS idx_league_matches_future_unique 
ON staging.league_matches(league_id, season_id, match_date, home_team, away_team) 
WHERE match_id IS NULL;

CREATE UNIQUE INDEX IF NOT EXISTS idx_team_matches_future_unique 
ON staging.team_matches(league_id, season_id, team_id, match_date, opponent) 
WHERE match_id IS NULL;

-- Add comments explaining the constraint strategy
COMMENT ON INDEX staging.idx_league_matches_match_id_unique IS 'Unique constraint for matches with IDs';
COMMENT ON INDEX staging.idx_league_matches_future_unique IS 'Unique constraint for future matches without IDs';
COMMENT ON INDEX staging.idx_team_matches_match_id_unique IS 'Unique constraint for team matches with IDs';
COMMENT ON INDEX staging.idx_team_matches_future_unique IS 'Unique constraint for future team matches without IDs';

-- Create trigger to update updated_at timestamp for league_matches
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_league_matches_updated_at 
    BEFORE UPDATE ON staging.league_matches 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_team_matches_updated_at 
    BEFORE UPDATE ON staging.team_matches 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column(); 