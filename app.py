"""
Stock Movement Prediction Tracker - Main Application
Monitors financial news predictions and tracks accuracy
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz
import time

from database import Database
from price_tracker import PriceTracker
from scraper import NewsScraper

# Page configuration
st.set_page_config(
    page_title="Stock Prediction Tracker",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Bloomberg Terminal CSS Styling
st.markdown("""
<style>
    /* Global styles */
    .main {
        background-color: #0a0e27;
        color: #ffb000;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #ffb000 !important;
        font-family: 'Courier New', monospace;
        text-shadow: 0 0 5px #ffb000;
        letter-spacing: 0.5px;
    }
    
    /* Main title */
    .main-title {
        font-size: 32px;
        font-weight: bold;
        text-align: center;
        padding: 20px;
        border-bottom: 2px solid #333333;
        margin-bottom: 20px;
    }
    
    /* Stats boxes */
    .stat-box {
        background-color: #1a1e37;
        border: 1px solid #333333;
        padding: 15px;
        border-radius: 0px;
        text-align: center;
        font-family: 'Courier New', monospace;
    }
    
    .stat-number {
        font-size: 28px;
        font-weight: bold;
        color: #ffb000;
        text-shadow: 0 0 5px #ffb000;
    }
    
    .stat-label {
        font-size: 14px;
        color: #ffb000;
        margin-top: 5px;
    }
    
    /* Status badges */
    .status-pending {
        background-color: #ffb00033;
        color: #ffb000;
        padding: 4px 8px;
        border-radius: 0px;
        font-weight: bold;
        font-family: 'Courier New', monospace;
    }
    
    .status-hit {
        background-color: #00ff0033;
        color: #00ff00;
        padding: 4px 8px;
        border-radius: 0px;
        font-weight: bold;
        font-family: 'Courier New', monospace;
    }
    
    .status-miss {
        background-color: #ff000033;
        color: #ff0000;
        padding: 4px 8px;
        border-radius: 0px;
        font-weight: bold;
        font-family: 'Courier New', monospace;
    }
    
    .status-partial {
        background-color: #ff880033;
        color: #ff8800;
        padding: 4px 8px;
        border-radius: 0px;
        font-weight: bold;
        font-family: 'Courier New', monospace;
    }
    
    /* Tables */
    .dataframe {
        font-family: 'Courier New', monospace;
        background-color: #1a1e37;
        color: #ffb000;
        border: 1px solid #333333;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #1a1e37;
        color: #ffb000;
        border: 1px solid #ffb000;
        border-radius: 0px;
        font-family: 'Courier New', monospace;
        font-weight: bold;
        padding: 10px 20px;
    }
    
    .stButton > button:hover {
        background-color: #2a2e47;
        border-color: #ffb000;
    }
    
    /* Info boxes */
    .info-box {
        background-color: #1a1e37;
        border: 1px solid #333333;
        padding: 10px;
        margin: 10px 0;
        font-family: 'Courier New', monospace;
        color: #ffb000;
    }
    
    /* Gain/Loss indicators */
    .gain {
        color: #00ff00 !important;
        font-weight: bold;
    }
    
    .loss {
        color: #ff0000 !important;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = datetime.now()
if 'auto_refresh' not in st.session_state:
    st.session_state.auto_refresh = True

# Initialize components
@st.cache_resource
def init_components():
    db = Database()
    price_tracker = PriceTracker()
    scraper = NewsScraper()
    return db, price_tracker, scraper

db, price_tracker, scraper = init_components()

def format_percentage(value):
    """Format percentage with color"""
    if value > 0:
        return f'<span class="gain">+{value:.2f}%</span>'
    elif value < 0:
        return f'<span class="loss">{value:.2f}%</span>'
    else:
        return f'{value:.2f}%'

def format_status(status):
    """Format status with badge"""
    status_classes = {
        'PENDING': 'status-pending',
        'HIT': 'status-hit',
        'MISS': 'status-miss',
        'PARTIAL': 'status-partial'
    }
    css_class = status_classes.get(status, 'status-pending')
    return f'<span class="{css_class}">{status}</span>'

def collect_articles():
    """Collect new articles from news sources"""
    with st.spinner("Collecting articles from news sources..."):
        articles = scraper.scrape_all_sources()
        
        today = scraper.get_todays_date()
        added_count = 0
        duplicate_count = 0
        invalid_count = 0
        
        for article in articles:
            # Validate ticker
            if not price_tracker.validate_ticker(article['ticker']):
                invalid_count += 1
                continue
            
            # Check for duplicates
            duplicates = db.check_for_duplicates(
                article['ticker'],
                article['claimed_percentage'],
                article['article_timestamp'],
                today
            )
            
            # Add article to database
            article_id = db.add_article(
                article['ticker'],
                article['claimed_percentage'],
                article['direction'],
                article['article_timestamp'],
                article['source_name'],
                article['article_url'],
                article['headline'],
                today
            )
            
            if article_id:
                added_count += 1
                
                # Mark as duplicate if needed
                if duplicates:
                    db.mark_as_duplicate(article_id)
                    duplicate_count += 1
            else:
                duplicate_count += 1
        
        return added_count, duplicate_count, invalid_count

def update_prices():
    """Update prices for all pending predictions"""
    with st.spinner("Updating stock prices..."):
        pending_articles = db.get_pending_articles()
        
        is_market_closed = price_tracker.is_market_closed()
        updated_count = 0
        
        for article in pending_articles:
            # Get price data
            price_data = price_tracker.get_price_data(article['ticker'])
            
            if not price_data:
                continue
            
            # Calculate gap
            gap = article['claimed_percentage'] - price_data['actual_movement_pct']
            
            # Add price snapshot
            db.add_price_snapshot(
                article['id'],
                price_data['previous_close'],
                price_data['current_price'],
                price_data['actual_movement_pct'],
                gap
            )
            
            # Determine and update status
            status = price_tracker.determine_status(
                article['claimed_percentage'],
                price_data['actual_movement_pct'],
                article['direction'],
                is_market_closed
            )
            
            db.update_article_status(article['id'], status)
            updated_count += 1
        
        return updated_count

def main():
    # Title
    st.markdown('<div class="main-title">STOCK MOVEMENT PREDICTION TRACKER</div>', unsafe_allow_html=True)
    
    # Current date/time and market status
    et_tz = pytz.timezone('US/Eastern')
    now = datetime.now(et_tz)
    market_status = price_tracker.get_market_status()
    
    col1, col2, col3 = st.columns([2, 2, 2])
    with col1:
        st.markdown(f'<div class="info-box">Current Time: {now.strftime("%Y-%m-%d %H:%M:%S ET")}</div>', unsafe_allow_html=True)
    with col2:
        status_color = "#00ff00" if market_status['status'] == "Market Open" else "#ff8800"
        st.markdown(f'<div class="info-box">Market Status: <span style="color: {status_color}; font-weight: bold;">{market_status["status"]}</span></div>', unsafe_allow_html=True)
    with col3:
        minutes_since_refresh = int((datetime.now() - st.session_state.last_refresh).total_seconds() / 60)
        st.markdown(f'<div class="info-box">Last Refresh: {minutes_since_refresh} minutes ago</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Control buttons
    col1, col2, col3, col4 = st.columns([2, 2, 2, 4])
    
    with col1:
        if st.button("🔄 Refresh Now", use_container_width=True):
            with st.spinner("Refreshing data..."):
                update_prices()
                st.session_state.last_refresh = datetime.now()
                st.rerun()
    
    with col2:
        if st.button("📰 Collect Articles", use_container_width=True):
            added, duplicates, invalid = collect_articles()
            st.success(f"Added {added} new articles ({duplicates} duplicates, {invalid} invalid tickers)")
            st.session_state.last_refresh = datetime.now()
            time.sleep(2)
            st.rerun()
    
    with col3:
        auto_refresh = st.checkbox("Auto-refresh (30 min)", value=st.session_state.auto_refresh)
        st.session_state.auto_refresh = auto_refresh
    
    st.markdown("---")
    
    # Get today's data
    today = scraper.get_todays_date()
    articles = db.get_todays_articles(today)
    stats = db.get_daily_stats(today)
    
    # Display daily statistics
    st.markdown("### Today's Predictions Summary")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f'''
            <div class="stat-box">
                <div class="stat-number">{stats['total_predictions']}</div>
                <div class="stat-label">Total Predictions</div>
            </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
            <div class="stat-box">
                <div class="stat-number" style="color: #00ff00;">{stats['hits']}</div>
                <div class="stat-label">Hits</div>
            </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'''
            <div class="stat-box">
                <div class="stat-number" style="color: #ff0000;">{stats['misses']}</div>
                <div class="stat-label">Misses</div>
            </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        st.markdown(f'''
            <div class="stat-box">
                <div class="stat-number" style="color: #ff8800;">{stats['partials']}</div>
                <div class="stat-label">Partials</div>
            </div>
        ''', unsafe_allow_html=True)
    
    with col5:
        hit_rate_color = "#00ff00" if stats['hit_rate'] > 60 else ("#ff8800" if stats['hit_rate'] > 40 else "#ff0000")
        st.markdown(f'''
            <div class="stat-box">
                <div class="stat-number" style="color: {hit_rate_color};">{stats['hit_rate']:.1f}%</div>
                <div class="stat-label">Hit Rate</div>
            </div>
        ''', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Prepare data for display
    if articles:
        display_data = []
        
        for article in articles:
            # Get latest price snapshot
            snapshot = db.get_latest_price_snapshot(article['id'])
            
            if snapshot:
                actual_pct = snapshot['actual_movement_pct']
                gap = snapshot['gap']
            else:
                actual_pct = 0.0
                gap = article['claimed_percentage']
            
            display_data.append({
                'Ticker': article['ticker'],
                'Predicted %': article['claimed_percentage'],
                'Actual %': actual_pct,
                'Gap': gap,
                'Status': article['status'],
                'Time': datetime.fromisoformat(article['article_timestamp']).strftime('%m/%d %H:%M'),
                'Source': article['source_name'],
                'Headline': article['headline'][:60] + '...' if len(article['headline']) > 60 else article['headline'],
                'URL': article['article_url'],
                'Duplicate': '[DUP]' if article['is_duplicate'] else ''
            })
        
        df = pd.DataFrame(display_data)
        
        # Split into gains and losses
        gains_df = df[df['Predicted %'] > 0].copy()
        losses_df = df[df['Predicted %'] < 0].copy()
        
        # Display Predicted Gains table
        st.markdown("### 📈 PREDICTED GAINS (Positive Predictions)")
        if not gains_df.empty:
            st.markdown(f"*Showing {len(gains_df)} predictions*")
            
            # Format the dataframe for display
            for idx, row in gains_df.iterrows():
                col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 1.5, 1.5, 1, 1.5, 1, 2])
                
                with col1:
                    st.markdown(f"**{row['Ticker']}** {row['Duplicate']}")
                with col2:
                    st.markdown(format_percentage(row['Predicted %']), unsafe_allow_html=True)
                with col3:
                    st.markdown(format_percentage(row['Actual %']), unsafe_allow_html=True)
                with col4:
                    st.markdown(f"{abs(row['Gap']):.2f}")
                with col5:
                    st.markdown(format_status(row['Status']), unsafe_allow_html=True)
                with col6:
                    st.markdown(f"{row['Time']}")
                with col7:
                    st.markdown(f"{row['Source']}")
                    if st.button("View", key=f"view_{idx}"):
                        st.markdown(f"**{row['Headline']}**")
                        st.markdown(f"[Read Article]({row['URL']})")
                
                st.markdown("---")
        else:
            st.info("No positive predictions found today")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Display Predicted Losses table
        st.markdown("### 📉 PREDICTED LOSSES (Negative Predictions)")
        if not losses_df.empty:
            st.markdown(f"*Showing {len(losses_df)} predictions*")
            
            for idx, row in losses_df.iterrows():
                col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 1.5, 1.5, 1, 1.5, 1, 2])
                
                with col1:
                    st.markdown(f"**{row['Ticker']}** {row['Duplicate']}")
                with col2:
                    st.markdown(format_percentage(row['Predicted %']), unsafe_allow_html=True)
                with col3:
                    st.markdown(format_percentage(row['Actual %']), unsafe_allow_html=True)
                with col4:
                    st.markdown(f"{abs(row['Gap']):.2f}")
                with col5:
                    st.markdown(format_status(row['Status']), unsafe_allow_html=True)
                with col6:
                    st.markdown(f"{row['Time']}")
                with col7:
                    st.markdown(f"{row['Source']}")
                    if st.button("View", key=f"view_loss_{idx}"):
                        st.markdown(f"**{row['Headline']}**")
                        st.markdown(f"[Read Article]({row['URL']})")
                
                st.markdown("---")
        else:
            st.info("No negative predictions found today")
    
    else:
        st.info("No predictions tracked today. Click 'Collect Articles' to start tracking.")
    
    # Auto-refresh logic
    if st.session_state.auto_refresh:
        time.sleep(5)  # Wait 5 seconds before checking
        minutes_elapsed = (datetime.now() - st.session_state.last_refresh).total_seconds() / 60
        if minutes_elapsed >= 30:
            update_prices()
            st.session_state.last_refresh = datetime.now()
            st.rerun()

if __name__ == "__main__":
    main()
