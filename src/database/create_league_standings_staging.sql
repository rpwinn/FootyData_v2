-- League Standings Staging Table
-- Stores league standings data from /league-standings endpoint

CREATE TABLE IF NOT EXISTS staging.league_standings (
    -- Primary key
    id SERIAL PRIMARY KEY,
    
    -- League and season identification
    league_id INTEGER NOT NULL,
    season_id VARCHAR(20),
    
    -- Standings metadata
    standings_type VARCHAR(50),
    
    -- Team standings data
    position INTEGER,
    team_id VARCHAR(20),
    team_name VARCHAR(100),
    
    -- Match statistics
    played INTEGER,
    won INTEGER,
    drawn INTEGER,
    lost INTEGER,
    
    -- Goal statistics
    goals_for INTEGER,
    goals_against INTEGER,
    goal_difference VARCHAR(10),
    points INTEGER,
    
    -- Additional data (nested JSON)
    top_team_scorer JSONB,
    
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Raw API response for debugging/backup
    raw_data JSONB,
    
    -- Composite unique constraint
    UNIQUE(league_id, season_id, team_id)
);

-- Add comments
COMMENT ON TABLE staging.league_standings IS 'Staging table for league standings data from /league-standings endpoint';
COMMENT ON COLUMN staging.league_standings.league_id IS 'Football reference league ID';
COMMENT ON COLUMN staging.league_standings.season_id IS 'Season ID (e.g., 2023-2024)';
COMMENT ON COLUMN staging.league_standings.standings_type IS 'Type of standings (e.g., Regular Season, Playoffs)';
COMMENT ON COLUMN staging.league_standings.position IS 'Team position in standings';
COMMENT ON COLUMN staging.league_standings.team_id IS 'Football reference team ID';
COMMENT ON COLUMN staging.league_standings.team_name IS 'Name of the team';
COMMENT ON COLUMN staging.league_standings.played IS 'Number of matches played';
COMMENT ON COLUMN staging.league_standings.won IS 'Number of matches won';
COMMENT ON COLUMN staging.league_standings.drawn IS 'Number of matches drawn';
COMMENT ON COLUMN staging.league_standings.lost IS 'Number of matches lost';
COMMENT ON COLUMN staging.league_standings.goals_for IS 'Goals scored by team';
COMMENT ON COLUMN staging.league_standings.goals_against IS 'Goals conceded by team';
COMMENT ON COLUMN staging.league_standings.goal_difference IS 'Goal difference (goals_for - goals_against)';
COMMENT ON COLUMN staging.league_standings.points IS 'Total points earned';
COMMENT ON COLUMN staging.league_standings.top_team_scorer IS 'Nested JSON with top scorer data';
COMMENT ON COLUMN staging.league_standings.raw_data IS 'Complete API response JSON for debugging and backup';

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_league_standings_league_id ON staging.league_standings(league_id);
CREATE INDEX IF NOT EXISTS idx_league_standings_season_id ON staging.league_standings(season_id);
CREATE INDEX IF NOT EXISTS idx_league_standings_team_id ON staging.league_standings(team_id);
CREATE INDEX IF NOT EXISTS idx_league_standings_position ON staging.league_standings(position);
CREATE INDEX IF NOT EXISTS idx_league_standings_points ON staging.league_standings(points);

-- Create composite indexes for common queries
CREATE INDEX IF NOT EXISTS idx_league_standings_league_season ON staging.league_standings(league_id, season_id);
CREATE INDEX IF NOT EXISTS idx_league_standings_league_position ON staging.league_standings(league_id, position);
CREATE INDEX IF NOT EXISTS idx_league_standings_team_season ON staging.league_standings(team_id, season_id);

-- Create trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_league_standings_updated_at 
    BEFORE UPDATE ON staging.league_standings 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column(); 