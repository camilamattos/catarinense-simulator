import json
from time import perf_counter

from fastapi import APIRouter, Request
from pydantic import BaseModel

from league_simulator.builders.dashboard_builder import (
    DashboardBuilder,
)
from league_simulator.config import (
    CHAMPIONSHIP,
    DASHBOARD,
    ITERATIONS,
)
from league_simulator.domain.forced_result import (
    ForcedResult,
)
from league_simulator.engines.monte_carlo_engine import (
    MonteCarloEngine,
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

        return json.load(
            file
        )


@router.post("/simulate")
def simulate(
    request: Request,
    body: SimulationRequest,
):

    start = perf_counter()

    client_ip = request.headers.get(
        "x-forwarded-for",
        request.client.host if request.client else "unknown",
    )

    scenarios = " | ".join(
        (
            f"{result.home} "
            f"{result.home_goals}x{result.away_goals} "
            f"{result.away}"
        )
        for result in body.results
    )

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
            for result in body.results
        ],
    )

    result = MonteCarloEngine(
        iterations=ITERATIONS,
    ).simulate(
        league,
    )

    elapsed = perf_counter() - start

    print(
        f"POST /simulate | "
        f"IP={client_ip} | "
        f"{len(body.results)} resultados | "
        f"{scenarios} | "
        f"{elapsed:.2f}s"
    )

    return DashboardBuilder.build(
        championship=CHAMPIONSHIP,
        league=league,
        result=result,
        iterations=ITERATIONS,
    )