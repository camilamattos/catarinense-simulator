from dataclasses import dataclass


@dataclass(frozen=True)
class ForcedResult:
    home: str
    away: str
    home_goals: int
    away_goals: int