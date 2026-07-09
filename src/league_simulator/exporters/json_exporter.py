from json import dump
from pathlib import Path

from league_simulator.domain.league import League
from league_simulator.domain.monte_carlo_result import (
    MonteCarloResult,
)


class JsonExporter:

    @staticmethod
    def export(
        championship: str,
        league: League,
        result: MonteCarloResult,
        output: Path,
    ) -> None:

        standings = sorted(
            league.standings,
            key=lambda standing: result.champions.get(
                standing.team.id,
                0,
            ),
            reverse=True,
        )

        data = {
            "championship": championship,
            "champion_probabilities": [
                {
                    "team": standing.team.name,
                    "probability": round(
                        result.champions.get(
                            standing.team.id,
                            0,
                        ),
                        2,
                    ),
                    "average_points": round(
                        result.average_points.get(
                            standing.team.id,
                            0,
                        ),
                        2,
                    ),
                }
                for standing in standings
            ],
        }

        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with output.open(
            "w",
            encoding="utf-8",
        ) as file:

            dump(
                data,
                file,
                indent=2,
                ensure_ascii=False,
            )