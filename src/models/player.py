from datetime import datetime
from enum import StrEnum
from pydantic import BaseModel


class PlayerArchetype(StrEnum):
    SHARP_SHOOTER = "Sharpshooter"
    RIM_PROTECTOR = "Rim Protector"
    # TODO: think of more archetypes


class PlayerAttributes(BaseModel):
    # physical
    speed: int
    strength: int
    vertical: int
    stamina: int
    # shooting
    inside_scoring: int
    midrange_scoring: int
    free_throw: int
    three_point: int
    # skill
    ball_handling: int
    passing: int
    off_ball_movement: int
    # defense
    perimeter_defense: int
    interior_defense: int
    steal: int
    block: int
    # mental
    iq: int
    clutch: int


# TODO: determine player model
class Player(BaseModel):
    id: str
    first_name: str
    last_name: str
    age: int
    attributes: PlayerAttributes
    archetype: PlayerArchetype
    dob: datetime  # could be fun to have dobs?
    team_id: str | int  # what should team ID types be?
