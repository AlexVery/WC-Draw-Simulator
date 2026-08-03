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

<div align="center">

  <p align="center">
    <img width="960" height="514" alt="Image" src="https://github.com/user-attachments/assets/7b873cfa-a3e2-4e60-9f61-2747acf05ca0" />
  </p>

  **Figure 1**: App main screen

</div>


<div align="center">

  <p align="center">
    <img width="960" height="514" alt="Image" src="https://github.com/user-attachments/assets/c92bafdd-22e5-4214-af66-72cff286e095" />
  </p>

  **Figure 2**: User selected a team

</div>


<div align="center">

  <p align="center">
    <img width="960" height="514" alt="Image" src="https://github.com/user-attachments/assets/f4fa0d1e-1b18-47d4-8a4a-73ab41523310" />
  </p>

  **Figure 3**: Team asssigned to a group

</div>


<div align="center">

  <p align="center">
    <img width="960" height="514" alt="Image" src="https://github.com/user-attachments/assets/5b9dacb8-6914-4065-81ba-117d33ead62b" />
  </p>

  **Figure 4**: *Confirm* button becomes available after all groups become full

</div>


<div align="center">

  <p align="center">
    <img width="960" height="514" alt="Image" src="https://github.com/user-attachments/assets/482571cc-2026-4349-982b-b29d21ee64cc" />
  </p>

  **Figure 5**: Round of 32 frames

</div>


<div align="center">

  <p align="center">
    <img width="960" height="514" alt="Image" src="https://github.com/user-attachments/assets/dd7d49a5-dd68-49f4-b7cf-f5ff6ccbda43" />
  </p>

  **Figure 6**: Calculated standings, qualified teams depicted using green

</div>


<div align="center">

  <p align="center">
    <img width="960" height="514" alt="Image" src="https://github.com/user-attachments/assets/f9f1a1a5-68c6-4131-9210-25c168ee7e5e" />
  </p>

  **Figure 7**: Draw for round of 16

</div>


<div align="center">

  <p align="center">
    <img width="960" height="514" alt="Image" src="https://github.com/user-attachments/assets/e0f299b0-6d9e-4f7c-9cd6-1df8493f4d88" />
  </p>

  **Figure 8**: *Confirm* button becomes available

</div>


<div align="center">

  <p align="center">
    <img width="960" height="514" alt="Image" src="https://github.com/user-attachments/assets/514d3c23-d37c-467f-8464-4090b590210a" />
  </p>

  **Figure 9**: Created knockout frames

</div>


<div align="center">

  <p align="center">
    <img width="960" height="514" alt="Image" src="https://github.com/user-attachments/assets/154ccf45-3d9b-47cb-9e20-02b29567055b" />
  </p>

  **Figure 10**: Generated round of 16

</div>


<div align="center">

  <p align="center">
    <img width="960" height="514" alt="Image" src="https://github.com/user-attachments/assets/1f70f861-f736-41b8-96f7-13dd127b939b" />
  </p>

  **Figure 11**: Generated Quarterfinals

</div>


<div align="center">

  <p align="center">
    <img width="960" height="514" alt="Image" src="https://github.com/user-attachments/assets/7ed3e074-e498-4988-adf8-3be015710bda" />
  </p>

  **Figure 12**: Generated Semifinals

</div>


<div align="center">

  <p align="center">
    <img width="960" height="514" alt="Image" src="https://github.com/user-attachments/assets/04ced2f5-8eb1-42ac-8a02-d016ca50b810" />
  </p>

  **Figure 13**: Generated Final

</div>


<div align="center">

  <p align="center">
    <img width="960" height="514" alt="Image" src="https://github.com/user-attachments/assets/91d113c1-8a9e-42ed-b1a9-e5462935137a" />
  </p>

  **Figure 14**: Crowned Champion!

</div>
