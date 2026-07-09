import math

from league_simulator.domain.league import League
from league_simulator.domain.match import Match
from league_simulator.domain.match_probability import MatchProbability
from league_simulator.domain.team import Team
from league_simulator.engines.rating_engine import RatingEngine


class ProbabilityEngine:
    def __init__(self, league: League):
        self._ratings = RatingEngine.calculate(league)

    def calculate(
        self,
        match: Match,
    ) -> MatchProbability:

        home = self._rating(match.home)
        away = self._rating(match.away)

        difference = (
            home.overall
            - away.overall
        )

        strength = 1 / (
            1 + math.exp(
                -difference / 15
            )
        )

        draw = max(
            0.15,
            0.30 - abs(difference) / 200,
        )

        remaining = 1 - draw

        home_win = remaining * strength
        away_win = remaining * (
            1 - strength
        )

        return MatchProbability(
            home_win=round(home_win, 4),
            draw=round(draw, 4),
            away_win=round(away_win, 4),
        )

    def _rating(
        self,
        team: Team,
    ):
        return self._ratings[team]