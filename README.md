<div align="center">

# WC-Draw-Simulator

</div>

A WC (World Cup) draw and games simulator. The user makes the draw and the rest are handled by the app. Multiple platforms/ datasers are used to extract info for the model deciding the results (logistic regression). The data extraction happens like this:
- **fifa.com**: extraction of team names, FIFA rankings, flags and other useful data provided by the FIFA national team ranking site (https://inside.fifa.com/fifa-rankings/world-ranking/men)
- **elo database**: extraction of elo rankings and important team statistics like games played (https://eloratings.net/), games won, goals scored etc. After research I found out that elo ranking is a better power-measuring method, because it takes various aspects into account and therefore FIFA ranking partially follows elo's implementation.
- **api football**: extract games stats for each team (https://www.api-football.com/). I use the last 10 matches and calculate the means for goals scored, conceded and the total games won, drawn and lost.

I then normalise each metric into a float value between 0-1 and calculate the final power of a team by using percentages for each metric. For example the elo ranking accounts for 45% of the total power, because it is a very valid and trusted power-ranking method. To calculate the win probability for a home team in a match I first calculate the power difference between the two teams and then use the logistic regression. I calculate the probability for the win and draw based on the result i update the standings when in group phase or advance the winner of the pair to the next round.

The project is organised into 9 files:
- **country_mappings.py**: includes dictionaries to solve any naming differences between platforms. I created them after trial and error.
- **normalise_data.py**: normalise the metrics (goals for, against, rankings etc.) into float values in the range 0-1. The goal is to create a final grade using weights for each metric that is also within the same range.
- **calculate_stats.py**: adds data from each fixture into the "form" dict of each team and calculate the means for them.
- **main_wc.py**: the file acting as the main function of the project. It inisialises the data and runs the root.mainlooop() of tkinter.
- **ui_setup.py**: contains useful functions used to create the frames and the overall layout of the app.
- **api_football.py**: implements functions for the extraction of data from the api football website.
- **fetch_national_team_data.py**: creates the teams object (acting as a dataset for our app, implemented as a dict, with the country names acting as keys for it).
- **connect_dict.py**: connects the two dicts (teams and teams2). The reason i needed two dicts is because there was a per minute and daily limit for the requests at api-football.com . One dict was being updatied daily while the other containing data extracted from sites with no daily limit remained untouched.
- **country_widgets.py**: The largest of the 9 files. It contains classes important for the organisation and function of the app. **CountryTileInGroup** represents the country when assigned to a group. CountryTile are the frames on the bottom of the start screen (all the available countries for the user to select from). **GroupBox** is meant to represent the groups, holding a list of teams. **Draw** is responsible for the draw procedure, while **Simulator** calculates the standings based on the groups generated from the *Draw* object. **App** organises all the above objects and ensures the smooth operation of the app.
