from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel


# Does every player have an archetype? Can players have more than 1 archetype?
class PlayerArchetype(StrEnum):
    FINISHER = "finisher"
    FLOOR_GENERAL = "floor_general"
    RIM_PROTECTOR = "rim_protector"
    SHARP_SHOOTER = "sharp_shooter"
    SLASHER = "slasher"
    THREE_AND_D = "three_and_d"
    UNICORN = "unicorn"
    # TODO: think of more archetypes


class PlayerPosition(StrEnum):
    PG = "PG"
    SG = "SG"
    SF = "SF"
    PF = "PF"
    C = "C"
    W = "W"


class PlayerAttributesDto(BaseModel):
    id: UUID
    player_id: UUID
    # physical
    speed: int
    agility: int
    strength: int
    stamina: int
    # vertical: int
    # shooting
    inside_scoring: int
    midrange_scoring: int
    free_throw: int
    three_point: int
    # skill
    ball_handling: int
    passing: int
    # off_ball_movement: int
    # defense
    perimeter_defense: int
    interior_defense: int
    steal: int
    block: int
    # rebounding
    off_rebound: int
    def_rebound: int
    # mental
    iq: int
    clutch: int


# TODO: determine final player model
class PlayerDto(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    age: int
    height: float  # inches
    # dob: datetime  TODO: include date of birth? could be fun
    attributes: PlayerAttributesDto
    archetype: PlayerArchetype
    team_id: int
    positions: list[PlayerPosition]
