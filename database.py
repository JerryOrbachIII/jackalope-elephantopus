"""
Database module for Stock Prediction Tracker
Handles all SQLite database operations
"""

import sqlite3
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import os

class Database:
    def __init__(self, db_path: str = "predictions.db"):
        """Initialize database connection and create tables if they don't exist"""
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Create all necessary tables and indexes"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Articles table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticker TEXT NOT NULL,
                claimed_percentage REAL NOT NULL,
                direction TEXT NOT NULL,
                article_timestamp TEXT NOT NULL,
                source_name TEXT NOT NULL,
                article_url TEXT UNIQUE NOT NULL,
                headline TEXT,
                status TEXT DEFAULT 'PENDING',
                is_duplicate INTEGER DEFAULT 0,
                collection_date TEXT NOT NULL
            )
        ''')
        
        # Price snapshots table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS price_snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                article_id INTEGER NOT NULL,
                check_timestamp TEXT NOT NULL,
                previous_close REAL NOT NULL,
                current_price REAL NOT NULL,
                actual_movement_pct REAL NOT NULL,
                gap REAL NOT NULL,
                FOREIGN KEY (article_id) REFERENCES articles (id)
            )
        ''')
        
        # Daily summary table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_summary (
                date TEXT PRIMARY KEY,
                total_predictions INTEGER,
                total_hits INTEGER,
                total_misses INTEGER,
                total_partials INTEGER,
                hit_rate REAL,
                avg_predicted_movement REAL,
                avg_actual_movement REAL,
                movement_accuracy REAL
            )
        ''')
        
        # Source accuracy table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS source_accuracy (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_name TEXT NOT NULL,
                date TEXT NOT NULL,
                predictions_count INTEGER,
                hits INTEGER,
                hit_rate REAL,
                avg_predicted REAL,
                avg_actual REAL,
                magnitude_accuracy REAL,
                weighted_score REAL
            )
        ''')
        
        # Create indexes
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_articles_ticker ON articles(ticker)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_articles_date ON articles(collection_date)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_articles_status ON articles(status)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_snapshots_article ON price_snapshots(article_id)')
        
        conn.commit()
        conn.close()
    
    def add_article(self, ticker: str, claimed_percentage: float, direction: str,
                    article_timestamp: str, source_name: str, article_url: str,
                    headline: str, collection_date: str) -> Optional[int]:
        """
        Add a new article to the database
        Returns article_id if successful, None if duplicate URL
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO articles 
                (ticker, claimed_percentage, direction, article_timestamp, 
                 source_name, article_url, headline, collection_date, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'PENDING')
            ''', (ticker, claimed_percentage, direction, article_timestamp,
                  source_name, article_url, headline, collection_date))
            
            article_id = cursor.lastrowid
            conn.commit()
            conn.close()
            return article_id
            
        except sqlite3.IntegrityError:
            # Duplicate URL
            return None
        except Exception as e:
            print(f"Error adding article: {e}")
            return None
    
    def add_price_snapshot(self, article_id: int, previous_close: float,
                          current_price: float, actual_movement_pct: float,
                          gap: float) -> bool:
        """Add a price snapshot for an article"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            check_timestamp = datetime.now().isoformat()
            
            cursor.execute('''
                INSERT INTO price_snapshots
                (article_id, check_timestamp, previous_close, current_price,
                 actual_movement_pct, gap)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (article_id, check_timestamp, previous_close, current_price,
                  actual_movement_pct, gap))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error adding price snapshot: {e}")
            return False
    
    def update_article_status(self, article_id: int, status: str) -> bool:
        """Update the status of an article"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE articles
                SET status = ?
                WHERE id = ?
            ''', (status, article_id))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error updating article status: {e}")
            return False
    
    def mark_as_duplicate(self, article_id: int) -> bool:
        """Mark an article as duplicate"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE articles
                SET is_duplicate = 1
                WHERE id = ?
            ''', (article_id,))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error marking duplicate: {e}")
            return False
    
    def get_todays_articles(self, collection_date: str) -> List[Dict]:
        """Get all articles for a specific date"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, ticker, claimed_percentage, direction, article_timestamp,
                   source_name, article_url, headline, status, is_duplicate
            FROM articles
            WHERE collection_date = ?
            ORDER BY article_timestamp DESC
        ''', (collection_date,))
        
        articles = []
        for row in cursor.fetchall():
            articles.append({
                'id': row[0],
                'ticker': row[1],
                'claimed_percentage': row[2],
                'direction': row[3],
                'article_timestamp': row[4],
                'source_name': row[5],
                'article_url': row[6],
                'headline': row[7],
                'status': row[8],
                'is_duplicate': bool(row[9])
            })
        
        conn.close()
        return articles
    
    def get_pending_articles(self) -> List[Dict]:
        """Get all articles with PENDING status"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, ticker, claimed_percentage, direction, article_timestamp,
                   source_name, article_url, headline, collection_date
            FROM articles
            WHERE status = 'PENDING'
        ''')
        
        articles = []
        for row in cursor.fetchall():
            articles.append({
                'id': row[0],
                'ticker': row[1],
                'claimed_percentage': row[2],
                'direction': row[3],
                'article_timestamp': row[4],
                'source_name': row[5],
                'article_url': row[6],
                'headline': row[7],
                'collection_date': row[8]
            })
        
        conn.close()
        return articles
    
    def get_latest_price_snapshot(self, article_id: int) -> Optional[Dict]:
        """Get the most recent price snapshot for an article"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT check_timestamp, previous_close, current_price,
                   actual_movement_pct, gap
            FROM price_snapshots
            WHERE article_id = ?
            ORDER BY check_timestamp DESC
            LIMIT 1
        ''', (article_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'check_timestamp': row[0],
                'previous_close': row[1],
                'current_price': row[2],
                'actual_movement_pct': row[3],
                'gap': row[4]
            }
        return None
    
    def get_daily_stats(self, date: str) -> Dict:
        """Calculate daily statistics for a given date"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN status = 'HIT' THEN 1 ELSE 0 END) as hits,
                SUM(CASE WHEN status = 'MISS' THEN 1 ELSE 0 END) as misses,
                SUM(CASE WHEN status = 'PARTIAL' THEN 1 ELSE 0 END) as partials,
                SUM(CASE WHEN status = 'PENDING' THEN 1 ELSE 0 END) as pending,
                AVG(claimed_percentage) as avg_predicted
            FROM articles
            WHERE collection_date = ?
        ''', (date,))
        
        row = cursor.fetchone()
        conn.close()
        
        total = row[0] or 0
        hits = row[1] or 0
        misses = row[2] or 0
        partials = row[3] or 0
        pending = row[4] or 0
        avg_predicted = row[5] or 0
        
        hit_rate = (hits / total * 100) if total > 0 else 0
        
        return {
            'total_predictions': total,
            'hits': hits,
            'misses': misses,
            'partials': partials,
            'pending': pending,
            'hit_rate': hit_rate,
            'avg_predicted': avg_predicted
        }
    
    def check_for_duplicates(self, ticker: str, claimed_percentage: float,
                            article_timestamp: str, collection_date: str) -> List[int]:
        """
        Check if similar articles exist
        Returns list of article IDs that are potential duplicates
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Parse timestamp
        try:
            article_time = datetime.fromisoformat(article_timestamp)
        except:
            article_time = datetime.now()
        
        # Check for articles with same ticker, similar percentage, within 2 hours
        cursor.execute('''
            SELECT id, article_timestamp, claimed_percentage
            FROM articles
            WHERE ticker = ?
            AND collection_date = ?
            AND ABS(claimed_percentage - ?) <= 3
        ''', (ticker, collection_date, claimed_percentage))
        
        duplicates = []
        for row in cursor.fetchall():
            article_id = row[0]
            existing_timestamp = row[1]
            
            try:
                existing_time = datetime.fromisoformat(existing_timestamp)
                time_diff = abs((article_time - existing_time).total_seconds() / 3600)
                
                if time_diff <= 2:
                    duplicates.append(article_id)
            except:
                continue
        
        conn.close()
        return duplicates
