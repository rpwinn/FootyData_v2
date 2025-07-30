#!/usr/bin/env python3
"""
Setup script for FootyData_v2

This script helps set up the project environment and database.
"""

import os
import sys
import subprocess

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print("✅ Python version compatible")
    return True

def install_dependencies():
    """Install project dependencies"""
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def check_environment():
    """Check if environment variables are set"""
    print("Checking environment variables...")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("FBR_API_KEY")
    database_url = os.getenv("DATABASE_URL")
    
    if not api_key:
        print("❌ FBR_API_KEY not set in .env file")
        print("   Please copy env.example to .env and add your FBR API key")
        return False
    
    if not database_url:
        print("❌ DATABASE_URL not set in .env file")
        print("   Please copy env.example to .env and add your database URL")
        return False
    
    print("✅ Environment variables configured")
    return True

def setup_database():
    """Set up the database schema"""
    print("Setting up database...")
    try:
        sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
        from database.setup import DatabaseSetup
        
        setup = DatabaseSetup()
        if setup.setup_database():
            print("✅ Database setup completed")
            return True
        else:
            print("❌ Database setup failed")
            return False
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return False

def test_api():
    """Test the FBR API connection"""
    print("Testing FBR API connection...")
    try:
        result = subprocess.run([sys.executable, "test_api.py"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ API connection test passed")
            return True
        else:
            print("❌ API connection test failed")
            print(result.stdout)
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up FootyData_v2...")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Check environment
    if not check_environment():
        print("\n📝 Setup Instructions:")
        print("1. Copy env.example to .env")
        print("2. Add your FBR API key to .env")
        print("3. Add your database URL to .env")
        print("4. Run this setup script again")
        return False
    
    # Setup database
    if not setup_database():
        return False
    
    # Test API
    if not test_api():
        return False
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Run data collection: python src/etl/data_collector.py")
    print("2. Check the database for collected data")
    print("3. Start building ETL processes")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 