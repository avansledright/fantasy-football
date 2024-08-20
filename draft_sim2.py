import json
import os
from collections import defaultdict
import creds as c
from espn_api.football import League
import sys
import time

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

def find_best_players(historical_data_dir, projected_data_dir):
    combined_players = []
    
    for position_file in os.listdir(projected_data_dir):
        position = position_file.split('.')[0]  # Removing .json to get position name
        projected_data = load_data(os.path.join(projected_data_dir, position_file))
        
        historical_data_paths = [os.path.join(historical_data_dir, file) for file in os.listdir(historical_data_dir) if file.startswith(position)]
        
        for projected_player in projected_data:
            player_name = projected_player['Name']
            historical_avg = combine_historical_data(historical_data_paths, player_name)
            combined_avg = (historical_avg + projected_player['proj_avg']) / 2
            
            combined_players.append({
                'Name': player_name,
                'Position': position,
                'historical_avg': historical_avg,
                'projected_avg': projected_player['proj_avg'],
                'combined_avg': combined_avg
            })
    
    # Sort all players by combined average in descending order
    combined_players.sort(key=lambda x: x['combined_avg'], reverse=True)
    
    return combined_players

def get_team_name(league, team_id):
    if team_id == 0:
        return "Free Agent"
    
    for team in league.teams:
        if team.team_id == team_id:
            return team.team_name
    return "Unknown Team"

def is_player_available(league, player_name, player_info_cache):
    if player_name in player_info_cache:
        player_info = player_info_cache[player_name]
    else:
        player_info = league.player_info(player_name)
        player_info_cache[player_name] = player_info
    
    return player_info is not None and not player_info.onTeamId  # Available if not assigned to any team

def snake_draft(combined_players, team_count, required_players, league):
    teams = defaultdict(lambda: defaultdict(list))
    team_roster_needs = {team: required_players.copy() for team in range(team_count)}
    
    total_picks = sum(required_players.values()) * team_count

    draft_log = []
    player_info_cache = {}

    for i in range(total_picks):
        # Determine which team is picking (snake draft logic)
        round_num = i // team_count
        if round_num % 2 == 0:  # Forward round
            team_pick = i % team_count
        else:  # Reverse round
            team_pick = team_count - 1 - (i % team_count)
        
        # Select the best available player that fits the team's roster needs
        for player in combined_players:
            position = player['Position']
            if team_roster_needs[team_pick][position] > 0 and is_player_available(league, player['Name'], player_info_cache):
                # Assign player to team
                teams[team_pick][position].append(player)
                # Decrease the need for that position
                team_roster_needs[team_pick][position] -= 1
                # Remove the player from the available pool
                combined_players.remove(player)
                # Log the draft pick
                draft_log.append(f"Round {round_num + 1}, Pick {i + 1}: Team {team_pick + 1} selected {player['Name']} ({position}) - Combined Avg: {player['combined_avg']:.2f}")
                break
    
    return teams, draft_log

# Display and save the draft results
def display_and_save_draft_results(teams, draft_log, output_file='draft_results.txt'):
    with open(output_file, 'w') as f:
        for team, positions in teams.items():
            team_output = f"Team {team + 1}:\n"
            f.write(team_output)
            print(team_output, end='')
            for position, players in positions.items():
                position_output = f"  {position}:\n"
                f.write(position_output)
                print(position_output, end='')
                for player in players:
                    player_output = (
                        f"    {player['Name']} - Historical Avg: {player['historical_avg']}, "
                        f"Projected Avg: {player['projected_avg']}, Combined Avg: {player['combined_avg']:.2f}\n"
                    )
                    f.write(player_output)
                    print(player_output, end='')
            f.write('\n')
            print()

        # Save and print the draft log
        f.write("\nDraft Log:\n")
        print("\nDraft Log:")
        for log in draft_log:
            f.write(log + '\n')
            print(log)


if __name__ == "__main__":
    start_time = time.time()  # Start the timer

    # Number of players required per position
    league_id = c.league_id
    espn_s2 = c.espn_s2
    swid = c.swid
    league = League(league_id=league_id, year=int(sys.argv[1]), espn_s2=espn_s2, swid=swid)
    year = int(sys.argv[1])
    required_players = {
        "K": 1,
        "QB": 3,
        "WR": 5,
        "RB": 5,
        "TE": 2
    }

    # Load and combine data
    combined_players = find_best_players('historical_data', 'projected_data')

    # Simulate the snake draft with 8 teams
    teams, draft_log = snake_draft(combined_players, team_count=8, required_players=required_players, league=league)

    # Display and save the results
    display_and_save_draft_results(teams, draft_log)

    end_time = time.time()  # End the timer
    elapsed_time = end_time - start_time  # Calculate the elapsed time

    print(f"Script execution time: {elapsed_time:.2f} seconds")