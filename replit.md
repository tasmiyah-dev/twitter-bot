# Twitter Automation Bot

## Overview
A Python-based Twitter automation bot that posts daily motivational quotes with custom-generated images, monitors mentions, and generates AI-powered replies using OpenAI GPT-4. The bot includes sentiment analysis, content moderation, and comprehensive analytics tracking.

## Current State
- **Status**: Fully operational and running
- **Last Updated**: October 6, 2025
- **Database**: SQLite initialized with tables for tweets, interactions, analytics, and state

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

## Running the Bot
The bot runs continuously via the "Twitter Bot" workflow:
- Initializes database on startup
- Schedules daily quote post at 9:00 AM IST
- Polls for mentions every 60 seconds
- Automatically handles Twitter rate limits with exponential backoff

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

## User Preferences
- None specified yet
