from dataclasses import dataclass


@dataclass(frozen=True)
class MonteCarloResult:
    champions: dict[str, float]
    average_points: dict[str, float]