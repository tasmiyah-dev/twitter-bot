#!/usr/bin/env python3
import logging
import time
import signal
import sys
from datetime import datetime

import schedule

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

def signal_handler(sig, frame):
    global running
    logger.info("Shutting down gracefully...")
    running = False
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def init():
    logger.info("Initializing Twitter Bot...")
    db.init_db()
    logger.info("Database initialized")
    
    logger.info(f"Scheduling daily quote post at {config.POST_TIME} IST")
    schedule.every().day.at(config.POST_TIME).do(post_daily_quote)
    
    logger.info(f"Monitoring hashtags: {config.HASHTAGS_TO_MONITOR}")
    logger.info(f"Reply keywords: {config.REPLY_KEYWORDS}")
    logger.info("Bot initialized successfully")

def run_scheduled_tasks():
    schedule.run_pending()

def main():
    init()
    
    logger.info("Starting main loop...")
    logger.info("Polling for mentions every 60 seconds")
    
    while running:
        try:
            run_scheduled_tasks()
            
            poll_and_reply_mentions()
            
            time.sleep(60)
            
        except KeyboardInterrupt:
            logger.info("Interrupted by user")
            break
        except Exception as e:
            logger.error(f"Error in main loop: {e}", exc_info=True)
            time.sleep(60)
    
    logger.info("Bot stopped")

if __name__ == "__main__":
    main()
