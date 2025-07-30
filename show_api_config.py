#!/usr/bin/env python3
"""
Script to demonstrate the structured API endpoint configuration
"""

import json
from src.api.endpoint_config import (
    get_endpoint_config, 
    get_working_endpoints, 
    get_failing_endpoints,
    get_endpoint_status_summary,
    get_example_calls,
    format_api_call
)

def show_endpoint_info(endpoint_name: str):
    """Show detailed information about a specific endpoint"""
    config = get_endpoint_config(endpoint_name)
    if not config:
        print(f"❌ Endpoint '{endpoint_name}' not found")
        return
    
    print(f"\n🔍 {config.name} Endpoint")
    print("=" * 50)
    print(f"Path: {config.path}")
    print(f"Status: {config.status.value}")
    print(f"Description: {config.description}")
    
    print(f"\n📋 Parameters:")
    if config.required_params:
        print("  Required:")
        for param, param_type in config.required_params.items():
            print(f"    {param} ({param_type})")
    
    if config.optional_params:
        print("  Optional:")
        for param, param_type in config.optional_params.items():
            print(f"    {param} ({param_type})")
    
    print(f"\n📝 Example Request:")
    if config.example_request:
        print(f"  {format_api_call(endpoint_name, config.example_request)}")
        print(f"  Parameters: {json.dumps(config.example_request, indent=2)}")
    else:
        print(f"  {format_api_call(endpoint_name, {})}")
    
    print(f"\n📊 Example Response:")
    print(f"  {json.dumps(config.example_response, indent=2)}")
    
    if config.notes:
        print(f"\n💡 Notes: {config.notes}")

def show_status_summary():
    """Show summary of all endpoint statuses"""
    summary = get_endpoint_status_summary()
    
    print("\n📊 API Endpoint Status Summary")
    print("=" * 40)
    for status, count in summary.items():
        print(f"{status}: {count} endpoints")

def show_working_endpoints():
    """Show all working endpoints"""
    working = get_working_endpoints()
    
    print("\n✅ Working Endpoints")
    print("=" * 30)
    for config in working:
        print(f"• {config.name} ({config.path})")
        if config.required_params:
            params = ", ".join([f"{k}: {v}" for k, v in config.required_params.items()])
            print(f"  Required: {params}")

def show_failing_endpoints():
    """Show all failing endpoints"""
    failing = get_failing_endpoints()
    
    print("\n❌ Failing Endpoints")
    print("=" * 30)
    for config in failing:
        print(f"• {config.name} ({config.path})")
        print(f"  Issue: {config.notes}")

def show_example_calls():
    """Show example API calls for all endpoints"""
    examples = get_example_calls()
    
    print("\n📞 Example API Calls")
    print("=" * 30)
    for endpoint, call in examples.items():
        print(f"• {endpoint}: {call}")

def main():
    """Main function to demonstrate the API configuration"""
    
    print("🎯 FBR API Endpoint Configuration")
    print("This demonstrates the structured storage of API endpoint information")
    
    # Show status summary
    show_status_summary()
    
    # Show working endpoints
    show_working_endpoints()
    
    # Show failing endpoints
    show_failing_endpoints()
    
    # Show example calls
    show_example_calls()
    
    # Show detailed info for a specific endpoint
    print("\n" + "="*60)
    show_endpoint_info("teams")
    
    # Show another endpoint
    print("\n" + "="*60)
    show_endpoint_info("league_standings")

if __name__ == "__main__":
    main() 