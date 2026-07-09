from league_simulator.domain.league import League
from league_simulator.domain.simulation import Simulation
from league_simulator.engines.expected_goals_engine import (
    ExpectedGoalsEngine,
)
from league_simulator.engines.score_engine import ScoreEngine


class SimulationEngine:

    def __init__(
        self,
        league: League,
    ):
        self._xg_engine = ExpectedGoalsEngine(
            league
        )

        self._score_engine = ScoreEngine()

    def simulate(
        self,
        league: League,
    ) -> Simulation:

        simulation = Simulation(
            league
        )

        for match in simulation.remaining_matches:

            expected_goals = (
                self._xg_engine.calculate(
                    match
                )
            )

            result = (
                self._score_engine.simulate(
                    expected_goals
                )
            )

            simulation.apply(
                match,
                result,
            )

        return simulation