from copy import deepcopy
import random

from league_simulator.domain.league import League
from league_simulator.domain.match import Match
from league_simulator.domain.match_result import MatchResult
from league_simulator.domain.standing import Standing


class Simulation:

    def __init__(
        self,
        league: League,
    ):
        self._standings: list[Standing] = deepcopy(
            league.standings
        )

        self._standings_by_team = {
            standing.team.id: standing
            for standing in self._standings
        }

        self._remaining_matches = (
            league.remaining_matches()
        )

    @property
    def standings(
        self,
    ) -> list[Standing]:
        return self._standings

    @property
    def remaining_matches(
        self,
    ) -> list[Match]:
        return self._remaining_matches

    def apply(
        self,
        match: Match,
        result: MatchResult,
    ) -> None:

        home = self._standing(
            match.home.id
        )

        away = self._standing(
            match.away.id
        )

        home.apply_match(
            result.home_goals,
            result.away_goals,
        )

        away.apply_match(
            result.away_goals,
            result.home_goals,
        )

    def table(
        self,
    ) -> list[Standing]:

        standings = self._standings.copy()

        random.shuffle(
            standings
        )

        return sorted(
            standings,
            key=lambda standing: standing.points,
            reverse=True,
        )

    def _standing(
        self,
        team_id: str,
    ) -> Standing:

        return self._standings_by_team[
            team_id
        ]