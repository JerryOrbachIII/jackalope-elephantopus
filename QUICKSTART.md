# QUICK START GUIDE

## Installation (5 minutes)

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Test the installation**:
```bash
python test_components.py
```

3. **Start the application**:
```bash
streamlit run app.py
```
OR
```bash
python start.py
```

## First Use

1. **Collect Articles**:
   - Click "📰 Collect Articles" button
   - Wait 30-60 seconds for scraping
   - System will find predictions from Yahoo Finance, MarketWatch, and Benzinga

2. **Update Prices**:
   - Click "🔄 Refresh Now" button
   - System fetches current stock prices
   - Status updates automatically (PENDING → HIT/MISS/PARTIAL)

3. **Enable Auto-Refresh**:
   - Check "Auto-refresh (30 min)" box
   - System will update prices every 30 minutes
   - Useful for tracking during market hours

## Understanding the Display

### Status Colors
- 🟡 **PENDING** (Amber): Prediction still being tracked
- 🟢 **HIT** (Green): Prediction came true (within ±5%)
- 🔴 **MISS** (Red): Prediction failed (market closed, didn't hit)
- 🟠 **PARTIAL** (Orange): Close but not exact (within ±10%)

### Statistics
- **Total Predictions**: All predictions tracked today
- **Hits**: Successfully predicted movements
- **Misses**: Failed predictions
- **Hit Rate**: % of accurate predictions (green >60%, yellow 40-60%, red <40%)

### Tables
- **Predicted Gains**: Articles claiming stock will rise
- **Predicted Losses**: Articles claiming stock will fall
- **[DUP]**: Indicates duplicate article (same ticker, similar %, within 2 hours)

## Tips

- **Best time to collect articles**: 
  - Before market open (6-9 AM ET)
  - During market hours (9:30 AM - 4 PM ET)
  - After major news events

- **Refresh frequency**:
  - Every 30 minutes during market hours for active tracking
  - Once at market close (4 PM ET) for final results

- **Market hours**: 9:30 AM - 4:00 PM ET (Monday-Friday)

- **Daily reset**: Midnight ET - previous day archived, new day begins

## Troubleshooting

**No articles found?**
- Try at different time of day
- Check internet connection
- Some sources may be temporarily unavailable

**Price data errors?**
- yfinance sometimes has delays
- Invalid tickers are skipped automatically
- Retry refresh after a few minutes

**Dashboard not loading?**
- Check all dependencies installed: `pip install -r requirements.txt`
- Run test script: `python test_components.py`
- Check terminal for error messages

## What to Expect (Phase 1 MVP)

✓ Basic article collection from 3 sources  
✓ Real-time price tracking  
✓ Manual and auto-refresh  
✓ Simple accuracy tracking  
✓ Bloomberg terminal styling  

✗ Limited to 3 news sources (more in Phase 2)  
✗ No historical analytics yet (Phase 3)  
✗ No export functionality yet (Phase 3)  
✗ No email alerts yet (Phase 4)  

## Next Steps

Once you're comfortable with Phase 1:
- Phase 2 will add more sources and automated scheduling
- Phase 3 will add analytics and historical tracking
- Phase 4 will add polish and advanced features

---

**Need more help?** See README.md for detailed documentation.
