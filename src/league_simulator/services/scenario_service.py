from league_simulator.domain.forced_result import (
    ForcedResult,
)
from league_simulator.domain.league import League


class ScenarioService:

    @staticmethod
    def apply(
        league: League,
        forced_results: list[ForcedResult],
    ) -> None:

        standings = {
            standing.team.id: standing
            for standing in league.standings
        }

        for forced in forced_results:

            match = next(
                (
                    match
                    for match in league.matches
                    if (
                        not match.played
                        and match.home.name == forced.home
                        and match.away.name == forced.away
                    )
                ),
                None,
            )

            if match is None:
                continue

            match.played = True
            match.home_goals = forced.home_goals
            match.away_goals = forced.away_goals

            standings[match.home.id].apply_match(
                forced.home_goals,
                forced.away_goals,
            )

            standings[match.away.id].apply_match(
                forced.away_goals,
                forced.home_goals,
            )