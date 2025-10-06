#!/usr/bin/env python3
import logging
import time
import signal
import sys
import threading
from datetime import datetime

import schedule
from flask import Flask, jsonify

from bot import config
from bot.utils import database as db
from bot.core.quote_poster import post_daily_quote
from bot.core.mention_handler import poll_and_reply_mentions

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(f"{config.LOG_DIR}/bot.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

running = True
bot_thread = None

app = Flask(__name__)

@app.route('/health')
def health_check():
    """Health check endpoint for uptime monitoring."""
    bot_status = "running" if bot_thread and bot_thread.is_alive() else "stopped"
    return jsonify({
        "status": "alive",
        "bot_status": bot_status,
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route('/')
def index():
    """Root endpoint."""
    return jsonify({
        "name": "Twitter Automation Bot",
        "status": "online",
        "endpoints": {
            "health": "/health"
        }
    })

def signal_handler(sig, frame):
    global running
    logger.info("Shutting down gracefully...")
    running = False
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def schedule_ist_job():
    """Wrapper to ensure scheduled job runs in IST timezone context."""
    now_ist = datetime.now(config.IST_TZ)
    logger.info(f"Running scheduled quote post at {now_ist.strftime('%Y-%m-%d %H:%M:%S')} IST")
    post_daily_quote()

def init_bot():
    """Initialize the bot database and scheduler."""
    logger.info("Initializing Twitter Bot...")
    db.init_db()
    logger.info("Database initialized")
    
    logger.info(f"Scheduling daily quote post at {config.POST_TIME} IST")
    logger.info("Note: Schedule library uses local system time. Ensure host timezone is set to IST or adjust accordingly.")
    schedule.every().day.at(config.POST_TIME).do(schedule_ist_job)
    
    logger.info(f"Monitoring hashtags: {config.HASHTAGS_TO_MONITOR}")
    logger.info(f"Reply keywords: {config.REPLY_KEYWORDS}")
    logger.info(f"Max replies per hour: {config.MAX_REPLIES_PER_HOUR}")
    logger.info("Bot initialized successfully")

def run_bot_loop():
    """Main bot loop that runs in background thread."""
    global running
    
    init_bot()
    
    logger.info("Starting bot loop in background thread...")
    logger.info("Polling for mentions every 60 seconds")
    
    while running:
        try:
            schedule.run_pending()
            poll_and_reply_mentions()
            time.sleep(60)
            
        except KeyboardInterrupt:
            logger.info("Bot loop interrupted by user")
            break
        except Exception as e:
            logger.error(f"Error in bot loop: {e}", exc_info=True)
            time.sleep(60)
    
    logger.info("Bot loop stopped")

def start_bot_thread():
    """Start the bot in a background thread with auto-restart."""
    global bot_thread
    
    def bot_wrapper():
        """Wrapper that auto-restarts the bot on crash."""
        while running:
            try:
                run_bot_loop()
            except Exception as e:
                logger.error(f"Bot thread crashed: {e}", exc_info=True)
                if running:
                    logger.info("Restarting bot in 10 seconds...")
                    time.sleep(10)
                else:
                    break
    
    bot_thread = threading.Thread(target=bot_wrapper, daemon=True, name="BotThread")
    bot_thread.start()
    logger.info("Bot thread started")

def main():
    """Main entry point - starts bot thread and Flask server."""
    logger.info("=" * 60)
    logger.info("Twitter Automation Bot - 24/7 Mode")
    logger.info("=" * 60)
    
    start_bot_thread()
    
    logger.info("Starting Flask web server on port 5000...")
    logger.info("Health check endpoint: http://localhost:5000/health")
    logger.info("Use UptimeRobot or similar to ping /health every 5 minutes")
    
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

if __name__ == "__main__":
    main()
