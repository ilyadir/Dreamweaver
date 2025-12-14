from datetime import datetime
from typing import Iterable, List, Sequence

from .knowledge_base import KnowledgeCard, find_matches


CLARIFYING_QUESTIONS = [
    "Что в этом сне вызвало у тебя самые сильные эмоции?",
    "С чем из реальной жизни сейчас больше всего рифмуется этот сон?",
]


def format_analysis(
    dream_text: str,
    clarifications: Sequence[str],
    matches: Iterable[KnowledgeCard],
) -> str:
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    archetypes = [m for m in matches if m.category == "archetype"]
    motifs = [m for m in matches if m.category == "motif"]
    methods = [m for m in matches if m.category == "method"]

    def bullet(items: List[KnowledgeCard]) -> str:
        if not items:
            return "- (ничего не найдено, используй общее наблюдение)"
        return "\n".join(
            f"- {item.name}: {item.summary}"
            for item in items[:3]
        )

    return (
        f"🌓 Разбор сна — прототип\n"
        f"Время: {now}\n\n"
        f"Исходный текст:\n{dream_text.strip()}\n\n"
        f"Уточнения:\n"
        + "\n".join(f"{i+1}) {answer}" for i, answer in enumerate(clarifications))
        + "\n\n"
        "Что откликается в базе знаний:\n"
        "Архетипы:\n" + bullet(archetypes) + "\n\n"
        "Мотивы:\n" + bullet(motifs) + "\n\n"
        "Методы для самостоятельной работы:\n" + bullet(methods) + "\n\n"
        "Следующий шаг: выбери один метод и зафиксируй, что попробуешь сделать в течение 24 часов."
    )


def analyze_dream(
    cards: List[KnowledgeCard],
    dream_text: str,
    clarification_answers: Sequence[str],
) -> str:
    combined_text = "\n".join([dream_text, *clarification_answers])
    matches = find_matches(cards, combined_text, limit=9)
    return format_analysis(dream_text, clarification_answers, matches)
