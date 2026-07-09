from league_simulator.domain.league import League
from league_simulator.domain.monte_carlo_result import (
    MonteCarloResult,
)
from league_simulator.engines.rating_engine import (
    RatingEngine,
)


class ConsoleReporter:

    @staticmethod
    def report(
        league: League,
        result: MonteCarloResult,
        iterations: int,
        elapsed: float,
    ) -> None:

        print()

        print("CATARINENSE SÉRIE B 2026")
        print(f"{iterations:,} simulações")

        print()

        print("=" * 40)
        print("PROBABILIDADE DE TÍTULO")
        print("=" * 40)

        print()

        standings = sorted(
            league.standings,
            key=lambda standing: result.champions.get(
                standing.team.id,
                0,
            ),
            reverse=True,
        )

        for standing in standings:

            probability = result.champions.get(
                standing.team.id,
                0,
            )

            average_points = result.average_points.get(
                standing.team.id,
                0,
            )

            print(
                f"{standing.team.name:<20}"
                f"{probability:>7.2f}%"
                f"   Média {average_points:>6.2f} pts"
            )

        print()

        print("=" * 40)
        print("RATINGS")
        print("=" * 40)

        print()

        ratings = RatingEngine.calculate(
            league
        )

        ordered = sorted(
            ratings.items(),
            key=lambda item: item[1].overall,
            reverse=True,
        )

        for team, rating in ordered:

            print(
                f"{team.name:<20}"
                f"Atk {rating.attack:>6.2f}  "
                f"Def {rating.defense:>6.2f}  "
                f"Ovr {rating.overall:>6.2f}"
            )

        print()

        print(
            f"Tempo: {elapsed:.2f}s"
        )