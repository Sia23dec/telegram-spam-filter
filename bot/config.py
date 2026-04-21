import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

def _parse_bool(value: str, default: bool) -> bool:
    if value is None: return default
    return str(value).strip().lower() in {"1", "true", "yes", "y"}

def _parse_int(value: str, default: int) -> int:
    try: return int(value)
    except: return default

@dataclass(frozen=True)
class Settings:
    bot_token: str
    spam_score_threshold: int
    warn_only: bool
    allowlist_user_ids: set[int]
    # NEW SETTINGS
    admin_ids: set[int]
    log_channel_id: int
    max_warnings: int
    flood_threshold: int # messages per 10 seconds

def load_settings() -> Settings:
    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    if not token: raise RuntimeError("Missing TELEGRAM_BOT_TOKEN")

    admins = {int(x.strip()) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()}
    allowlist = {int(x.strip()) for x in os.getenv("ALLOWLIST_USER_IDS", "").split(",") if x.strip()}

    return Settings(
        bot_token=token,
        spam_score_threshold=_parse_int(os.getenv("SPAM_SCORE_THRESHOLD"), 6),
        warn_only=_parse_bool(os.getenv("WARN_ONLY"), False),
        allowlist_user_ids=allowlist,
        admin_ids=admins,
        log_channel_id=_parse_int(os.getenv("LOG_CHANNEL_ID"), 0),
        max_warnings=_parse_int(os.getenv("MAX_WARNINGS"), 3),
        flood_threshold=_parse_int(os.getenv("FLOOD_THRESHOLD"), 5)
    )
