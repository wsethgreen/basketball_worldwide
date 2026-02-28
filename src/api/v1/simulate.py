from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_async_session
from src.models.simulate import (
    SimulateGameRequest,
    SimulateGameResponse,
    SimulateScheduleRequest,
    SimulateScheduleResponse,
    SimulateScheduleDeleteResponse,
)
from src.services.league import LeagueService
from src.services.player import PlayerService
from src.services.sim_service import SimService
from src.services.team import TeamService


simulate_router = APIRouter(prefix="/simulate", tags=["simulate"])


@simulate_router.post("/game", response_model=SimulateGameResponse)
async def simulate_game(
    request: SimulateGameRequest,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        player_service = PlayerService(session=session)
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

        result = await sim_service.sim_game()

        await player_service.batch_insert_game_stats(result.away_player_stats)
        await player_service.batch_insert_game_stats(result.home_player_stats)

        return result

    except Exception as e:
        logger.error(f"An Error occurred when simulating game: {e}")
        raise


@simulate_router.post("/schedule/{league_id}", response_model=SimulateScheduleResponse)
async def simulate_schedule(
    league_id: int,
    request: SimulateScheduleRequest,
    session: AsyncSession = Depends(get_async_session),
):
    league_service = LeagueService(session=session)
    try:
        games_created = await league_service.generate_schedule_for_league(
            league_id=league_id,
            season_year=request.season_year,
            batch_size=100,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc

    return SimulateScheduleResponse(
        season_year=request.season_year, games_created=games_created
    )


@simulate_router.delete(
    "/schedule/{league_id}/{season_year}",
    response_model=SimulateScheduleDeleteResponse,
)
async def delete_schedule(
    league_id: int,
    season_year: int,
    session: AsyncSession = Depends(get_async_session),
):
    league_service = LeagueService(session=session)
    games_deleted = await league_service.delete_schedule_for_league(
        league_id=league_id, season_year=season_year
    )
    return SimulateScheduleDeleteResponse(
        season_year=season_year, games_deleted=games_deleted
    )
