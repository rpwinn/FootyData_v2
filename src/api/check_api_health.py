#!/usr/bin/env python3
"""
API Health Check Script
Checks if the FBR API is online and responding
"""

import os
import sys
import time
from dotenv import load_dotenv

# Add src to path
sys.path.append('src')

from api.fbr_client import FBRClient

def check_api_health():
    """Check if the FBR API is online and responding"""
    load_dotenv()
    
    print("🏥 FBR API Health Check")
    print("=" * 40)
    
    try:
        client = FBRClient()
        print("✅ FBR Client initialized")
        
        # Track results
        results = {}
        overall_healthy = True
        
        # Test 1: Countries endpoint (all countries)
        print("\n📡 Testing countries endpoint (all countries)...")
        start_time = time.time()
        countries_response = client.get_countries()
        end_time = time.time()
        
        if "error" in countries_response:
            print(f"❌ Countries API failed: {countries_response['error']}")
            # Extract HTTP status code if available
            error_msg = countries_response['error']
            if "500" in error_msg:
                print(f"   🔍 HTTP Status: 500 (Internal Server Error)")
            elif "404" in error_msg:
                print(f"   🔍 HTTP Status: 404 (Not Found)")
            elif "403" in error_msg:
                print(f"   🔍 HTTP Status: 403 (Forbidden)")
            elif "401" in error_msg:
                print(f"   🔍 HTTP Status: 401 (Unauthorized)")
            else:
                print(f"   🔍 HTTP Status: Unknown")
            results['countries'] = {'status': 'failed', 'error': countries_response['error']}
            overall_healthy = False
        else:
            print(f"✅ Countries API working: {len(countries_response.get('data', []))} countries")
            print(f"⏱️ Response time: {end_time - start_time:.2f} seconds")
            results['countries'] = {'status': 'working', 'response_time': end_time - start_time}
        
        # Test 2: Leagues endpoint (ENG example)
        print("\n📡 Testing leagues endpoint (ENG example)...")
        start_time = time.time()
        eng_leagues_response = client.get_leagues("ENG")
        end_time = time.time()
        
        if "error" in eng_leagues_response:
            print(f"❌ Leagues API failed: {eng_leagues_response['error']}")
            results['leagues'] = {'status': 'failed', 'error': eng_leagues_response['error']}
            overall_healthy = False
        else:
            print(f"✅ Leagues API working: {len(eng_leagues_response.get('data', []))} league types")
            print(f"⏱️ Response time: {end_time - start_time:.2f} seconds")
            results['leagues'] = {'status': 'working', 'response_time': end_time - start_time}
        
        # Test 3: League seasons endpoint
        print("\n📡 Testing league seasons endpoint (League 9)...")
        start_time = time.time()
        seasons_response = client.get_league_seasons(9)
        end_time = time.time()
        
        if "error" in seasons_response:
            print(f"❌ League seasons API failed: {seasons_response['error']}")
            results['league_seasons'] = {'status': 'failed', 'error': seasons_response['error']}
            overall_healthy = False
        else:
            print(f"✅ League seasons API working: {len(seasons_response.get('data', []))} seasons")
            print(f"⏱️ Response time: {end_time - start_time:.2f} seconds")
            results['league_seasons'] = {'status': 'working', 'response_time': end_time - start_time}
        
        # Summary
        print(f"\n📊 API Health Summary:")
        print("=" * 30)
        working_count = sum(1 for result in results.values() if result['status'] == 'working')
        failed_count = sum(1 for result in results.values() if result['status'] == 'failed')
        
        print(f"✅ Working endpoints: {working_count}")
        print(f"❌ Failed endpoints: {failed_count}")
        print(f"📈 Success rate: {working_count}/{len(results)} ({working_count/len(results)*100:.1f}%)")
        
        if overall_healthy:
            print(f"\n🎉 All API endpoints are working!")
        else:
            print(f"\n⚠️ Some API endpoints are failing")
        
        return overall_healthy
        
    except Exception as e:
        print(f"❌ Error during API health check: {e}")
        return False

def main():
    """Main function"""
    print("Starting API health check...")
    
    is_healthy = check_api_health()
    
    if is_healthy:
        print("\n✅ API is healthy - you can run collection scripts")
        return 0
    else:
        print("\n❌ API is unhealthy - collection scripts will fail")
        print("💡 Wait for API to recover before running collection scripts")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 