import importlib.util
import os
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.append(str(Path(__file__).resolve().parents[1]))
    from dreamweaver.handlers import build_conversation_handler
else:
    from .handlers import build_conversation_handler

if importlib.util.find_spec("telegram.ext") is None:  # pragma: no cover - import-time validation
    raise RuntimeError(
        "Install the python-telegram-bot package (>=20,<21) and remove any conflicting "
        "'telegram' package: pip uninstall telegram && pip install python-telegram-bot==20.7"
    )

from telegram.ext import Application


def run() -> None:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not set")

    application = Application.builder().token(token).build()
    application.add_handler(build_conversation_handler())

    application.run_polling(allowed_updates=["message"])


if __name__ == "__main__":
    run()
