# /leagues Endpoint Documentation

## Overview
Endpoint to retrieve meta-data for all unique leagues associated with a specified country. Data is retrieved based on a country's three-letter country code used as identification within football reference.

## Endpoint Details
- **URL**: `/leagues`
- **Method**: GET
- **Base URL**: https://fbrapi.com

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `country_code` | string | Yes | Three-letter code used by football reference to identify specific country |

## Response Structure

### Success Response (200)
```json
{
    "data": [
        {
            "league_type": "domestic_leagues",
            "leagues": [
                {
                    "league_id": 25,
                    "competition_name": "J1 League",
                    "gender": "M",
                    "first_season": "2014",
                    "last_season": "2024",
                    "tier": "1st"
                }
            ]
        }
    ]
}
```

### Error Response (4xx/5xx)
```json
{
    "error": "Error message description"
}
```

## Field Descriptions

### Top-Level Fields
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `data` | array | Array of league type objects | `[{league_type: "domestic_leagues", leagues: [...]}]` |

### League Type Object Fields
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `league_type` | string | Classification of league type | "domestic_leagues", "international_competitions" |
| `leagues` | array | Array of league objects | `[{league_id: 25, competition_name: "J1 League", ...}]` |

### League Object Fields
| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `league_id` | integer | Football reference league ID number | 25, 893, 49 |
| `competition_name` | string | Name of the league | "J1 League", "AFC Champions League" |
| `gender` | string | Gender classification | "M" (male), "F" (female) |
| `first_season` | string | Season ID for earliest tracked season | "2014", "2021-2022" |
| `last_season` | string | Season ID for latest tracked season | "2024", "2023-2024" |
| `tier` | string | Level in country's football pyramid | "1st", "2nd" |

## League Classifications

### League Types
- **domestic_leagues**: Club-level league competitions occurring only within the specified country
- **domestic_cups**: Club-level cup competitions occurring only within the specified country
- **international_competitions**: Club-level competitions occurring between teams in the specified country and teams from other countries
- **national_team_competitions**: National team-level competitions where the specified country's national team participated

### Gender Types
- **M**: Male competitions
- **F**: Female competitions

### Tier Levels
- **1st**: Top tier of the football pyramid
- **2nd**: Second tier of the football pyramid
- **3rd**: Third tier of the football pyramid
- **4th**: Fourth tier of the football pyramid

## Usage Examples

### Get All Leagues for a Country
```bash
GET /leagues?country_code=JPN
```

### Get All Leagues for England
```bash
GET /leagues?country_code=ENG
```

### Using curl
```bash
curl -H "X-API-Key: YOUR_API_KEY" \
     -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
     "https://fbrapi.com/leagues/?country_code=ENG"
```

### Using Python
```python
import requests

headers = {
    'X-API-Key': 'YOUR_API_KEY',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
}

# Get all leagues for England
response = requests.get('https://fbrapi.com/leagues/?country_code=ENG', headers=headers)
england_leagues = response.json()

# Get all leagues for Japan
response = requests.get('https://fbrapi.com/leagues/?country_code=JPN', headers=headers)
japan_leagues = response.json()
```

### Using JavaScript/Fetch
```javascript
fetch('https://fbrapi.com/leagues/?country_code=ENG', {
    headers: {
        'X-API-Key': 'YOUR_API_KEY',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
})
.then(response => response.json())
.then(data => {
    console.log('England Leagues:', data.data);
});
```

## Data Volume
- **Leagues per Country**: Varies by country (typically 5-50 leagues)
- **Update Frequency**: Static (rarely changes)
- **Data Size**: Small to medium (few KB per request)

## Dependencies
- **Requires**: `/countries` endpoint (for country_code validation)
- **Used by**: `/league-seasons` endpoint (league_id parameter)

## Notes

Meta-data, when available, includes:

- **league_id (int)**: Football reference league ID number.
- **competition_name (str)**: Name of the league.
- **gender (str)**: 'M' for male or 'F' for female.
- **first_season (str)**: Season ID for the earliest season that the league is tracked in Football Reference.
- **last_season (str)**: Season ID for the latest season that the league is tracked in Football Reference.
- **tier (str)**: Determines the level on the country's football pyramid to which the competition belongs.

### Additional Notes
- League IDs are unique across the entire FBR system
- Some leagues may not have tier information (especially international competitions)
- Season formats vary (e.g., "2014", "2021-2022")
- Not all countries have all league types
- International competitions may not have tier or season information 