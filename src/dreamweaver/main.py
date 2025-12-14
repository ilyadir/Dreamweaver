import os

from .handlers import build_conversation_handler


def run() -> None:
    try:
        from telegram.ext import Application
    except ImportError as exc:  # pragma: no cover - environment specific
        raise RuntimeError(
            "Install the python-telegram-bot package (>=20,<21) and remove any conflicting "
            "'telegram' package: pip uninstall telegram && pip install python-telegram-bot==20.7"
        ) from exc

    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not set")

    application = Application.builder().token(token).build()
    application.add_handler(build_conversation_handler())

    application.run_polling(allowed_updates=["message"])


if __name__ == "__main__":
    run()
