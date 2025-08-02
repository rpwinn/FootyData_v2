#!/usr/bin/env python3
"""
Endpoint Blacklist Utility
Handles tracking and checking of broken endpoints to avoid unnecessary API calls
"""

import os
import yaml
from typing import Dict, List, Optional, Set
from datetime import datetime, timedelta

class EndpointBlacklist:
    """Manages endpoint blacklist to avoid calling broken endpoints"""
    
    def __init__(self, config_path: str = "config/collection_config.yaml"):
        """Initialize the blacklist manager"""
        self.config_path = config_path
        self.blacklist_config = self._load_blacklist_config()
        self.blacklisted_endpoints = self._build_blacklist()
    
    def _load_blacklist_config(self) -> Dict:
        """Load blacklist configuration from config file"""
        try:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)
                return config.get('endpoint_blacklist', {})
        except Exception as e:
            print(f"❌ Error loading blacklist config: {e}")
            return {}
    
    def _build_blacklist(self) -> Dict[str, Dict[str, Set]]:
        """Build blacklist from configuration with flexible parameter support"""
        blacklist = {}
        
        if not self.blacklist_config.get('enabled', False):
            return blacklist
        
        permanent_failures = self.blacklist_config.get('permanent_failures', [])
        
        for failure in permanent_failures:
            endpoint = failure.get('endpoint')
            
            if not endpoint:
                continue
                
            if endpoint not in blacklist:
                blacklist[endpoint] = {}
            
            # Support multiple parameter types
            for param_type, values in failure.items():
                if param_type in ['league_ids', 'season_ids', 'team_ids', 'player_ids']:
                    if values:  # Only add if values exist
                        blacklist[endpoint][param_type] = set(values)
        
        return blacklist
    
    def is_blacklisted(self, endpoint: str, **kwargs) -> bool:
        """
        Check if an endpoint/parameter combination is blacklisted
        
        Args:
            endpoint: The API endpoint (e.g., "league-seasons")
            **kwargs: Parameters to check (league_id, season_id, team_id, player_id, etc.)
            
        Returns:
            bool: True if blacklisted, False otherwise
        """
        if not self.blacklist_config.get('enabled', False):
            return False
        
        # Check if endpoint is blacklisted
        if endpoint not in self.blacklisted_endpoints:
            return False
        
        endpoint_blacklist = self.blacklisted_endpoints[endpoint]
        
        # Check each parameter type
        for param_name, param_value in kwargs.items():
            param_type = f"{param_name}s"  # Convert league_id -> league_ids
            
            if param_type in endpoint_blacklist:
                if param_value in endpoint_blacklist[param_type]:
                    return True
        
        return False
    
    def get_blacklisted_leagues(self, endpoint: str) -> Set[int]:
        """Get all blacklisted league IDs for an endpoint"""
        return self.blacklisted_endpoints.get(endpoint, {}).get('league_ids', set())
    
    def get_blacklisted_seasons(self, endpoint: str) -> Set[str]:
        """Get all blacklisted season IDs for an endpoint"""
        return self.blacklisted_endpoints.get(endpoint, {}).get('season_ids', set())
    
    def get_blacklisted_teams(self, endpoint: str) -> Set[int]:
        """Get all blacklisted team IDs for an endpoint"""
        return self.blacklisted_endpoints.get(endpoint, {}).get('team_ids', set())
    
    def get_blacklist_summary(self) -> Dict[str, Dict[str, List]]:
        """Get summary of all blacklisted endpoints"""
        summary = {}
        for endpoint, params in self.blacklisted_endpoints.items():
            summary[endpoint] = {}
            for param_type, values in params.items():
                summary[endpoint][param_type] = list(values)
        return summary
    
    def print_blacklist_summary(self):
        """Print a summary of blacklisted endpoints"""
        if not self.blacklist_config.get('enabled', False):
            print("ℹ️ Endpoint blacklist is disabled")
            return
        
        summary = self.get_blacklist_summary()
        if not summary:
            print("ℹ️ No endpoints are currently blacklisted")
            return
        
        print("🚫 Blacklisted Endpoints:")
        print("=" * 40)
        for endpoint, params in summary.items():
            print(f"📡 {endpoint}:")
            for param_type, values in params.items():
                print(f"   {param_type}: {sorted(values)}")
            print()

def load_endpoint_blacklist(config_path: str = "config/collection_config.yaml") -> EndpointBlacklist:
    """Load endpoint blacklist from configuration"""
    return EndpointBlacklist(config_path) 