from fastapi import APIRouter, Depends
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_async_session
from src.models.simulate import SimulateGameRequest, SimulateGameResponse
from src.services.sim_service import SimService
from src.services.team import TeamService


simulate_router = APIRouter(prefix="/simulate", tags=["simulate"])


@simulate_router.post("/game", response_model=SimulateGameResponse)
async def simulate_game(
    request: SimulateGameRequest,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        team_service = TeamService(session=session)
        team_profiles = await team_service.get_team_profiles(
            away_team_id=request.away_team_id,
            home_team_id=request.home_team_id,
        )

        sim_service = SimService(
            away_team_profile=team_profiles.away_team_profile,
            home_team_profile=team_profiles.home_team_profile,
            away_roster=team_profiles.away_roster,
            home_roster=team_profiles.home_roster,
        )
        if request.number_games == 1:
            result = await sim_service.sim_game()
        else:
            result = await sim_service.sim_many(request.number_games)

        return result
    except Exception as e:
        logger.error(f"An Error occurred when simulating game: {e}")
        raise
