from typing import List

from telegram import Update
from telegram.ext import (CallbackContext, CommandHandler, ConversationHandler,
                          MessageHandler, filters)

from .analysis import CLARIFYING_QUESTIONS, analyze_dream
from .knowledge_base import load_knowledge_base

# Conversation states
ASK_DREAM, ASK_CLARIFICATIONS = range(2)


def start(update: Update, context: CallbackContext) -> int:
    context.user_data.clear()
    update.message.reply_text(
        "Привет! Я помогу зафиксировать сон. Опиши его свободным текстом."
    )
    return ASK_DREAM


def receive_dream(update: Update, context: CallbackContext) -> int:
    dream_text = update.message.text
    context.user_data["dream_text"] = dream_text
    context.user_data["clarifications"] = []
    update.message.reply_text(CLARIFYING_QUESTIONS[0])
    return ASK_CLARIFICATIONS


def receive_clarification(update: Update, context: CallbackContext) -> int:
    clarifications: List[str] = context.user_data.get("clarifications", [])
    clarifications.append(update.message.text)
    context.user_data["clarifications"] = clarifications

    if len(clarifications) < len(CLARIFYING_QUESTIONS):
        update.message.reply_text(CLARIFYING_QUESTIONS[len(clarifications)])
        return ASK_CLARIFICATIONS

    kb = load_knowledge_base()
    dream_text = context.user_data.get("dream_text", "")
    analysis = analyze_dream(kb, dream_text, clarifications)
    update.message.reply_text(analysis)
    update.message.reply_text("Готово. Отправь новый текст сна или /start, чтобы начать заново.")
    context.user_data.clear()
    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    context.user_data.clear()
    update.message.reply_text("Ок, будем готовы начать заново, когда захочешь. Напиши /start.")
    return ConversationHandler.END


def build_conversation_handler() -> ConversationHandler:
    return ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASK_DREAM: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_dream)],
            ASK_CLARIFICATIONS: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_clarification)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        name="dream_conversation",
    )
