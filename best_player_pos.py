import json
import os
import creds as c
from espn_api.football import League

def load_data(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)

def combine_historical_data(historical_data_paths, player_name):
    historical_avg_points = []
    
    for path in historical_data_paths:
        data = load_data(path)
        for player in data:
            if player['Name'] == player_name:
                historical_avg_points.append(player['avg_pts'])
    
    if historical_avg_points:
        return sum(historical_avg_points) / len(historical_avg_points)
    return 0

def is_player_available(league, player_name):
    player_info = league.player_info(player_name)
    return player_info is not None and not player_info.onTeamId  # Available if not assigned to any team

def find_best_player(historical_data_dir, projected_data_dir, position, league):
    historical_data_paths = [os.path.join(historical_data_dir, file) for file in os.listdir(historical_data_dir) if file.startswith(position)]
    projected_data_path = os.path.join(projected_data_dir, f"{position}.json")
    
    projected_data = load_data(projected_data_path)
    best_player = None
    highest_combined_avg = 0
    
    for projected_player in projected_data:
        player_name = projected_player['Name']
        historical_avg = combine_historical_data(historical_data_paths, player_name)
        combined_avg = (historical_avg + projected_player['proj_avg']) / 2
        
        if combined_avg > highest_combined_avg and is_player_available(league, player_name):
            best_player = {
                'Name': player_name,
                'Position': position,
                'historical_avg': historical_avg,
                'projected_avg': projected_player['proj_avg'],
                'combined_avg': combined_avg
            }
            highest_combined_avg = combined_avg
    
    return best_player

def display_best_player(player):
    if player:
        print(f"Best available player for {player['Position']} position:")
        print(f"Name: {player['Name']}")
        print(f"Historical Avg: {player['historical_avg']}")
        print(f"Projected Avg: {player['projected_avg']}")
        print(f"Combined Avg: {player['combined_avg']:.2f}")
    else:
        print("No available player found for the given position.")

if __name__ == "__main__":
    # Initialize the ESPN League API
    league_id = c.league_id
    espn_s2 = c.espn_s2
    swid = c.swid
    league = League(league_id=league_id, year=2024, espn_s2=espn_s2, swid=swid)
    
    historical_data_dir = 'historical_data'
    projected_data_dir = 'projected_data'
    position = input("Enter the position (e.g., QB, RB, WR, TE, K): ").upper()

    best_player = find_best_player(historical_data_dir, projected_data_dir, position, league)
    display_best_player(best_player)
