import math
import random
import enum
import tkinter as tk
from PIL import Image, ImageTk, ImageOps

class CountryTileInGroup(tk.Frame):
    def __init__(self, parent, team_name, team, row, width=30, height=20):
        super().__init__(parent, bd=1, relief="solid")
        
        img = Image.open(team["image"]).resize((width, height))
        
        self.color_img = ImageTk.PhotoImage(img)
        self.gray_img = ImageTk.PhotoImage(
            ImageOps.grayscale(img)
        )
        
        self.flag = tk.Label(self, image=self.color_img)
        
        self.team_name = team_name
        self.team_info = team
        
        self.label = tk.Label(
            self,
            text=team["country_code"],
            font=("Arial", 10, "bold")
        )
        self.label2 = tk.Label(
            self,
            text="0",
            font=("Arial", 10, "bold")
        )
        
        self.row = row
        self.grade = team["norm"]["grade"]
        
        self.flag.grid(row=row, column=0, sticky="w")
        self.label.grid(row=row, column=1, sticky="w", padx=(5, 0))
        
    def change_colors(self, bg_col=None, fg_col=None):
        for label in (self.label, self.label2, self.flag):
            if bg_col is not None: label.configure(bg=bg_col)
            if fg_col is not None: label.configure(fg=fg_col)
        
    def change_table_position(self, row):
        self.flag.grid(row=row, column=0, sticky="w")
        self.label.grid(row=row, column=1, sticky="w", padx=(5, 0))
        
    def change_points_label(self, points):
        self.label2.configure(text=str(points))
        
    def add_points_col(self):
        self.label2.grid(row=self.row, column=2, sticky="w", padx=(20, 0))
        
    def paint_grayscale(self):
        self.flag.configure(image=self.gray_img)
        self.label.configure(fg="gray50")

class CountryTile(tk.Frame):
    def __init__(self, parent, team, team_name, width=30, height=20):
        super().__init__(parent, bd=1, relief="solid")
        
        self.team_name = team_name
        
        self.assigned = False
        self.unavailable = False
        
        self.team_info = team
        #print(team)
        img = Image.open(team["image"]).resize((width, height))
        
        self.color_img = ImageTk.PhotoImage(img)
        self.gray_img = ImageTk.PhotoImage(
            ImageOps.grayscale(img)
        )
        
        self.flag = tk.Label(self, image=self.color_img)
        self.flag.pack()
        
        self.label = tk.Label(
            self,
            text=team["country_code"],
            font=("Arial", 10, "bold")
        )
        self.label.pack()
        
    def assign(self):
        self.flag.configure(image=self.gray_img)
        self.label.configure(fg="gray50")
        self.assigned = True
    
    def unassign(self):
        self.flag.configure(image=self.color_img)
        self.label.configure(fg="black")
        self.assigned = False
        
    def set_available(self):
        self.unavailable = False
        self.toggle()
        
    def set_unavailable(self):
        self.unavailable = True
        
    def toggle(self):
        if self.unavailable: return
        if self.assigned:
            self.unassign()
        else:
            self.assign()
            
class GroupBox(tk.Frame):
    def __init__(self, parent, name, num, callback_remove_team, padx, pady):
        super().__init__(parent, bd=1, relief="solid")
        
        # the number of the group
        self.num = num
        
        self.parent = parent
        self.label = tk.LabelFrame(parent, text=name, width=70, height=50, padx=padx, pady=pady)
        
        self.teams = []
        self.original_widgets = []
        
        # callback to call when deleting a team from the group
        self.callback_rem = callback_remove_team
        # before clicking on "Confirm" the user can change the groups
        # according to their liking, but after confirming them they should
        # not be mutated any further
        self.mutable = True
        
    def change_labelwidget(self):
        #self.parent.update_idletasks()
        
        label_area = tk.Frame(self.parent)
        label_area.pack_propagate(False)
        label_area.config(width=self.label.winfo_width()+10, height=25)
        
        tk.Label(label_area, text=self.label.cget("text"), font=("Arial", 10, "bold")).pack(side="left")
        tk.Label(label_area, text="Pts").pack(side="right")
        
        self.label.config(labelwidget=label_area)
        
    def add_label(self, text):
        self.label2 = tk.LabelFrame(self.parent, text=text, width=100, height=150)
        
    def change_mutability(self, condition):
        self.mutable = condition
        
    def remove_team(self, team):
        if not self.mutable: return
        indx = self.teams.index(team)
        self.teams[indx].destroy()
        del self.teams[indx]
        
        self.original_widgets[indx].set_available()
        del self.original_widgets[indx]
        
        self.callback_rem(self.num, team.team_name)
        
    def bind_button_functionality(self, country):
        # lambda e, t => 'e' is for the event and 't' for the object whose method we call upon triggering
        country.bind("<Button-1>", lambda e, t=country : self.remove_team(country))
        country.label.bind("<Button-1>", lambda e, t=country : self.remove_team(country))
        country.flag.bind("<Button-1>", lambda e, t=country : self.remove_team(country))
        
    def add_team(self, country):
        new_country_in_group = CountryTileInGroup(self.label, country.team_name, country.team_info, len(self.teams))
        self.bind_button_functionality(new_country_in_group)
        new_country_in_group.pack()
        self.teams.append(new_country_in_group)
        
        self.original_widgets.append(country)
    
class Draw:
    def __init__(self, teams, teams_in_group, root, teams_frame, groups_frame, app_callback, groups_rows=2, groups_columns=6, add_points_col=True):
        self.country_selected = None
        self.teams = teams
        self.teams_in_group = teams_in_group
        
        self.confirm_button = tk.Button(root, text="Confirm", 
                                        activebackground="#2E7D32", activeforeground="#FFFFFF",
                                        state=tk.DISABLED, command=self.remove_teams_pot)
        #self.confirm_button.bind("<Button-1>", lambda e, t=self.confirm_button : self.remove_teams_pot())
        self.default_but_bg = self.confirm_button.cget("bg")
        self.default_but_fg = self.confirm_button.cget("fg")
        self.confirm_button.place(relx=1.0, rely=1.0, anchor="se")
        
        self.groups = []
        
        self.teams_frame = teams_frame
        self.groups_frame = groups_frame
        
        self.draw_finished = False
        
        self.groups_rows = groups_rows
        self.groups_columns = groups_columns
        
        self.add_points_col = add_points_col
        self.app_callback = app_callback
        
        self.country_names = [list() for _ in range(self.groups_rows * self.groups_columns)]
        
    def create_groups_ui(self):
        
        for i in range(self.groups_rows * self.groups_columns):
            for team_frame in self.groups[i].teams:
                team_frame.add_points_col()
            self.groups[i].change_labelwidget()
        
    # remove the 220 teams widgets, only keep the ones assigned to a group
    def remove_teams_pot(self):
        self.teams_frame.destroy()
        del self.teams_frame
        
        self.confirm_button.destroy()
        del self.confirm_button
        
        for group in self.groups:
            group.change_mutability(False)
            
        if self.add_points_col: self.create_groups_ui()
        
        self.app_callback()
        
    def add_groups(self, groups):
        self.groups = groups
    
    def place_button(self):
        self.confirm_button.place(relx=1.0, rely=1.0, anchor="se")
        
    def update_button(self):
        # len(group.teams) == self.teams_in_group           IS THE CORRECT ONE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        are_groups_filled = all([(len(group.teams) == self.teams_in_group ) for group in self.groups])
        state = tk.DISABLED if (not are_groups_filled) else tk.ACTIVE
        bg, fg = (self.default_but_bg, self.default_but_fg) if (not are_groups_filled) else ("#4CAF50", "#FFFFFF")
        self.confirm_button.config(bg=bg, fg=fg, state=state)
        
    def country_click(self, country):
        if country.unavailable: 
            self.country_selected = None
            return
        if self.country_selected is not None:
            self.country_selected.toggle()
        self.country_selected = country
        self.country_selected.toggle()
        
    def remove_team(self, group_num, country):
        #print(self.country_names[group_num])
        self.country_names[group_num].remove(country)
        #print(self.country_names[group_num])
        self.update_button()
        
    def group_click(self, group):
        country = self.country_selected
        if (country is None) or (country.unavailable): return
        if (len(group.teams) < self.teams_in_group) and (country not in group.teams):
            country.set_unavailable()
            group.add_team(country)
            self.country_names[group.num].append(country.team_name)
        else:
            country.toggle()
        self.country_selected = None
        self.update_button()
            
# the main class used to simulate and predict the games after the
# draw is finished
class Simulator:
    def __init__(self, groups_rows, groups_columns):
        self.counter = 0
        # boolean value to ensure the groups frames are set only once
        self.groups_set = False
        self.groups = None
        self.country_names = None
        
        self.groups_rows = groups_rows
        self.groups_columns = groups_columns
        # the first two of each group are automatically qualified
        self.automatic_qual = 2
        self.rest_to_qualify = 32 - (self.groups_rows * self.groups_columns * self.automatic_qual)
    
    def destroy_all(self):
        #print(len(self.groups), self.groups)
        #for i in range(len(self.groups)):
        for i, group in enumerate(self.groups):
            #print(i)
            group.destroy()
            for j, team in enumerate(group.teams):
                team.destroy()
                del group.teams[j]
            del group.teams
            del self.groups[i]
        
        del self.groups
        
        del self.country_names
        
    # delta is the difference in power between the teams and k controls the
    # sensitivity of the model
    def win_probability(self, delta, k):
        return 1 / (1 + math.exp(-k * delta))
        
    def get_result(self, home_win, draw):
        r = random.random()
        
        if r < home_win:
            return 1
        elif r < home_win + draw:
            return 0
        else:
            return -1
        
    # used to compare two teams and determine the result between them utilising
    # the normalised data we created in the normalise_data.py file ("norm" key
    # points to a dict of normalised values. 'grade' is the power of the team,
    # a value in the range 0-1)
     # k determines how sensitive the model is
    def comp_func(self, team1, team2, teams, k=12):
        # the difference between team1's and team2's 'grade' value stored in the 
        # normalised data dict
        difference = teams[team1]["norm"]["grade"] - teams[team2]["norm"]["grade"]
        p = self.win_probability(difference, k)
        
        draw_prob = max(0.15, 0.3 - abs(difference))
        remaining = 1 - draw_prob
        
        win_prob = remaining * p
        lose_prob = remaining * (1 - p)
        
        return self.get_result(win_prob, draw_prob)
        
    # this function sorts the list of the thirds and keeps the best 8 of them.
    # This happens because there are 12 groups, the top 2 from each group qualify
    # to the next round (24 teams in total), so there are 8 teams left to form the
    # round of 32 (that's why we only keep self.rest_to_qualify teams).
    # The sorting uses a tuple as the return value, because in tuples python checks
    # each value seperately until it finds any difference. For example for two tuples:
    # (2, 1.7), (2, 3.2) where we apply reverse sort order it will return: (2, 3.2), (2, 1.7).
    # The first values in each pair are equal, therefore python continues with the next ones.
    def draw_best_third(self, best_three, round_32_teams):
        best_three = sorted(best_three, key=lambda x : (x[0], x[1].grade), reverse=True)[:self.rest_to_qualify]
        
        # for each of the team color the background lime green and the foreground white
        # to indicate they were one of the best 8 teams that finished 3rd in their group
        for points, frame in best_three:
            round_32_teams.append(frame.team_name)
            frame.change_colors(bg_col="#30BD30", fg_col="#FFFFFF")
            frame.pack()
        
    # function to change the background and foreground for the automatically
    # qualified teams (first two of each group) 
    # i is the index of the current group, points is a list of the points
    # earned based on the model's predictions
    def draw_group_standings(self, i, points, round_32_teams):
        best_third = None
        
        new_table = [(j, point) for j, point in enumerate(points)]
        new_table = sorted(new_table, key=lambda x : x[1], reverse=True)
        
        third = new_table[2]
        best_third = (self.groups[i].teams[third[0]], third[1])
        
        new_table = [item[0] for item in new_table]
        
        for j, team_frame in enumerate(self.groups[i].teams):
            team_frame.pack_forget()
            
        # new_table now has the indexes in the correct order, for example [3, 0, 2, 1].
        # This means that the original 4th team in the group now is the leader of it. Packing
        # the labels at the correct order is necessary to ensure this ordering.
        for j, new_index in enumerate(new_table):
            # change background to dark green for the top two in each group as they
            # are automatically qualified. 
            if j < 2: 
                round_32_teams.append(self.groups[i].teams[new_index].team_name)
                self.groups[i].teams[new_index].change_colors(bg_col="#006400", fg_col="#FFFFFF")
    
            self.groups[i].teams[new_index].pack()
            
        # return the 3rd in the group
        return best_third
        
    # calculate the groups standings based on the compare function provided
    def calculate_groups_standings(self, teams):
        round_32_teams = list()
        checked_pairs = set()
        # best_third is a list to hold the third of each group
        best_third = list()
        
        for i in range(self.groups_rows * self.groups_columns):
            # points earned by each team in group
            points = [0 for _ in range(len(self.country_names[i]))]
            
            for num1, team_h in enumerate(self.country_names[i]):
                for num2, team_a in enumerate(self.country_names[i]):
                    
                    if team_h == team_a: continue
                    if ((team_h, team_a) in checked_pairs) or ((team_a, team_h) in checked_pairs): continue
                    
                    res = self.comp_func(team_h, team_a, teams)
                    points[num1] += 3 if (res == 1) else 1 if (res == 0) else 0
                    points[num2] += 3 if (res == -1) else 1 if (res == 0) else 0
                    checked_pairs.add((team_h, team_a))
                    
            for j, team_frame in enumerate(self.groups[i].teams):
                # we keep the index of the group the team is assigned to (i),
                # the points it managed to secure, the grade of the team (from
                # normalise_data.py) and the team's frame
                team_frame.change_points_label(points[j])
                
            third_team_frame, third_team_pts = self.draw_group_standings(i, points, round_32_teams)
            best_third.append((third_team_pts, third_team_frame))
            
        self.draw_best_third(best_third, round_32_teams)
    
        return round_32_teams
        
class TournamentStage(enum.Enum):
    GROUPS = enum.auto()
    ROUND_OF_32 = enum.auto()
    ROUND_OF_16 = enum.auto()
    QUARTERS = enum.auto()
    SEMIS = enum.auto()
    FINAL = enum.auto()
    END = enum.auto()
    
class App:
    def __init__(self, root, main_frame, group_frame, team_frame, teams, simulator, funs):
        self.root = root
        self.main_frame = main_frame
        self.group_frame = group_frame
        self.team_frame = team_frame

        self.teams = teams
        self.stage = TournamentStage.GROUPS
        
        self.stage_dict = {
            TournamentStage.ROUND_OF_32: "R32",
            TournamentStage.ROUND_OF_16: "R16",
            TournamentStage.QUARTERS: "QF",
            TournamentStage.SEMIS : "SF",
            TournamentStage.FINAL: "F",
            TournamentStage.END : "E"
        }
        
        self.stages = [self.stage, *list(self.stage_dict.keys())]

        self.draw = None
        self.simulator = simulator
        
        self.tiles = None
        
        self.configure_layout, self.create_groups, self.create_country_tiles = funs
        
        self.knockout_frames = {
            TournamentStage.ROUND_OF_32: 16,
            TournamentStage.ROUND_OF_16: 8,
            TournamentStage.QUARTERS: 4,
            TournamentStage.SEMIS : 2,
            TournamentStage.FINAL: 1
        }
        
        self.LEFT_X = [50, 220, 390, 560]
        self.RIGHT_X = [50, 220, 390, 560]
        self.FINAL_X = 730
        
        self.canvas = tk.Canvas(root, width=1400, height=700, bg="white")
        
        self.groups = {
            phase : list() for phase in ["R32", "R16", "QF", "SF", "F"]
        }
        
        self.step = [2, 4, 8, 16, 32]
        
        # division_dict helps us get the correct index of each group
        self.division_num = [2, 4, 4, 4, 2]
        self.division_dict = {key : value for key, value in zip(self.knockout_frames.keys(), self.division_num)}
        self.start_column = [0, 1, 3, 7, 7]
        
        self.pairs_in_phase = {
            "R32" : 16,
            "R16" : 8,
            "QF" : 4,
            "SF" : 2,
            "F" : 1
        }
        
        self.declared_winner = False

    def add_draw(self, draw):
        self.draw = draw
        
    def draw_frames(self, rows, columns):
        for group_num, group in enumerate(self.groups.values()):
            group_len = len(group)
            half_frames = group_len // 2
            
            start_column = self.start_column[group_num]
            
            for i in range(half_frames):
                self.create_match(group_num, start_column + i * self.step[group_num], group[i].label)
                
            for i in range(half_frames, group_len):
                # set the column value within the range: 0-half_frames
                cur_col = i % max(1, half_frames)  # avoid division by 0
                self.create_match(rows-group_num, start_column + cur_col * self.step[group_num], group[i].label)
        
    def destroy_all(self):
        self.group_frame.destroy()
        self.team_frame.destroy()
        
    def create_match(self, row, column, match_frame):
        match_frame.grid(row=row, column=column)
        
    def next_round(self, previous):
        return [(previous[i] + previous[i+1]) / 2 for i in range(0, len(previous), 2)]
    
    # add the groups to app and remove them from draw object
    def handle_knockout_draw_exit(self):
        self.team_frame.destroy()
        self.groups["R32"] = self.draw.groups
        self.draw.groups = list()
        
    # remove the frame desplaying the teams available for draw and
    # move the second row to the bottom of the screen
    def create_knockout_ui(self):
        self.handle_knockout_draw_exit()
        
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.groups_frame.grid(row=0, column=0, sticky="nsew")
        
        rounds = len(self.knockout_frames)
        rows = 2 * rounds - 1
        
        for r in range(rows):
            self.groups_frame.grid_rowconfigure(r, weight=1)

        # we divide by 2 because we want to find the columns needed at
        # each side, for example there need to be 8 frames at the top
        # and 8 at the bottom for the round of 32, then half of them
        # for the round of 16 etc.
        columns = sum([num//2 for num in self.knockout_frames.values()])
        
        for c in range(columns):
            self.groups_frame.grid_columnconfigure(c, weight=1)
        
        for phase in self.groups:
            # round 32 has been already calculated, therefore move one to the
            # next rounds
            if len(self.groups[phase]) != 0: continue
            group_name = ("Pair {:}" + f" {phase}:") if (phase != "F") else "Final"
            self.groups[phase] = self.create_groups(self.groups_frame, self.draw, rows, 
                                    [str(num+1) for num in range(self.pairs_in_phase[phase])], 
                                    group_name=group_name, padx=1, pady=1)
            for group in self.groups[phase]:
                group.change_mutability(False)
            
        self.draw_frames(rows, columns)
    
    def create_simulator_group_frames(self):
        self.simulator.groups = self.draw.groups
        self.simulator.country_names = self.draw.country_names
        self.draw.group_frames = list()
        self.draw.country_names = list()
        
    # creates new frames for the knockout phase
    def create_knockout_frames(self, teams):
        groups_rows = 2
        groups_columns = 8

        tiles = {}
        self.groups_frame = tk.Frame(self.main_frame)
        self.countries_frame = tk.Frame(self.main_frame)

        self.simulator = Simulator(groups_rows, groups_columns)
        
        self.draw = Draw(teams, 2, self.root, self.countries_frame, self.groups_frame, self.create_knockout_ui, 
                         groups_rows=groups_rows, groups_columns=groups_columns, add_points_col=False)

        self.configure_layout(self.groups_frame, self.countries_frame, groups_rows, groups_columns, countries_col=groups_columns*groups_rows)

        groups = self.create_groups(self.groups_frame, self.draw, groups_columns, 
                                    [str(num+1) for num in range(groups_rows * groups_columns)], 
                                    group_name="Pair {:} R32:", padx=10)

        self.create_country_tiles(self.countries_frame, teams, self.draw, tiles, columns=groups_columns*groups_rows)
        
    # get the result for a game in the knockout phase: executing until a winner is
    # decided, a draw is not wanted since either team must win to advance
    def get_knockout_game_result(self, pair):
        ret = 0
        while ret == 0:
            ret = self.simulator.comp_func(pair[0].team_name, pair[1].team_name, self.teams)
        return ret
        
    # res is a boolean value: 0 means home won, else 1 means away won
    def get_next_frame(self, num_group, res, pair):
        pair_indexes = num_group * 2, num_group * 2 + 1
        next_frame_indx = sum(pair_indexes) // self.division_dict[self.stage]
        self.groups[self.stage_dict[self.stage]][next_frame_indx].add_team(pair[res])
        
    # res is a value 0/1, reflecting the win of home or away team,
    # the opposite of res gives as the looser
    def color_loosing_team(self, teams, res):
        teams[abs(1 - res)].paint_grayscale()
        
    def color_champion(self, teams, res):
        teams[res].flag.config(bg="#D3AF37")
        teams[res].label.config(bg="#D3AF37")
    
    def get_next_phase(self):
        if self.declared_winner: return
        
        prev_stage = self.stages[max(0, self.stages.index(self.stage)-1)]
        groups = self.groups[self.stage_dict[prev_stage]]
        
        for num, pairs in enumerate([groups[i:i+2] for i in range(0, len(groups), 2)]):
            for pair in pairs:
                ret = self.get_knockout_game_result(pair.teams)
                ret = 0 if (ret == 1) else 1
                self.color_loosing_team(pair.teams, ret)
                if self.stage != TournamentStage.END:
                    self.get_next_frame(num, ret, pair.teams)
                else:
                    self.color_champion(pair.teams, ret)
                    self.declared_winner = True
        
    def get_next_stage(self):
        stage_indx = self.stages.index(self.stage)
        new_index = stage_indx + 1
        if new_index >= len(self.stages): return self.stage
        return self.stages[new_index]
        
    def continue_simulation(self):
        
        if self.stage == TournamentStage.GROUPS:
            round_32_teams = self.simulator.calculate_groups_standings(self.teams)
            self.teams = {team : self.teams[team] for team in round_32_teams}
            
            self.stage = self.get_next_stage()
            
        elif self.stage == TournamentStage.ROUND_OF_32:
            
            self.destroy_all()
            self.create_knockout_frames(self.teams)
            
            self.stage = self.get_next_stage()
            
        else:
            self.get_next_phase()
            self.stage = self.get_next_stage()