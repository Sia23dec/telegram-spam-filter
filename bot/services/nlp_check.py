from textblob import TextBlob

def get_sentiment_score(text: str) -> int:
    """Detects 'Urgency' or 'Aggression' common in scams."""
    analysis = TextBlob(text)
    # Scams often have high subjectivity (opinion/hype) and neutral-to-positive polarity
    if analysis.subjectivity > 0.8:
        return 2 # High hype/subjectivity
    return 0