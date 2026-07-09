from time import perf_counter

from league_simulator.config import (
    CHAMPIONSHIP,
    DASHBOARD,
    DATASET,
    ITERATIONS,
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


def main() -> None:

    league = JsonLoader.load(
        DATASET
    )

    engine = MonteCarloEngine(
        iterations=ITERATIONS,
    )

    start = perf_counter()

    result = engine.simulate(
        league,
    )

    elapsed = perf_counter() - start

    JsonExporter.export(
        championship=CHAMPIONSHIP,
        league=league,
        result=result,
        output=DASHBOARD,
    )

    ConsoleReporter.report(
        league=league,
        result=result,
        iterations=ITERATIONS,
        elapsed=elapsed,
    )


if __name__ == "__main__":
    main()