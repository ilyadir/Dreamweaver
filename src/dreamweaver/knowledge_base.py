from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Sequence
import json


@dataclass
class KnowledgeCard:
    id: str
    category: str
    name: str
    summary: str
    keywords: Sequence[str]


def load_knowledge_base(
    path: Path | str = Path(__file__).resolve().parents[2] / "data" / "knowledge_base.json",
) -> List[KnowledgeCard]:
    data_path = Path(path)
    with data_path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return [KnowledgeCard(**item) for item in payload]


def find_matches(cards: Iterable[KnowledgeCard], text: str, limit: int = 5) -> List[KnowledgeCard]:
    lowered = text.lower()
    matches: List[KnowledgeCard] = []
    for card in cards:
        if any(keyword in lowered for keyword in card.keywords):
            matches.append(card)
        if len(matches) >= limit:
            break
    if not matches:
        matches = list(cards)[:limit]
    return matches
