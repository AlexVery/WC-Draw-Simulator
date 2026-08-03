from country_mappings import *
from api_football import *
from calculate_stats import *
from normalise_data import *
from connect_dict import *
from pathlib import Path
import requests
import pickle

def fetch_data(url, headers):
    response = requests.get(url, headers=headers)
    return response

# creates a database from 'data' (the return value of the request
# from the fifa's api found at the specified url)
def parse_fifa_rankings(data):
    
    teams = {}
    
    for team in data["Results"]:
        name = team["TeamName"][0]["Description"]

        teams[name] = {
            "rank": team["Rank"],
            "points": team["TotalPoints"],
            "previous_rank": team["PrevRank"],
            "previous_points": team["PrevPoints"],
            "country_code": team["IdCountry"],
            "confederation": team["ConfederationName"]
        }
        
    return teams

def download_flags(teams_database, headers):
    
    folder = Path("flags")
    if folder.exists: return
    folder.mkdir()
    
    for team, data in teams_database.items():
        
        code = data["country_code"]
        
        url = f"https://api.fifa.com/api/v3/picture/flags-sq-2/{code}"
        
        img = fetch_data(url, headers).content
        
        filename = folder / f"{code}.png"
        
        with open(filename, "wb") as f:
            f.write(img)
        
        data["image"] = str(filename)
        
def parse_elo_team_names(elo_team_names):
    elo_team_names = elo_team_names.decode("utf-8")
    elo_team_names = elo_team_names.split(sep="\n")
    elo_team_names = [item.split("\t") for item in elo_team_names]
    elo_team_names = {name[0] : name[1] for name in elo_team_names if (len(name) > 1)}
    return elo_team_names

def elo_string_to_int(elo_string):
    elo_string = elo_string.replace('−', '-').replace('–', '-').replace('—', '-')
    return "0" if (elo_string == "-") else elo_string

def parse_elo_team_table(elo_teams_table):
    elo_teams_table = elo_teams_table.decode("utf-8")
    elo_teams_table = elo_teams_table.split("\n")
    elo_teams_table = [item.split("\t") for item in elo_teams_table]
    elo_data = {}
    for data in elo_teams_table:
        rank, code, points = data[0], data[2], data[3]
        average_rank, average_points = data[6], data[7]
        one_year_dif_ranking, one_year_dif_points = data[14], data[15]
        matches_T, matches_H, matches_A, matches_N = data[22:26]
        matches_W, matches_L, matches_D = data[26:29]
        Goals_F, Goals_A = data[29:]
        
        elo_data[code] = {"rank" : rank, 
                          "points" : points, 
                          "avg_rank" : average_rank, 
                          "avg_points" : average_points, 
                          "1_year_dif_rank": one_year_dif_ranking, 
                          "1_year_dif_points" : one_year_dif_points,
                          "total_games" : matches_T, 
                          "home_games" : matches_H, 
                          "away_games" : matches_A, 
                          "neutral_games" : matches_N, 
                          "games_won" : matches_W, 
                          "games_lost": matches_L, 
                          "games_drawn" : matches_D, 
                          "goals_for" : Goals_F,
                          "goals_against" : Goals_A}
        
        # some negative ints when shown as strings are using a Unicode minus character (−, U+2212),
        # not the normal ASCII hyphen-minus (-), so we must replace them first to avoid any errors
        elo_data[code] = {key : elo_string_to_int(value) for (key, value) in elo_data[code].items()}
        # the data is displayed as string, therefore it must be transformed to int
        elo_data[code] = {key : int(value) for (key, value) in elo_data[code].items()}
        
    return elo_data
    
def get_elo_ratings(headers, teams):
    request_table_url = "https://eloratings.net/World.tsv?_=1784292286123"
    request_team_names_url = "https://eloratings.net/en.teams.tsv?_=1784292286121"
    
    elo_teams_table = fetch_data(request_table_url, headers).content
    elo_teams_table = parse_elo_team_table(elo_teams_table)
    
    elo_team_names = fetch_data(request_team_names_url, headers).content
    elo_team_names = parse_elo_team_names(elo_team_names)
    
    return elo_teams_table, elo_team_names

def create_team_database(headers):
    url = "https://api.fifa.com/api/v3/fifarankings/rankings/live?gender=1&sportType=0&language=en"

    data = fetch_data(url, headers).json()
    teams = parse_fifa_rankings(data)
    return teams

def save_pickle(filename, teams_database):
    with open(filename, "wb") as f:
        pickle.dump(teams_database, f)

def load_pickle(filename):
    with open(filename, "rb") as f:
        return pickle.load(f)

def get_team_database():
    
    filename = "teams_2.pickle"
    filename2 = "teams.pickle"
    
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://inside.fifa.com/"
    }
    
    if not Path(filename).exists():
        teams = create_team_database(headers)
        download_flags(teams, headers)
        fifa_names = {name : teams[name]["country_code"] for name in teams}
        elo_table, elo_names = get_elo_ratings(headers, teams)
        add_elo_rating(teams, fifa_names, elo_names, elo_table)
        get_team_id(teams)
        # add the last 10 matches for each team
        get_teams_form(teams)
        # create the detailed stats extracted from form
        create_form_stats(teams)
        # normalise data for the detailed stats
        add_normalised_data(teams)
        save_pickle(filename, teams)
    else:
        teams = load_pickle(filename)
        teams2 = load_pickle(filename2)
        add_to_dict(teams, teams2, ["form", "stats"])
        add_normalised_data(teams2)
        save_pickle(filename, teams)
        
    return teams2

def add_elo_rating(teams, fifa_names, elo_names, elo_table):
    elo_name_to_code = {}

    for code, name in elo_names.items():
        elo_name_to_code[name] = code

    for name in fifa_names:

        if name in ELO_DEFUNCT:
            continue

        elo_name = FIFA_TO_ELO.get(name, name)

        elo_code = elo_name_to_code[elo_name]

        teams[name]["elo"] = elo_table[elo_code]


teams = get_team_database()
