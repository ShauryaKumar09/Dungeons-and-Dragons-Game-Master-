"""Piece 4a: build the rules vector index on first run, load it after."""
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from app.config import embeddings, CHROMA_DIR

RULES_FILE = Path("rules/srd.md")


def get_retriever(k: int = 4):
    """Return a retriever over the rulebook.

    On first run, builds the Chroma index from rules/srd.md (slow — it embeds
    every chunk). On later runs, loads the already-built index from disk (fast).
    """
    index_exists = Path(CHROMA_DIR).exists() and any(Path(CHROMA_DIR).iterdir())

    if index_exists:
        # Reuse the index we built last time.
        vectorstore = Chroma(
            persist_directory=CHROMA_DIR,
            embedding_function=embeddings,
        )
    else:
        # First run: split the rulebook, embed each chunk, and store them.
        text = RULES_FILE.read_text()
        splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
        chunks = splitter.create_documents([text])
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=CHROMA_DIR,
        )

    return vectorstore.as_retriever(search_kwargs={"k": k})