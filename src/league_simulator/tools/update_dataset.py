import json
from pathlib import Path

from league_simulator.parsers.fcf_parser import FCFParser
from league_simulator.providers.fcf_provider import FCFProvider


def save_json(path: Path, data: list[dict]) -> None:
    with open(
        path,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False,
        )


def main() -> None:
    parser = FCFParser()

    standings_html = FCFProvider.get_standings_html()
    matches_html = FCFProvider.get_matches_html()

    teams = parser.parse_teams(standings_html)
    standings = parser.parse_standings(standings_html)
    matches = parser.parse_matches(matches_html)

    dataset_path = (
        Path("datasets")
        / "catarinense_serie_b_2026"
    )

    dataset_path.mkdir(
        parents=True,
        exist_ok=True,
    )

    save_json(dataset_path / "teams.json", teams)
    save_json(dataset_path / "standings.json", standings)
    save_json(dataset_path / "matches.json", matches)

    print(f"✅ Generated {len(teams)} teams")
    print(f"✅ Generated {len(standings)} standings")
    print(f"✅ Generated {len(matches)} matches")


if __name__ == "__main__":
    main()