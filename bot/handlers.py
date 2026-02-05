from telegram import Update
from telegram.ext import ContextTypes

from .actions import warn_user, delete_message, mute_user
from .filters import score_message
from .config import Settings


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message
    if message is None or message.from_user is None:
        return

    settings: Settings = context.bot_data["settings"]

    if message.from_user.is_bot:
        return

    if message.from_user.id in settings.allowlist_user_ids:
        return

    text = message.text or message.caption or ""
    result = score_message(text)

    if result.score < settings.spam_score_threshold:
        return

    if settings.warn_only:
        await warn_user(message, result.reasons)
        return

    await delete_message(message)
    await warn_user(message, result.reasons)
    await mute_user(message)
