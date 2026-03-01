from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_async_session
from src.models.simulate import (
    SimulateGameRequest,
    SimulateGameResponse,
    SimulateDayRequest,
    SimulateDayResponse,
    SimulateScheduleRequest,
    SimulateScheduleResponse,
    SimulateScheduleDeleteResponse,
)
from src.models.scheduled_game import ScheduledGameStatus, ScheduledGameUpdate
from src.models.team import TeamGameStatsDto
from src.repositories.scheduled_game import ScheduledGameRepo
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


@simulate_router.post("/day", response_model=SimulateDayResponse)
async def simulate_day(
    request: SimulateDayRequest,
    session: AsyncSession = Depends(get_async_session),
):
    scheduled_game_repo = ScheduledGameRepo(session=session)
    team_service = TeamService(session=session)
    player_service = PlayerService(session=session)

    games = await scheduled_game_repo.get_for_date(request.game_date)
    games_simulated = 0

    for game in games:
        team_profiles = await team_service.get_team_profiles(
            away_team_id=game.away_team_id,
            home_team_id=game.home_team_id,
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

        await team_service.create_game_stats(
            TeamGameStatsDto(
                team_id=game.away_team_id,
                game_id=game.id,
                season_year=game.season_year,
                points=result.away_score,
                fg_attempted=sum(p.fg_attempted for p in result.away_player_stats),
                fg_made=sum(p.fg_made for p in result.away_player_stats),
                three_point_attempted=sum(
                    p.three_point_attempted for p in result.away_player_stats
                ),
                three_point_made=sum(
                    p.three_point_made for p in result.away_player_stats
                ),
                ft_attempted=sum(p.ft_attempted for p in result.away_player_stats),
                ft_made=sum(p.ft_made for p in result.away_player_stats),
                off_rebounds=sum(p.off_rebounds for p in result.away_player_stats),
                def_rebounds=sum(p.def_rebounds for p in result.away_player_stats),
                rebounds=sum(
                    p.off_rebounds + p.def_rebounds for p in result.away_player_stats
                ),
                assists=sum(p.assists for p in result.away_player_stats),
                turnovers=sum(p.turnovers for p in result.away_player_stats),
            )
        )

        await team_service.create_game_stats(
            TeamGameStatsDto(
                team_id=game.home_team_id,
                game_id=game.id,
                season_year=game.season_year,
                points=result.home_score,
                fg_attempted=sum(p.fg_attempted for p in result.home_player_stats),
                fg_made=sum(p.fg_made for p in result.home_player_stats),
                three_point_attempted=sum(
                    p.three_point_attempted for p in result.home_player_stats
                ),
                three_point_made=sum(
                    p.three_point_made for p in result.home_player_stats
                ),
                ft_attempted=sum(p.ft_attempted for p in result.home_player_stats),
                ft_made=sum(p.ft_made for p in result.home_player_stats),
                off_rebounds=sum(p.off_rebounds for p in result.home_player_stats),
                def_rebounds=sum(p.def_rebounds for p in result.home_player_stats),
                rebounds=sum(
                    p.off_rebounds + p.def_rebounds for p in result.home_player_stats
                ),
                assists=sum(p.assists for p in result.home_player_stats),
                turnovers=sum(p.turnovers for p in result.home_player_stats),
            )
        )

        await team_service.record_result(
            team_id=game.away_team_id,
            won=result.winner == team_profiles.away_team_profile.name,
            year=game.season_year,
        )
        await team_service.record_result(
            team_id=game.home_team_id,
            won=result.winner == team_profiles.home_team_profile.name,
            year=game.season_year,
        )

        await scheduled_game_repo.update(
            game_id=game.id,
            update=ScheduledGameUpdate(status=ScheduledGameStatus.PLAYED),
        )
        games_simulated += 1
        logger.info(f"Simulated game number: {games_simulated}")

    return SimulateDayResponse(
        game_date=request.game_date, games_simulated=games_simulated
    )
