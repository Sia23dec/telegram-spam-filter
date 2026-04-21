from .services.cas_check import check_global_ban
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from datetime import datetime, timedelta

from .actions import warn_user, delete_message, mute_user, ban_user, log_to_admin
from .filters import score_message
from .config import Settings
from .database import increment_warning, reset_warnings
from .services.user_check import get_profile_spam_score

# In-memory storage for anti-flood (clears on restart)
user_message_stats = {} 

async def handle_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """CAPTCHA: Mute new users until they click a button."""
    for member in update.message.new_chat_members:
        if member.is_bot: continue
        
        await context.bot.restrict_chat_member(
            chat_id=update.effective_chat.id,
            user_id=member.id,
            permissions={"can_send_messages": False}
        )
        
        keyboard = [[InlineKeyboardButton("I am human ✅", callback_data=f"verify_{member.id}")]]
        await update.message.reply_text(
            f"Welcome {member.first_name}! Click below to verify.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the CAPTCHA button click."""
    query = update.callback_query
    user_id = int(query.data.split("_")[1])
    
    if query.from_user.id != user_id:
        return await query.answer("This is not for you!", show_alert=True)
    
    await context.bot.restrict_chat_member(
        chat_id=update.effective_chat.id,
        user_id=user_id,
        permissions={"can_send_messages": True, "can_send_other_messages": True}
    )
    await query.message.delete()
    await query.answer("Verified!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message
    if not message or not message.from_user: return
    settings: Settings = context.bot_data["settings"]

    if message.from_user.is_bot:
        return
    # Emergency demo override: score allowlisted users too.
    # if message.from_user.id in settings.allowlist_user_ids:
    #     return

    if await check_global_ban(message.from_user.id):
        await ban_user(message)
        await message.reply_text("🚫 User is globally blacklisted for spam. Auto-banned.")
        return

    # 1. ANTI-FLOOD Check
    now = datetime.now()
    u_id = message.from_user.id
    user_stats = user_message_stats.get(u_id, [])
    user_stats = [t for t in user_stats if (now - t).seconds < 10]
    user_stats.append(now)
    user_message_stats[u_id] = user_stats
    
    if len(user_stats) > settings.flood_threshold:
        await delete_message(message)
        await log_to_admin(context, f"User {u_id} flagged for FLOODING.")
        return

    # 2. SCORING
    text = message.text or message.caption or ""
    result = score_message(text)
    
    # Add profile scrutiny score
    profile_score = await get_profile_spam_score(update)
    final_score = result.score + profile_score

    if final_score < settings.spam_score_threshold:
        return

    # 3. ACTIONS & DB ESCALATION
    await delete_message(message)
    
    if settings.warn_only:
        await warn_user(message, result.reasons)
        return

    count = await increment_warning(u_id)
    await log_to_admin(context, f"Spam detected from {u_id}. Score: {final_score}. Warnings: {count}")

    if count >= settings.max_warnings:
        await ban_user(message)
        await message.reply_text("⛔ User banned for repeated spamming.")
    else:
        await warn_user(message, result.reasons, count)
        await mute_user(message)

# ADMIN COMMANDS
async def admin_unwarn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    settings: Settings = context.bot_data["settings"]
    if update.effective_user.id not in settings.admin_ids: return
    
    if update.message.reply_to_message:
        target_id = update.message.reply_to_message.from_user.id
        await reset_warnings(target_id)
        await update.message.reply_text("✅ Warnings reset for user.")
