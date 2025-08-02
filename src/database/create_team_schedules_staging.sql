-- Team Schedules Staging Table
-- Stores team schedule data from /teams endpoint team_schedule section

CREATE TABLE IF NOT EXISTS staging.team_schedules (
    -- Primary key
    id SERIAL PRIMARY KEY,
    
    -- Team and match identification
    team_id VARCHAR(20) NOT NULL,
    match_id VARCHAR(20) NOT NULL,
    
    -- Match details
    match_date DATE,
    match_time TIME,
    league_name VARCHAR(100),
    league_id INTEGER,
    
    -- Opponent information
    opponent VARCHAR(100),
    opponent_id VARCHAR(20),
    home_away VARCHAR(10),
    
    -- Match results
    result VARCHAR(5),
    goals_for INTEGER,
    goals_against INTEGER,
    
    -- Additional match details
    attendance VARCHAR(20),
    captain VARCHAR(100),
    formation VARCHAR(20),
    referee VARCHAR(100),
    
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Raw API response for debugging/backup
    raw_data JSONB,
    
    -- Composite unique constraint
    UNIQUE(team_id, match_id)
);

-- Add comments
COMMENT ON TABLE staging.team_schedules IS 'Staging table for team schedule data from /teams endpoint team_schedule section';
COMMENT ON COLUMN staging.team_schedules.team_id IS 'Football reference team ID (8-character string)';
COMMENT ON COLUMN staging.team_schedules.match_id IS 'Football reference match ID';
COMMENT ON COLUMN staging.team_schedules.match_date IS 'Match date';
COMMENT ON COLUMN staging.team_schedules.match_time IS 'Match time';
COMMENT ON COLUMN staging.team_schedules.league_name IS 'Name of the league';
COMMENT ON COLUMN staging.team_schedules.league_id IS 'League ID';
COMMENT ON COLUMN staging.team_schedules.opponent IS 'Name of opponent team';
COMMENT ON COLUMN staging.team_schedules.opponent_id IS 'Football reference opponent team ID';
COMMENT ON COLUMN staging.team_schedules.home_away IS 'Home, Away, or Neutral';
COMMENT ON COLUMN staging.team_schedules.result IS 'Match result (W, L, D)';
COMMENT ON COLUMN staging.team_schedules.goals_for IS 'Goals scored by team';
COMMENT ON COLUMN staging.team_schedules.goals_against IS 'Goals conceded by team';
COMMENT ON COLUMN staging.team_schedules.attendance IS 'Match attendance';
COMMENT ON COLUMN staging.team_schedules.captain IS 'Team captain for the match';
COMMENT ON COLUMN staging.team_schedules.formation IS 'Team formation used';
COMMENT ON COLUMN staging.team_schedules.referee IS 'Match referee';
COMMENT ON COLUMN staging.team_schedules.raw_data IS 'Complete API response JSON for debugging and backup';

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_team_schedules_team_id ON staging.team_schedules(team_id);
CREATE INDEX IF NOT EXISTS idx_team_schedules_match_id ON staging.team_schedules(match_id);
CREATE INDEX IF NOT EXISTS idx_team_schedules_match_date ON staging.team_schedules(match_date);
CREATE INDEX IF NOT EXISTS idx_team_schedules_league_id ON staging.team_schedules(league_id);
CREATE INDEX IF NOT EXISTS idx_team_schedules_opponent_id ON staging.team_schedules(opponent_id);
CREATE INDEX IF NOT EXISTS idx_team_schedules_result ON staging.team_schedules(result);

-- Create composite indexes for common queries
CREATE INDEX IF NOT EXISTS idx_team_schedules_team_match ON staging.team_schedules(team_id, match_id);
CREATE INDEX IF NOT EXISTS idx_team_schedules_league_date ON staging.team_schedules(league_id, match_date);
CREATE INDEX IF NOT EXISTS idx_team_schedules_team_date ON staging.team_schedules(team_id, match_date);

-- Create trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_team_schedules_updated_at 
    BEFORE UPDATE ON staging.team_schedules 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column(); 