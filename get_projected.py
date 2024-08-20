from espn_api.football import League
import creds as c
import sys
import os
import json

def save_projected_data(position, players):
    if not os.path.exists('projected_data'):
        os.makedirs('projected_data')
    filename = f"projected_data/{position}.json"
    with open(filename, 'w') as f:
        json.dump(players, f, indent=4)
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    # Initialize your league
    league_id = c.league_id
    espn_s2 = c.espn_s2
    swid = c.swid
    league = League(league_id=league_id, year=int(sys.argv[1]), espn_s2=espn_s2, swid=swid)
    
    # Ensure we are working with the year 2024
    if int(sys.argv[1]) != 2024:
        sys.exit(1)
    
    # Get projected info for all positions
    for position in c.positions:
        all_players = league.free_agents(size=1000, position=position)
        
        available_players = []
        for player in all_players:
            print(player)
            obj = {
                "Name": player.name,
                "proj_avg": player.projected_avg_points,
                "proj_total": player.projected_total_points
            }
            available_players.append(obj)
        
        # Save all players' projected data for the position
        save_projected_data(position, available_players)

    print("All projected data has been saved.")
