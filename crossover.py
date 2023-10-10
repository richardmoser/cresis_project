import numpy as np
import pickle
import matplotlib.pyplot as plt
from layer_class import Layer
from layer_class import Twtt_Posit
from mpl_toolkits.basemap import Basemap
from shapely.geometry import LineString
from library import *

plot_map = False
# plot_map = True
seg_length = 100
flight = "20181030_01"
file_name = "layer_export_" + flight + ".pickle"


def main():
    layers = read_layers(flight, file_name)  # read in the layers from the pickle file

    intersection_points, intersection_indices = cross_point(layers[0], seg_length, quiet=True)
    # find the crossover points

    twtt_at_intersect = twtt_at_point(layers[1], layers[0], intersection_indices)
    # find the twtt at the crossover points
    twtt_difference_at_intersect = twtt_at_intersect[0][0] - twtt_at_intersect[0][1]
    # find the difference in twtt at the crossover points
    print(f"twtt difference at crossover point: {twtt_difference_at_intersect} ns")

    refractive_index = 1.77
    depth_1 = twtt_to_depth(twtt_at_intersect[0][0], refractive_index)
    depth_2 = twtt_to_depth(twtt_at_intersect[0][1], refractive_index)

    print(f"depth at crossover point on segment 1: {depth_1} m")
    print(f"depth at crossover point on segment 2: {depth_2} m")
    print(f"crossover point lat-long: {intersection_points[0]}")

    posit = Twtt_Posit(layers[1], "2018_Antarctica_DC8", "20181030_01", intersection_indices)
    # create a Twtt_Posit object to store the crossover point data
    print(f"posit.layer_name: {posit.layer_name}")

    print("saving posit...")
    save_posit(posit)

    if plot_map:
        plot_layers_at_cross(layers, intersection_indices, intersection_points,zoom=False)


if __name__ == "__main__":
    main()

# TODO: now that everything is in the library file -> look at the plot_layers_at_cross function and see if the corrected
    # layer portion is something that should be its own function and if it needs to be part of the posit object that is
    # being saved.