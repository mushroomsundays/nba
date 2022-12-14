import json
import numpy as np
import pandas as pd
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players, teams

# get_players() and get_teams() fetch a list of dictionaries

# id, full_name, first_name, last_name, is_active
all_players = players.get_players()
print(type(all_players))
for i in range(30):
    print(all_players[i])

# id, full_name, abbreviation, nickname, city, state, year_founded
all_teams = teams.get_teams()
#for i in range(32):
#    print(all_teams[i])

json_players = json.dumps(all_players, indent=2)
with open("all_players.json", "w") as f:
    f.write(json_players)

