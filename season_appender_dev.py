import matplotlib.pyplot as plt

from project_classes import *
from functions import *
from iceflow_library import *

seg_length = 100
season = "2018_Antarctica_DC8" # a layerData season

# full_season_layerize(season)

# append_layers needs a file name to append and layers to append to

# make the layers from the initial flight

flight1 = "20181018_01"  # the flight date and frame numbe
mat_pickler_layer(season, flight1)
file_name = "layer_export_" + flight1 + ".pickle"
layers = read_layers(file_name)

flight2 = "20181030_01"
