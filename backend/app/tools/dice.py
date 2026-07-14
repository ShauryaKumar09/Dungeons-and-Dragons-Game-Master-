"""Piece 2: the dice-rolling tool. Real randomness lives here, not in the LLM."""
import random
import re
from langchain_core.tools import tool


@tool
def roll_dice(notation: str) -> dict:
    """Roll tabletop dice and return the result.

    Use this whenever an action's outcome depends on chance: attacks,
    saving throws, ability checks.

    Args:
        notation: Dice string like "3d20", "1d6+2", or "d20".
    """
    m = re.fullmatch(r"(\d*)d(\d+)([+-]\d+)?", notation.replace(" ", "").lower())
    if not m:
        raise ValueError(f"Bad dice notation: {notation}")
    count = int(m.group(1) or 1)
    sides = int(m.group(2))
    mod = int(m.group(3)) if m.group(3) else 0
    rolls = [random.randint(1, sides) for _ in range(count)]
    return {"rolls": rolls, "modifier": mod, "total": sum(rolls) + mod}