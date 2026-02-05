import re
from dataclasses import dataclass

URL_RE = re.compile(r"https?://|t\.me/|bit\.ly/|tinyurl\.com", re.IGNORECASE)
PHONE_RE = re.compile(r"\+?\d[\d\s\-]{7,}")
REPEAT_CHAR_RE = re.compile(r"(.)\1{6,}")
ZALGO_RE = re.compile(r"[\u0300-\u036f]{3,}")

SUSPICIOUS_KEYWORDS = {
    "free", "crypto", "airdrop", "giveaway", "earn", "profit", "investment",
    "signal", "whatsapp", "adult", "dating", "loan", "click", "bonus",
}


@dataclass
class SpamResult:
    score: int
    reasons: list[str]


def score_message(text: str) -> SpamResult:
    if not text:
        return SpamResult(score=0, reasons=[])

    lowered = text.lower()
    score = 0
    reasons: list[str] = []

    if URL_RE.search(text):
        score += 3
        reasons.append("contains link")

    if PHONE_RE.search(text):
        score += 2
        reasons.append("contains phone-like pattern")

    if REPEAT_CHAR_RE.search(text):
        score += 2
        reasons.append("excessive repeated characters")

    if ZALGO_RE.search(text):
        score += 1
        reasons.append("unicode combining marks")

    keyword_hits = [k for k in SUSPICIOUS_KEYWORDS if k in lowered]
    if keyword_hits:
        score += min(3, len(keyword_hits))
        reasons.append("suspicious keywords: " + ", ".join(keyword_hits[:5]))

    if len(text) > 800:
        score += 1
        reasons.append("very long message")

    return SpamResult(score=score, reasons=reasons)
