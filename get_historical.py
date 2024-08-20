from espn_api.football import League
import creds as c
import sys
import requests
import logging
import time
import concurrent.futures
import os
import json

def save_to_json(data, year, position):
    if not os.path.exists('historical_data'):
        os.makedirs('historical_data')
    filename = f"historical_data/{position}_{year}.json"
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    logger.info(f"Saved {position} data to {filename}")

def save_historical_data_by_position(players, year):
    positions = ['QB', 'RB', 'WR', 'TE', 'K']
    for position in positions:
        players_by_position = [p for p in players if position in p['Slots']]
        save_to_json(players_by_position, year, position)

def fetch_player_info(league, player_name, retries=3, delay=2):
    for i in range(retries):
        try:
            player_info = league.player_info(player_name)
            if player_info is not None:
                return {
                    'Name': player_name,
                    'Slots': player_info.eligibleSlots,
                    'Avail': player_info.active_status,
                    'onTeam': player_info.onTeamId,
                    'avg_pts': player_info.avg_points,
                    'total_pts': player_info.total_points
                }
        except requests.exceptions.RequestException as e:
            logger.warning(f"Request failed for {player_name}: {e}")
            time.sleep(delay * (2 ** i))  # Exponential backoff
    return None

def collect_draftable_players(league, max_workers=5):
    player_names = [x['fullName'] for x in league.espn_request.get_pro_players()]
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(lambda name: fetch_player_info(league, name), player_names))
    draftable_players = [player for player in results if player is not None]
    return draftable_players

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # Initialize your league
    league_id = c.league_id
    espn_s2 = c.espn_s2
    swid = c.swid
    league = League(league_id=league_id, year=int(sys.argv[1]), espn_s2=espn_s2, swid=swid)
    year = int(sys.argv[1])
    # End init
    # Get historical info:
    if sys.argv[1] != 2024:
        available_players = collect_draftable_players(league, max_workers=5)
        save_historical_data_by_position(available_players, year)