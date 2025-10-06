import sqlite3
import threading
from contextlib import contextmanager
from datetime import datetime, date
from typing import Optional, Iterable, Any, Dict

from .. import config

_lock = threading.Lock()

@contextmanager
def get_conn():
    with _lock:
        conn = sqlite3.connect(config.DB_PATH)
        try:
            conn.row_factory = sqlite3.Row
            yield conn
        finally:
            conn.commit()
            conn.close()

def init_db():
    with get_conn() as conn:
        c = conn.cursor()
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS tweets (
                id INTEGER PRIMARY KEY,
                tweet_id TEXT UNIQUE,
                content TEXT,
                type TEXT,
                likes INTEGER DEFAULT 0,
                retweets INTEGER DEFAULT 0,
                replies INTEGER DEFAULT 0,
                posted_at TIMESTAMP
            )
            """
        )
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY,
                user_id TEXT,
                username TEXT,
                tweet_id TEXT,
                interaction_type TEXT,
                our_response TEXT,
                sentiment REAL,
                created_at TIMESTAMP
            )
            """
        )
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS analytics (
                id INTEGER PRIMARY KEY,
                date DATE UNIQUE,
                followers_count INTEGER,
                mentions_count INTEGER,
                replies_sent INTEGER,
                avg_sentiment REAL,
                engagement_rate REAL
            )
            """
        )
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS state (
                key TEXT PRIMARY KEY,
                value TEXT
            )
            """
        )


def set_state(key: str, value: str):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO state(key, value) VALUES(?, ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
            (key, value),
        )


def get_state(key: str, default: Optional[str] = None) -> Optional[str]:
    with get_conn() as conn:
        cur = conn.execute("SELECT value FROM state WHERE key=?", (key,))
        row = cur.fetchone()
        return row[0] if row else default


def log_tweet(tweet_id: str, content: str, ttype: str, posted_at: Optional[datetime] = None):
    with get_conn() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO tweets(tweet_id, content, type, posted_at) VALUES (?, ?, ?, ?)",
            (tweet_id, content, ttype, posted_at or datetime.utcnow()),
        )


def update_tweet_metrics(tweet_id: str, likes: int, retweets: int, replies: int):
    with get_conn() as conn:
        conn.execute(
            "UPDATE tweets SET likes=?, retweets=?, replies=? WHERE tweet_id=?",
            (likes, retweets, replies, tweet_id),
        )


def log_interaction(user_id: str, username: str, tweet_id: str, interaction_type: str, our_response: str, sentiment: float):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO interactions(user_id, username, tweet_id, interaction_type, our_response, sentiment, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (user_id, username, tweet_id, interaction_type, our_response, sentiment, datetime.utcnow()),
        )


def upsert_analytics(day: date, followers_count: int, mentions_count: int, replies_sent: int, avg_sentiment: float, engagement_rate: float):
    with get_conn() as conn:
        conn.execute(
            """
            INSERT INTO analytics(date, followers_count, mentions_count, replies_sent, avg_sentiment, engagement_rate)
            VALUES(?, ?, ?, ?, ?, ?)
            ON CONFLICT(date) DO UPDATE SET
                followers_count=excluded.followers_count,
                mentions_count=excluded.mentions_count,
                replies_sent=excluded.replies_sent,
                avg_sentiment=excluded.avg_sentiment,
                engagement_rate=excluded.engagement_rate
            """,
            (day, followers_count, mentions_count, replies_sent, avg_sentiment, engagement_rate),
        )
