import re

from bs4 import BeautifulSoup


class FCFParser:
    def slugify(self, name: str) -> str:
        return (
            name.lower()
            .replace(" ", "-")
            .replace("ã", "a")
            .replace("á", "a")
            .replace("â", "a")
            .replace("à", "a")
            .replace("é", "e")
            .replace("ê", "e")
            .replace("í", "i")
            .replace("ó", "o")
            .replace("ô", "o")
            .replace("õ", "o")
            .replace("ú", "u")
            .replace("ç", "c")
        )

    def parse_teams(self, html: str) -> list[dict]:
        soup = BeautifulSoup(html, "lxml")

        table = soup.find_all("table")[3]

        teams = []

        for row in table.find_all("tr"):
            columns = row.find_all("td")

            if not columns:
                continue

            columns = [
                column.get_text(strip=True)
                for column in columns
            ]

            name = columns[1]

            teams.append(
                {
                    "id": self.slugify(name),
                    "name": name.title(),
                }
            )

        return teams

    def parse_standings(self, html: str) -> list[dict]:
        soup = BeautifulSoup(html, "lxml")

        table = soup.find_all("table")[3]

        standings = []

        for row in table.find_all("tr"):
            columns = row.find_all("td")

            if not columns:
                continue

            columns = [
                column.get_text(strip=True)
                for column in columns
            ]

            standings.append(
                {
                    "team": self.slugify(columns[1]),
                    "points": int(columns[2]),
                    "wins": int(columns[4]),
                    "draws": int(columns[5]),
                    "losses": int(columns[6]),
                    "goals_for": int(columns[7]),
                    "goals_against": int(columns[8]),
                }
            )

        return standings

    def parse_matches(self, html: str) -> list[dict]:
        soup = BeautifulSoup(html, "lxml")

        tables = soup.find_all("table")

        matches = []

        current_round = None

        for index, table in enumerate(tables):
            text = table.get_text(" ", strip=True)

            if "RODADA" in text.upper():
                match = re.search(r"(\d+)", text)

                if match:
                    current_round = int(match.group(1))

                continue

            if not text.startswith("Jogo:"):
                continue

            score_table = tables[index + 1]
            teams_table = tables[index + 2]

            score_text = score_table.get_text(" ", strip=True)

            score_match = re.match(
                r"(\d+)\s*x\s*(\d+)",
                score_text,
            )

            if score_match:
                home_goals = int(score_match.group(1))
                away_goals = int(score_match.group(2))
                played = True
            else:
                home_goals = None
                away_goals = None
                played = False

            team_cells = teams_table.find_all("td")

            home = team_cells[1].get_text(strip=True)
            away = team_cells[3].get_text(strip=True)

            matches.append(
                {
                    "round": current_round,
                    "home": self.slugify(home),
                    "away": self.slugify(away),
                    "played": played,
                    "home_goals": home_goals,
                    "away_goals": away_goals,
                }
            )

        return matches