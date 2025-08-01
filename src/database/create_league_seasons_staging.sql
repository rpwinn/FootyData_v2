-- Create League Seasons Staging Table
-- TASK-002-03: Create League Seasons Staging Table

-- Drop table if it exists
DROP TABLE IF EXISTS staging.league_seasons;

-- Create the league_seasons staging table
CREATE TABLE staging.league_seasons (
    -- Primary key
    id SERIAL PRIMARY KEY,
    
    -- League identification
    league_id INTEGER NOT NULL,
    competition_name VARCHAR(255) NOT NULL,
    
    -- Season information
    season_id VARCHAR(20) NOT NULL,
    num_squads INTEGER,
    
    -- Champion and top scorer information
    champion VARCHAR(255),
    top_scorer_player TEXT, -- Can be string or array, stored as JSON string
    top_scorer_goals INTEGER,
    
    -- Audit fields
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Raw API response
    raw_data JSONB NOT NULL,
    
    -- Composite unique constraint
    UNIQUE(league_id, season_id)
);

-- Create indexes for performance
CREATE INDEX idx_league_seasons_league_id ON staging.league_seasons(league_id);
CREATE INDEX idx_league_seasons_season_id ON staging.league_seasons(season_id);
CREATE INDEX idx_league_seasons_competition_name ON staging.league_seasons(competition_name);

-- Add comments
COMMENT ON TABLE staging.league_seasons IS 'Raw league seasons data from FBR API /league-seasons endpoint';
COMMENT ON COLUMN staging.league_seasons.league_id IS 'Football reference league ID';
COMMENT ON COLUMN staging.league_seasons.competition_name IS 'Name of the league competition';
COMMENT ON COLUMN staging.league_seasons.season_id IS 'Season identifier (e.g., "2023-2024", "2024")';
COMMENT ON COLUMN staging.league_seasons.num_squads IS 'Number of teams that competed in the league-season';
COMMENT ON COLUMN staging.league_seasons.champion IS 'Name of the team that won the competition';
COMMENT ON COLUMN staging.league_seasons.top_scorer_player IS 'Name of top scorer(s) - can be single player or array for ties';
COMMENT ON COLUMN staging.league_seasons.top_scorer_goals IS 'Number of goals scored by top scorer';
COMMENT ON COLUMN staging.league_seasons.raw_data IS 'Full JSON response from API';

-- Create trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_league_seasons_updated_at 
    BEFORE UPDATE ON staging.league_seasons 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Grant permissions (adjust as needed for your setup)
-- GRANT ALL PRIVILEGES ON TABLE staging.league_seasons TO your_user;
-- GRANT USAGE, SELECT ON SEQUENCE staging.league_seasons_id_seq TO your_user; 