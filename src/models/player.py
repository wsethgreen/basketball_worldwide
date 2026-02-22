from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, computed_field


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


class PlayerGameStatsCreate(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    player_id: UUID
    minutes: int = 0
    points: int = 0
    fg_attempted: int = 0
    fg_made: int = 0
    three_point_attempted: int = 0
    three_point_made: int = 0
    ft_attempted: int = 0
    ft_made: int = 0
    off_rebounds: int = 0
    def_rebounds: int = 0
    assists: int = 0
    turnovers: int = 0
    steals: int = 0
    blocks: int = 0
    personal_fouls: int = 0
    technical_fouls: int = 0
    plus_minus: int = 0

    @computed_field
    @property
    def fg_percent(self) -> float:
        return self.fg_made / self.fg_attempted if self.fg_attempted else 0.0

    @computed_field
    @property
    def three_point_percent(self) -> float:
        return (
            self.three_point_made / self.three_point_attempted
            if self.three_point_attempted
            else 0.0
        )

    @computed_field
    @property
    def ft_percent(self) -> float:
        return self.ft_made / self.ft_attempted if self.ft_attempted else 0.0

    @computed_field
    @property
    def rebounds(self) -> float:
        return self.off_rebounds + self.def_rebounds
