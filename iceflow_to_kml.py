print("test")
#%%
import matplotlib.pyplot as plt

from project_classes import *
from functions import *
#%%
zoom = True
seg_length = 100
# season = "2009_Antarctica_DC8"
# season = "2018_Antarctica_DC8" # a layerData season
season = "2016_Antarctica_DC8" # a season with both layer and layerData
# season = "2014_Antarctica_DC8" # a layerData season
# flight = "20181030_01"  # the flight date and frame number
# flight = "20181018_01"
# flight = "20181103_01"
# flight = "20181109_01"
# flight = "20181112_02"  # the problem flight
flight = "20161024_05"
# flight = "20161111_05"
# flight = "20161024_05"
# flight = '20141026_06'
# file_name = "layer_export_" + flight + ".pickle"
file_name = "C:\\Users\\rj\\Documents\\cresis_project\\pickle_jar\\layer_export_" + flight + ".pickle"
testing = False
#%%
"""
read in the layers from the layer files and save them to a pickle file
"""
# mat_pickler_layer(season, flight, testing_mode=testing)  # make it
mat_pickler_h5py(season, flight, testing_mode=testing)  # make it
layers = read_layers(file_name)  # read in the layers from the pickle file

# TODO: figure out the difference in file structure between the h5py and sio based pickler outputs
#%% md
### read in the iceflow data from the iceflow data files and save them to a pickle file
#%%
if not os.path.isfile("C:\\Users\\rj\\Documents\\cresis_project\\iceflow\\iceflow_data.pickle"):  # if the file does not exist
    print("The iceflow data pickle file was not found. Creating a new one...")
    filename = iceflow_saver()
    iceflow_data = iceflow_loader(filename)
    print("The iceflow data pickle file was successfully created.")
# try:
iceflow_data = iceflow_loader("C:\\Users\\rj\\Documents\\cresis_project\\iceflow\\iceflow_data.pickle")
print("The iceflow data pickle file was found and loaded.")

x = iceflow_data[0]
y = iceflow_data[1]
velocity_x = iceflow_data[2]
velocity_y = iceflow_data[3]
latitude = iceflow_data[4]
longitude = iceflow_data[5]
#%%
# if the file at filename exists, read in the intersection_indices and intersection_points from the pickle file
# otherwise, find the intersection_indices and intersection_points and save them to a pickle file
filename = f"C:\\Users\\rj\\Documents\\cresis_project\\pickle_jar\\{season}_{flight}_crossover_points.pickle"
if not os.path.isfile(filename):  # if the file does not exist
    print(f"File {filename} does not exist. Making it...")
    intersection_points, intersection_indices, segment_ends = cross_point(layers[0], seg_length, quiet=True)
    with open(filename, 'wb') as file:
        pickle.dump(intersection_indices, file)
        pickle.dump(intersection_points, file)
        pickle.dump(segment_ends, file)
    print(f"intersection_indices and intersection_points saved to {filename}")
else:
    with open(filename, 'rb') as file:
        intersection_indices = pickle.load(file)
        intersection_points = pickle.load(file)
        segment_ends = pickle.load(file)
    print(f"intersection_indices and intersection_points loaded from {filename}")
#%%
# TODO: deconstruct the nested lists and make them make more sense
    # put them in class objects?

# print(f"intersection_indices: {intersection_indices}")
# print(f"intersection_points: {intersection_points}")
#%%
"""Start conversion dev 26Jun24"""
#%%
i = 0
# cross_lat = intersection_points[i][0]
# cross_lon = intersection_points[i][1]


import random
# x and y are randomly selected from the range of the iceflow data
cross_x = random.uniform(min(x) * 0.2, max(x) * 0.2)
cross_y = random.uniform(min(y) * 0.2, max(y) * 0.2)

cross_x = -479569.5607
cross_y = 839579.5925
# cross_x: -479569.5607, cross_y: 839579.5925


print(f"\n\nrandomly selected cross_x: {cross_x}, cross_y: {cross_y}")

cross_lat, cross_lon = xy_to_latlon(cross_x, cross_y)
print(f"calculated cross_lat: {cross_lat}, cross_lon: {cross_lon} (from random cross_x and cross_y)")
print(section_break + "\n" + section_break)

cross_x, cross_y = latlon_to_xy(cross_lat, cross_lon)
# print(f"type(cross_x): {type(cross_x)}, type(cross_y): {type(cross_y)}")
print(f"cross_x: {cross_x:.4f}, cross_y: {cross_y:.4f} (from cross_lat and cross_lon)")
print(section_break)

# nearest_y_index, nearest_x_index = latlon_to_nearest_unmasked_index(cross_lat, cross_lon, iceflow_data, max_radius=10)
nearest_x_index, nearest_y_index = latlon_to_nearest_unmasked_index(cross_lat, cross_lon, iceflow_data, max_radius=10)

print(f"nearest_x_index: {nearest_x_index}, nearest_y_index: {nearest_y_index}")

print(f"flow at cross_x: {velocity_x[nearest_y_index, nearest_x_index]}, flow at cross_y: {velocity_y[nearest_y_index, nearest_x_index]}")