import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


def _parse_bool(value: str, default: bool) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y"}


def _parse_int(value: str, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


@dataclass(frozen=True)
class Settings:
    bot_token: str
    spam_score_threshold: int
    warn_only: bool
    allowlist_user_ids: set[int]


def load_settings() -> Settings:
    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        raise RuntimeError("Missing TELEGRAM_BOT_TOKEN in environment")

    threshold = _parse_int(os.getenv("SPAM_SCORE_THRESHOLD"), 6)
    warn_only = _parse_bool(os.getenv("WARN_ONLY"), False)
    allowlist_raw = os.getenv("ALLOWLIST_USER_IDS", "")
    allowlist = set()
    for part in allowlist_raw.split(","):
        part = part.strip()
        if part:
            try:
                allowlist.add(int(part))
            except ValueError:
                continue

    return Settings(
        bot_token=token,
        spam_score_threshold=threshold,
        warn_only=warn_only,
        allowlist_user_ids=allowlist,
    )
