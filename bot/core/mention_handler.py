import logging
from datetime import datetime, timezone

from .. import config
from ..utils.twitter_api import TwitterClient
from ..utils import database as db
from .sentiment_analyzer import analyze_sentiment
from ..utils.openai_helper import generate_reply, moderate_text

logger = logging.getLogger(__name__)


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

    logger.info(f"Replied to mention {mention['id']} with {reply_id}")


def poll_and_reply_mentions():
    client = TwitterClient()
    since_id = db.get_state("mentions_since_id")
    mentions = client.get_mentions_since(since_id)
    if not mentions:
        return
    mentions = sorted(mentions, key=lambda m: int(m["id"]))
    for m in mentions:
        if _should_reply(m.get("text", "")):
            handle_mention(m)
        db.set_state("mentions_since_id", m["id"])  # update as we go
