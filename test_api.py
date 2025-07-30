#!/usr/bin/env python3
"""
Test script for FBR API client
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from api.fbr_client import FBRClient

def test_api_connection():
    """Test the FBR API connection"""
    print("Testing FBR API connection...")
    
    try:
        client = FBRClient()
        
        # Test connection
        if client.test_connection():
            print("✅ API connection successful!")
        else:
            print("❌ API connection failed!")
            return False
        
        # Test countries endpoint
        print("\nTesting countries endpoint...")
        countries = client.get_countries()
        if "error" not in countries:
            print(f"✅ Countries endpoint working! Found {len(countries.get('data', []))} countries")
        else:
            print(f"❌ Countries endpoint failed: {countries.get('error')}")
            return False
        
        # Test leagues endpoint for England
        print("\nTesting leagues endpoint for England...")
        leagues = client.get_leagues("ENG")
        if "error" not in leagues:
            print(f"✅ Leagues endpoint working! Found {len(leagues.get('data', []))} leagues")
        else:
            print(f"❌ Leagues endpoint failed: {leagues.get('error')}")
            return False
        
        print("\n🎉 All tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

if __name__ == "__main__":
    test_api_connection() 