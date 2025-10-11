"""
Test script for Stock Prediction Tracker components
Run this to verify all components are working correctly
"""

import sys
from datetime import datetime

def test_imports():
    """Test if all required libraries can be imported"""
    print("Testing imports...")
    try:
        import streamlit
        print("✓ streamlit")
        import pandas
        print("✓ pandas")
        import yfinance
        print("✓ yfinance")
        import feedparser
        print("✓ feedparser")
        import requests
        print("✓ requests")
        from bs4 import BeautifulSoup
        print("✓ beautifulsoup4")
        import pytz
        print("✓ pytz")
        print("\n✓ All imports successful!\n")
        return True
    except ImportError as e:
        print(f"\n✗ Import failed: {e}")
        print("Run: pip install -r requirements.txt")
        return False

def test_database():
    """Test database initialization"""
    print("Testing database...")
    try:
        from database import Database
        db = Database("test_predictions.db")
        
        # Test adding an article
        article_id = db.add_article(
            ticker="AAPL",
            claimed_percentage=25.0,
            direction="up",
            article_timestamp=datetime.now().isoformat(),
            source_name="Test Source",
            article_url="https://test.com/article1",
            headline="Test headline",
            collection_date=datetime.now().strftime('%Y-%m-%d')
        )
        
        if article_id:
            print("✓ Database operations working")
            
            # Clean up
            import os
            if os.path.exists("test_predictions.db"):
                os.remove("test_predictions.db")
            
            return True
        else:
            print("✗ Failed to add article to database")
            return False
            
    except Exception as e:
        print(f"✗ Database test failed: {e}")
        return False

def test_price_tracker():
    """Test price tracking functionality"""
    print("\nTesting price tracker...")
    try:
        from price_tracker import PriceTracker
        tracker = PriceTracker()
        
        # Test with a well-known ticker
        print("  Testing ticker validation (AAPL)...")
        is_valid = tracker.validate_ticker("AAPL")
        if is_valid:
            print("  ✓ Ticker validation working")
        else:
            print("  ✗ Ticker validation failed")
            return False
        
        print("  Testing price fetching (AAPL)...")
        price_data = tracker.get_price_data("AAPL")
        if price_data:
            print(f"  ✓ Price data retrieved:")
            print(f"    - Previous Close: ${price_data['previous_close']:.2f}")
            print(f"    - Current Price: ${price_data['current_price']:.2f}")
            print(f"    - Movement: {price_data['actual_movement_pct']:+.2f}%")
            return True
        else:
            print("  ✗ Failed to get price data")
            return False
            
    except Exception as e:
        print(f"✗ Price tracker test failed: {e}")
        return False

def test_scraper():
    """Test news scraping (limited test)"""
    print("\nTesting news scraper...")
    try:
        from scraper import NewsScraper
        scraper = NewsScraper()
        
        # Test pattern matching
        test_text = "AAPL surges 25% after earnings"
        result = scraper.extract_ticker_and_percentage(test_text)
        
        if result:
            ticker, percentage, direction = result
            print(f"  ✓ Pattern matching working")
            print(f"    - Extracted: {ticker}, {percentage}%, {direction}")
            
            if ticker == "AAPL" and percentage == 25.0 and direction == "up":
                print("  ✓ Extraction accurate")
                return True
            else:
                print("  ✗ Extraction inaccurate")
                return False
        else:
            print("  ✗ Pattern matching failed")
            return False
            
    except Exception as e:
        print(f"✗ Scraper test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("="*50)
    print("STOCK PREDICTION TRACKER - COMPONENT TESTS")
    print("="*50)
    print()
    
    results = []
    
    # Test imports
    results.append(("Imports", test_imports()))
    
    # Test database
    results.append(("Database", test_database()))
    
    # Test price tracker
    results.append(("Price Tracker", test_price_tracker()))
    
    # Test scraper
    results.append(("News Scraper", test_scraper()))
    
    # Summary
    print("\n" + "="*50)
    print("TEST SUMMARY")
    print("="*50)
    
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name}: {status}")
    
    all_passed = all(result[1] for result in results)
    
    print()
    if all_passed:
        print("✓ All tests passed! The application is ready to run.")
        print("\nTo start the application, run:")
        print("  streamlit run app.py")
    else:
        print("✗ Some tests failed. Please fix the issues before running the application.")
    
    print("="*50)

if __name__ == "__main__":
    main()
