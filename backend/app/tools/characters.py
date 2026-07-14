"""Piece 3 (tools): create and fetch D&D characters, saved to disk as JSON."""
import json
import random
from langchain_core.tools import tool
from app.config import CHARACTER_DIR


def _roll_stat() -> int:
    """Roll 4d6 and drop the lowest die — standard D&D ability score."""
    dice = sorted(random.randint(1, 6) for _ in range(4))
    return sum(dice[1:])  # sum the top 3, dropping dice[0] (the lowest)


@tool
def create_character(name: str, race: str, char_class: str) -> dict:
    """Create a new D&D character with rolled ability scores and save it.

    Args:
        name: The character's name.
        race: e.g. "Human", "Elf", "Dwarf".
        char_class: e.g. "Fighter", "Wizard", "Rogue".
    """
    stats = {s: _roll_stat() for s in ["STR", "DEX", "CON", "INT", "WIS", "CHA"]}
    sheet = {
        "name": name,
        "race": race,
        "class": char_class,
        "stats": stats,
        "hp": 10 + (stats["CON"] - 10) // 2,
    }
    (CHARACTER_DIR / f"{name.lower()}.json").write_text(json.dumps(sheet, indent=2))
    return sheet


@tool
def get_character(name: str) -> dict:
    """Retrieve a saved character by name."""
    path = CHARACTER_DIR / f"{name.lower()}.json"
    if not path.exists():
        return {"error": f"No character named {name}."}
    return json.loads(path.read_text())