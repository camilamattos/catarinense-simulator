from league_simulator.domain.team import Team
from league_simulator.domain.standing import Standing


class FootballDataParser:

    @staticmethod
    def slugify(name: str) -> str:
        return (
            name.lower()
            .replace(" ", "-")
            .replace("/", "-")
            .replace(".", "")
            .replace("'", "")
        )

    @classmethod
    def parse_teams(
        cls,
        standings_json: dict,
    ) -> list[Team]:

        table = standings_json["standings"][0]["table"]

        teams = []

        for row in table:

            teams.append(
                Team(
                    id=cls.slugify(
                        row["team"]["name"]
                    ),
                    name=row["team"]["name"],
                )
            )

        return teams

    @classmethod
    def parse_standings(
        cls,
        standings_json: dict,
    ) -> list[Standing]:

        table = standings_json["standings"][0]["table"]

        teams = {
            cls.slugify(
                row["team"]["name"]
            ): Team(
                id=cls.slugify(
                    row["team"]["name"]
                ),
                name=row["team"]["name"],
            )
            for row in table
        }

        standings = []

        for row in table:

            team_id = cls.slugify(
                row["team"]["name"]
            )

            standings.append(
                Standing(
                    team=teams[team_id],
                    points=row["points"],
                    wins=row["won"],
                    draws=row["draw"],
                    losses=row["lost"],
                    goals_for=row["goalsFor"],
                    goals_against=row["goalsAgainst"],
                )
            )

        return standings