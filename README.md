# Stock Movement Prediction Tracker

A real-time dashboard that monitors financial news sources for stock movement predictions (>20% or <-20%), validates these claims against actual stock prices, and tracks prediction accuracy by source.

## Features (Phase 1 - MVP)

- **Article Collection**: Automatically scrapes Yahoo Finance, MarketWatch, and Benzinga for stock movement predictions
- **Real-Time Price Tracking**: Uses yfinance to monitor actual stock movements
- **Prediction Validation**: Classifies predictions as HIT, MISS, PARTIAL, or PENDING
- **Bloomberg Terminal Aesthetic**: 1980s-inspired dark theme with amber text and CRT glow effects
- **Manual & Auto-Refresh**: Control when data updates (manual or every 30 minutes)
- **Duplicate Detection**: Identifies and flags duplicate articles
- **Daily Statistics**: Track hit rates and prediction accuracy

## Requirements

- Python 3.10 or higher
- Internet connection for scraping news and fetching stock prices

## Installation

1. **Clone or download this repository**

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run the application**:
```bash
streamlit run app.py
```

4. **Access the dashboard**:
- The application will open automatically in your browser
- If not, navigate to `http://localhost:8501`

## Usage

### Collecting Articles

1. Click the **"📰 Collect Articles"** button to scrape news sources
2. The system will:
   - Search for articles claiming stock movements ≥20% or ≤-20%
   - Validate ticker symbols
   - Check for duplicates
   - Add valid predictions to the database

### Updating Prices

1. Click the **"🔄 Refresh Now"** button to update stock prices
2. The system will:
   - Fetch current prices for all tracked stocks
   - Calculate actual movement percentages
   - Update prediction status (HIT/MISS/PARTIAL/PENDING)
   - Store price snapshots in the database

### Auto-Refresh

- Enable **"Auto-refresh (30 min)"** checkbox for automatic updates
- The system will refresh prices every 30 minutes during market hours

### Understanding the Dashboard

**Status Indicators**:
- 🟡 **PENDING**: Market is still open, prediction not yet resolved
- 🟢 **HIT**: Actual movement within ±5% of predicted (same direction)
- 🔴 **MISS**: Market closed, actual movement >±5% from predicted
- 🟠 **PARTIAL**: Actual movement within ±10% but not ±5%

**Statistics**:
- **Total Predictions**: Number of predictions tracked today
- **Hits**: Predictions that came true (within ±5%)
- **Misses**: Predictions that didn't come true
- **Partials**: Predictions that were close but not exact
- **Hit Rate**: Percentage of successful predictions

**Tables**:
- **Predicted Gains**: Articles predicting stock increases
- **Predicted Losses**: Articles predicting stock decreases
- Each row shows: Ticker, Predicted %, Actual %, Gap, Status, Time, Source

## How It Works

### Article Pattern Matching

The scraper looks for phrases like:
- "TICKER surges 25%"
- "TICKER plunges 30%"
- "$TICKER up 22%"
- "TICKER stock jumps 40%"

And **ignores** speculative language:
- "could surge"
- "might jump"
- "expected to rise"
- "if analysts predict"

### Price Calculation

**Previous Close**: The reference point (previous trading day's 4 PM ET close)  
**Current Price**: Most recent available price  
**Actual Movement %**: ((Current - Previous) / Previous) × 100

### Status Determination

The system continuously monitors each prediction until:
- **HIT**: Actual movement comes within ±5% of prediction (same direction)
- **MISS**: Market closes without hitting ±5% threshold
- **PARTIAL**: Actual movement within ±10% but not ±5%
- **PENDING**: Still tracking (market open or same calendar day)

### Daily Reset

At midnight ET, the system:
- Archives previous day's predictions
- Clears active tracking list
- Resets counters for the new day

## File Structure

```
stock_prediction_tracker/
├── app.py                 # Main Streamlit application
├── database.py            # SQLite database operations
├── price_tracker.py       # Stock price tracking with yfinance
├── scraper.py            # News source scraping
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── predictions.db        # SQLite database (created on first run)
```

## Database Schema

The system uses SQLite with four main tables:

**articles**: Stores scraped predictions  
**price_snapshots**: Stores price checks over time  
**daily_summary**: Aggregated daily statistics  
**source_accuracy**: Per-source accuracy metrics

## Troubleshooting

### No Articles Found

- Check internet connection
- Verify news sources are accessible
- Try scraping at different times of day
- Some sources may have rate limits

### Price Data Errors

- yfinance occasionally has delays or missing data
- Invalid ticker symbols will be skipped
- Check errors.txt for detailed error logs

### Performance Issues

- Reduce number of tracked predictions
- Clear old data from database
- Disable auto-refresh if causing slowdowns

## Limitations (Phase 1)

- Only 3 news sources (Yahoo Finance, MarketWatch, Benzinga)
- Manual refresh required (auto-refresh every 30 min)
- Basic pattern matching (may miss some article formats)
- No historical analytics yet
- No export functionality yet

## Future Phases

**Phase 2** (Coming Soon):
- Add Seeking Alpha and Business Insider sources
- Improve deduplication logic
- Implement midnight daily reset automation
- Enhanced error handling

**Phase 3** (Planned):
- Accuracy metrics page with source leaderboard
- Historical tracking over 30/90 days
- Charts and visualizations
- CSV export functionality

**Phase 4** (Planned):
- Email alerts for large predictions
- Mobile-responsive design
- PDF report generation
- Advanced filtering and search

## Technical Notes

### Rate Limiting

The scraper respects rate limits:
- 1 request per second per source
- 2-second delays between sources
- Automatic retry with exponential backoff

### Timezone Handling

All times are stored and displayed in Eastern Time (ET):
- Market hours: 9:30 AM - 4:00 PM ET
- Daily reset: Midnight ET

### Data Retention

- Current version keeps all data indefinitely
- Future versions will archive data older than 90 days

## Contributing

This is Phase 1 (MVP) of a 4-phase project. Current focus is on:
- Validating the core concept
- Testing article pattern matching accuracy
- Ensuring price tracking reliability

## Support

For issues or questions:
1. Check the Troubleshooting section above
2. Review errors.txt for detailed error logs
3. Verify all dependencies are installed correctly

## License

This project is for educational and research purposes.

---

**Built with**: Python, Streamlit, yfinance, BeautifulSoup4  
**Version**: 1.0.0 (Phase 1 MVP)  
**Last Updated**: October 2025
