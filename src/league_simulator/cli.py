from pathlib import Path
from time import perf_counter

from league_simulator.domain.forced_result import (
    ForcedResult,
)
from league_simulator.engines.monte_carlo_engine import (
    MonteCarloEngine,
)
from league_simulator.exporters.json_exporter import (
    JsonExporter,
)
from league_simulator.loaders.json_loader import (
    JsonLoader,
)
from league_simulator.reporters.console_reporter import (
    ConsoleReporter,
)
from league_simulator.services.scenario_service import (
    ScenarioService,
)


def main() -> None:

    league = JsonLoader.load(
        Path(
            "datasets/catarinense_serie_b_2026"
        )
    )

    iterations = 10_000

    engine = MonteCarloEngine(
        iterations=iterations,
    )

    start = perf_counter()

    result = engine.simulate(
        league,
    )

    elapsed = perf_counter() - start

    JsonExporter.export(
        championship="Catarinense Série B 2026",
        league=league,
        result=result,
        output=Path(
            "outputs/catarinense_serie_b_2026.json"
        ),
    )

    ConsoleReporter.report(
        league=league,
        result=result,
        iterations=iterations,
        elapsed=elapsed,
    )


if __name__ == "__main__":
    main()