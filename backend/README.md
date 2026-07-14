# 🐉 Backend — The AI Game Master

The Python brain of the project: a LangGraph **supervisor** agent (the Game Master) that delegates to two specialist agents and a dice tool, all running on a **local Ollama model**.

## Architecture

| Piece | File | Job |
|---|---|---|
| Config | `app/config.py` | Loads `.env`, builds the chat + embedding models |
| Dice tool | `app/tools/dice.py` | Real randomness — parses `1d20+2` style notation |
| Character tools | `app/tools/characters.py` | Rolls 4d6-drop-lowest stats, saves sheets as JSON |
| Character agent | `app/agents/character_agent.py` | Creates/fetches characters via the tools |
| Rules RAG | `app/rag/index.py` | Chunks + embeds `rules/srd.md` into Chroma |
| Rules agent | `app/agents/rules_agent.py` | Answers rules questions grounded in the rulebook |
| Game Master | `app/agents/game_master.py` | Supervisor that routes to the specialists and narrates |
| Structured turn | `app/schemas.py` + `app/game.py` | Formats each turn into `narrative / suggested_actions / dice` |
| CLI | `app/cli.py` | Terminal game loop |

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # point OLLAMA_BASE_URL at your Ollama server
```

Pull the models on your Ollama host:

```bash
ollama pull gpt-oss:20b
ollama pull nomic-embed-text
```

## Play in the terminal

```bash
python -m app.cli
```

## Run as a LangGraph server (for the web UI)

```bash
langgraph dev
```

The first run builds the Chroma rules index (slow); later runs load it from disk.
