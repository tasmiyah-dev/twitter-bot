import os
from dotenv import load_dotenv
from zoneinfo import ZoneInfo

# Load .env if present
load_dotenv()

# Environment variables (never commit secrets)
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY", "")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET", "")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN", "")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET", "")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Configuration
POST_TIME = "09:00"  # IST
IST_TZ = ZoneInfo("Asia/Kolkata")
HASHTAGS_TO_MONITOR = ["freelancing", "webdevelopment", "AItools"]
REPLY_KEYWORDS = ["pricing", "cost", "hire", "available"]
MAX_REPLIES_PER_HOUR = 30
SENTIMENT_ALERT_THRESHOLD = -0.5

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
DB_PATH = os.path.join(DATA_DIR, "bot.db")
QUOTES_JSON = os.path.join(DATA_DIR, "quotes.json")
MEDIA_DIR = os.path.join(DATA_DIR, "media")
LOG_DIR = os.path.join(BASE_DIR, "..", "logs")

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MEDIA_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)
