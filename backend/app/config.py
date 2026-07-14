"""Piece 1: shared config — loads env vars and builds the two models."""
import os
from pathlib import Path
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_ollama import OllamaEmbeddings

load_dotenv()  # reads the .env file into environment variables

OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://192.168.6.136:11434")
CHAT_MODEL = os.getenv("CHAT_MODEL", "gpt-oss:20b")
EMBED_MODEL = os.getenv("EMBED_MODEL", "nomic-embed-text")
CHROMA_DIR = os.getenv("CHROMA_DIR", "./chroma_rules")
CHARACTER_DIR = Path(os.getenv("CHARACTER_DIR", "./characters"))
CHARACTER_DIR.mkdir(exist_ok=True)

# The chat brain used by every agent. Low temp = reliable tool calls + JSON.
llm = init_chat_model(
    f"ollama:{CHAT_MODEL}", temperature=0.2, base_url=OLLAMA_URL
)

# The embedding model, used only by the rules RAG to turn text into vectors.
embeddings = OllamaEmbeddings(model=EMBED_MODEL, base_url=OLLAMA_URL)