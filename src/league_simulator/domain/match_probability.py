from dataclasses import dataclass


@dataclass(frozen=True)
class MatchProbability:
    home_win: float
    draw: float
    away_win: float