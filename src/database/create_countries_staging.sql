-- Create Countries Staging Table
-- Step 3: Create Staging Table

-- Create staging schema if it doesn't exist
CREATE SCHEMA IF NOT EXISTS staging;

-- Create countries staging table
CREATE TABLE IF NOT EXISTS staging.countries (
    id SERIAL PRIMARY KEY,
    country_name VARCHAR(100) NOT NULL,
    country_code VARCHAR(3) UNIQUE NOT NULL,
    governing_body VARCHAR(20) NOT NULL,
    num_clubs INTEGER DEFAULT 0,
    num_players INTEGER DEFAULT 0,
    national_teams TEXT[] DEFAULT '{}',
    raw_data JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_countries_country_code 
ON staging.countries(country_code);

CREATE INDEX IF NOT EXISTS idx_countries_governing_body 
ON staging.countries(governing_body);

CREATE INDEX IF NOT EXISTS idx_countries_raw_data 
ON staging.countries USING GIN(raw_data);

-- Add comments for documentation
COMMENT ON TABLE staging.countries IS 
'Staging table for countries data from FBR API /countries endpoint';

COMMENT ON COLUMN staging.countries.country_name IS 
'Full country name (e.g., Afghanistan)';

COMMENT ON COLUMN staging.countries.country_code IS 
'3-letter ISO country code (e.g., AFG)';

COMMENT ON COLUMN staging.countries.governing_body IS 
'Football governing body (e.g., AFC, UEFA, CONCACAF)';

COMMENT ON COLUMN staging.countries.num_clubs IS 
'Number of clubs in the country';

COMMENT ON COLUMN staging.countries.num_players IS 
'Number of players tracked in the country';

COMMENT ON COLUMN staging.countries.national_teams IS 
'Types of national teams (M for men, F for women)';

COMMENT ON COLUMN staging.countries.raw_data IS 
'Raw JSON response from API for debugging and data integrity';

-- Create trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_countries_updated_at 
    BEFORE UPDATE ON staging.countries 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column(); 