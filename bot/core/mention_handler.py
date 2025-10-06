import logging
from datetime import datetime, timezone, timedelta

from .. import config
from ..utils.twitter_api import TwitterClient
from ..utils import database as db
from .sentiment_analyzer import analyze_sentiment
from ..utils.openai_helper import generate_reply, moderate_text

logger = logging.getLogger(__name__)

_reply_timestamps = []


def _can_reply() -> bool:
    """Check if we can send another reply based on rate limit."""
    global _reply_timestamps
    now = datetime.utcnow()
    one_hour_ago = now - timedelta(hours=1)
    
    _reply_timestamps = [ts for ts in _reply_timestamps if ts > one_hour_ago]
    
    if len(_reply_timestamps) >= config.MAX_REPLIES_PER_HOUR:
        logger.warning(f"Rate limit reached: {len(_reply_timestamps)} replies in the last hour. Skipping.")
        return False
    
    return True


def _record_reply():
    """Record that we sent a reply."""
    global _reply_timestamps
    _reply_timestamps.append(datetime.utcnow())


def _should_reply(text: str) -> bool:
    if not text:
        return False
    t = text.lower()
    return any(k in t for k in config.REPLY_KEYWORDS) or True  # reply to all mentions politely


def handle_mention(mention: dict):
    text = mention.get("text", "")
    author = mention.get("author", {})

    if not moderate_text(text):
        logger.info("Skipping reply due to moderation")
        return

    if not _can_reply():
        return

    label, score = analyze_sentiment(text)

    context = {
        "text": text,
        "profile": {
            "username": author.get("username"),
            "bio": author.get("description"),
            "followers": author.get("followers", 0),
        },
        "sentiment": label,
    }

    reply = generate_reply(context)

    client = TwitterClient()
    reply_id = client.reply(mention["id"], reply[:270])

    db.log_interaction(
        user_id=author.get("id", ""),
        username=author.get("username", ""),
        tweet_id=mention["id"],
        interaction_type="mention",
        our_response=reply,
        sentiment=score,
    )

    _record_reply()
    logger.info(f"Replied to mention {mention['id']} with {reply_id}")


def poll_and_reply_mentions():
    try:
        client = TwitterClient()
        since_id = db.get_state("mentions_since_id")
        mentions = client.get_mentions_since(since_id)
        if not mentions:
            return
        mentions = sorted(mentions, key=lambda m: int(m["id"]))
        for m in mentions:
            try:
                if _should_reply(m.get("text", "")):
                    handle_mention(m)
            except Exception as e:
                logger.error(f"Error handling mention {m.get('id')}: {e}", exc_info=True)
            finally:
                db.set_state("mentions_since_id", m["id"])  # update as we go
    except Exception as e:
        logger.error(f"Error polling mentions: {e}", exc_info=True)
