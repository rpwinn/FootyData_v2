#!/usr/bin/env python3
"""
Collection Configuration Management
Handles loading and validation of collection scopes and configurations
"""

import os
import yaml
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

@dataclass
class TimePeriod:
    """Represents a time period for data collection"""
    start_season: Optional[str] = None
    end_season: Optional[str] = None
    pattern: Optional[str] = None  # Regex pattern for season matching
    description: Optional[str] = None
    
    def is_valid(self) -> bool:
        """Validate time period configuration"""
        # Must have either start/end seasons or a pattern
        if not self.start_season and not self.end_season and not self.pattern:
            return False
        return True
    
    def matches_season(self, season_id: str) -> bool:
        """Check if a season ID matches this time period"""
        if self.pattern:
            import re
            return bool(re.match(self.pattern, season_id))
        
        # Simple range checking
        if self.start_season and self.end_season:
            return self.start_season <= season_id <= self.end_season
        elif self.start_season:
            return season_id >= self.start_season
        elif self.end_season:
            return season_id <= self.end_season
        
        return True  # No constraints

@dataclass
class CollectionScope:
    """Represents a collection scope configuration"""
    name: str
    description: str
    countries: Optional[List[str]] = None
    leagues: Optional[List[str]] = None
    time_period: Optional[TimePeriod] = None
    priority: str = "medium"
    
    def is_valid(self) -> bool:
        """Validate scope configuration"""
        if not self.name or not self.description:
            return False
        
        # Must have either countries or leagues defined (null is valid for "all")
        # Note: countries=None means "all countries", countries=[] means "no countries"
        if self.countries is not None and not self.countries and not self.leagues:
            return False
            
        # Validate time period if present
        if self.time_period and not self.time_period.is_valid():
            return False
            
        return True

class CollectionConfig:
    """Manages collection configuration and scopes"""
    
    def __init__(self, config_path: str = "config/collection_config.yaml"):
        """Initialize configuration manager"""
        self.config_path = config_path
        self.config = self._load_config()
        self.scopes = self._load_scopes()
        self.defaults = self.config.get('defaults', {})
        self.error_handling = self.config.get('error_handling', {})
        self.progress = self.config.get('progress', {})
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"❌ Configuration file not found: {self.config_path}")
            return {}
        except yaml.YAMLError as e:
            print(f"❌ Error parsing configuration file: {e}")
            return {}
    
    def _load_scopes(self) -> Dict[str, CollectionScope]:
        """Load and validate collection scopes"""
        scopes = {}
        scope_configs = self.config.get('collection_scopes', {})
        time_periods = self.config.get('time_periods', {})
        
        for scope_name, scope_config in scope_configs.items():
            # Parse time period
            time_period_config = scope_config.get('time_period')
            time_period = None
            
            if time_period_config:
                if isinstance(time_period_config, str):
                    # Reference to predefined time period
                    if time_period_config in time_periods:
                        tp_config = time_periods[time_period_config]
                        time_period = TimePeriod(
                            start_season=tp_config.get('start_season'),
                            end_season=tp_config.get('end_season'),
                            pattern=tp_config.get('pattern'),
                            description=tp_config.get('description')
                        )
                    else:
                        print(f"⚠️ Unknown time period reference: {time_period_config}")
                else:
                    # Inline time period configuration
                    time_period = TimePeriod(
                        start_season=time_period_config.get('start_season'),
                        end_season=time_period_config.get('end_season'),
                        pattern=time_period_config.get('pattern'),
                        description=time_period_config.get('description')
                    )
            
            # Create scope object
            scope = CollectionScope(
                name=scope_name,
                description=scope_config.get('description', ''),
                countries=scope_config.get('countries'),
                leagues=scope_config.get('leagues'),
                time_period=time_period,
                priority=scope_config.get('priority', 'medium')
            )
            
            # Validate scope
            if scope.is_valid():
                scopes[scope_name] = scope
            else:
                print(f"⚠️ Invalid scope configuration: {scope_name}")
        
        return scopes
    
    def get_scope(self, scope_name: str) -> Optional[CollectionScope]:
        """Get a specific scope by name"""
        return self.scopes.get(scope_name)
    
    def list_scopes(self) -> List[str]:
        """List all available scope names"""
        return list(self.scopes.keys())
    
    def validate_scope(self, scope_name: str) -> bool:
        """Validate if a scope exists and is properly configured"""
        if scope_name not in self.scopes:
            print(f"❌ Scope not found: {scope_name}")
            return False
        
        scope = self.scopes[scope_name]
        if not scope.is_valid():
            print(f"❌ Invalid scope configuration: {scope_name}")
            return False
        
        return True
    
    def create_custom_scope(self, 
                          name: str,
                          description: str,
                          countries: Optional[List[str]] = None,
                          leagues: Optional[List[str]] = None,
                          time_period: Optional[TimePeriod] = None,
                          priority: str = "medium") -> CollectionScope:
        """Create a custom scope configuration"""
        
        scope = CollectionScope(
            name=name,
            description=description,
            countries=countries,
            leagues=leagues,
            time_period=time_period,
            priority=priority
        )
        
        if not scope.is_valid():
            raise ValueError(f"Invalid scope configuration: {name}")
        
        return scope
    
    def get_defaults(self) -> Dict[str, Any]:
        """Get default configuration settings"""
        return self.defaults
    
    def get_error_handling(self) -> Dict[str, Any]:
        """Get error handling configuration"""
        return self.error_handling
    
    def get_progress_config(self) -> Dict[str, Any]:
        """Get progress tracking configuration"""
        return self.progress
    
    def get_time_period(self, time_period_name: str) -> Optional[TimePeriod]:
        """Get a time period by name"""
        time_periods = self.config.get('time_periods', {})
        
        if time_period_name in time_periods:
            tp_config = time_periods[time_period_name]
            return TimePeriod(
                start_season=tp_config.get('start_season'),
                end_season=tp_config.get('end_season'),
                pattern=tp_config.get('pattern'),
                description=tp_config.get('description')
            )
        
        return None
    
    def print_available_scopes(self):
        """Print all available scopes with descriptions"""
        print("📋 Available Collection Scopes:")
        print("=" * 50)
        
        for scope_name, scope in self.scopes.items():
            print(f"\n🔸 {scope_name}")
            print(f"   Description: {scope.description}")
            print(f"   Priority: {scope.priority}")
            
            if scope.countries:
                print(f"   Countries: {', '.join(scope.countries)}")
            elif scope.countries is None:
                print(f"   Countries: All countries")
            
            if scope.leagues:
                print(f"   Leagues: {', '.join(scope.leagues)}")
            
            if scope.time_period:
                tp = scope.time_period
                if tp.description:
                    print(f"   Time Period: {tp.description}")
                elif tp.start_season and tp.end_season:
                    print(f"   Time Period: {tp.start_season} to {tp.end_season}")
                elif tp.start_season:
                    print(f"   Time Period: {tp.start_season} onwards")
                elif tp.end_season:
                    print(f"   Time Period: Up to {tp.end_season}")
                else:
                    print(f"   Time Period: All time periods")

def load_collection_config(config_path: str = "config/collection_config.yaml") -> CollectionConfig:
    """Convenience function to load collection configuration"""
    return CollectionConfig(config_path)

if __name__ == "__main__":
    # Test the configuration loader
    config = load_collection_config()
    config.print_available_scopes()
    
    # Test season matching
    print("\n🧪 Testing Season Matching:")
    print("=" * 30)
    
    test_seasons = ["2020", "2020-2021", "2021", "2021-2022", "2022-2023", "2023-2024", "2024", "2024-2025", "2025-2026"]
    
    for scope_name, scope in config.scopes.items():
        if scope.time_period:
            print(f"\n🔸 {scope_name} ({scope.time_period.description}):")
            for season in test_seasons:
                matches = scope.time_period.matches_season(season)
                status = "✅" if matches else "❌"
                print(f"   {status} {season}") 