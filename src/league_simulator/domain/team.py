from dataclasses import dataclass

@dataclass(frozen=True)
class Team:
    id: str
    name: str