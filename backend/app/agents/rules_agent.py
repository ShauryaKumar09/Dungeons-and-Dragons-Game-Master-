"""Piece 4b: the rules expert — a RAG agent grounded in the rulebook."""
from langchain_core.tools import tool
from langchain.agents import create_agent
from app.config import llm
from app.rag.index import get_retriever

_retriever = get_retriever()  # built once when this module loads


@tool
def search_rules(query: str) -> str:
    """Look up official D&D rules relevant to a player's action.

    Use this before allowing anything unusual, to check whether it's possible
    and how it works mechanically.
    """
    docs = _retriever.invoke(query)
    return "\n\n".join(d.page_content for d in docs)


rules_agent = create_agent(
    model=llm,
    tools=[search_rules],
    system_prompt=(
        "You are the D&D rules expert. Answer using ONLY the rules returned by "
        "search_rules. If an action is impossible in a medieval-fantasy world "
        "(e.g. flying a rocket to the moon), say so and explain why. "
        "Always call search_rules before answering."
    ),
    name="rules_expert",
)