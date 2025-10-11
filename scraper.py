"""
News scraper module for Stock Prediction Tracker
Scrapes financial news sources for stock movement predictions
"""

import re
import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import time
import pytz

class NewsScraper:
    def __init__(self):
        """Initialize the news scraper"""
        self.et_timezone = pytz.timezone('US/Eastern')
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Patterns to match stock movement claims
        self.movement_patterns = [
            # TICKER surges/jumps/soars/rallies X%
            r'(\b[A-Z]{2,5}\b)\s+(?:surges?|jumps?|soars?|rallies?|climbs?)\s+(\d+(?:\.\d+)?)\s*%',
            # TICKER plunges/drops/falls/declines X%
            r'(\b[A-Z]{2,5}\b)\s+(?:plunges?|drops?|falls?|declines?|tumbles?)\s+(\d+(?:\.\d+)?)\s*%',
            # $TICKER up/down X%
            r'\$([A-Z]{2,5})\s+(?:up|down)\s+(\d+(?:\.\d+)?)\s*%',
            # TICKER stock/shares up/down X%
            r'(\b[A-Z]{2,5}\b)\s+(?:stock|shares)\s+(?:up|down)\s+(\d+(?:\.\d+)?)\s*%',
        ]
        
        # Exclusion patterns - ignore articles with these phrases
        self.exclusion_patterns = [
            r'could\s+(?:surge|jump|rise|gain)',
            r'might\s+(?:surge|jump|rise|gain)',
            r'may\s+(?:surge|jump|rise|gain)',
            r'expected\s+to',
            r'projected\s+to',
            r'forecasted\s+to',
            r'if\s+',
            r'analysts?\s+predict',
            r'price\s+target',
            r'last\s+week',
            r'yesterday',
            r'last\s+month',
            r'last\s+quarter',
            r'surged\s+last',
            r'dropped\s+last',
        ]
    
    def extract_ticker_and_percentage(self, text: str) -> Optional[Tuple[str, float, str]]:
        """
        Extract ticker symbol and claimed percentage from text
        Returns (ticker, percentage, direction) or None
        """
        # Check for exclusion patterns first
        text_lower = text.lower()
        for pattern in self.exclusion_patterns:
            if re.search(pattern, text_lower):
                return None
        
        # Try each movement pattern
        for pattern in self.movement_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            
            for match in matches:
                ticker = match.group(1).upper()
                percentage_str = match.group(2)
                
                try:
                    percentage = float(percentage_str)
                except ValueError:
                    continue
                
                # Check if percentage meets threshold (≥20% or ≤-20%)
                if percentage < 20:
                    continue
                
                # Determine direction from context
                direction = 'up'
                match_text = match.group(0).lower()
                if any(word in match_text for word in ['plunge', 'drop', 'fall', 'decline', 'tumble', 'down']):
                    direction = 'down'
                    percentage = -percentage
                
                return (ticker, percentage, direction)
        
        return None
    
    def scrape_yahoo_finance_rss(self) -> List[Dict]:
        """
        Scrape Yahoo Finance RSS feed for news articles
        """
        articles = []
        
        try:
            url = "https://finance.yahoo.com/news/rssindex"
            feed = feedparser.parse(url)
            
            for entry in feed.entries[:50]:  # Limit to 50 most recent
                try:
                    headline = entry.get('title', '')
                    article_url = entry.get('link', '')
                    
                    # Try to get publication date
                    if 'published_parsed' in entry:
                        pub_time = datetime(*entry.published_parsed[:6])
                        pub_time = self.et_timezone.localize(pub_time)
                    else:
                        pub_time = datetime.now(self.et_timezone)
                    
                    # Combine headline and summary for pattern matching
                    summary = entry.get('summary', '')
                    full_text = f"{headline} {summary}"
                    
                    # Extract ticker and percentage
                    result = self.extract_ticker_and_percentage(full_text)
                    if result:
                        ticker, percentage, direction = result
                        
                        articles.append({
                            'ticker': ticker,
                            'claimed_percentage': percentage,
                            'direction': direction,
                            'headline': headline,
                            'article_url': article_url,
                            'source_name': 'Yahoo Finance',
                            'article_timestamp': pub_time.isoformat()
                        })
                
                except Exception as e:
                    print(f"Error processing Yahoo Finance entry: {e}")
                    continue
            
        except Exception as e:
            print(f"Error scraping Yahoo Finance: {e}")
        
        return articles
    
    def scrape_marketwatch_rss(self) -> List[Dict]:
        """
        Scrape MarketWatch RSS feed for news articles
        """
        articles = []
        
        try:
            url = "https://www.marketwatch.com/rss/topstories"
            feed = feedparser.parse(url)
            
            for entry in feed.entries[:50]:
                try:
                    headline = entry.get('title', '')
                    article_url = entry.get('link', '')
                    
                    if 'published_parsed' in entry:
                        pub_time = datetime(*entry.published_parsed[:6])
                        pub_time = self.et_timezone.localize(pub_time)
                    else:
                        pub_time = datetime.now(self.et_timezone)
                    
                    summary = entry.get('summary', '')
                    full_text = f"{headline} {summary}"
                    
                    result = self.extract_ticker_and_percentage(full_text)
                    if result:
                        ticker, percentage, direction = result
                        
                        articles.append({
                            'ticker': ticker,
                            'claimed_percentage': percentage,
                            'direction': direction,
                            'headline': headline,
                            'article_url': article_url,
                            'source_name': 'MarketWatch',
                            'article_timestamp': pub_time.isoformat()
                        })
                
                except Exception as e:
                    print(f"Error processing MarketWatch entry: {e}")
                    continue
            
        except Exception as e:
            print(f"Error scraping MarketWatch: {e}")
        
        return articles
    
    def scrape_benzinga_web(self) -> List[Dict]:
        """
        Scrape Benzinga website for news articles
        """
        articles = []
        
        try:
            url = "https://www.benzinga.com/news"
            
            # Add delay to respect rate limiting
            time.sleep(1)
            
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find article elements (structure may vary)
            article_elements = soup.find_all(['article', 'div'], class_=re.compile(r'story|article|news'), limit=30)
            
            for element in article_elements:
                try:
                    # Try to find headline
                    headline_elem = element.find(['h2', 'h3', 'a'], class_=re.compile(r'title|headline'))
                    if not headline_elem:
                        continue
                    
                    headline = headline_elem.get_text(strip=True)
                    
                    # Try to find link
                    link_elem = headline_elem if headline_elem.name == 'a' else headline_elem.find('a')
                    article_url = link_elem.get('href', '') if link_elem else ''
                    
                    if article_url and not article_url.startswith('http'):
                        article_url = f"https://www.benzinga.com{article_url}"
                    
                    # Get timestamp (approximate)
                    pub_time = datetime.now(self.et_timezone)
                    
                    # Extract ticker and percentage from headline
                    result = self.extract_ticker_and_percentage(headline)
                    if result:
                        ticker, percentage, direction = result
                        
                        articles.append({
                            'ticker': ticker,
                            'claimed_percentage': percentage,
                            'direction': direction,
                            'headline': headline,
                            'article_url': article_url,
                            'source_name': 'Benzinga',
                            'article_timestamp': pub_time.isoformat()
                        })
                
                except Exception as e:
                    print(f"Error processing Benzinga article: {e}")
                    continue
            
        except Exception as e:
            print(f"Error scraping Benzinga: {e}")
        
        return articles
    
    def scrape_all_sources(self) -> List[Dict]:
        """
        Scrape all configured news sources
        Returns combined list of articles
        """
        all_articles = []
        
        print("Scraping Yahoo Finance...")
        yahoo_articles = self.scrape_yahoo_finance_rss()
        all_articles.extend(yahoo_articles)
        print(f"Found {len(yahoo_articles)} articles from Yahoo Finance")
        
        # Rate limiting between sources
        time.sleep(2)
        
        print("Scraping MarketWatch...")
        marketwatch_articles = self.scrape_marketwatch_rss()
        all_articles.extend(marketwatch_articles)
        print(f"Found {len(marketwatch_articles)} articles from MarketWatch")
        
        time.sleep(2)
        
        print("Scraping Benzinga...")
        benzinga_articles = self.scrape_benzinga_web()
        all_articles.extend(benzinga_articles)
        print(f"Found {len(benzinga_articles)} articles from Benzinga")
        
        print(f"\nTotal articles found: {len(all_articles)}")
        
        return all_articles
    
    def get_todays_date(self) -> str:
        """Get today's date in ET timezone"""
        now = datetime.now(self.et_timezone)
        return now.strftime('%Y-%m-%d')
