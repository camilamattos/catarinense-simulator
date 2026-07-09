from dataclasses import dataclass


@dataclass(frozen=True)
class MatchResult:
    home_goals: int
    away_goals: int

    @property
    def home_points(self) -> int:
        if self.home_goals > self.away_goals:
            return 3

        if self.home_goals == self.away_goals:
            return 1

        return 0

    @property
    def away_points(self) -> int:
        if self.away_goals > self.home_goals:
            return 3

        if self.home_goals == self.away_goals:
            return 1

        return 0