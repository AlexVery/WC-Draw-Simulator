

# normalise_elo normalises the elo points to a value in the range 0-1.
# min_elo and max_elo act roughly as the boundaries of the elo ranking
def normalise_elo(country, key, teams, min_elo=350, max_elo=2300):
    elo_points = teams[country]["elo"]["points"]
    
    e = (elo_points - min_elo) / (max_elo - min_elo)
    e = max(0, min(1, e))
    teams[country][key]["elo"] = e
    return e

def normalise_fifa(country, key, teams, min_rank=1, max_rank=211):
    fifa_rank = teams[country]["rank"]
    
    f = 1 - ((fifa_rank - min_rank) / (max_rank - min_rank))
    f = max(0, min(1, f))
    teams[country][key]["fifa"] = f
    return f
    
# calculates the normalised form adding 3 points for each win and one
# for the draws. Capturing the draws as well creates a better understanding
# of the team's form
def normalise_form(country, key, teams):
    wins = teams[country]["stats"]["W"]
    draws = teams[country]["stats"]["D"]
    games_played = teams[country]["stats"]["GP"]
    
    try:
        r = (3 * wins + draws) / (3 * games_played)
    except:
        # avoid division by 0
        r = 0
    r = max(0, min(1, r))
    teams[country][key]["form"] = r
    return r
    
# we normalise between -3 and 3 (can be altered), therefore:
def normalise_goal_difference(country, key, teams, min_gd=-3, max_gd=3):
    goal_difference = teams[country]["stats"]["GD"]
    
    g = (goal_difference - min_gd) / (max_gd - min_gd)
    g = max(0, min(1, g))
    teams[country][key]["GD"] = g
    return g
    
# normalise between 0-4 (can be altered)
def normalise_goals_scored(country, key, teams, min_g=0, max_g=4):
    goals_scored = teams[country]["stats"]["GF"]
    
    g = (goals_scored - min_g) / (max_g - min_g)
    g = max(0, min(1, g))
    teams[country][key]["GF"] = g
    return g
    
# we normalise between  0-4 (can be altered)
def normalise_goals_against(country, key, teams, min_g=0, max_g=4):
    goals_against = teams[country]["stats"]["GA"]
    
    g = 1 - ((goals_against - min_g) / (max_g - min_g))
    g = max(0, min(1, g))
    teams[country][key]["GA"] = g
    return g
    
# this function weights the normalised data contributing a certain weight to each metric.
# elo_w = elo ranking weight
# form_w = recent form weight
# gd_w = goal difference weight
# gf_w = goals scored weight
# ga_w = goals conceded weight
# fifa_rank_w = fifa ranking weight
def weight_features(country, features, key, teams,
                    elo_w=0.45, form_w=0.25, gd_w=0.1, gf_w=0.07, ga_w=0.08, fifa_rank_w=0.05):
    
    elo, form, gd, gf, ga, fifa = features
    grade = (elo * elo_w + form * form_w + gd * gd_w + gf * gf_w + ga * ga_w + fifa * fifa_rank_w)
    # grade is already normalised so it needs no further normalisation
    teams[country][key]["grade"] = grade
    return grade

def add_normalised_data(teams):
    # the key of the key : value pair. The value is a dict holding the normalised metrics
    norm_key = "norm"
    
    for country in teams:
        teams[country].setdefault(norm_key, {})
        
        elo = normalise_elo(country, norm_key, teams)
        form = normalise_form(country, norm_key, teams)
        gd = normalise_goal_difference(country, norm_key, teams)
        gf = normalise_goals_scored(country, norm_key, teams)
        ga = normalise_goals_against(country, norm_key, teams)
        fifa = normalise_fifa(country, norm_key, teams)
        
        weight_features(country, [elo, form, gd, gf, ga, fifa], norm_key, teams)