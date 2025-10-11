# FILE STRUCTURE GUIDE
## Stock Prediction Tracker - What Each File Does

```
stock_prediction_tracker/
│
├── 📱 MAIN APPLICATION FILES
│   ├── app.py ⭐
│   │   └── Main Streamlit dashboard
│   │       • UI and visual display
│   │       • User interactions (buttons, filters)
│   │       • Data presentation
│   │       • Bloomberg terminal styling
│   │       • Auto-refresh logic
│   │
│   ├── database.py
│   │   └── Database operations
│   │       • SQLite setup and initialization
│   │       • CRUD operations (Create, Read, Update, Delete)
│   │       • Article storage
│   │       • Price snapshot tracking
│   │       • Statistics calculations
│   │       • Duplicate checking
│   │
│   ├── price_tracker.py
│   │   └── Stock price tracking
│   │       • yfinance integration
│   │       • Ticker validation
│   │       • Previous close fetching
│   │       • Current price fetching
│   │       • Movement calculation
│   │       • Status determination (HIT/MISS/PARTIAL)
│   │       • Market hours checking
│   │
│   └── scraper.py
│       └── News article scraping
│           • RSS feed parsing
│           • Web scraping
│           • Pattern matching (regex)
│           • Ticker extraction
│           • Percentage extraction
│           • Exclusion filtering
│           • Multi-source collection
│
├── 📋 CONFIGURATION & SETUP
│   ├── requirements.txt
│   │   └── Python package dependencies
│   │       Lists all required libraries
│   │
│   └── config_template.py
│       └── Configuration template
│           • Customizable settings
│           • Source URLs
│           • Thresholds and limits
│           • Future feature flags
│
├── 🧪 TESTING & UTILITIES
│   ├── test_components.py
│   │   └── Component testing suite
│   │       • Import verification
│   │       • Database testing
│   │       • Price tracker testing
│   │       • Scraper testing
│   │       • Validation checks
│   │
│   └── start.py
│       └── Automated startup script
│           • Python version check
│           • Dependency checking
│           • Automatic installation
│           • Application launch
│
├── 📚 DOCUMENTATION
│   ├── README.md
│   │   └── Comprehensive guide
│   │       • Full feature documentation
│   │       • Installation instructions
│   │       • Usage examples
│   │       • Technical details
│   │       • Troubleshooting
│   │       • 10+ pages of content
│   │
│   ├── QUICKSTART.md
│   │   └── Quick start guide
│   │       • 5-minute setup
│   │       • Essential steps only
│   │       • Common tasks
│   │       • Tips and tricks
│   │
│   ├── PROJECT_OVERVIEW.md ⭐
│   │   └── Project overview
│   │       • What's been built
│   │       • Deployment guide
│   │       • Technical architecture
│   │       • Phase roadmap
│   │       • Success criteria
│   │
│   └── THIS FILE
│       └── File structure guide
│           You are here!
│
└── 🔧 DEVELOPMENT FILES
    └── .gitignore
        └── Git ignore rules
            • Python cache files
            • Database files
            • Virtual environments
            • IDE files
            • Log files

```

---

## 🎯 WHERE TO START

### For Users (Just Want to Use It)
1. **QUICKSTART.md** - Get running in 5 minutes
2. **app.py** - Run this: `streamlit run app.py`

### For Developers (Want to Understand It)
1. **PROJECT_OVERVIEW.md** - Understand what's built
2. **README.md** - Read full documentation
3. **app.py** - Study main application
4. **database.py** - Understand data storage
5. **scraper.py** - See how articles are collected
6. **price_tracker.py** - Learn price calculations

### For Testing
1. **test_components.py** - Run: `python test_components.py`
2. Check all components work correctly

---

## 📊 FILE SIZES & IMPORTANCE

| File | Size | Importance | Purpose |
|------|------|------------|---------|
| app.py | 16KB | ⭐⭐⭐⭐⭐ | Main application |
| database.py | 13KB | ⭐⭐⭐⭐⭐ | Data persistence |
| scraper.py | 11KB | ⭐⭐⭐⭐⭐ | Article collection |
| price_tracker.py | 9KB | ⭐⭐⭐⭐⭐ | Price tracking |
| README.md | 6.8KB | ⭐⭐⭐⭐ | Documentation |
| test_components.py | 5.2KB | ⭐⭐⭐ | Testing |
| config_template.py | 3.1KB | ⭐⭐ | Configuration |
| QUICKSTART.md | 3.1KB | ⭐⭐⭐⭐ | Quick start |
| start.py | 2.4KB | ⭐⭐ | Startup helper |
| requirements.txt | 133B | ⭐⭐⭐⭐⭐ | Dependencies |

**Total Project Size**: ~81KB (compact!)

---

## 🔄 FILE DEPENDENCIES

```
app.py
  ├── imports database.py
  ├── imports price_tracker.py
  └── imports scraper.py

database.py
  └── standalone (only uses Python stdlib)

price_tracker.py
  └── uses yfinance library

scraper.py
  ├── uses feedparser
  ├── uses BeautifulSoup4
  └── uses requests

test_components.py
  ├── imports database.py
  ├── imports price_tracker.py
  └── imports scraper.py
```

---

## 🚀 TYPICAL WORKFLOW

### When Application Starts
1. `app.py` initializes
2. Imports `database.py`, `price_tracker.py`, `scraper.py`
3. Creates database if doesn't exist
4. Displays dashboard

### When User Clicks "Collect Articles"
1. `app.py` calls `scraper.scrape_all_sources()`
2. `scraper.py` fetches articles from news sources
3. `scraper.py` extracts tickers and percentages
4. `app.py` validates tickers using `price_tracker.py`
5. `app.py` stores articles using `database.py`

### When User Clicks "Refresh Now"
1. `app.py` calls `database.get_pending_articles()`
2. For each article:
   - `price_tracker.py` fetches current price
   - `price_tracker.py` calculates movement %
   - `price_tracker.py` determines status
   - `database.py` stores price snapshot
   - `database.py` updates article status

### Every 30 Minutes (Auto-Refresh)
1. Repeat "Refresh Now" workflow
2. Update dashboard display

---

## 🎨 CODE STRUCTURE

### app.py Structure
```python
1. Imports and page configuration
2. CSS styling (Bloomberg terminal)
3. Session state initialization
4. Component initialization (database, tracker, scraper)
5. Helper functions (formatting, etc.)
6. collect_articles() function
7. update_prices() function
8. main() function
   - Display header
   - Show market status
   - Control buttons
   - Statistics
   - Data tables
   - Auto-refresh logic
```

### database.py Structure
```python
1. Database class definition
2. __init__() - Initialize connection
3. init_database() - Create tables
4. add_article() - Insert new article
5. add_price_snapshot() - Insert price check
6. update_article_status() - Update status
7. get_todays_articles() - Fetch today's data
8. get_pending_articles() - Fetch active predictions
9. get_daily_stats() - Calculate statistics
10. check_for_duplicates() - Find duplicates
```

---

## 🔍 WHAT'S NOT INCLUDED (Yet)

These files will be added in future phases:

**Phase 2**:
- `scheduler.py` - Automated task scheduling
- `config.py` - User configuration

**Phase 3**:
- `analytics.py` - Historical analysis
- `visualizations.py` - Charts and graphs
- `export.py` - CSV/JSON export

**Phase 4**:
- `alerts.py` - Email notifications
- `api.py` - REST API endpoints
- `mobile.py` - Mobile optimizations

---

## 💾 GENERATED FILES (During Use)

These files are created automatically:

- **predictions.db** - SQLite database (all data stored here)
- **errors.txt** - Error log (if errors occur)
- **__pycache__/** - Python cache (can be deleted)

**Note**: These are in .gitignore and won't be tracked

---

## 🎓 LEARNING PATH

### Beginner Level
Start with these files:
1. QUICKSTART.md
2. requirements.txt
3. test_components.py

### Intermediate Level
Then explore:
1. database.py (simpler logic)
2. price_tracker.py (API calls)
3. scraper.py (web scraping)

### Advanced Level
Finally study:
1. app.py (complex UI logic)
2. config_template.py (system design)

---

## 🔧 MODIFICATION GUIDE

**Want to add a news source?**
→ Modify `scraper.py`

**Want to change thresholds (HIT/MISS)?**
→ Modify `price_tracker.py`

**Want to add database fields?**
→ Modify `database.py`

**Want to change UI appearance?**
→ Modify CSS in `app.py`

**Want to customize settings?**
→ Copy and edit `config_template.py`

---

## 📦 MINIMAL DEPLOYMENT

Absolute minimum files needed:
- app.py
- database.py
- price_tracker.py
- scraper.py
- requirements.txt

Everything else is documentation or utilities.

---

## ⭐ MOST IMPORTANT FILES

For daily use:
1. **app.py** - The application itself
2. **QUICKSTART.md** - How to use it
3. **requirements.txt** - What to install

For development:
1. **PROJECT_OVERVIEW.md** - Understanding the system
2. **README.md** - Full documentation
3. **test_components.py** - Validation

---

**Last Updated**: October 2025  
**Total Files**: 11  
**Total Documentation**: 4 files (~20KB)  
**Total Code**: 7 files (~61KB)
