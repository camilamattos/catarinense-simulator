import math

from league_simulator.config import RATING_EXPONENT
from league_simulator.domain.expected_goals import ExpectedGoals
from league_simulator.domain.league import League
from league_simulator.domain.match import Match
from league_simulator.domain.team import Team
from league_simulator.engines.rating_engine import RatingEngine


class ExpectedGoalsEngine:

    def __init__(
        self,
        league: League,
    ):
        self._ratings = RatingEngine.calculate(
            league
        )

        played_matches = [
            match
            for match in league.matches
            if match.played
        ]

        total_home_goals = sum(
            match.home_goals
            for match in played_matches
            if match.home_goals is not None
        )

        total_away_goals = sum(
            match.away_goals
            for match in played_matches
            if match.away_goals is not None
        )

        matches = len(played_matches)

        self._home_average_goals = (
            total_home_goals / matches
        )

        self._away_average_goals = (
            total_away_goals / matches
        )

    def calculate(
        self,
        match: Match,
    ) -> ExpectedGoals:

        home = self._rating(match.home)
        away = self._rating(match.away)

        home_attack = math.pow(
            home.attack / 100,
            RATING_EXPONENT,
        )

        away_attack = math.pow(
            away.attack / 100,
            RATING_EXPONENT,
        )

        home_defense = math.pow(
            home.defense / 100,
            RATING_EXPONENT,
        )

        away_defense = math.pow(
            away.defense / 100,
            RATING_EXPONENT,
        )

        home_xg = (
            self._home_average_goals
            * home_attack
            * (2 - away_defense)
        )

        away_xg = (
            self._away_average_goals
            * away_attack
            * (2 - home_defense)
        )

        return ExpectedGoals(
            home=round(home_xg, 2),
            away=round(away_xg, 2),
        )

    def _rating(
        self,
        team: Team,
    ):
        return self._ratings[team]