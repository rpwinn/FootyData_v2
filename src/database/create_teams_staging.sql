-- Teams Staging Table
-- Stores team roster and schedule data from /teams endpoint

CREATE TABLE IF NOT EXISTS staging.teams (
    -- Primary key
    id SERIAL PRIMARY KEY,
    
    -- Team info fields
    team_id VARCHAR(20) NOT NULL,
    team_name VARCHAR(100),
    league_id INTEGER,
    league_name VARCHAR(100),
    season_id VARCHAR(20),
    
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Raw API response for debugging/backup
    raw_data JSONB,
    
    -- Composite unique constraint
    UNIQUE(team_id, season_id)
);

-- Add comments
COMMENT ON TABLE staging.teams IS 'Staging table for team roster and schedule data from /teams endpoint';
COMMENT ON COLUMN staging.teams.team_id IS 'Football reference team ID (8-character string)';
COMMENT ON COLUMN staging.teams.team_name IS 'Name of the team';
COMMENT ON COLUMN staging.teams.league_id IS 'League ID the team competes in';
COMMENT ON COLUMN staging.teams.league_name IS 'Name of the league';
COMMENT ON COLUMN staging.teams.season_id IS 'Season ID (format varies by league)';
COMMENT ON COLUMN staging.teams.raw_data IS 'Complete API response JSON for debugging and backup';

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_teams_team_id ON staging.teams(team_id);
CREATE INDEX IF NOT EXISTS idx_teams_league_id ON staging.teams(league_id);
CREATE INDEX IF NOT EXISTS idx_teams_season_id ON staging.teams(season_id);
CREATE INDEX IF NOT EXISTS idx_teams_team_name ON staging.teams(team_name);

-- Create composite indexes for common queries
CREATE INDEX IF NOT EXISTS idx_teams_team_season ON staging.teams(team_id, season_id);
CREATE INDEX IF NOT EXISTS idx_teams_league_season ON staging.teams(league_id, season_id);

-- Create trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_teams_updated_at 
    BEFORE UPDATE ON staging.teams 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column(); 