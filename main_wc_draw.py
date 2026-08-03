import tkinter as tk
import math
from ui_setup import *
from fetch_national_team_data import teams
from country_widgets import *

root = tk.Tk()
root.title("WC Draw Simulator")
root.geometry("1400x700")
root.pack_propagate(False)

tiles = {}

main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)

main_frame.grid_rowconfigure(0, weight=2)
main_frame.grid_rowconfigure(1, weight=1)
main_frame.grid_columnconfigure(0, weight=1)

# main containers
groups_frame = tk.Frame(main_frame)
countries_frame = tk.Frame(main_frame)

groups_rows = 2
# * 2 because for each group we need another frame for the
# statistics: games played, wins, draw, loses and points earned
groups_columns = 6

simulator = Simulator(groups_rows, groups_columns)
app = App(root, main_frame, groups_frame, countries_frame, teams, simulator, [configure_layout, create_groups, create_country_tiles])
draw = Draw(teams, 4, root, countries_frame, groups_frame, app.create_simulator_group_frames)
app.add_draw(draw)

configure_layout(groups_frame, countries_frame, groups_rows, groups_columns)

groups = create_groups(groups_frame, draw, groups_columns, "ABCDEFGHIJKL")

create_country_tiles(countries_frame, teams, draw, tiles)

bind_events(root, app)

root.mainloop()