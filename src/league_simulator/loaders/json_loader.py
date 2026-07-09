import json
from pathlib import Path

from league_simulator.domain.league import League
from league_simulator.domain.match import Match
from league_simulator.domain.standing import Standing
from league_simulator.domain.team import Team


class JsonLoader:
    @staticmethod
    def load(dataset_path: str | Path) -> League:
        dataset_path = Path(dataset_path)

        with open(
            dataset_path / "teams.json",
            encoding="utf-8",
        ) as file:
            teams_data = json.load(file)

        with open(
            dataset_path / "standings.json",
            encoding="utf-8",
        ) as file:
            standings_data = json.load(file)

        with open(
            dataset_path / "matches.json",
            encoding="utf-8",
        ) as file:
            matches_data = json.load(file)

        teams = [
            Team(
                id=team["id"],
                name=team["name"],
            )
            for team in teams_data
        ]

        teams_by_id = {
            team.id: team
            for team in teams
        }

        standings = [
            Standing(
                team=teams_by_id[item["team"]],
                points=item["points"],
                wins=item["wins"],
                draws=item["draws"],
                losses=item["losses"],
                goals_for=item["goals_for"],
                goals_against=item["goals_against"],
            )
            for item in standings_data
        ]

        matches = [
            Match(
                round=item["round"],
                home=teams_by_id[item["home"]],
                away=teams_by_id[item["away"]],
                played=item["played"],
                home_goals=item["home_goals"],
                away_goals=item["away_goals"],
            )
            for item in matches_data
        ]

        return League(
            teams=teams,
            standings=standings,
            matches=matches,
        )