from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_async_session
from src.generators.team import TeamGenerator
from src.simulators.game import GameSimulator
from src.models.simulate import SimulateGameRequest
from src.repositories.team import TeamRepo
from src.services.player import PlayerService


simulate_router = APIRouter(prefix="/simulate", tags=["simulate"])


@simulate_router.post("/game")
async def simulate_game(
    request: SimulateGameRequest,
    session: AsyncSession = Depends(get_async_session),
):
    player_service = PlayerService(session=session)
    team_repo = TeamRepo(session=session)
    team_generator = TeamGenerator()
    teams = await team_repo.get_teams_by_ids(
        [request.away_team_id, request.home_team_id]
    )
    teams_by_id = {team.id: team for team in teams}
    away_team = teams_by_id.get(request.away_team_id)
    home_team = teams_by_id.get(request.home_team_id)
    if away_team is None or home_team is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Team not found"
        )

    away_roster = await player_service.get_players_for_team(team_id=away_team.id)
    home_roster = await player_service.get_players_for_team(team_id=home_team.id)
    if not away_roster or not home_roster:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Both teams must have a roster to simulate a game.",
        )

    away_team_profile = team_generator.build_team_profile_from_roster(
        team_name=f"{away_team.city} {away_team.nickname}",
        roster=away_roster,
    )
    home_team_profile = team_generator.build_team_profile_from_roster(
        team_name=f"{home_team.city} {home_team.nickname}",
        roster=home_roster,
    )

    simulator = GameSimulator(away_team_profile, home_team_profile)
    result = simulator.simulate_game()

    return {
        "away_team": away_team_profile.name,
        "home_team": home_team_profile.name,
        "away_score": result.away_score,
        "home_score": result.home_score,
        "winner": result.winner,
        "possessions": result.possessions,
    }
