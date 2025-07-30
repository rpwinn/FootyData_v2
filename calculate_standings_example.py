#!/usr/bin/env python3
"""
Example script showing how to calculate league standings from match data
Since the /league-standings endpoint is broken, this is an alternative approach
"""

import os
import sys
from collections import defaultdict
from src.api.fbr_client import FBRClient

def calculate_standings_from_matches(league_id=9, season_id="2024-2025"):
    """
    Calculate league standings from match data
    This is an alternative when the /league-standings endpoint is broken
    """
    
    if not os.getenv('FBR_API_KEY'):
        print("❌ Error: FBR_API_KEY environment variable not set")
        return None
    
    client = FBRClient()
    
    print(f"🔍 Calculating standings for League {league_id}, Season {season_id}")
    print("=" * 60)
    
    try:
        # Get all matches for the league and season
        matches_response = client.get_matches(str(league_id), season_id)
        
        if "error" in matches_response:
            print(f"❌ Failed to get matches: {matches_response['error']}")
            return None
        
        matches = matches_response.get('data', [])
        print(f"📊 Found {len(matches)} matches")
        
        # Initialize standings tracking
        standings = defaultdict(lambda: {
            'team_name': '',
            'played': 0,
            'won': 0,
            'drawn': 0,
            'lost': 0,
            'goals_for': 0,
            'goals_against': 0,
            'points': 0
        })
        
        # Process each match
        for match in matches:
            home_team = match.get('home', 'Unknown')
            away_team = match.get('away', 'Unknown')
            home_score = match.get('home_team_score')
            away_score = match.get('away_team_score')
            
            # Skip matches without scores (future matches)
            if home_score is None or away_score is None:
                continue
            
            # Update home team stats
            standings[home_team]['team_name'] = home_team
            standings[home_team]['played'] += 1
            standings[home_team]['goals_for'] += home_score
            standings[home_team]['goals_against'] += away_score
            
            # Update away team stats
            standings[away_team]['team_name'] = away_team
            standings[away_team]['played'] += 1
            standings[away_team]['goals_for'] += away_score
            standings[away_team]['goals_against'] += home_score
            
            # Determine result and update points
            if home_score > away_score:
                # Home win
                standings[home_team]['won'] += 1
                standings[home_team]['points'] += 3
                standings[away_team]['lost'] += 1
            elif home_score < away_score:
                # Away win
                standings[away_team]['won'] += 1
                standings[away_team]['points'] += 3
                standings[home_team]['lost'] += 1
            else:
                # Draw
                standings[home_team]['drawn'] += 1
                standings[home_team]['points'] += 1
                standings[away_team]['drawn'] += 1
                standings[away_team]['points'] += 1
        
        # Convert to list and sort by points (descending)
        standings_list = list(standings.values())
        standings_list.sort(key=lambda x: (x['points'], x['goals_for'] - x['goals_against'], x['goals_for']), reverse=True)
        
        # Display standings
        print(f"\n🏆 League Standings (Calculated from Match Data)")
        print(f"League: {league_id}, Season: {season_id}")
        print("=" * 80)
        print(f"{'Pos':<4} {'Team':<25} {'P':<3} {'W':<3} {'D':<3} {'L':<3} {'GF':<3} {'GA':<3} {'GD':<4} {'Pts':<4}")
        print("-" * 80)
        
        for i, team in enumerate(standings_list, 1):
            if team['played'] > 0:  # Only show teams that have played
                goal_diff = team['goals_for'] - team['goals_against']
                print(f"{i:<4} {team['team_name']:<25} {team['played']:<3} {team['won']:<3} {team['drawn']:<3} {team['lost']:<3} {team['goals_for']:<3} {team['goals_against']:<3} {goal_diff:+<4} {team['points']:<4}")
        
        print("=" * 80)
        print(f"📊 Total teams with matches: {len([t for t in standings_list if t['played'] > 0])}")
        
        return standings_list
        
    except Exception as e:
        print(f"❌ Error calculating standings: {e}")
        return None

def main():
    """Main function to demonstrate standings calculation"""
    
    print("🎯 League Standings Calculator")
    print("This demonstrates how to calculate standings from match data")
    print("since the /league-standings endpoint is currently broken.\n")
    
    # Calculate standings for Premier League 2023-2024 (completed season)
    standings = calculate_standings_from_matches(9, "2023-2024")
    
    if standings:
        print("\n✅ Successfully calculated standings from match data!")
        print("This approach can be used as an alternative to the broken endpoint.")
    else:
        print("\n❌ Failed to calculate standings")

if __name__ == "__main__":
    main() 