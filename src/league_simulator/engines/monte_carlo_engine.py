from collections import defaultdict
import random

from league_simulator.domain.league import League
from league_simulator.domain.monte_carlo_result import (
    MonteCarloResult,
)
from league_simulator.engines.simulation_engine import (
    SimulationEngine,
)


class MonteCarloEngine:

    DEFAULT_ITERATIONS = 10_000

    def __init__(
        self,
        iterations: int = DEFAULT_ITERATIONS,
    ):
        self._iterations = iterations

    def simulate(
        self,
        league: League,
    ) -> MonteCarloResult:

        random.seed(42)

        simulation_engine = SimulationEngine()

        champions = defaultdict(int)
        total_points = defaultdict(float)

        for _ in range(self._iterations):

            simulation = simulation_engine.simulate(
                league
            )

            table = simulation.table()

            champion = table[0]

            champions[
                champion.team.id
            ] += 1

            for standing in table:
                total_points[
                    standing.team.id
                ] += standing.points

        return MonteCarloResult(
            champions={
                team_id: (
                    count
                    / self._iterations
                    * 100
                )
                for team_id, count in champions.items()
            },
            average_points={
                team_id: (
                    points
                    / self._iterations
                )
                for team_id, points in total_points.items()
            },
        )