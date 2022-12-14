import json
import numpy as np
import pandas as pd
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players, teams

# get_players() and get_teams() fetch a list of dictionaries

# id, full_name, first_name, last_name, is_active
all_players = players.get_players()
# id, full_name, abbreviation, nickname, city, state, year_founded
all_teams = teams.get_teams()


json_players = json.dumps(all_players, indent=2)
json_teams = json.dumps(all_teams, indent=2)
with open("all_players.json", "w") as f:
    f.write(json_players)
with open("all_teams.json", "w") as f:
    f.write(json_teams)


