# Configuration Template for Stock Prediction Tracker
# Copy this to config.py and modify as needed

# NEWS SOURCES (Phase 1: 3 sources active)
NEWS_SOURCES = {
    'yahoo_finance': {
        'enabled': True,
        'url': 'https://finance.yahoo.com/news/rssindex',
        'type': 'rss'
    },
    'marketwatch': {
        'enabled': True,
        'url': 'https://www.marketwatch.com/rss/topstories',
        'type': 'rss'
    },
    'benzinga': {
        'enabled': True,
        'url': 'https://www.benzinga.com/news',
        'type': 'web_scraping'
    },
    # Phase 2 additions
    'seeking_alpha': {
        'enabled': False,  # Enable in Phase 2
        'url': 'https://seekingalpha.com/feed.xml',
        'type': 'rss'
    },
    'business_insider': {
        'enabled': False,  # Enable in Phase 2
        'url': 'https://markets.businessinsider.com/rss/news',
        'type': 'rss'
    }
}

# PREDICTION THRESHOLDS
MINIMUM_PERCENTAGE = 20.0  # Only track predictions >= 20% or <= -20%

# STATUS THRESHOLDS
HIT_THRESHOLD = 5.0  # Within ±5 percentage points = HIT
PARTIAL_THRESHOLD = 10.0  # Within ±10 percentage points = PARTIAL

# DUPLICATE DETECTION
DUPLICATE_PERCENTAGE_TOLERANCE = 3.0  # Within ±3% = potential duplicate
DUPLICATE_TIME_WINDOW_HOURS = 2  # Within 2 hours = potential duplicate

# REFRESH SETTINGS
AUTO_REFRESH_INTERVAL_MINUTES = 30
SCRAPING_INTERVAL_MINUTES = 30

# MARKET HOURS (Eastern Time)
MARKET_OPEN_HOUR = 9
MARKET_OPEN_MINUTE = 30
MARKET_CLOSE_HOUR = 16
MARKET_CLOSE_MINUTE = 0

# OPERATING HOURS
SCRAPING_START_HOUR = 4  # 4:00 AM ET
SCRAPING_END_HOUR = 23  # 11:59 PM ET

# DAILY RESET
DAILY_RESET_HOUR = 0  # Midnight ET

# DATA RETENTION
ARCHIVE_DAYS = 90  # Keep 90 days of historical data

# RATE LIMITING
REQUESTS_PER_SECOND = 1
DELAY_BETWEEN_SOURCES_SECONDS = 2
MAX_RETRY_ATTEMPTS = 3
RETRY_BACKOFF_SECONDS = [1, 5, 15]

# DATABASE
DATABASE_PATH = "predictions.db"
MAX_TRACKED_STOCKS = 100  # Batch limit per refresh

# LOGGING
ERROR_LOG_PATH = "errors.txt"
STATS_LOG_PATH = "stats.log"
LOG_LEVEL = "INFO"

# UI SETTINGS
PAGE_TITLE = "Stock Prediction Tracker"
PAGE_ICON = "📈"
LAYOUT = "wide"

# BLOOMBERG TERMINAL STYLING
COLORS = {
    'background': '#0a0e27',
    'primary_text': '#ffb000',
    'gain': '#00ff00',
    'loss': '#ff0000',
    'warning': '#ff8800',
    'border': '#333333',
    'table_row_alt_1': '#1a1e37',
    'table_row_alt_2': '#0f1229'
}

# EMAIL ALERTS (Phase 4)
EMAIL_ALERTS_ENABLED = False
ALERT_THRESHOLD_PERCENTAGE = 100.0  # Alert for predictions >100%
SMTP_SERVER = ""
SMTP_PORT = 587
EMAIL_FROM = ""
EMAIL_TO = ""
EMAIL_PASSWORD = ""

# EXPORT SETTINGS (Phase 3)
EXPORT_FORMATS = ['csv', 'json', 'pdf']
EXPORT_PATH = "exports/"

# API SETTINGS (Future feature)
ENABLE_API = False
API_PORT = 8000
API_KEY_REQUIRED = False

# NOTES FOR CUSTOMIZATION:
# - Phase 1: Only basic settings are used
# - Phase 2: Will use scheduling and source settings
# - Phase 3: Will use export and analytics settings
# - Phase 4: Will use email and advanced settings
# 
# To use this config:
# 1. Copy this file to config.py
# 2. Modify values as needed
# 3. Import in your modules: from config import *
