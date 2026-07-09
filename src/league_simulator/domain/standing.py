from dataclasses import dataclass

from league_simulator.domain.team import Team


@dataclass
class Standing:
    team: Team
    points: int
    wins: int
    draws: int
    losses: int
    goals_for: int
    goals_against: int

    @property
    def goal_difference(self) -> int:
        return self.goals_for - self.goals_against

    @property
    def matches_played(self) -> int:
        return (
            self.wins
            + self.draws
            + self.losses
        )

    def apply_match(
        self,
        goals_for: int,
        goals_against: int,
    ) -> None:

        self.goals_for += goals_for
        self.goals_against += goals_against

        if goals_for > goals_against:
            self.points += 3
            self.wins += 1
            return

        if goals_for == goals_against:
            self.points += 1
            self.draws += 1
            return

        self.losses += 1