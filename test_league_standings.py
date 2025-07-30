#!/usr/bin/env python3
"""
Simple script to test the league-standings endpoint
"""

import os
import sys
import json
from src.api.fbr_client import FBRClient

def test_league_standings():
    """Test the league-standings endpoint with various parameters"""
    
    # Check if API key is set
    if not os.getenv('FBR_API_KEY'):
        print("❌ Error: FBR_API_KEY environment variable not set")
        print("Please set your API key: export FBR_API_KEY=your_api_key_here")
        return False
    
    client = FBRClient()
    
    print("🔍 Testing League Standings Endpoint")
    print("=" * 50)
    
    # Test cases with different parameters
    test_cases = [
        {
            "name": "Premier League 2024-2025 (with season)",
            "league_id": 9,
            "season_id": "2024-2025"
        },
        {
            "name": "Premier League Current Season (no season)",
            "league_id": 9,
            "season_id": None
        },
        {
            "name": "La Liga 2024-2025 (with season)",
            "league_id": 13,
            "season_id": "2024-2025"
        },
        {
            "name": "La Liga Current Season (no season)",
            "league_id": 13,
            "season_id": None
        },
        {
            "name": "Premier League 2023-2024 (completed season)",
            "league_id": 9,
            "season_id": "2023-2024"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. Testing: {test_case['name']}")
        print(f"   Parameters: league_id={test_case['league_id']}, season_id={test_case['season_id']}")
        
        try:
            # Make the API call
            if test_case['season_id']:
                response = client.get_league_standings(test_case['league_id'], test_case['season_id'])
            else:
                response = client.get_league_standings(test_case['league_id'])
            
            # Check if successful
            if "error" not in response:
                print("   ✅ SUCCESS!")
                print(f"   Response keys: {list(response.keys())}")
                if 'data' in response:
                    print(f"   Number of teams: {len(response['data'])}")
                    if response['data']:
                        print(f"   Sample team: {response['data'][0].get('team_name', 'Unknown')}")
                elif 'outfield' in response or 'keepers' in response:
                    print("   Response contains player data structure")
                else:
                    print("   Response structure:", list(response.keys()))
            else:
                print(f"   ❌ FAILED: {response.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"   ❌ EXCEPTION: {e}")
        
        print("-" * 50)
    
    print("\n🎯 Summary:")
    print("If all tests return 500 Server Error, the endpoint is broken on the server side.")
    print("If some tests work, we can identify the correct parameter format.")

if __name__ == "__main__":
    test_league_standings() 