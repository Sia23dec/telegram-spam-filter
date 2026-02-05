import logging
from telegram.ext import ApplicationBuilder, MessageHandler, filters

from .config import load_settings
from .handlers import handle_message


def main() -> None:
    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        level=logging.INFO,
    )

    settings = load_settings()

    app = ApplicationBuilder().token(settings.bot_token).build()
    app.bot_data["settings"] = settings

    message_filter = filters.TEXT | filters.CAPTION
    app.add_handler(MessageHandler(message_filter, handle_message))

    app.run_polling(close_loop=False)


if __name__ == "__main__":
    main()
