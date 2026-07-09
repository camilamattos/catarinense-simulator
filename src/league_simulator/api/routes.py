from datetime import datetime
from pathlib import Path

from fastapi import APIRouter
from pydantic import BaseModel

from league_simulator.domain.forced_result import (
    ForcedResult,
)
from league_simulator.engines.monte_carlo_engine import (
    MonteCarloEngine,
)
from league_simulator.loaders.json_loader import (
    JsonLoader,
)
from league_simulator.services.scenario_service import (
    ScenarioService,
)

router = APIRouter()

DATASET = Path(
    "datasets/catarinense_serie_b_2026"
)


class MatchResultRequest(BaseModel):
    home: str
    away: str
    home_goals: int
    away_goals: int


class SimulationRequest(BaseModel):
    results: list[MatchResultRequest]


def load_league():
    return JsonLoader.load(
        DATASET
    )


def build_dashboard(
    league,
):

    iterations = 10_000

    result = MonteCarloEngine(
        iterations=iterations,
    ).simulate(
        league,
    )

    standings = sorted(
        league.standings,
        key=lambda standing: (
            standing.points,
            standing.goal_difference,
            standing.goals_for,
        ),
        reverse=True,
    )

    probability_by_team = result.champions
    average_points_by_team = result.average_points

    teams = []

    for index, standing in enumerate(
        standings
    ):

        teams.append(
            {
                "position": index + 1,
                "id": standing.team.id,
                "name": standing.team.name,

                "points": standing.points,
                "wins": standing.wins,
                "draws": standing.draws,
                "losses": standing.losses,

                "goals_for": standing.goals_for,
                "goals_against": standing.goals_against,
                "goal_difference": standing.goal_difference,

                "champion_probability": round(
                    probability_by_team.get(
                        standing.team.id,
                        0,
                    ),
                    2,
                ),

                "average_points": round(
                    average_points_by_team.get(
                        standing.team.id,
                        0,
                    ),
                    2,
                ),
            }
        )

    matches = sorted(
        league.remaining_matches(),
        key=lambda match: (
            match.round,
            match.home.name,
        ),
    )

    return {
        "championship": "Catarinense Série B 2026",
        "updated_at": datetime.now().isoformat(),
        "iterations": iterations,

        "teams": teams,

        "matches": [
            {
                "round": match.round,

                "home": {
                    "id": match.home.id,
                    "name": match.home.name,
                },

                "away": {
                    "id": match.away.id,
                    "name": match.away.name,
                },
            }
            for match in matches
        ],
    }


@router.get("/")
def home():

    return {
        "message": "League Simulator API",
    }


@router.get("/dashboard")
def dashboard():

    league = load_league()

    return build_dashboard(
        league
    )


@router.post("/simulate")
def simulate(
    request: SimulationRequest,
):

    league = load_league()

    ScenarioService.apply(
        league,
        [
            ForcedResult(
                home=result.home,
                away=result.away,
                home_goals=result.home_goals,
                away_goals=result.away_goals,
            )
            for result in request.results
        ],
    )

    return build_dashboard(
        league
    )