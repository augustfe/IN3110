"""Script for fetching player statistics, and plotting based on points scored."""

import os
import re
from operator import itemgetter
from typing import Dict, List
from urllib.parse import urljoin
from collections import Counter

import numpy as np
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
from requesting_urls import get_html
from time_planner import extract_events

## --- Task 8, 9 and 10 --- ##

try:
    import requests_cache
except ImportError:
    print("install requests_cache to improve performance")
    pass
else:
    requests_cache.install_cache()

base_url = "https://en.wikipedia.org"


def find_best_players(url: str) -> None:
    """Find the best players in the semifinals of the nba.

    This is the top 3 scorers from every team in semifinals.
    Displays plot over points, assists, rebounds

    arguments:
        - html (str) : html string from wiki basketball
    returns:
        - None
    """
    # gets the teams
    teams = get_teams(url)
    # Gets the player for every team and stores in dict (get_players)
    all_players = {team["name"]: get_players(team["url"]) for team in teams}

    # get player statistics for each player,
    # using get_player_stats
    for team, players in all_players.items():
        print(team)
        for i in range(len(players)):
            players[i].update(get_player_stats(players[i]["url"], team))

    # at this point, we should have a dict of the form:
    # {
    #     "team name": [
    #         {
    #             "name": "player name",
    #             "url": "https://player_url",
    #             # added by get_player_stats
    #             "points": 5,
    #             "assists": 1.2,
    #             # ...,
    #         },
    #     ]
    # }
    # Select top 3 for each team by points:
    best = {}
    for team in all_players:
        first_best = 0
        second_best = 0
        third_best = 0
        first_name = ''
        second_name = ''
        third_name = ''
        for player in all_players[team]:
            player_score = player["points"]
            if player_score > first_best:
                third_best = second_best
                third_name = second_name
                second_best = first_best
                second_name = first_name
                first_best = player_score
                first_name = player
            elif player_score > second_best:
                third_best = second_best
                third_name = second_name
                second_best = player_score
                second_name = player
            elif player_score > third_best:
                third_name = player
                third_best = player_score
        best[team] = [first_name, second_name, third_name]

    stats_to_plot = ["points", "assists", "rebounds"]
    for stat in stats_to_plot:
        plot_best(best, stat=stat)

color_table = {
    "Golden State": "#1D428A",
    "Philadelphia": "#006BB6",
    "Miami": "#98002E",
    "Memphis": "#5D76A9",
    "Milwaukee": "#00471B",
    "Phoenix": "#1D1160",
    "Dallas": "#00538C",
    "Boston": "#007A33",
}

def plot_best(best: Dict[str, List[Dict]], stat: str = "points") -> None:
    """Plot a single stat for the top 3 players from every team.

    Arguments:
        best (dict) : dict with the top 3 players from every team
            has the form:

            {
                "team name": [
                    {
                        "name": "player name",
                        "points": 5,
                        ...
                    },
                ],
            }

            where the _keys_ are the team name,
            and the _values_ are lists of length 3,
            containing dictionaries about each player,
            with their name and stats.

        stat (str) : [points | assists | rebounds] which stat to plot.
            Should be a key in the player info dictionary.
    """
    stats_dir = "NBA_player_statistics"
    count_so_far = 0
    all_names = []
    spacing = []
    max_points = 0
    # iterate through each team and the
    for team, players in best.items():
        points = []
        names = []

        color = color_table[team]
        for player in players:
            names.append(player["name"])
            points.append(player[stat])
        # record all the names, for use later in x label
        all_names.extend(names)

        # the position of bars is shifted by the number of players so far
        x = np.arange(count_so_far, count_so_far + len(players))
        count_so_far += len(players)
        # make bars for this team's players points,
        # with the team name as the label

        spacing.append(x[1] + count_so_far/2)
        bars = plt.bar(x + count_so_far/2, points, color=color, label=team)
        # add the value as text on the bars
        plt.bar_label(bars, labels=names, rotation=90, size=6, padding=3)
        max_points = np.max([np.max(points), max_points])

    # use the names, rotated 90 degrees as the labels for the bars
    plt.xticks(spacing, best, rotation=90)
    # add the legend with the colors  for each team
    plt.legend(loc=2, ncol=3, fontsize=7)
    # turn off gridlines
    plt.grid(False)
    plt.ylim(0, max_points*5/3)
    # set the title
    plt.title(f"{stat} per game")
    # save the figure to a file
    if not os.path.exists(stats_dir):
        os.makedirs(stats_dir)
    filename = f"{stats_dir}/{stat}.png"
    print(f"Creating {filename}")
    plt.tight_layout()
    plt.savefig(filename, dpi=200)
    plt.clf()


def get_teams(url: str) -> list:
    """Extract all the teams that were in the semi finals in nba.

    arguments:
        - url (str) : url of the nba finals wikipedia page
    returns:
        teams (list) : list with all teams
            Each team is a dictionary of {'name': team name, 'url': team page
    """
    # Get the table
    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find(id="Bracket").find_next("table")

    # find all rows in table
    rows = table.find_all("tr")
    rows = rows[2:]
    # maybe useful: identify cells that look like 'E1' or 'W5', etc.
    seed_pattern = re.compile(r"^[EW][1-8]$")

    # lots of ways to do this,
    # but one way is to build a set of team names in the semifinal
    # and a dict of {team name: team url}

    team_links = {}  # dict of team name: team url
    in_semifinal = set()  # set of teams in the semifinal

    # Loop over every row and extract teams from semi finals
    # also locate the links tot he team pages from the First Round column
    for row in rows:
        cols = row.find_all("td")
        # useful for showing structure

        # quarterfinal, E1/W8 is in column 1
        # team name, link is in column 2
        if len(cols) >= 3 and seed_pattern.match(cols[1].get_text(strip=True)):
            team_col = cols[2]
            a = team_col.find("a")
            team_links[team_col.get_text(strip=True)] = urljoin(base_url, a["href"])

        elif len(cols) >= 4 and seed_pattern.match(cols[2].get_text(strip=True)):
            team_col = cols[3]
            in_semifinal.add(team_col.get_text(strip=True))

        elif len(cols) >= 5 and seed_pattern.match(cols[3].get_text(strip=True)):
            team_col = cols[4]
            in_semifinal.add(team_col.get_text(strip=True))

    # return list of dicts (there will be 8):
    # [
    #     {
    #         "name": "team name",
    #         "url": "https://team url",
    #     }
    # ]

    assert len(in_semifinal) == 8
    return [
        {
            "name": team_name.rstrip("*"),
            "url": team_links[team_name],
        }
        for team_name in in_semifinal
    ]


def get_players(team_url: str) -> list:
    """Get all the players from a team that were in the roster for semi finals.

    arguments:
        team_url (str) : the url for the team
    returns:
        player_infos (list) : list of player info dictionaries
            with form: {'name': player name, 'url': player wikipedia page url}
    """
    print(f"Finding players in {team_url}")

    html = get_html(team_url)
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find(id="Roster").find_next("table", {"class": "toccolours"})

    players = []
    # Loop over every row and get the names from roster
    table = table.find_next("tbody")
    rows = table.find_all("tr")[3:]
    for row in rows:
        # Get the columns
        cols = row.find_all("td")
        col = cols[2].next

        # find name links (a tags)
        name_pat = re.compile(r"(?<=>)([^<]*)")
        name = name_pat.search(str(col))[0]
        url_pat = re.compile(r"(?<=href=\")([^\"]*)")
        url = url_pat.search(str(col))[0]
        url = base_url + url
        # and add to players a dict with
        # {'name':, 'url':}
        players += [{'name': name, 'url': url}]

    # return list of players

    return players


def get_player_stats(player_url: str, team: str) -> dict:
    """Get the player stats for a player in a given team.
    
    arguments:
        player_url (str) : url for the wiki page of player
        team (str) : the name of the team the player plays for
    returns:
        stats (dict) : dictionary with the keys (at least): points, assists, and rebounds keys
    """
    print(f"Fetching stats for player in {player_url}")

    # Get the table with stats
    html = get_html(player_url)
    soup = BeautifulSoup(html, "html.parser")

    if soup.find(id="NBA") != None:
        table = soup.find(id="NBA").find_next("table", {"class": "wikitable sortable"})
    elif soup.find(id="Regular_season") != None:
        table = soup.find(id="Regular_season").find_next("table", {"class": "wikitable sortable"})
    else:
        raise RuntimeError(f"Could not find table for {player_url}.")

    stats = {}
    keys = ["rebounds", "assists", "points"]
    abbr_keys = ["RPG", "APG", "PPG"]

    wanted = ["Year", "Team"] + abbr_keys
    df = extract_events(table, wanted)
    if "2021–22†" in df.values:
        n_df = df.loc[df["Year"] == "2021–22†"].loc[df["Team"] == team]
    else:
        n_df = df.loc[df["Year"] == "2021–22"].loc[df["Team"] == team]

    # Incase player doens't have stats
    if not n_df.empty:
        for key, abbr in zip(keys, abbr_keys):
            m = re.search(r"[\d\.]+", n_df.iloc[0][abbr])
            stats[key] = float(m.group(0))
    
    if len(stats) == 0:
        print(player_url, " not found")
        for key in keys:
            stats[key] = 0
    return stats


# run the whole thing if called as a script, for quick testing
if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/2022_NBA_playoffs"
    find_best_players(url)
