from typing import Sequence

from src.models.player import PlayerDto
from src.models.team import TeamProfile


class TeamGenerator:
    @staticmethod
    def build_team_profile_from_roster(
        team_name: str, roster: Sequence[PlayerDto]
    ) -> TeamProfile:
        if not roster:
            raise ValueError(f"{team_name} roster is empty")

        def avg_attr(attr: str) -> float:
            return sum(getattr(p.attributes, attr) for p in roster) / len(roster)

        def norm(value: float, low: float = 0.0, high: float = 100.0) -> float:
            if high <= low:
                return 0.0
            return max(0.0, min(1.0, (value - low) / (high - low)))

        speed = avg_attr("speed")
        agility = avg_attr("agility")
        stamina = avg_attr("stamina")
        ball_handling = avg_attr("ball_handling")
        passing = avg_attr("passing")
        iq = avg_attr("iq")
        three_point = avg_attr("three_point")
        inside_scoring = avg_attr("inside_scoring")
        midrange_scoring = avg_attr("midrange_scoring")
        free_throw = avg_attr("free_throw")

        pace = 94 + norm((speed * 0.5) + (agility * 0.3) + (stamina * 0.2)) * 14
        turnover_rate = (
            0.20 - norm((ball_handling * 0.6) + (passing * 0.3) + (iq * 0.1)) * 0.08
        )
        three_rate = 0.25 + norm(three_point) * 0.20
        two_pct = 0.44 + norm((inside_scoring * 0.6) + (midrange_scoring * 0.4)) * 0.14
        three_pct = 0.30 + norm(three_point) * 0.12
        ft_rate = (
            0.12
            + norm((inside_scoring * 0.4) + (ball_handling * 0.3) + (iq * 0.3)) * 0.14
        )
        ft_pct = 0.62 + norm(free_throw) * 0.20

        return TeamProfile(
            name=team_name,
            pace=pace,
            turnover_rate=max(0.05, min(0.30, turnover_rate)),
            three_rate=max(0.10, min(0.60, three_rate)),
            two_pct=max(0.35, min(0.70, two_pct)),
            three_pct=max(0.25, min(0.50, three_pct)),
            ft_rate=max(0.05, min(0.40, ft_rate)),
            ft_pct=max(0.50, min(0.90, ft_pct)),
        )
