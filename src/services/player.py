from sqlalchemy.ext.asyncio import AsyncSession

from src.generators.player import PlayerGenerator
from src.models.player import PlayerAttributesDto, PlayerDto
from src.repositories.player import PlayerRepo
from src.repositories.player_attributes import PlayerAttributesRepo


class PlayerService:
    def __init__(self, session: AsyncSession):
        self.player_generator = PlayerGenerator()
        self.player_attributes_repo = PlayerAttributesRepo(session=session)
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

    async def delete_players_for_team(self, team_id: int) -> int:
        result = await self.player_repo.delete_players_from_team(team_id=team_id)
        return result
