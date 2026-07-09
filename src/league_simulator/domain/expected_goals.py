from dataclasses import dataclass


@dataclass(frozen=True)
class ExpectedGoals:
    home: float
    away: float