"""Piece 5: the Game Master — supervisor that routes to the specialist agents."""
from langgraph_supervisor import create_supervisor
from langgraph.checkpoint.memory import InMemorySaver
from app.config import llm
from app.tools.dice import roll_dice
from app.agents.character_agent import character_agent
from app.agents.rules_agent import rules_agent

GM_PROMPT = (
    "You are the Game Master of a Dungeons & Dragons campaign. "
    "Never answer character, rules, or dice questions yourself. Instead:\n"
    "- delegate character work to character_manager\n"
    "- delegate rules questions to rules_expert\n"
    "- call roll_dice for any chance-based outcome\n"
    "Then weave the results into vivid narration for the player. "
    "End with a short list of 2-4 actions the player could take next."
)

# No response_format here — let the model narrate freely (reliable on local models).
game_master = create_supervisor(
    agents=[character_agent, rules_agent],
    model=llm,
    tools=[roll_dice],
    prompt=GM_PROMPT,
).compile(checkpointer=InMemorySaver())