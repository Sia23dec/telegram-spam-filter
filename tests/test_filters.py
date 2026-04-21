from bot.filters import score_message

def test_spam_detection():
    # Test clean message
    assert score_message("Hello friend, how are you?").score == 0
    
    # Test obvious spam
    result = score_message("FREE CRYPTO AIRDROP CLICK NOW http://scam.me")
    assert result.score >= 5
    assert "contains link" in result.reasons


def test_bare_domain_is_detected_as_link():
    result = score_message("google.com")
    assert result.score >= 3
    assert "contains link" in result.reasons
