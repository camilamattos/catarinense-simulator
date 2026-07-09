from league_simulator.providers.football_data_provider import (
    FootballDataProvider,
)

API_KEY = "4ef75fb8a8cc456c8c733b94328bc048"


def main() -> None:

    provider = FootballDataProvider(
        API_KEY
    )

    league = provider.load()

    print()

    print(
        f"Teams: {len(league.teams)}"
    )

    print(
        f"Standings: {len(league.standings)}"
    )

    print(
        f"Matches: {len(league.matches)}"
    )

    print(
        f"Remaining: {len(league.remaining_matches())}"
    )


if __name__ == "__main__":
    main()