# STOCK PREDICTION TRACKER - PHASE 1 MVP
## Project Overview & Deployment Guide

---

## 🎯 What Has Been Built

### Phase 1 MVP - Complete Feature Set

This is a **fully functional** financial news prediction tracker that:

1. **Monitors Financial News**: Scrapes Yahoo Finance, MarketWatch, and Benzinga for stock movement predictions
2. **Validates Predictions**: Tracks actual stock prices using yfinance and compares to predictions
3. **Calculates Accuracy**: Determines if predictions HIT, MISS, or are PARTIAL
4. **Provides Dashboard**: Bloomberg Terminal-styled interface with real-time updates
5. **Stores Data**: SQLite database for historical tracking

---

## 📁 Project Structure

```
stock_prediction_tracker/
│
├── app.py                      # Main Streamlit dashboard application
├── database.py                 # Database operations (SQLite)
├── price_tracker.py            # Stock price fetching and calculations
├── scraper.py                  # News source scraping
│
├── requirements.txt            # Python dependencies
├── README.md                   # Comprehensive documentation
├── QUICKSTART.md              # Quick start guide
│
├── test_components.py          # Component testing script
├── start.py                    # Automated startup script
├── config_template.py          # Configuration template
│
└── .gitignore                  # Git ignore rules
```

---

## 🚀 Quick Deployment (5 Minutes)

### Step 1: Install Dependencies
```bash
cd stock_prediction_tracker
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
streamlit run app.py
```

The dashboard will open automatically at `http://localhost:8501`

### Alternative: Use Startup Script
```bash
python start.py
```

---

## 💡 How to Use

### First-Time Setup

1. **Start the Application**
   ```bash
   streamlit run app.py
   ```

2. **Collect Articles**
   - Click "📰 Collect Articles" button
   - Wait 30-60 seconds for scraping
   - System finds predictions from 3 news sources

3. **Update Prices**
   - Click "🔄 Refresh Now" button
   - System fetches current stock prices
   - Statuses update automatically

4. **Enable Auto-Refresh** (Optional)
   - Check "Auto-refresh (30 min)" box
   - System will update every 30 minutes

### Understanding the Dashboard

**Status Indicators**:
- 🟡 **PENDING**: Still tracking (market open or same day)
- 🟢 **HIT**: Prediction accurate (within ±5%)
- 🔴 **MISS**: Prediction failed (market closed, didn't hit)
- 🟠 **PARTIAL**: Close but not exact (within ±10%)

**Key Metrics**:
- **Total Predictions**: All predictions tracked today
- **Hit Rate**: Percentage of accurate predictions
- **Hits/Misses/Partials**: Breakdown by accuracy

---

## 🎨 Design Features

### Bloomberg Terminal Aesthetic

The dashboard features authentic 1980s Bloomberg Terminal styling:
- **Dark blue-black background** (#0a0e27)
- **Amber/gold text** (#ffb000) with CRT glow effect
- **Green/red indicators** for gains/losses
- **Monospace font** (Courier New)
- **No rounded corners** (true retro aesthetic)
- **Minimal but functional** design

---

## 🔧 Technical Implementation

### Core Technologies

- **Streamlit**: Web dashboard framework
- **yfinance**: Real-time stock price data
- **SQLite**: Local database storage
- **BeautifulSoup4**: Web scraping
- **feedparser**: RSS feed parsing
- **pandas**: Data manipulation

### Data Flow

1. **Article Collection**:
   - Scrapes RSS feeds and websites
   - Extracts ticker + percentage using regex
   - Validates ticker symbols
   - Stores in database

2. **Price Tracking**:
   - Fetches previous close (baseline)
   - Fetches current price
   - Calculates actual movement %
   - Compares to predicted %

3. **Status Determination**:
   - HIT: Actual within ±5% of predicted
   - PARTIAL: Actual within ±10% but not ±5%
   - MISS: Market closed, didn't hit ±5%
   - PENDING: Still tracking

4. **Data Persistence**:
   - Articles table (predictions)
   - Price snapshots table (price checks)
   - Daily summary table (statistics)
   - Source accuracy table (metrics)

---

## 📊 Database Schema

### Tables

1. **articles**: Stores all predictions
   - ticker, claimed_percentage, direction
   - source_name, article_url, headline
   - status, is_duplicate, collection_date

2. **price_snapshots**: Stores price checks
   - article_id, check_timestamp
   - previous_close, current_price
   - actual_movement_pct, gap

3. **daily_summary**: Daily statistics
   - date, total_predictions
   - hits, misses, partials
   - hit_rate, avg_predicted, avg_actual

4. **source_accuracy**: Per-source metrics
   - source_name, date
   - predictions_count, hits, hit_rate
   - magnitude_accuracy, weighted_score

---

## 🔍 Testing & Validation

### Run Component Tests
```bash
python test_components.py
```

This will test:
- ✓ Import verification
- ✓ Database operations
- ✓ Price tracking
- ✓ Pattern matching

### Expected Output
```
✓ All tests passed! The application is ready to run.
```

---

## 📝 Configuration

### Current Settings (Phase 1)

- **Minimum Prediction**: ±20%
- **HIT Threshold**: ±5%
- **PARTIAL Threshold**: ±10%
- **Auto-refresh**: 30 minutes
- **Sources**: 3 (Yahoo Finance, MarketWatch, Benzinga)
- **Market Hours**: 9:30 AM - 4:00 PM ET
- **Daily Reset**: Midnight ET

### Customization

To customize settings:
1. Copy `config_template.py` to `config.py`
2. Modify values as needed
3. Import in modules: `from config import *`

---

## 🐛 Troubleshooting

### Common Issues

**No articles found?**
- Try scraping at different times
- Check internet connection
- Some sources may be rate-limited

**Price data errors?**
- yfinance occasionally has delays
- Invalid tickers skipped automatically
- Retry after a few minutes

**Dashboard not loading?**
- Verify all dependencies: `pip install -r requirements.txt`
- Run tests: `python test_components.py`
- Check terminal for errors

---

## 🎯 What's Included (Phase 1 Checklist)

### ✅ Completed Features

- ✓ Database setup and operations
- ✓ Article scraping from 3 sources
- ✓ Pattern matching for predictions
- ✓ Ticker validation
- ✓ Real-time price tracking
- ✓ Status determination (HIT/MISS/PARTIAL/PENDING)
- ✓ Duplicate detection
- ✓ Daily statistics calculation
- ✓ Bloomberg terminal styling
- ✓ Manual refresh button
- ✓ Auto-refresh (30 min)
- ✓ Separate gains/losses tables
- ✓ Status color coding
- ✓ Market status display
- ✓ Comprehensive documentation
- ✓ Test suite
- ✓ Startup script

### 🔄 Phase 2 (Next Steps)

- Add Seeking Alpha and Business Insider sources
- Implement automated scheduling
- Enhanced duplicate detection
- Midnight daily reset automation
- Improved error logging

### 📈 Phase 3 (Future)

- Historical analytics page
- Source leaderboard
- Charts and visualizations
- CSV/JSON export
- 30/90-day trends

### 🎨 Phase 4 (Polish)

- Email alerts
- Mobile-responsive design
- PDF report generation
- Advanced filtering
- Prediction conflicts view

---

## 📋 Requirements

- **Python**: 3.10 or higher
- **Internet**: For scraping and price data
- **Storage**: ~50MB for database
- **RAM**: ~200MB during operation

---

## 🔐 Data & Privacy

- **No user data** collected
- **Public market data** only
- **Local storage** (SQLite)
- **No external APIs** requiring keys (Phase 1)
- **Respects robots.txt** for web scraping

---

## 📚 Documentation

- **README.md**: Comprehensive guide (full features and usage)
- **QUICKSTART.md**: Get started in 5 minutes
- **This file**: Project overview and deployment
- **config_template.py**: Configuration reference

---

## 🎓 Learning Resources

### Understanding the Code

1. **app.py**: Start here - main application logic
2. **scraper.py**: See how articles are collected
3. **price_tracker.py**: Understand price calculations
4. **database.py**: Learn data persistence

### Key Concepts

- **Regex pattern matching**: How articles are parsed
- **yfinance API**: How prices are fetched
- **Streamlit**: How dashboard is built
- **SQLite**: How data is stored

---

## 🤝 Contributing

Phase 1 is MVP - focus on:
1. Testing article pattern matching accuracy
2. Validating price tracking reliability
3. Ensuring database operations work correctly
4. Improving scraping patterns

Report issues by documenting:
- What you tried to do
- What happened
- Error messages (check terminal)
- Your Python version

---

## 📄 License

Educational and research purposes.

---

## 🎉 Success Criteria

Phase 1 is successful if:
- ✓ Articles are collected from news sources
- ✓ Predictions are stored in database
- ✓ Prices update correctly
- ✓ Status changes accurately (HIT/MISS/PARTIAL)
- ✓ Dashboard displays data properly
- ✓ No critical errors during operation

---

## 🔮 Future Vision

### Ultimate Goal (Phase 4)

A comprehensive prediction tracking system that:
- Monitors 5+ news sources 24/7
- Provides real-time accuracy analytics
- Generates automated reports
- Sends email alerts for major predictions
- Exports data in multiple formats
- Displays rich visualizations
- Offers mobile-friendly interface

### Current State (Phase 1)

A functional MVP that proves the concept and provides immediate value.

---

## 📞 Support

For help:
1. Check **QUICKSTART.md** for common questions
2. Review **README.md** for detailed documentation
3. Run `python test_components.py` to diagnose issues
4. Check terminal output for error messages

---

**Version**: 1.0.0 (Phase 1 MVP)  
**Status**: Complete and Deployable  
**Last Updated**: October 2025

---

## 🚀 Ready to Deploy?

```bash
cd stock_prediction_tracker
pip install -r requirements.txt
streamlit run app.py
```

**That's it!** Your prediction tracker is now live.
