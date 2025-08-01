-- Create Leagues Staging Table
-- Step 3: Create Staging Table

-- Create staging schema if it doesn't exist
CREATE SCHEMA IF NOT EXISTS staging;

-- Create leagues staging table
CREATE TABLE IF NOT EXISTS staging.leagues (
    id SERIAL PRIMARY KEY,
    country_code VARCHAR(3) NOT NULL,
    league_type VARCHAR(50) NOT NULL,
    league_id INTEGER NOT NULL,
    competition_name VARCHAR(200) NOT NULL,
    gender VARCHAR(1) NOT NULL,
    first_season VARCHAR(20),
    last_season VARCHAR(20),
    tier VARCHAR(10),
    raw_data JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_leagues_country_code 
ON staging.leagues(country_code);

CREATE INDEX IF NOT EXISTS idx_leagues_league_id 
ON staging.leagues(league_id);

CREATE INDEX IF NOT EXISTS idx_leagues_league_type 
ON staging.leagues(league_type);

CREATE INDEX IF NOT EXISTS idx_leagues_gender 
ON staging.leagues(gender);

CREATE INDEX IF NOT EXISTS idx_leagues_raw_data 
ON staging.leagues USING GIN(raw_data);

-- Create unique constraint to prevent duplicates
CREATE UNIQUE INDEX IF NOT EXISTS idx_leagues_unique 
ON staging.leagues(country_code, league_id);

-- Add comments for documentation
COMMENT ON TABLE staging.leagues IS 
'Staging table for leagues data from FBR API /leagues endpoint';

COMMENT ON COLUMN staging.leagues.country_code IS 
'3-letter country code (e.g., ENG, USA, BRA)';

COMMENT ON COLUMN staging.leagues.league_type IS 
'Classification of league type (domestic_leagues, domestic_cups, international_competitions, national_team_competitions)';

COMMENT ON COLUMN staging.leagues.league_id IS 
'Football reference league ID number';

COMMENT ON COLUMN staging.leagues.competition_name IS 
'Name of the league (e.g., Premier League, J1 League)';

COMMENT ON COLUMN staging.leagues.gender IS 
'Gender classification (M for male, F for female)';

COMMENT ON COLUMN staging.leagues.first_season IS 
'Season ID for earliest tracked season (e.g., 2014, 2021-2022)';

COMMENT ON COLUMN staging.leagues.last_season IS 
'Season ID for latest tracked season (e.g., 2024, 2023-2024)';

COMMENT ON COLUMN staging.leagues.tier IS 
'Level in country football pyramid (1st, 2nd, 3rd, 4th)';

COMMENT ON COLUMN staging.leagues.raw_data IS 
'Raw JSON response from API for debugging and data integrity';

-- Create trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_leagues_updated_at 
    BEFORE UPDATE ON staging.leagues 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column(); 