from json import dump
from pathlib import Path

from league_simulator.builders.dashboard_builder import (
    DashboardBuilder,
)
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

        data = DashboardBuilder.build(
            championship=championship,
            league=league,
            result=result,
            iterations=10_000,
        )

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