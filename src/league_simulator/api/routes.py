import json

from fastapi import APIRouter
from pydantic import BaseModel

from league_simulator.config import DASHBOARD
from league_simulator.domain.forced_result import (
    ForcedResult,
)
from league_simulator.services.dashboard_service import (
    build_dashboard,
)
from league_simulator.services.league_cache import (
    get_league,
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

        return json.load(file)


@router.post("/simulate")
def simulate(
    request: SimulationRequest,
):

    league = get_league()

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
        league,
    )