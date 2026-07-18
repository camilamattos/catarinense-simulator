import json
import logging
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

logger = logging.getLogger(__name__)

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

    user_agent = request.headers.get(
        "user-agent",
        "unknown",
    )

    logger.info("=" * 80)
    logger.info("POST /simulate")
    logger.info("IP: %s", client_ip)
    logger.info("User-Agent: %s", user_agent)
    logger.info("Resultados enviados: %s", len(body.results))

    for result in body.results:
        logger.info(
            "%s %s x %s %s",
            result.home,
            result.home_goals,
            result.away_goals,
            result.away,
        )

    logger.info(
        "Payload:\n%s",
        json.dumps(
            body.model_dump(),
            indent=2,
            ensure_ascii=False,
        ),
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

    logger.info(
        "Simulation finished in %.2fs",
        elapsed,
    )
    logger.info("=" * 80)

    return DashboardBuilder.build(
        championship=CHAMPIONSHIP,
        league=league,
        result=result,
        iterations=ITERATIONS,
    )