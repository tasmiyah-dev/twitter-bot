from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

_analyzer = SentimentIntensityAnalyzer()


def analyze_sentiment(text: str):
    scores = _analyzer.polarity_scores(text or "")
    compound = scores.get("compound", 0.0)
    label = "positive" if compound >= 0.05 else ("negative" if compound <= -0.05 else "neutral")
    return label, compound
