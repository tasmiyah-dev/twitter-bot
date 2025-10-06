# Twitter Automation Bot

## Overview
A Python-based Twitter automation bot that posts daily motivational quotes with custom-generated images, monitors mentions, and generates AI-powered replies using OpenAI GPT-4. The bot includes sentiment analysis, content moderation, and comprehensive analytics tracking.

## Current State
- **Status**: Fully operational and running 24/7
- **Last Updated**: October 6, 2025
- **Database**: SQLite initialized with tables for tweets, interactions, analytics, and state
- **Mode**: 24/7 continuous operation with Flask web server and health monitoring

## Features
1. **Daily Quote Posting**: Scheduled daily posts at 9:00 AM IST with custom-generated quote images
2. **AI-Powered Mention Replies**: Monitors mentions every 60 seconds and generates context-aware replies using OpenAI
3. **Sentiment Analysis**: Uses VADER sentiment analysis to track interaction sentiment
4. **Content Moderation**: All incoming mentions are filtered through OpenAI's moderation API before replies are generated
5. **Rate Limiting**: Max 30 replies per hour to avoid spam detection
6. **Hashtag Monitoring**: Tracks keywords (freelancing, webdevelopment, AItools)
7. **Analytics Tracking**: Logs all interactions, tweets, and metrics in SQLite database

## Project Architecture

### Directory Structure
```
├── bot/
│   ├── __init__.py
│   ├── config.py                 # Configuration and environment variables
│   ├── core/
│   │   ├── __init__.py
│   │   ├── mention_handler.py    # Mention polling and reply logic
│   │   ├── quote_poster.py       # Daily quote posting with image generation
│   │   └── sentiment_analyzer.py # VADER sentiment analysis
│   └── utils/
│       ├── __init__.py
│       ├── database.py            # SQLite database operations
│       ├── openai_helper.py       # OpenAI API integration
│       └── twitter_api.py         # Twitter API v2 wrapper
├── data/
│   ├── quotes.json                # Quote library (20 quotes across 4 categories)
│   ├── media/                     # Generated quote images
│   └── bot.db                     # SQLite database (auto-created)
├── logs/
│   └── bot.log                    # Application logs
├── main.py                        # Entry point with scheduling loop
└── .env.example                   # Template for API credentials
```

### Dependencies
- **tweepy 4.16.0**: Twitter API v1.1 and v2 client
- **openai 2.1.0**: OpenAI GPT-4 and moderation API
- **vaderSentiment 3.3.2**: Sentiment analysis
- **Pillow 11.3.0**: Image generation for quotes
- **schedule 1.2.2**: Task scheduling
- **python-dotenv 1.1.1**: Environment variable management
- **Flask 3.1.2**: Web server for health monitoring and keeping Repl alive

### Database Schema
- **tweets**: Tracks posted tweets with metrics (likes, retweets, replies)
- **interactions**: Logs all user interactions with sentiment scores
- **analytics**: Daily aggregated metrics (followers, mentions, engagement)
- **state**: Key-value store for tracking API cursors (e.g., last seen mention ID)

## API Credentials (Stored in Replit Secrets)
- `TWITTER_API_KEY`: Twitter API consumer key
- `TWITTER_API_SECRET`: Twitter API consumer secret
- `TWITTER_ACCESS_TOKEN`: User access token
- `TWITTER_ACCESS_TOKEN_SECRET`: User access token secret
- `TWITTER_BEARER_TOKEN`: Bearer token for v2 API
- `OPENAI_API_KEY`: OpenAI API key for GPT-4 and moderation

## Running the Bot - 24/7 Mode

The bot runs continuously via the "Twitter Bot" workflow with Flask web server:

### Architecture
- **Flask Web Server**: Runs on port 5000 to keep the Repl alive
- **Background Bot Thread**: Bot logic runs in a daemon thread named "BotThread"
- **Auto-Restart**: If the bot crashes, it automatically restarts after 10 seconds
- **Health Monitoring**: `/health` endpoint for external uptime monitoring

### Endpoints
- **GET /**: Root endpoint showing bot info and available endpoints
- **GET /health**: Health check endpoint returning `{"status": "alive", "bot_status": "running", "timestamp": "..."}`

### Bot Operations
- Initializes database on startup
- Schedules daily quote post at 9:00 AM IST
- Polls for mentions every 60 seconds
- Automatically handles Twitter rate limits with exponential backoff
- Enforces 30 replies per hour limit

### Keeping the Bot Running 24/7
To ensure the bot never sleeps:
1. The Flask web server on port 5000 keeps the Repl active
2. Set up **UptimeRobot** (or similar service) to ping the `/health` endpoint every 5 minutes
3. Use your Repl's public URL: `https://[your-repl-name].[your-username].repl.co/health`

This setup ensures continuous 24/7 operation without interruption.

## Known Behaviors
- Twitter API has strict rate limits - the bot automatically waits when limits are exceeded
- LSP diagnostics show import warnings (packages installed via uv, not issues)
- Quote categories rotate by day of week (Business, Success, Motivation, Technology)
- All AI-generated replies are kept under 270 characters to fit Twitter's limits

## Recent Changes
- **2025-10-06**: Initial project setup with all core modules
- **2025-10-06**: Installed Python 3.11 and all required packages
- **2025-10-06**: Created database schema and quote library (20 quotes)
- **2025-10-06**: Configured workflow and verified bot startup
- **2025-10-06**: Bot successfully running and handling Twitter API rate limits
- **2025-10-06**: Added Flask web server for 24/7 operation with health monitoring
- **2025-10-06**: Refactored bot to run in background thread with auto-restart on crash
- **2025-10-06**: Created /health endpoint for UptimeRobot monitoring

## User Preferences
- None specified yet
