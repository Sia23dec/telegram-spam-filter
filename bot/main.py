import logging, asyncio
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, CommandHandler

from .config import load_settings
from .handlers import handle_message, handle_new_member, handle_callback, admin_unwarn
from .database import init_db

def main() -> None:
    logging.basicConfig(level=logging.INFO)
    settings = load_settings()

    # Init DB
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_db())

    app = ApplicationBuilder().token(settings.bot_token).build()
    app.bot_data["settings"] = settings

    # Handlers
    app.add_handler(CommandHandler("unwarn", admin_unwarn))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, handle_new_member))
    app.add_handler(CallbackQueryHandler(handle_callback))
    
    message_filter = (filters.TEXT | filters.CAPTION) & (~filters.COMMAND)
    app.add_handler(MessageHandler(message_filter, handle_message))

    print("Bot is running...")
    app.run_polling(close_loop=False)

if __name__ == "__main__":
    main()
