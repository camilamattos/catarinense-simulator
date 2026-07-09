from datetime import UTC, datetime

from league_simulator.domain.league import League
from league_simulator.domain.monte_carlo_result import (
    MonteCarloResult,
)


class DashboardBuilder:

    @staticmethod
    def build(
        championship: str,
        league: League,
        result: MonteCarloResult,
        iterations: int,
    ) -> dict:

        standings = sorted(
            league.standings,
            key=lambda standing: (
                standing.points,
                standing.wins,
                standing.goal_difference,
                standing.goals_for,
            ),
            reverse=True,
        )

        probability_by_team = result.champions
        average_points_by_team = result.average_points

        teams = []

        for index, standing in enumerate(
            standings
        ):

            teams.append(
                {
                    "position": index + 1,
                    "id": standing.team.id,
                    "name": (
                        "CAT"
                        if standing.team.id == "tubarao-saf"
                        else standing.team.name
                    ),
                    "points": standing.points,
                    "wins": standing.wins,
                    "draws": standing.draws,
                    "losses": standing.losses,

                    "goals_for": standing.goals_for,
                    "goals_against": standing.goals_against,
                    "goal_difference": standing.goal_difference,

                    "champion_probability": round(
                        probability_by_team.get(
                            standing.team.id,
                            0,
                        ),
                        2,
                    ),

                    "average_points": round(
                        average_points_by_team.get(
                            standing.team.id,
                            0,
                        ),
                        2,
                    ),
                }
            )

        matches = sorted(
            league.remaining_matches(),
            key=lambda match: (
                match.round,
                match.home.name,
            ),
        )

        return {
            "championship": championship,

            "updated_at": datetime.now(
                UTC,
            ).isoformat(),

            "iterations": iterations,

            "teams": teams,

            "matches": [
                {
                    "round": match.round,

                    "home": {
                        "id": match.home.id,
                        "name": (
                            "CAT"
                            if match.home.id == "tubarao-saf"
                            else match.home.name
                        ),
                    },

                    "away": {
                        "id": match.away.id,
                        "name": (
                            "CAT"
                            if match.away.id == "tubarao-saf"
                            else match.away.name
                        ),
                    },
                }
                for match in matches
            ],
        }