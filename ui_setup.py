from country_widgets import *

# configure the layout of the frames 
def configure_layout(groups_frame, countries_frame, groups_rows, groups_columns, countries_col=32):

    # vertical stacking
    groups_frame.grid(row=0, column=0, sticky="n")
    countries_frame.grid(row=1, column=0, sticky="n")

    for r in range(groups_rows):
        groups_frame.grid_rowconfigure(r, weight=1)

    for c in range(groups_columns):
        groups_frame.grid_columnconfigure(c, weight=1, minsize=70)

    for c in range(countries_col):
        countries_frame.grid_columnconfigure(c, weight=1)
        
# create the group frames/ boxes
def create_groups(groups_frame, draw, groups_columns, groups_names, 
                  group_name="Group: {:}", padx=15, pady=10):

    groups = []

    for i, letter in enumerate(groups_names):
        group = GroupBox(
            groups_frame,
            group_name.format(letter),
            i,
            draw.remove_team,
            padx=padx,
            pady=pady
        )

        group.label.grid(
            row=i // groups_columns,
            column=i % groups_columns,
            sticky="nsew",
            padx=5,
            pady=5
        )

        group.grid_propagate(False)

        group.bind(
            "<Button-1>",
            lambda e, g=group: draw.group_click(g)
        )
        group.label.bind(
            "<Button-1>",
            lambda e, g=group: draw.group_click(g)
        )

        groups.append(group)

    draw.add_groups(groups)
    return groups

# create selectable country tiles/frames (widgets)
def create_country_tiles(countries_frame, teams, draw, tiles, columns=32):

    for i, (country, info) in enumerate(teams.items()):
        tile = CountryTile(
            countries_frame,
            info,
            country
        )

        tile.grid(
            row=i // columns,
            column=i % columns,
            sticky="n",
            padx=3,
            pady=3
        )

        tile.bind(
            "<Button-1>",
            lambda e, t=tile: draw.country_click(t)
        )
        tile.flag.bind(
            "<Button-1>",
            lambda e, t=tile: draw.country_click(t)
        )
        tile.label.bind(
            "<Button-1>",
            lambda e, t=tile: draw.country_click(t)
        )

        tiles[country] = tile

# create triger events for the draw process
def bind_events(root, app):

    root.bind(
        "<Return>",
        lambda e: app.continue_simulation()
    )