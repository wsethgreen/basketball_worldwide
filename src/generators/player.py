import random
from loguru import logger
from uuid import UUID, uuid4

from faker import Faker

from src.models.player import (
    PlayerArchetype,
    PlayerAttributesDto,
    PlayerDto,
    PlayerPosition,
)


class PlayerGenerator:
    def __init__(self) -> None:
        self._faker = Faker()

    def generate(
        self, team_id: int, position: PlayerPosition | None = None
    ) -> PlayerDto:
        if not position:
            logger.info("position not provided. randomly selecting position.")
            position = random.choice(list(PlayerPosition))

        positions = self._pick_positions(position)
        player_id = uuid4()

        attributes = self._generate_attributes(player_id, position)
        height = self._generate_height(position)

        return PlayerDto(
            id=player_id,
            first_name=self._faker.first_name_male(),
            last_name=self._faker.last_name(),
            age=random.randint(18, 38),
            height=height,
            attributes=attributes,
            archetype=random.choice(list(PlayerArchetype)),
            team_id=team_id or random.randint(1, 30),
            positions=positions,
        )

    @staticmethod
    def _pick_positions(primary: PlayerPosition) -> list[PlayerPosition]:
        positions = [primary]
        if random.random() < 0.25:
            secondary = random.choice([p for p in PlayerPosition if p != primary])
            positions.append(secondary)
        return positions

    def _generate_attribute(self, key: str, position: PlayerPosition) -> int:
        ranges = self._position_ranges(position)
        low, high = ranges[key]
        return random.randint(low, high)

    def _generate_attributes(
        self, player_id: UUID, position: PlayerPosition
    ) -> PlayerAttributesDto:
        return PlayerAttributesDto(
            id=player_id,
            player_id=player_id,
            speed=self._generate_attribute("speed", position),
            agility=self._generate_attribute("agility", position),
            strength=self._generate_attribute("strength", position),
            stamina=self._generate_attribute("stamina", position),
            inside_scoring=self._generate_attribute("inside_scoring", position),
            midrange_scoring=self._generate_attribute("midrange_scoring", position),
            free_throw=self._generate_attribute("free_throw", position),
            three_point=self._generate_attribute("three_point", position),
            ball_handling=self._generate_attribute("ball_handling", position),
            passing=self._generate_attribute("passing", position),
            perimeter_defense=self._generate_attribute("perimeter_defense", position),
            interior_defense=self._generate_attribute("interior_defense", position),
            steal=self._generate_attribute("steal", position),
            block=self._generate_attribute("block", position),
            off_rebound=self._generate_attribute("off_rebound", position),
            def_rebound=self._generate_attribute("def_rebound", position),
            iq=self._generate_attribute("iq", position),
            clutch=self._generate_attribute("clutch", position),
        )

    @staticmethod
    def _generate_height(position: PlayerPosition) -> float:
        low, high = PlayerGenerator._height_ranges(position)
        step = 0.25
        steps = int(round((high - low) / step))
        return round(low + step * random.randint(0, steps), 2)

    @staticmethod
    def _height_ranges(position: PlayerPosition) -> tuple[float, float]:
        if position == PlayerPosition.PG:
            return 70.0, 77.5  # 5'10" - 6'5.5"
        if position == PlayerPosition.SG:
            return 73.0, 80.5  # 6'1" - 6'8.5"
        if position == PlayerPosition.SF:
            return 76.0, 82.0  # 6'4" - 6'10"
        if position == PlayerPosition.PF:
            return 78.0, 83.0  # 6'6" - 6'11"
        if position == PlayerPosition.C:
            return 81.0, 87.0  # 6'9" - 7'3"
        # Wing/utility
        return 75.0, 82.0  # 6'3" - 6'10"

    @staticmethod
    def _position_ranges(position: PlayerPosition) -> dict[str, tuple[int, int]]:
        # Default baseline for all positions
        attributes = {
            "speed": (55, 85),
            "agility": (55, 85),
            "strength": (45, 80),
            "stamina": (60, 90),
            "inside_scoring": (50, 80),
            "midrange_scoring": (50, 85),
            "free_throw": (55, 90),
            "three_point": (45, 85),
            "ball_handling": (50, 85),
            "passing": (50, 85),
            "perimeter_defense": (50, 85),
            "interior_defense": (45, 80),
            "steal": (45, 80),
            "block": (35, 70),
            "off_rebound": (40, 75),
            "def_rebound": (40, 75),
            "iq": (55, 90),
            "clutch": (45, 85),
        }

        if position == PlayerPosition.PG:
            attributes.update(
                {
                    "ball_handling": (75, 98),
                    "passing": (75, 98),
                    "three_point": (65, 95),
                    "speed": (70, 95),
                    "agility": (70, 95),
                    "interior_defense": (40, 70),
                    "block": (30, 60),
                    "off_rebound": (35, 65),
                    "def_rebound": (35, 65),
                }
            )
        elif position == PlayerPosition.SG:
            attributes.update(
                {
                    "three_point": (70, 95),
                    "midrange_scoring": (70, 95),
                    "ball_handling": (65, 90),
                    "passing": (60, 85),
                    "speed": (65, 90),
                }
            )
        elif position == PlayerPosition.SF:
            attributes.update(
                {
                    "inside_scoring": (65, 90),
                    "midrange_scoring": (60, 88),
                    "three_point": (55, 85),
                    "perimeter_defense": (60, 88),
                    "def_rebound": (55, 85),
                }
            )
        elif position == PlayerPosition.PF:
            attributes.update(
                {
                    "strength": (65, 95),
                    "inside_scoring": (70, 95),
                    "interior_defense": (65, 92),
                    "off_rebound": (60, 90),
                    "def_rebound": (60, 90),
                    "block": (55, 88),
                }
            )
        elif position == PlayerPosition.C:
            attributes.update(
                {
                    "strength": (75, 99),
                    "inside_scoring": (75, 99),
                    "interior_defense": (70, 98),
                    "off_rebound": (70, 98),
                    "def_rebound": (70, 98),
                    "block": (65, 95),
                    "three_point": (35, 65),
                    "ball_handling": (35, 65),
                }
            )
        elif position == PlayerPosition.W:
            # Versatile wing
            attributes.update(
                {
                    "speed": (65, 92),
                    "agility": (65, 92),
                    "three_point": (60, 90),
                    "perimeter_defense": (60, 90),
                    "inside_scoring": (60, 88),
                    "ball_handling": (55, 85),
                }
            )

        return attributes
