import json, time, logging, boto3
import numpy as np
import pandas as pd
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players, teams
from utils import create_boto3_session, upload_to_s3

# Create and configure logger
logging.basicConfig(filename="get_data.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
# Creating an object
logger = logging.getLogger()
 
# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)


def download_from_nba_api():
    """
    Uses nba_api to get career data for players and teams
    Uploads JSON to s3://mushroomsundays/nba
    """
    ##################################
    # Players
    ##################################

    # id, full_name, first_name, last_name, is_active
    all_players = players.get_players() # list of dicts
    json_players = json.dumps(all_players, indent=2)

    with open("all_players.json", "w") as f:
        f.write(json_players)

    # Using id, get player career stats
    for d in all_players:
        id = d.get('id')
        career = playercareerstats.PlayerCareerStats(per_mode36='Totals', player_id=id)
        logging.info("Got player career stats for {id}")
        #career_df = career.get_data_frames()[0] # Error; use json instead
        career_json = career.get_json()
        career_dict = career.get_dict()['resultSets'][0]
        headers = career_dict['headers']
        data = career_dict['rowSet']
        career_df = pd.DataFrame(data, columns=headers)
        
        time.sleep(1)
        break

    ##################################
    # Teams
    ##################################

    # id, full_name, abbreviation, nickname, city, state, year_founded
    all_teams = teams.get_teams() # list of dicts
    json_teams = json.dumps(all_teams, indent=2)

    with open("all_teams.json", "w") as f:
        f.write(json_teams)

def main():
    download_from_nba_api() 

if __name__ == "__main__":
    main()

