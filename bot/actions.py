from datetime import timedelta, datetime, timezone
from telegram import ChatPermissions


async def warn_user(message, reasons: list[str]) -> None:
    reason_text = ", ".join(reasons) if reasons else "spam signal"
    await message.reply_text(
        f"Warning: your message looks like spam ({reason_text})."
    )


async def delete_message(message) -> None:
    try:
        await message.delete()
    except Exception:
        # Ignore if we lack rights or the message is already gone.
        return


async def mute_user(message, minutes: int = 10) -> None:
    try:
        until_date = datetime.now(timezone.utc) + timedelta(minutes=minutes)
        permissions = ChatPermissions(
            can_send_messages=False,
            can_send_polls=False,
            can_send_other_messages=False,
            can_add_web_page_previews=False,
            can_change_info=False,
            can_invite_users=False,
            can_pin_messages=False,
        )
        await message.chat.restrict_member(
            user_id=message.from_user.id,
            permissions=permissions,
            until_date=until_date,
        )
    except Exception:
        return
