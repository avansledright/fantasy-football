# Fantasy Football Draft Simulation and Player Analysis

## Overview
This repository provides scripts to simulate a fantasy football draft, identify the best players available by position, and manage player data based on historical and projected performance.

This code utilizes a Python library that was created by [cwendt94](https://github.com/cwendt94/espn-api).


## Files
1. **`best_player_pos.py`**: Identifies the best available player for a specified position based on historical and projected data.
2. **`draft_sim2.py`**: Simulates a snake draft for an 8-team fantasy football league, ensuring only available players are drafted.
3. **`get_historical.py`**: Retrieves and processes historical player data for previous seasons.
4. **`get_projected.py`**: Retrieves and processes projected player data for the upcoming season.

## Setup
1. **Install Required Libraries**:
   - Install `espn-api` via pip:
     ```bash
     pip install espn-api
     ```
   - Ensure you have Python 3.6+ installed.

2. **Credentials Setup**:
   - Create a `creds.py` file in the root directory with the following structure:
     ```python
     league_id = 'YOUR_LEAGUE_ID'
     espn_s2 = 'YOUR_ESPN_S2_COOKIE'
     swid = 'YOUR_SWID'
     ```
To get these values check out the guide [here](https://github.com/cwendt94/espn-api/discussions/150)

3. **Data Preparation**:
   - Store historical and projected data in `historical_data/` and `projected_data/` directories, respectively.
   - Data files should be in JSON format, named by position and year, e.g., `QB_2023.json`.

## Usage
### Retrieving and Processing Data
- Use get_historical.py and get_projected.py to fetch and process player data before running simulations.
``` bash
python get_historical.py <year>
python get_projected.py
```
### Running the Draft Simulation
- Run the draft simulation script with the league year as an argument:
  ```bash
  python draft_sim2.py 2024
  ```
Results are saved to draft_results.txt, including detailed logs of the draft process and selected players.
This setup enables you to simulate drafts, analyze player performance, and manage your fantasy football team effectively.

### Finding the Best Player by Position
- Run the best_player_pos.py script and specify the position when prompted:
  ``` bash
  python best_player_pos.py
  ```



