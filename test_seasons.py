#!/usr/bin/env python3
"""
Get sample seasons for testing
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from api.fbr_client import FBRClient

def get_sample_seasons():
    """Get a few sample seasons to test with"""
    client = FBRClient()
    
    print("Getting sample seasons for Premier League (league_id=9)...")
    seasons = client.get_league_seasons("9")
    
    if "error" not in seasons and seasons.get('data'):
        print(f"Found {len(seasons['data'])} seasons")
        print("\nFirst 10 seasons:")
        for i, season in enumerate(seasons['data'][:10]):
            print(f"{i+1}. {season['season_id']} - {season['competition_name']}")
        
        print("\nLast 10 seasons:")
        for i, season in enumerate(seasons['data'][-10:]):
            print(f"{len(seasons['data'])-9+i}. {season['season_id']} - {season['competition_name']}")

if __name__ == "__main__":
    get_sample_seasons() 