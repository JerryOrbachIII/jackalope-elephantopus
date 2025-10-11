#!/usr/bin/env python3
"""
Startup script for Stock Prediction Tracker
Checks dependencies and starts the Streamlit application
"""

import sys
import subprocess
import os

def check_python_version():
    """Check if Python version is 3.10 or higher"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print(f"✗ Python 3.10+ required. Current version: {version.major}.{version.minor}")
        return False
    print(f"✓ Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def check_dependencies():
    """Check if all required packages are installed"""
    required_packages = [
        'streamlit',
        'pandas',
        'yfinance',
        'feedparser',
        'requests',
        'beautifulsoup4',
        'pytz'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"✗ Missing packages: {', '.join(missing_packages)}")
        print("\nInstalling missing packages...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
        return True
    
    print("✓ All dependencies installed")
    return True

def start_application():
    """Start the Streamlit application"""
    print("\nStarting Stock Prediction Tracker...")
    print("="*50)
    
    try:
        # Run streamlit
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 'app.py',
            '--server.headless', 'true',
            '--browser.gatherUsageStats', 'false'
        ])
    except KeyboardInterrupt:
        print("\n\nApplication stopped by user.")
    except Exception as e:
        print(f"\n✗ Error starting application: {e}")
        return False
    
    return True

def main():
    """Main startup routine"""
    print("="*50)
    print("STOCK PREDICTION TRACKER - STARTUP")
    print("="*50)
    print()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        print("\n✗ Dependency check failed")
        print("Try running: pip install -r requirements.txt")
        sys.exit(1)
    
    # Start application
    print()
    start_application()

if __name__ == "__main__":
    main()
