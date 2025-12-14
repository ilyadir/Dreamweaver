import os

from telegram.ext import Application

from .handlers import build_conversation_handler


def run() -> None:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not set")

    application = Application.builder().token(token).build()
    application.add_handler(build_conversation_handler())

    application.run_polling(allowed_updates=["message"])


if __name__ == "__main__":
    run()
