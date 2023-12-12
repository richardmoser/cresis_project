import math
import datetime
from layer_class import Twtt_Posit
from functions import *

season = "2018_Antarctica_DC8"
flight = "20181030_01"  # the flight date and frame number
file_name = "layer_export_" + flight + ".pickle"

layers = read_layers(file_name)  # read in the layers from the pickle file

# print(layers[0].gps_time[0])

# print(datetime.datetime.fromtimestamp(layers[0].gps_time[0]))

timestamp = gps_time_to_date(layers[0].gps_time[0])

print(timestamp.day)

