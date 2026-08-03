
# i created this file because i needed two dicts when working on the project.
# One to maintain the data extracted from the elo database and fifa site and
# the other to systematically add data extracted from api football, because i
# was limited to the limited plan and could only make 100 requests per day.
# One error meant the whole pickle file was either going to be too hard to debug
# or contain false data.

# add_to_dict adds the key : value pairs from dict1 to dict2 
def add_to_dict(dict1, dict2, keys_to_add):
    for key1 in dict1:
        for key_to_add in keys_to_add:
            dict2[key1][key_to_add] = dict1[key1][key_to_add]
    
#team1 = load_pickle("teams.pickle")
#team2 = load_pickle("teams_2.pickle")
#team3 = team1 | team2
#add_to_dict(team2, team1, ["form", "stats"])
#print(team1["Germany"], "\n", team2["Germany"]) #, "\n", team3["Germany"])