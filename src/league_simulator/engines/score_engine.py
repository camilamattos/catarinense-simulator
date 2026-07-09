import math
import random

from league_simulator.domain.expected_goals import ExpectedGoals
from league_simulator.domain.match_result import MatchResult


class ScoreEngine:

    MAX_GOALS = 10

    def simulate(
        self,
        expected_goals: ExpectedGoals,
    ) -> MatchResult:

        return MatchResult(
            home_goals=self._poisson(
                expected_goals.home
            ),
            away_goals=self._poisson(
                expected_goals.away
            ),
        )

    def _poisson(
        self,
        mean: float,
    ) -> int:

        l = math.exp(-mean)  # noqa: E741

        k = 0

        p = 1.0

        while (
            p > l
            and k < self.MAX_GOALS
        ):
            k += 1
            p *= random.random()

        return k - 1