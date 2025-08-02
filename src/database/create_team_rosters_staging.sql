-- Team Rosters Staging Table
-- Stores team roster data from /teams endpoint team_roster section

CREATE TABLE IF NOT EXISTS staging.team_rosters (
    -- Primary key
    id SERIAL PRIMARY KEY,
    
    -- Team and player identification
    team_id VARCHAR(20) NOT NULL,
    player_id VARCHAR(20) NOT NULL,
    player_name VARCHAR(100),
    
    -- Player details
    nationality VARCHAR(10),
    position VARCHAR(20),
    age INTEGER,
    
    -- Season statistics
    matches_played INTEGER,
    starts INTEGER,
    
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Raw API response for debugging/backup
    raw_data JSONB,
    
    -- Composite unique constraint
    UNIQUE(team_id, player_id)
);

-- Add comments
COMMENT ON TABLE staging.team_rosters IS 'Staging table for team roster data from /teams endpoint team_roster section';
COMMENT ON COLUMN staging.team_rosters.team_id IS 'Football reference team ID (8-character string)';
COMMENT ON COLUMN staging.team_rosters.player_id IS 'Football reference player ID';
COMMENT ON COLUMN staging.team_rosters.player_name IS 'Name of the player';
COMMENT ON COLUMN staging.team_rosters.nationality IS '3-letter country code';
COMMENT ON COLUMN staging.team_rosters.position IS 'Player position(s) (e.g., FW,MF,DF,GK)';
COMMENT ON COLUMN staging.team_rosters.age IS 'Player age';
COMMENT ON COLUMN staging.team_rosters.matches_played IS 'Number of matches played';
COMMENT ON COLUMN staging.team_rosters.starts IS 'Number of starts';
COMMENT ON COLUMN staging.team_rosters.raw_data IS 'Complete API response JSON for debugging and backup';

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_team_rosters_team_id ON staging.team_rosters(team_id);
CREATE INDEX IF NOT EXISTS idx_team_rosters_player_id ON staging.team_rosters(player_id);
CREATE INDEX IF NOT EXISTS idx_team_rosters_position ON staging.team_rosters(position);
CREATE INDEX IF NOT EXISTS idx_team_rosters_nationality ON staging.team_rosters(nationality);

-- Create composite indexes for common queries
CREATE INDEX IF NOT EXISTS idx_team_rosters_team_player ON staging.team_rosters(team_id, player_id);
CREATE INDEX IF NOT EXISTS idx_team_rosters_position_nationality ON staging.team_rosters(position, nationality);

-- Create trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_team_rosters_updated_at 
    BEFORE UPDATE ON staging.team_rosters 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column(); 