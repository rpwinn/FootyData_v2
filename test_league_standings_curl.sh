#!/bin/bash

# Test script for league-standings endpoint using curl
# Make sure to set your API key: export FBR_API_KEY=your_api_key_here

API_KEY=${FBR_API_KEY}
BASE_URL="https://fbrapi.com"

if [ -z "$API_KEY" ]; then
    echo "❌ Error: FBR_API_KEY environment variable not set"
    echo "Please set your API key: export FBR_API_KEY=your_api_key_here"
    exit 1
fi

echo "🔍 Testing League Standings Endpoint with curl"
echo "================================================"

# Test 1: Premier League 2024-2025
echo "1. Testing Premier League 2024-2025:"
curl -s -X GET \
  "${BASE_URL}/league-standings/?league_id=9&season_id=2024-2025" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" | jq '.'

echo -e "\n" && echo "--------------------------------------------------"

# Test 2: Premier League current season (no season_id)
echo "2. Testing Premier League current season (no season_id):"
curl -s -X GET \
  "${BASE_URL}/league-standings/?league_id=9" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" | jq '.'

echo -e "\n" && echo "--------------------------------------------------"

# Test 3: La Liga 2024-2025
echo "3. Testing La Liga 2024-2025:"
curl -s -X GET \
  "${BASE_URL}/league-standings/?league_id=13&season_id=2024-2025" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" | jq '.'

echo -e "\n" && echo "--------------------------------------------------"

# Test 4: Premier League 2023-2024 (completed season)
echo "4. Testing Premier League 2023-2024 (completed season):"
curl -s -X GET \
  "${BASE_URL}/league-standings/?league_id=9&season_id=2023-2024" \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" | jq '.'

echo -e "\n" && echo "🎯 Summary:"
echo "If all tests return 500 Server Error, the endpoint is broken on the server side."
echo "If some tests work, we can identify the correct parameter format." 