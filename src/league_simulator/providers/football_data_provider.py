import requests

from league_simulator.domain.league import League
from league_simulator.domain.match import Match
from league_simulator.domain.standing import Standing
from league_simulator.domain.team import Team


class FootballDataProvider:

    BASE_URL = "https://api.football-data.org/v4"

    def __init__(
        self,
        api_key: str,
    ):
        self._headers = {
            "X-Auth-Token": api_key,
        }

    def load(self) -> League:

        standings = self._get_standings()

        matches = self._get_matches()

        table = standings["standings"][0]["table"]

        teams = {}

        for row in table:

            team = Team(
                id=str(row["team"]["id"]),
                name=row["team"]["shortName"],
            )

            teams[team.id] = team

        standings_list = []

        for row in table:

            team = teams[
                str(row["team"]["id"])
            ]

            standings_list.append(
                Standing(
                    team=team,
                    points=row["points"],
                    wins=row["won"],
                    draws=row["draw"],
                    losses=row["lost"],
                    goals_for=row["goalsFor"],
                    goals_against=row["goalsAgainst"],
                )
            )

        matches_list = []

        for row in matches["matches"]:

            home = teams[
                str(
                    row["homeTeam"]["id"]
                )
            ]

            away = teams[
                str(
                    row["awayTeam"]["id"]
                )
            ]

            score = row["score"]["fullTime"]

            matches_list.append(
                Match(
                    round=row["matchday"],
                    home=home,
                    away=away,
                    played=row["status"] == "FINISHED",
                    home_goals=score["home"],
                    away_goals=score["away"],
                )
            )

        return League(
            teams=list(
                teams.values()
            ),
            standings=standings_list,
            matches=matches_list,
        )

    def _get_standings(self):

        response = requests.get(
            f"{self.BASE_URL}/competitions/BSA/standings",
            headers=self._headers,
            timeout=30,
        )

        response.raise_for_status()

        return response.json()

    def _get_matches(self):

        response = requests.get(
            f"{self.BASE_URL}/competitions/BSA/matches",
            headers=self._headers,
            timeout=30,
        )

        response.raise_for_status()

        return response.json()