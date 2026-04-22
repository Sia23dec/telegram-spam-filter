import re
from dataclasses import dataclass

# Expanded URL Regex to catch redirection services
URL_RE = re.compile(r"https?://|t\.me/|bit\.ly/|tinyurl\.com|cutt\.ly|ow\.ly|is\.gd|buff\.ly", re.IGNORECASE)
# Regex for file-sharing patterns (Piracy)
FILE_RE = re.compile(r"\.(pdf|epub|mobi|zip|rar|exe|dmg|apk)$", re.IGNORECASE)
REPEAT_CHAR_RE = re.compile(r"(.)\1{6,}")
ZALGO_RE = re.compile(r"[\u0300-\u036f]{3,}")

# CATEGORIZED KEYWORDS
SCAM_KEYWORDS = {
    "free", "money", "crypto", "airdrop", "giveaway", "earn", "profit", "investment",
    "signal", "whatsapp", "loan", "click", "bonus", "verify", "account", "prize"
}

PIRACY_KEYWORDS = {
    "download", "full book", "pirated", "cracked", "libgen", "z-library", "torrent", 
    "free pdf", "premium free", "leaked"
}

# Add local slangs or rude words here
TOXIC_KEYWORDS = {
    "shut up", "idiot", "stupid", "dumb", "trash", "hate you", "loser", 
    "kill yourself", "kys", "motherfucker" # Add more college-specific slangs
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

    # 1. LINK DETECTION (Redirection/Scam)
    if URL_RE.search(text):
        score += 3
        reasons.append("contains link/redirection")

    # 2. PIRACY DETECTION
    if FILE_RE.search(text) or any(k in lowered for k in PIRACY_KEYWORDS):
        score += 4 # High penalty for piracy links
        reasons.append("potential piracy/illegal download")

    # 3. TOXICITY/RUDE BEHAVIOR
    toxic_hits = [k for k in TOXIC_KEYWORDS if k in lowered]
    if toxic_hits:
        score += 3
        reasons.append(f"toxic language detected: {toxic_hits[0]}")

    # 4. SCAM KEYWORDS
    scam_hits = [k for k in SCAM_KEYWORDS if k in lowered]
    if scam_hits:
        score += min(4, len(scam_hits))
        reasons.append("scam/clickbait patterns")

    # 5. TECHNICAL TRICKS
    if REPEAT_CHAR_RE.search(text):
        score += 2
        reasons.append("excessive repeated characters")

    if ZALGO_RE.search(text):
        score += 2
        reasons.append("unicode evasion (zalgo)")

    return SpamResult(score=score, reasons=reasons)
