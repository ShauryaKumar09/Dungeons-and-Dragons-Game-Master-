"""Piece 5 (schema): the structured shape every game turn returns."""
from pydantic import BaseModel, Field


class GameMasterTurn(BaseModel):
    narrative: str = Field(description="What the player sees and hears now.")
    suggested_actions: list[str] = Field(
        default_factory=list, description="2-4 things the player could try next."
    )
    dice: str | None = Field(
        default=None, description="Any dice rolled this turn, e.g. '1d20 -> 17'."
    )