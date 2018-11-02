import csv

CSVFILE = "soccer_players.csv"
TEAMS = ["Sharks", "Dragons", "Raptors"]
TEAMFILE = "teams.txt"
LETTER_TEMPLATE = """Dear {},

I am delighted to inform you that {} has been selected to play
for the {} team in the upcoming season.  First practice is at 19:00 on
November 5th 2018 at Old Trafford.

See you there!"""


def get_experienced_players(players):
    """Create a list of players with prior soccer experience.
    """
    return [player for player in players if player["Soccer Experience"] == "YES"]


def get_novice_players(players):
    """Create a list of players without prior soccer experience.
    """
    return [player for player in players if player["Soccer Experience"] == "NO"]


def create_teams(experienced_players, novice_players):
    """Create a list of teams evenly distributed from available players.
    """
    num_teams = len(TEAMS)
    # Divide experienced players into number of desired teams
    experienced_groups = [
        experienced_players[num_teams * i : num_teams * (i + 1)]
        for i in range(len(experienced_players) // num_teams)
    ]
    # Divide remaining players into number of desired teams
    novice_groups = [
        novice_players[num_teams * i : num_teams * (i + 1)]
        for i in range(len(novice_players) // num_teams)
    ]
    # Create list of dicts, each containing final team roster.
    return [{"team": team, "players": experienced_groups.pop() + novice_groups.pop()} for team in TEAMS]


def read_player_list():
    """Create a list of players from CSV file.
    """
    with open(CSVFILE, "r") as csv_file:
        players = csv.DictReader(csv_file)
        return [row for row in players]


def write_teams(teams):
    """Write each provided team and its players out to a text file.
    """
    # Player information we want for team roster.
    pertinent_stats = {"Name", "Soccer Experience", "Guardian Name(s)"}
    with open(TEAMFILE, "a") as team_file:
        for team in teams:
            team_file.write("{}\n".format(team["team"]))
            for player in team["players"]:
                team_file.write(
                    "{}, {}, {}\n".format(
                        *[v for k, v in player.items() if k in pertinent_stats]
                    )
                )


def create_letters(teams):
    """Create a letter for the guardian(s) of each selected player.
    """
    for team in teams:
        for player in team["players"]:
            letter_file = player["Name"].lower().replace(" ", "_") + ".txt"
            with open(letter_file, "w") as player_letter:
                player_letter.write(
                    LETTER_TEMPLATE.format(
                        player["Guardian Name(s)"], player["Name"], team["team"]
                    )
                )


def main():
    """Main program run logic.
    """
    available_players = read_player_list()
    experienced_players = get_experienced_players(available_players)
    novice_players = get_novice_players(available_players)
    teams = create_teams(experienced_players, novice_players)
    write_teams(teams)
    create_letters(teams)


if __name__ == "__main__":
    main()
