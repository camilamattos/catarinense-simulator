from dataclasses import dataclass

from league_simulator.domain.match import Match
from league_simulator.domain.standing import Standing
from league_simulator.domain.team import Team


@dataclass
class League:
    teams: list[Team]
    standings: list[Standing]
    matches: list[Match]

    def remaining_matches(self) -> list[Match]:
        return [
            match
            for match in self.matches
            if not match.played
        ]