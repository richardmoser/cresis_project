import os
import PySimpleGUI as gui
from doitfile import doit

# creates a simple GUI to run doitfile.py. a drop down should show the available seasons and flights by listing the
# contents of the C:\Users\rj\Documents\cresis directory

contents = os.listdir(r"C:\Users\rj\Documents\cresis\rds")
flights = []
draw_plots = True
seg_length = 100
zoom = True


def season_getter(contents):
    seasons = []
    for item in contents:
        seasons.append(item)
    # flights are the contents of the season directory's CSARP_layerData directory
    return seasons


def flight_getter(contents, season):
    flights = []
    contents = os.listdir(r"C:\Users\rj\Documents\cresis\rds" + "\\" + season + "\\CSARP_layerData")
    for item in contents:
        flights.append(item)
    return flights


seasons = season_getter(contents)


# once a season is selected, the flights drop down should populate with the available flights

layout = [
    [gui.Text("Select a season")],
    [gui.Combo(seasons, key='season', size=25, enable_events=True)],
    [gui.Text("Select a flight")],
    [gui.Combo(flights, key='flight', size=15)],
    [gui.Button("Run!", size=(10, 3), key='Run')]
]

window = gui.Window("CReSIS Data Viewer").Layout(layout)

while True:
    # print("Debug: Getting here")
    event, values = window.Read()
    if event == "Run":
        print("Running...\n")
        season = values['season']
        flight = values['flight']
        print(f"Running {season} {flight}")
        # run the doitfile.py with the selected season and flight
        try:
            (doit(season, flight, draw_plots, seg_length, zoom))
        except Exception as e:
            print(e)
        print("done\n\n--------------------\n\n")

    # if event is setting the season, then the flights should be populated
    if event == 'season':
        print("Getting flights...")
        flights = flight_getter(contents, values['season'])
        window['flight'].Update(values=flights)
        print("Flight list populated.\n")

    if event is None:
        break
    # print(event, values)
window.Close()


