from project_classes import *
from functions import *
from iceflow_library import *

"""Cell Break in dev.ipynb"""

zoom = True
seg_length = 100
season = "2018_Antarctica_DC8" # a layerData season
season = "2016_Antarctica_DC8" # a season with both layer and layerData
# season = "2014_Antarctica_DC8" # a layerData season
flight = "20181030_01"  # the flight date and frame number
flight = "20181103_01"
# flight = "20181112_02"  # the problem flight
flight = "20161024_05"
# flight = '20141026_06'
file_name = "layer_export_" + flight + ".pickle"
testing = False

"""Cell Break in dev.ipynb"""

mat_pickler_layer(season, flight, testing_mode=testing)  # make it
layers = read_layers(file_name)  # read in the layers from the pickle file

"""Cell Break in dev.ipynb"""

### read in the iceflow data from the iceflow data files and save them to a pickle file

try:
    iceflow_data = iceflow_data_file_loader()
    print("The iceflow data pickle file was found and loaded.")
except FileNotFoundError:
    print("The iceflow data pickle file was not found. Creating a new one...")
    filename = iceflow_saver()
    iceflow_data = iceflow_loader(filename)
    print("The iceflow data pickle file was successfully created.")

x = iceflow_data[0]
y = iceflow_data[1]
velocity_x = iceflow_data[2]
velocity_y = iceflow_data[3]
latitude = iceflow_data[4]
longitude = iceflow_data[5]

"""Cell Break in dev.ipynb"""

intersection_points_base, intersection_indices_base, segment_ends = cross_point(layers[0], seg_length, quiet=True)
# find the crossover points
print(f"len(intersection_indices): {len(intersection_indices_base)}")
print(f"len(intersection_points): {len(intersection_points_base)}")

"""Cell Break in dev.ipynb"""

plot_layers_at_cross(layers[0], intersection_indices_base, segment_ends, zoom=zoom)


"""Cell Break in dev.ipynb"""



"""Cell Break in dev.ipynb"""



"""Cell Break in dev.ipynb"""



"""Cell Break in dev.ipynb"""
