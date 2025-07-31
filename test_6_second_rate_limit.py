#!/usr/bin/env python3
"""
Test 6-second rate limit to see if it fixes 500 errors
"""

import os
import time
from dotenv import load_dotenv

# Add src to path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from api.fbr_client import FBRClient

def test_6_second_rate_limit():
    """Test the /leagues endpoint with 6-second delays"""
    
    print("🧪 Testing 6-Second Rate Limit")
    print("=" * 35)
    
    # Load environment variables
    load_dotenv()
    api_key = os.getenv("FBR_API_KEY")
    
    if not api_key:
        print("❌ FBR_API_KEY not found in .env file")
        return False
    
    # Initialize API client (will now use 6-second rate limit from config)
    client = FBRClient()
    
    # Test with countries that were failing (around where it stopped)
    test_countries = ["COK", "COL", "COM", "CPV", "CRC", "CRO"]
    
    for i, country_code in enumerate(test_countries, 1):
        print(f"\n📡 Testing {country_code} ({i}/{len(test_countries)})...")
        
        try:
            start_time = time.time()
            response = client.get_leagues(country_code)
            api_time = time.time() - start_time
            
            if "error" in response:
                print(f"   ❌ API Error: {response['error']}")
            else:
                leagues_data = response.get('data', [])
                total_leagues = sum(len(league_type_obj.get('leagues', [])) for league_type_obj in leagues_data)
                print(f"   ✅ Success! {total_leagues} leagues found in {api_time:.2f}s")
                
                for league_type_obj in leagues_data:
                    league_type = league_type_obj.get('league_type', 'Unknown')
                    leagues = league_type_obj.get('leagues', [])
                    print(f"      • {league_type}: {len(leagues)} leagues")
            
            # The FBRClient will automatically handle the 6-second rate limit
            print(f"   ⏱️  Rate limit applied automatically by client...")
            
        except Exception as e:
            print(f"   ❌ Exception: {e}")
    
    return True

if __name__ == "__main__":
    test_6_second_rate_limit() 