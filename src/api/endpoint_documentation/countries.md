# /countries Endpoint Documentation

## Overview
Endpoint to retrieve meta-data for all available countries that have either domestic or international football teams tracked by football reference.

## Endpoint Details
- **URL**: `/countries`
- **Method**: GET
- **Base URL**: https://fbrapi.com
- **Rate Limit**: 1 request per 3 seconds

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `country` | string | No | Name of the country for which to retrieve data |

## Response Structure

### Success Response (200)
```json
{
    "data": [
        {
            "country": "Afghanistan",
            "country_code": "AFG",
            "governing_body": "AFC",
            "#_clubs": 0,
            "#_players": 194,
            "national_teams": ["M", "F"]
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

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `country` | string | Full country name | "Afghanistan" |
| `country_code` | string | 3-letter ISO country code | "AFG" |
| `governing_body` | string | Football governing body | "AFC", "UEFA", "CONCACAF" |
| `#_clubs` | integer | Number of clubs in the country | 0, 17, 500 |
| `#_players` | integer | Number of players tracked | 194, 543, 10000 |
| `national_teams` | array[string] | Types of national teams | ["M"], ["F"], ["M", "F"] |

## Governing Bodies
- **AFC**: Asian Football Confederation
- **UEFA**: Union of European Football Associations
- **CONCACAF**: Confederation of North, Central America and Caribbean Association Football
- **CAF**: Confederation of African Football
- **CONMEBOL**: South American Football Confederation
- **OFC**: Oceania Football Confederation

## National Team Types
- **M**: Men's national team
- **F**: Women's national team

## Usage Examples

### Get All Countries
```bash
GET /countries
```

### Get Specific Country
```bash
GET /countries?country=England
```

## Data Volume
- **Total Countries**: ~225 countries
- **Update Frequency**: Static (rarely changes)
- **Data Size**: Small (few KB per request)

## Dependencies
- **Used by**: `/leagues` endpoint (country_code parameter)
- **Dependencies**: None

## Notes

Meta-data, when available, includes:

- **country (str)**: Name of the country.
- **country_code (str)**: Three-letter country abbreviation, used by FbrefLeaguesScraper to identify league information related to the country.
- **governing_body (str)**: Abbreviation of the country's governing body, typically based on geographical location.
- **#_clubs (int)**: Number of club teams in the country that are covered by Football Reference.
- **#_players (int)**: Number of players from the country that are covered by Football Reference.
- **national_teams (list of str)**: National teams from the country that are covered by Football Reference.

### Additional Notes
- Country codes follow ISO 3166-1 alpha-3 standard
- Some countries may have 0 clubs but still have players tracked
- National teams array indicates which gender teams exist
- Governing body indicates continental federation membership 