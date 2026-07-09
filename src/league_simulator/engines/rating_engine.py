from league_simulator.domain.league import League
from league_simulator.domain.team import Team
from league_simulator.domain.team_rating import TeamRating


class RatingEngine:

    ITERATIONS = 5

    @staticmethod
    def calculate(
        league: League,
    ) -> dict[Team, TeamRating]:

        standings_by_team = {
            standing.team.id: standing
            for standing in league.standings
        }

        attack = {
            team.id: 1.0
            for team in league.teams
        }

        defense = {
            team.id: 1.0
            for team in league.teams
        }

        played_matches = [
            match
            for match in league.matches
            if match.played
        ]

        total_home_goals = sum(
            match.home_goals
            for match in played_matches
        )

        total_away_goals = sum(
            match.away_goals
            for match in played_matches
        )

        league_home_average = (
            total_home_goals
            / len(played_matches)
        )

        league_away_average = (
            total_away_goals
            / len(played_matches)
        )

        for _ in range(RatingEngine.ITERATIONS):

            new_attack: dict[str, float] = {}
            new_defense: dict[str, float] = {}

            for team in league.teams:

                attack_values = []
                defense_values = []

                for match in played_matches:

                    if match.home.id == team.id:

                        attack_values.append(
                            (
                                match.home_goals
                                * defense[match.away.id]
                            )
                        )

                        defense_values.append(
                            (
                                match.away_goals
                                * attack[match.away.id]
                            )
                        )

                    elif match.away.id == team.id:

                        attack_values.append(
                            (
                                match.away_goals
                                * defense[match.home.id]
                            )
                        )

                        defense_values.append(
                            (
                                match.home_goals
                                * attack[match.home.id]
                            )
                        )

                if attack_values:
                    new_attack[team.id] = (
                        sum(attack_values)
                        / len(attack_values)
                    )
                else:
                    new_attack[team.id] = 1.0

                if defense_values:
                    average = (
                        sum(defense_values)
                        / len(defense_values)
                    )

                    new_defense[team.id] = (
                        1 / (1 + average)
                    )
                else:
                    new_defense[team.id] = 1.0

            attack = new_attack
            defense = new_defense

        max_attack = max(attack.values())
        max_defense = max(defense.values())

        ratings: dict[Team, TeamRating] = {}

        max_goal_difference = max(
            standing.goal_difference
            for standing in league.standings
        )

        for standing in league.standings:

            win_rate = (
                standing.points
                / (standing.matches_played * 3)
            ) * 100

            goal_difference = (
                standing.goal_difference
                / max_goal_difference
            ) * 100

            attack_score = (
                attack[standing.team.id]
                / max_attack
            ) * 100

            defense_score = (
                defense[standing.team.id]
                / max_defense
            ) * 100

            ratings[standing.team] = TeamRating(
                attack=round(
                    attack_score,
                    2,
                ),
                defense=round(
                    defense_score,
                    2,
                ),
            )

        return ratings