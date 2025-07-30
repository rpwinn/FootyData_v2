#!/usr/bin/env python3
"""
Example showing how to use the structured API configuration
"""

import json
from src.api.fbr_client import FBRClient

def demonstrate_api_usage():
    """Demonstrate how to use the API with structured configuration"""
    
    client = FBRClient()
    
    print("🎯 FBR API Usage Examples")
    print("=" * 50)
    
    # Example 1: Get endpoint information
    print("\n1. Getting endpoint information:")
    teams_info = client.get_endpoint_info("teams")
    if teams_info:
        print(f"   Endpoint: {teams_info['name']}")
        print(f"   Status: {teams_info['status']}")
        print(f"   Required params: {teams_info['required_params']}")
        print(f"   Description: {teams_info['description']}")
    
    # Example 2: Format API calls
    print("\n2. Formatting API calls:")
    params = {"team_id": "19538871", "season_id": "2024-2025"}
    formatted_call = client.format_api_call("teams", params)
    print(f"   {formatted_call}")
    
    # Example 3: Get working endpoints
    print("\n3. Working endpoints:")
    working = client.get_working_endpoints()
    for endpoint in working[:5]:  # Show first 5
        print(f"   • {endpoint}")
    
    # Example 4: Get failing endpoints
    print("\n4. Failing endpoints:")
    failing = client.get_failing_endpoints()
    for endpoint in failing:
        print(f"   • {endpoint}")
    
    # Example 5: Make an actual API call with proper parameters
    print("\n5. Making API calls with proper parameters:")
    
    # Get the endpoint config to ensure we use correct parameters
    teams_config = client.get_endpoint_info("teams")
    if teams_config:
        print(f"   Making call to {teams_config['name']} endpoint...")
        
        # Use the example parameters from the config
        example_params = teams_config['example_request']
        print(f"   Using parameters: {example_params}")
        
        try:
            # This would make the actual API call
            # response = client.get_teams(example_params['team_id'], example_params['season_id'])
            print(f"   ✅ API call would be made with correct parameters")
        except Exception as e:
            print(f"   ❌ API call failed: {e}")

def show_parameter_validation():
    """Show how to validate parameters against endpoint config"""
    
    client = FBRClient()
    
    print("\n🔍 Parameter Validation Example")
    print("=" * 40)
    
    # Example: Validate parameters for teams endpoint
    teams_config = client.get_endpoint_info("teams")
    if teams_config:
        print(f"Teams endpoint requires: {teams_config['required_params']}")
        print(f"Teams endpoint accepts: {teams_config['optional_params']}")
        
        # Example of validating parameters
        test_params = {"team_id": "19538871", "season_id": "2024-2025"}
        print(f"\nTesting parameters: {test_params}")
        
        # Check if all required parameters are present
        required_params = teams_config['required_params'].keys()
        missing_params = [param for param in required_params if param not in test_params]
        
        if missing_params:
            print(f"❌ Missing required parameters: {missing_params}")
        else:
            print(f"✅ All required parameters present")
            
        # Check if all provided parameters are valid
        all_valid_params = {**teams_config['required_params'], **teams_config['optional_params']}
        invalid_params = [param for param in test_params.keys() if param not in all_valid_params]
        
        if invalid_params:
            print(f"❌ Invalid parameters: {invalid_params}")
        else:
            print(f"✅ All parameters are valid")

def main():
    """Main function"""
    
    print("📚 FBR API Structured Configuration Usage")
    print("This shows how to use the structured API endpoint configuration")
    
    # Demonstrate basic usage
    demonstrate_api_usage()
    
    # Show parameter validation
    show_parameter_validation()
    
    print("\n🎉 Benefits of this approach:")
    print("• Centralized endpoint configuration")
    print("• Type-safe parameter validation")
    print("• Easy to maintain and update")
    print("• Consistent API call formatting")
    print("• Clear documentation of working vs failing endpoints")

if __name__ == "__main__":
    main() 