import json

from fastapi import APIRouter
from pydantic import BaseModel

from league_simulator.builders.dashboard_builder import (
    DashboardBuilder,
)
from league_simulator.config import (
    CHAMPIONSHIP,
    DASHBOARD,
    DATASET,
    ITERATIONS,
)
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


@router.get("/")
def home():

    return {
        "message": "League Simulator API",
    }


@router.get("/dashboard")
def dashboard():

    with DASHBOARD.open(
        encoding="utf-8",
    ) as file:

        return json.load(
            file
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

    result = MonteCarloEngine(
        iterations=ITERATIONS,
    ).simulate(
        league,
    )

    return DashboardBuilder.build(
        championship=CHAMPIONSHIP,
        league=league,
        result=result,
        iterations=ITERATIONS,
    )