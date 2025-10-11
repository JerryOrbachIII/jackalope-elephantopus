"""
Price tracking module for Stock Prediction Tracker
Uses yfinance to get real-time stock prices and calculate movements
"""

import yfinance as yf
from datetime import datetime, timedelta
from typing import Optional, Dict, Tuple
import pytz

class PriceTracker:
    def __init__(self):
        """Initialize the price tracker"""
        self.et_timezone = pytz.timezone('US/Eastern')
    
    def validate_ticker(self, ticker: str) -> bool:
        """
        Validate if a ticker symbol exists and has data
        Returns True if valid, False otherwise
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Check if we got meaningful data back
            if not info or len(info) < 5:
                return False
            
            # Try to get recent price data
            hist = stock.history(period="1d")
            if hist.empty:
                return False
            
            return True
            
        except Exception as e:
            print(f"Error validating ticker {ticker}: {e}")
            return False
    
    def get_previous_close(self, ticker: str) -> Optional[float]:
        """
        Get the previous trading day's closing price at 4:00 PM ET
        This is the baseline for percentage calculations
        """
        try:
            stock = yf.Ticker(ticker)
            
            # Get last 5 days of data to ensure we have the previous close
            hist = stock.history(period="5d")
            
            if hist.empty or len(hist) < 1:
                return None
            
            # Get the most recent close that's not today
            # If market is open, previous close is yesterday's close
            # If market is closed, previous close might be today's close
            now = datetime.now(self.et_timezone)
            current_hour = now.hour
            
            # Market closes at 4 PM ET (16:00)
            if current_hour >= 16:
                # After market close, use today's close
                previous_close = hist['Close'].iloc[-1]
            else:
                # Before market close, use previous day's close
                if len(hist) >= 2:
                    previous_close = hist['Close'].iloc[-2]
                else:
                    previous_close = hist['Close'].iloc[-1]
            
            return float(previous_close)
            
        except Exception as e:
            print(f"Error getting previous close for {ticker}: {e}")
            return None
    
    def get_current_price(self, ticker: str) -> Optional[float]:
        """
        Get the current/most recent price for a ticker
        """
        try:
            stock = yf.Ticker(ticker)
            
            # Try to get real-time price first
            try:
                current_price = stock.info.get('currentPrice') or stock.info.get('regularMarketPrice')
                if current_price:
                    return float(current_price)
            except:
                pass
            
            # Fallback to latest historical price
            hist = stock.history(period="1d", interval="1m")
            if not hist.empty:
                current_price = hist['Close'].iloc[-1]
                return float(current_price)
            
            # Last fallback - get today's data
            hist = stock.history(period="1d")
            if not hist.empty:
                current_price = hist['Close'].iloc[-1]
                return float(current_price)
            
            return None
            
        except Exception as e:
            print(f"Error getting current price for {ticker}: {e}")
            return None
    
    def calculate_movement(self, previous_close: float, current_price: float) -> float:
        """
        Calculate percentage movement from previous close to current price
        Formula: ((Current - Previous) / Previous) × 100
        """
        if previous_close == 0:
            return 0.0
        
        movement = ((current_price - previous_close) / previous_close) * 100
        return round(movement, 2)
    
    def get_price_data(self, ticker: str) -> Optional[Dict[str, float]]:
        """
        Get complete price data for a ticker
        Returns dict with previous_close, current_price, and actual_movement_pct
        """
        previous_close = self.get_previous_close(ticker)
        if previous_close is None:
            return None
        
        current_price = self.get_current_price(ticker)
        if current_price is None:
            return None
        
        actual_movement = self.calculate_movement(previous_close, current_price)
        
        return {
            'previous_close': previous_close,
            'current_price': current_price,
            'actual_movement_pct': actual_movement
        }
    
    def determine_status(self, claimed_percentage: float, actual_movement_pct: float,
                        direction: str, is_market_closed: bool = False) -> str:
        """
        Determine the prediction status based on claimed vs actual movement
        
        HIT: Actual within ±5 percentage points and same direction
        PARTIAL: Actual within ±10 percentage points but not ±5
        MISS: Market closed and didn't hit within ±5
        PENDING: Market still open and hasn't hit yet
        """
        # Check if directions match
        claimed_direction = 'up' if claimed_percentage > 0 else 'down'
        actual_direction = 'up' if actual_movement_pct > 0 else 'down'
        
        if claimed_direction != actual_direction and is_market_closed:
            return 'MISS'
        
        # Calculate the gap (absolute difference in magnitude)
        gap = abs(abs(claimed_percentage) - abs(actual_movement_pct))
        
        # Check for HIT (within 5 percentage points)
        if gap <= 5 and claimed_direction == actual_direction:
            return 'HIT'
        
        # Check for PARTIAL (within 10 percentage points but not 5)
        if gap <= 10 and claimed_direction == actual_direction:
            if is_market_closed:
                return 'PARTIAL'
            else:
                return 'PENDING'  # Still might hit
        
        # Check for MISS (market closed and didn't hit)
        if is_market_closed:
            return 'MISS'
        
        # Default to PENDING if market is still open
        return 'PENDING'
    
    def is_market_closed(self) -> bool:
        """
        Check if US stock market is currently closed
        Market hours: 9:30 AM - 4:00 PM ET, Monday-Friday
        """
        now = datetime.now(self.et_timezone)
        
        # Check if weekend
        if now.weekday() >= 5:  # Saturday = 5, Sunday = 6
            return True
        
        # Check if outside market hours
        market_open = now.replace(hour=9, minute=30, second=0, microsecond=0)
        market_close = now.replace(hour=16, minute=0, second=0, microsecond=0)
        
        if now < market_open or now >= market_close:
            return True
        
        return False
    
    def should_end_tracking(self) -> bool:
        """
        Check if we should end tracking for the day
        End tracking at midnight ET
        """
        now = datetime.now(self.et_timezone)
        
        # Check if it's past midnight (new day)
        midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
        next_midnight = midnight + timedelta(days=1)
        
        return now >= next_midnight
    
    def get_market_status(self) -> Dict[str, any]:
        """
        Get current market status information
        """
        now = datetime.now(self.et_timezone)
        is_closed = self.is_market_closed()
        
        # Calculate time to market open/close
        if now.weekday() >= 5:
            # Weekend - calculate days to Monday
            days_to_monday = (7 - now.weekday()) % 7
            if days_to_monday == 0:
                days_to_monday = 1
            next_open = now + timedelta(days=days_to_monday)
            next_open = next_open.replace(hour=9, minute=30, second=0, microsecond=0)
            status = "Weekend"
        elif is_closed:
            if now.hour < 9 or (now.hour == 9 and now.minute < 30):
                # Before market open
                next_open = now.replace(hour=9, minute=30, second=0, microsecond=0)
                status = "Pre-Market"
            else:
                # After market close
                next_open = (now + timedelta(days=1)).replace(hour=9, minute=30, second=0, microsecond=0)
                # Skip weekend
                if next_open.weekday() >= 5:
                    days_to_add = (7 - next_open.weekday()) % 7 or 1
                    next_open += timedelta(days=days_to_add)
                status = "After-Hours"
        else:
            next_open = now.replace(hour=16, minute=0, second=0, microsecond=0)
            status = "Market Open"
        
        return {
            'status': status,
            'is_closed': is_closed,
            'current_time': now,
            'next_change': next_open
        }
