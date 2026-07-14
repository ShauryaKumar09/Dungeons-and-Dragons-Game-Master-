"""Piece 6: the game loop layer — run one turn, return structured output."""
from langchain_core.messages import HumanMessage
from app.agents.game_master import game_master
from app.config import llm
from app.schemas import GameMasterTurn

# A second model, told to ONLY reformat text into our schema. One job, done well.
_formatter = llm.with_structured_output(GameMasterTurn)


def run_turn(player_input: str, session_id: str = "default") -> GameMasterTurn:
    """Play one turn: send player input to the GM, return a structured result."""
    cfg = {"configurable": {"thread_id": session_id}, "recursion_limit": 12}

    # 1. Let the game master narrate freely (reliable on a local model).
    try:
        result = game_master.invoke(
            {"messages": [HumanMessage(content=player_input)]}, cfg
        )
        narration = result["messages"][-1].content
    except Exception:
        # Local models sometimes loop or emit a malformed tool call. Don't crash.
        narration = (
            "The Game Master pauses, momentarily distracted. "
            "(Try rephrasing your action.)"
        )

    # 2. Convert that narration into our structured shape in a separate step.
    try:
        return _formatter.invoke(
            "Convert this Game Master narration into the required format. "
            "Put the story in 'narrative', list next options in 'suggested_actions', "
            "and any dice rolls in 'dice'.\n\n" + narration
        )
    except Exception:
        # If the local model botches the JSON, fall back to raw narration.
        return GameMasterTurn(narrative=narration)