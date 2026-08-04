from country_mappings import *
import requests
import time

headers = {
    # Change the key into your own, after you complete the registration at api football
    'x-apisports-key':  "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    }

def get_team_id(teams):
    
    for country in teams:
        key_exists = teams[country].get("api_id", None)
        if key_exists is not None: continue
        
        r = requests.get(
            "https://v3.football.api-sports.io/teams",
            headers=headers,
            params={"name": NAME_TO_ELO.get(country, country)}
        )

        data = r.json()

        if data["results"] == 0:
            print(r.status_code, r.json(), country)
            time.sleep(7)
            continue
        
        teams[country]["api_id"] = data["response"][0]["team"]["id"]
        print(country, teams[country]["api_id"])
        
        time.sleep(7)
        
def get_teams_form(teams):
    for country in teams:
        # if key exists continue, don't recalculate everything
        key_exists = teams[country].get("form", None)
        if key_exists is not None: continue
        
        # team was not in api football dataset (like Bosnia's and North 
        # Macedonia's men national teams)
        if 'api_id' not in teams[country]: 
            teams[country]["form"] = list()
            continue
        
        r = requests.get(
            f"https://v3.football.api-sports.io/fixtures?team={teams[country]['api_id']}&season=2024",
            headers=headers
        )

        data = r.json()

        if data["results"] == 0:
            teams[country]["form"] = list()
            print(r.status_code, r.json(), country)
            time.sleep(7)
            continue
        
        # get 10 latest fixtures for the team
        fixtures_sorted = sorted(
            data["response"],
            key=lambda x : x["fixture"]["timestamp"],
            reverse=True
        )
        
        last10 = fixtures_sorted[:10]
        
        teams[country]["form"] = last10
        
        time.sleep(7)

   
