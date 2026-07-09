from dataclasses import dataclass

from league_simulator.domain.team import Team


@dataclass
class Match:
    round: int
    home: Team
    away: Team
    played: bool
    home_goals: int | None
    away_goals: int | None