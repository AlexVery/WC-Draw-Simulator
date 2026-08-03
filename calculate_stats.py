from country_mappings import *

def calculate_means(team_name, key, response, teams_dict):
    # some teams may not have played a game during the requested
    # time period, so to avoid dividing with zero, we simply return
    if len(response) == 0: return
    
    teams_dict[team_name][key]["GD"] = teams_dict[team_name][key]["GF"] - teams_dict[team_name][key]["GA"]
    
    means_to_caclulate = ["GF", "GA", "GD"]
    
    for mean in means_to_caclulate:
        teams_dict[team_name][key][mean] /= len(response)

# extract_data takes the data, applies the fun_to_apply function to it
# and in case an error is raised, the default value def_value is returned 
def extract_data(data, fun_to_apply, def_value):
    try:
        return fun_to_apply(data)
    except:
        return def_value

# team_name is the name of the team, key. is_home is a boolean value 
# that indicated whether team named team_name plays at home or away.
def add_stats_to_dict(team_name, key, is_home, fixture, teams_dict):
    
    home_team_goals = extract_data(fixture["goals"]["home"], int, 0)
    away_team_goals = extract_data(fixture["goals"]["away"], int, 0)
    
    home_team_won = extract_data(fixture["teams"]["home"]["winner"], bool, False)
    away_team_won = extract_data(fixture["teams"]["away"]["winner"], bool, False)
    
    teams_dict[team_name][key]["GP"] += 1
    
    teams_dict[team_name][key]["GF"] += home_team_goals
    teams_dict[team_name][key]["GA"] += away_team_goals
    
    if (not home_team_won) and (not away_team_won):
        teams_dict[team_name][key]["D"] += 1
    elif (home_team_won and is_home) or (away_team_won and (not is_home)):
        teams_dict[team_name][key]["W"] += 1
    else:
        teams_dict[team_name][key]["L"] += 1

# repsonse is a dict containing fixtures for each national team returned from api football:
# {'fixture': {'id': 1168769, 'referee': 'M. Oliver', 'timezone': 'UTC', 'date': '2024-03-22T20:30:00+00:00', 
# 'timestamp': 1711139400, 'periods': {'first': 1711139400, 'second': 1711143000}, 'venue': {'id': 598, 'name': 
# 'London Stadium', 'city': 'London'}, 'status': {'long': 'Match Finished', 'short': 'FT', 'elapsed': 90, 
# 'extra': None}}, 'league': {'id': 10, 'name': 'Friendlies', 'country': 'World', 
# 'logo': 'https://media.api-sports.io/football/leagues/10.png', 'flag': None, 'season': 2024, 
# 'round': 'Friendlies 1', 'standings': False}, 'teams': {'home': {'id': 9, 'name': 'Spain', 
# 'logo': 'https://media.api-sports.io/football/teams/9.png', 'winner': False}, 'away': {'id': 8, 
# 'name': 'Colombia', 'logo': 'https://media.api-sports.io/football/teams/8.png', 'winner': True}}, 
# 'goals': {'home': 0, 'away': 1}, 'score': {'halftime': {'home': 0, 'away': 0}, 'fulltime': {'home': 0, 
# 'away': 1}, 'extratime': {'home': None, 'away': None}, 'penalty': {'home': None, 'away': None}}}

# country is the FIFA name of the country

def structure_stats(response, country, teams_dict):
    
    # ELO_TO_NAME is a dict created to solve any naming issues among
    # the different platforms (FIFA, api football etc)
    country = ELO_TO_NAME.get(country, country)
    
    # stats_dict is used to store the averages to reflect the
    # current form of the team, 'GP' = games played, 'W' = wins, 
    # 'D' = draws, 'L' = loses, 'GF' = goals for, 'GA' = goals against, 
    # 'GD' = goal difference 
    stats_dict = {
        "GP" : 0,
        "W" : 0,
        "D" : 0,
        "L" : 0,
        "GF" : 0,
        "GA" : 0,
        "GD" : 0
    }
    
    # team_stats_dict is the key : value
    # pair to be inserted to the team's dict (its structure can be seen in structure_stats
    # function
    teams_dict[country].setdefault("stats", stats_dict.copy())
    stats_key = "stats"
    
    for fixture in response:
        
        teams = fixture['teams']
        home_team_stats, away_team_stats = teams["home"], teams["away"]
        
        home_team_name, away_team_name = home_team_stats["name"], away_team_stats["name"]
        home_team_name = ELO_TO_NAME.get(home_team_name, home_team_name)
        away_team_name = ELO_TO_NAME.get(away_team_name, away_team_name)
        
        is_home = home_team_name == country
        team_name = home_team_name if is_home else away_team_name
        
        add_stats_to_dict(team_name, stats_key, is_home, fixture, teams_dict)
        
    calculate_means(country, stats_key, response, teams_dict)
        
def create_form_stats(teams_dict):
    for team in teams_dict:
        structure_stats(teams_dict[team]["form"], team, teams_dict)