-- League Season Details Staging Table
-- Stores metadata for specific league-season combinations

CREATE TABLE IF NOT EXISTS staging.league_season_details (
    -- Primary key
    id SERIAL PRIMARY KEY,
    
    -- API response fields
    league_id INTEGER NOT NULL,
    season_id VARCHAR(20) NOT NULL,
    league_start DATE,
    league_end DATE,
    league_type VARCHAR(10) CHECK (league_type IN ('cup', 'league')),
    has_adv_stats VARCHAR(3) CHECK (has_adv_stats IN ('yes', 'no')),
    rounds JSONB, -- Array of round names for cup competitions
    
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Raw API response for debugging/backup
    raw_data JSONB,
    
    -- Composite unique constraint
    UNIQUE(league_id, season_id)
);

-- Add comments
COMMENT ON TABLE staging.league_season_details IS 'Staging table for league season details metadata from /league-season-details endpoint';
COMMENT ON COLUMN staging.league_season_details.league_id IS 'League ID (same as input parameter)';
COMMENT ON COLUMN staging.league_season_details.season_id IS 'Season ID (same as input parameter) - format varies by league';
COMMENT ON COLUMN staging.league_season_details.league_start IS 'First match date for the league-season in YYYY-MM-DD format';
COMMENT ON COLUMN staging.league_season_details.league_end IS 'Last match date for the league-season in YYYY-MM-DD format';
COMMENT ON COLUMN staging.league_season_details.league_type IS 'Either cup or league';
COMMENT ON COLUMN staging.league_season_details.has_adv_stats IS 'Whether advanced stats are available (yes/no)';
COMMENT ON COLUMN staging.league_season_details.rounds IS 'Array of round names for cup competitions with multiple rounds';
COMMENT ON COLUMN staging.league_season_details.raw_data IS 'Complete API response JSON for debugging and backup';

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_league_season_details_league_id ON staging.league_season_details(league_id);
CREATE INDEX IF NOT EXISTS idx_league_season_details_season_id ON staging.league_season_details(season_id);
CREATE INDEX IF NOT EXISTS idx_league_season_details_league_type ON staging.league_season_details(league_type);
CREATE INDEX IF NOT EXISTS idx_league_season_details_has_adv_stats ON staging.league_season_details(has_adv_stats);
CREATE INDEX IF NOT EXISTS idx_league_season_details_league_start ON staging.league_season_details(league_start);
CREATE INDEX IF NOT EXISTS idx_league_season_details_league_end ON staging.league_season_details(league_end);

-- Create composite indexes for common queries
CREATE INDEX IF NOT EXISTS idx_league_season_details_league_season ON staging.league_season_details(league_id, season_id);
CREATE INDEX IF NOT EXISTS idx_league_season_details_type_stats ON staging.league_season_details(league_type, has_adv_stats);

-- Create trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_league_season_details_updated_at 
    BEFORE UPDATE ON staging.league_season_details 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column(); 