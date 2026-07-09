from league_simulator.domain.league import League
from league_simulator.domain.team import Team
from league_simulator.domain.team_rating import TeamRating


class IterativeRatingEngine:

    ITERATIONS = 100

    INITIAL_RATING = 1.0

    @staticmethod
    def calculate(
        league: League,
    ) -> dict[Team, TeamRating]:

        attack = {
            team.id: IterativeRatingEngine.INITIAL_RATING
            for team in league.teams
        }

        defense = {
            team.id: IterativeRatingEngine.INITIAL_RATING
            for team in league.teams
        }

        played_matches = [
            match
            for match in league.matches
            if match.played
        ]

        for _ in range(
            IterativeRatingEngine.ITERATIONS
        ):

            new_attack = {}
            new_defense = {}

            for team in league.teams:

                attack_sum = 0.0
                defense_sum = 0.0

                attack_games = 0
                defense_games = 0

                for match in played_matches:

                    if match.home.id == team.id:

                        attack_sum += (
                            match.home_goals
                            * defense[
                                match.away.id
                            ]
                        )

                        defense_sum += (
                            attack[
                                match.away.id
                            ]
                            / (
                                1
                                + match.away_goals
                            )
                        )

                        attack_games += 1
                        defense_games += 1

                    elif match.away.id == team.id:

                        attack_sum += (
                            match.away_goals
                            * defense[
                                match.home.id
                            ]
                        )

                        defense_sum += (
                            attack[
                                match.home.id
                            ]
                            / (
                                1
                                + match.home_goals
                            )
                        )

                        attack_games += 1
                        defense_games += 1

                new_attack[team.id] = (
                    attack_sum / attack_games
                    if attack_games
                    else 1.0
                )

                new_defense[team.id] = (
                    defense_sum / defense_games
                    if defense_games
                    else 1.0
                )

            attack = new_attack
            defense = new_defense

        max_attack = max(
            attack.values()
        )

        max_defense = max(
            defense.values()
        )

        ratings = {}

        for team in league.teams:

            ratings[team] = TeamRating(
                attack=round(
                    attack[team.id]
                    / max_attack
                    * 100,
                    2,
                ),
                defense=round(
                    defense[team.id]
                    / max_defense
                    * 100,
                    2,
                ),
            )

        return ratings