"""Piece 3 (agent): wraps the character tools in an agent that calls them itself."""
from langchain.agents import create_agent
from app.config import llm
from app.tools.characters import create_character, get_character

character_agent = create_agent(
    model=llm,
    tools=[create_character, get_character],
    system_prompt=(
        "You manage D&D characters. Use your tools to create or fetch "
        "characters. Never invent stats yourself — always call the tool."
    ),
    name="character_manager",
)