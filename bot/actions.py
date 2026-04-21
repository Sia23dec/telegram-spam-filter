from datetime import timedelta, datetime, timezone
from telegram import ChatPermissions, Update
from telegram.ext import ContextTypes

async def warn_user(message, reasons: list[str], count: int = 0) -> None:
    reason_text = ", ".join(reasons) if reasons else "spam signal"
    await message.reply_text(
        f"⚠️ Warning {count}: Your message looks like spam ({reason_text})."
    )

async def delete_message(message) -> None:
    try: await message.delete()
    except: return

async def mute_user(message, minutes: int = 10) -> None:
    try:
        until_date = datetime.now(timezone.utc) + timedelta(minutes=minutes)
        permissions = ChatPermissions(can_send_messages=False)
        await message.chat.restrict_member(user_id=message.from_user.id, permissions=permissions, until_date=until_date)
    except: return

async def ban_user(message) -> None:
    try:
        await message.chat.ban_member(user_id=message.from_user.id)
    except: return

async def log_to_admin(context: ContextTypes.DEFAULT_TYPE, text: str):
    log_id = context.bot_data["settings"].log_channel_id
    if log_id:
        try: await context.bot.send_message(chat_id=log_id, text=f"🛡 LOG: {text}")
        except: pass
            
