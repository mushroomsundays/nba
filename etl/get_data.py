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


def upload_all_players_career_stats_to_s3(s3, players: list, bucket: str) -> None:
    """
    Uses nba_api to get career data for players and teams
    Uploads JSON to s3://mushroomsundays/nba
    """
    
    # Using id, get player career stats
    for d in players:
        id = d.get('id')
        career = playercareerstats.PlayerCareerStats(per_mode36='Totals', player_id=id)
        logging.info("Loaded player career stats for {id}.")
        #career_df = career.get_data_frames()[0] # Error; use json instead
        career_json = career.get_json()

        key = f"nba/players/{id}.json"
        upload_to_s3(s3, obj=career_json, bucket=bucket, key=key)
        logging.info(f"Successful S3 upload: S3://{bucket}/{key}.")
        
        time.sleep(1)
        break

def main():
    # Create boto3 session for uploading files to S3
    s3 = create_boto3_session()
    logging.info("Boto3 session created.")

    # Bucket for S3 uploads
    bucket = "mushroomsundays"

    # Get player IDs and other info for all players; upload to S3
    # id, full_name, first_name, last_name, is_active
    all_players = players.get_players() # list of dicts
    all_players_json = json.dumps(all_players, indent=2)
    key = "nba/player_lookup.json"
    upload_to_s3(s3, obj=all_players_json, bucket=bucket, key=key)
    logging.info(f"Successful S3 upload: S3://{bucket}/{key}.")

    # Get team IDs and other info for all teams; upload to S3
    # id, full_name, abbreviation, nickname, city, state, year_founded
    all_teams = teams.get_teams() # list of dicts
    all_teams_json = json.dumps(all_teams, indent=2)
    key = "nba/team_lookup.json"
    upload_to_s3(s3, obj=all_teams_json, bucket=bucket, key=key)
    logging.info(f"Successful S3 upload: S3://{bucket}/{key}.")

    # Get all players career stats; upload to S3
    upload_all_players_career_stats_to_s3(s3, players=all_players, bucket=bucket) 

if __name__ == "__main__":
    main()

