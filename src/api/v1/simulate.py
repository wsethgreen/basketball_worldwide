from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_async_session
from src.models.simulate import SimulateGameRequest
from src.services.sim_service import SimService


simulate_router = APIRouter(prefix="/simulate", tags=["simulate"])


@simulate_router.post("/game")
async def simulate_game(
    request: SimulateGameRequest,
    session: AsyncSession = Depends(get_async_session),
):
    sim_service = SimService(session=session)
    result = await sim_service.sim_game(request.away_team_id, request.home_team_id)

    return result
