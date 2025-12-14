# Dreamweaver Telegram Bot (MVP)

This repository contains a minimal Telegram bot that collects a dream report, asks two clarifying questions, and returns an analysis based on a small knowledge base of archetypes, motifs, and interpretive methods. The current implementation runs locally and does not call external LLM services.

## Features
- Collect a dream description from the user.
- Ask two clarifying questions to refine context.
- Generate an analysis using a fixed template that references a curated knowledge base (80 cards covering archetypes, motifs, and method tips).
- Stateless start-over flow with the `/start` command.

## Quickstart
1. **Install dependencies**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. **Set environment variables**
   - `TELEGRAM_BOT_TOKEN`: Telegram bot token from BotFather.
3. **Run the bot**
   ```bash
   python -m dreamweaver.main
   ```
   You can also run the file directly from the repo root if you prefer:
   ```bash
   PYTHONPATH=src python src/dreamweaver/main.py
   ```

If you see an import error mentioning `telegram.Chat`, make sure you do **not** have the legacy
`telegram` package installed. Remove it and reinstall the pinned dependency:
```bash
pip uninstall telegram
pip install -r requirements.txt
```

## Project structure
- `src/dreamweaver/main.py`: Entrypoint that wires handlers and starts polling.
- `src/dreamweaver/handlers.py`: Conversation handlers for collecting dreams, clarifications, and generating the response.
- `src/dreamweaver/analysis.py`: Matching and templating logic for the dream analysis.
- `src/dreamweaver/knowledge_base.py`: Loading and querying the static knowledge base.
- `data/knowledge_base.json`: Curated archetype, motif, and method cards.

## Customizing
- Add or edit cards in `data/knowledge_base.json` to tune interpretations.
- Adjust clarifying questions in `handlers.py` if your domain needs different probes.
- Replace the templating in `analysis.py` with a call to your preferred LLM or RAG pipeline once available.

## Testing locally without Telegram
Use the `demo_analyze` helper to simulate an interaction:
```bash
python - <<'PY'
from dreamweaver.analysis import analyze_dream
from dreamweaver.knowledge_base import load_knowledge_base

kb = load_knowledge_base()
print(analyze_dream(
    kb,
    dream_text="I was walking through a forest and found a hidden door.",
    clarification_answers=["I felt curious and a little afraid.", "The forest reminded me of childhood trips."]
))
PY
```
