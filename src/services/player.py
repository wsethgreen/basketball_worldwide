from sqlalchemy.ext.asyncio import AsyncSession

from src.generators.player import PlayerGenerator
from src.models.game import PlayerGameStats
from src.models.player import PlayerAttributesDto, PlayerDto, PlayerGameStatsCreate
from src.repositories.player import PlayerRepo
from src.repositories.player_attributes import PlayerAttributesRepo
from src.repositories.player_game_stats import PlayerGameStatsRepo


class PlayerService:
    def __init__(self, session: AsyncSession):
        self.player_generator = PlayerGenerator()
        self.player_attributes_repo = PlayerAttributesRepo(session=session)
        self.game_stats_repo = PlayerGameStatsRepo(session=session)
        self.player_repo = PlayerRepo(session=session)

    async def get_players_for_team(self, team_id: int) -> list[PlayerDto]:
        players = await self.player_repo.get_players_for_team(team_id=team_id)
        return [
            PlayerDto.model_validate(player, from_attributes=True) for player in players
        ]

    async def create_generated_player(self, team_id: int) -> PlayerDto:
        generated = self.player_generator.generate(team_id=team_id)

        await self.player_repo.create(generated)

        attributes_data: PlayerAttributesDto = generated.attributes
        attributes_data.id = generated.attributes.player_id
        await self.player_attributes_repo.create(attributes_data)

        return generated

    async def batch_insert_game_stats(self, game_stats: list[PlayerGameStats]) -> None:
        dto_list = [
            PlayerGameStatsCreate(
                player_id=stats.player_id,
                minutes=0,
                points=stats.points,
                fg_attempted=stats.fg_attempted,
                fg_made=stats.fg_made,
                three_point_attempted=stats.three_point_attempted,
                three_point_made=stats.three_point_made,
                ft_attempted=stats.ft_attempted,
                ft_made=stats.ft_made,
                off_rebounds=stats.off_rebounds,
                def_rebounds=stats.def_rebounds,
                rebounds=stats.off_rebounds + stats.def_rebounds,
                assists=stats.assists,
                turnovers=stats.turnovers,
                steals=0,
                blocks=0,
                personal_fouls=0,
                technical_fouls=0,
                plus_minus=0,
            )
            for stats in game_stats
        ]
        await self.game_stats_repo.create_many(dto_list)

    async def delete_players_for_team(self, team_id: int) -> int:
        result = await self.player_repo.delete_players_from_team(team_id=team_id)
        return result
