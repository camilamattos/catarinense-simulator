from dataclasses import dataclass


@dataclass(frozen=True)
class TeamRating:
    attack: float
    defense: float

    @property
    def overall(self) -> float:
        return (
            self.attack
            + self.defense
        ) / 2