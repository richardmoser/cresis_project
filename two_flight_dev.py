import matplotlib.pyplot as plt
from project_classes import *
from functions import *
# from scipy.optimize import curve_fit
# import scipy.optimize as opt
#%%
zoom = True
seg_length = 500
# season = "2009_Antarctica_DC8"
season = "2018_Antarctica_DC8"
season = "2016_Antarctica_DC8"
# season = "2014_Antarctica_DC8"
season = "2022_Antarctica_BaslerMKB"

# flight = "20181030_01"  # the flight date and frame number
    # that flight only has one point
# flight = "20181018_01"
# flight = "20181103_01"
# flight = "20181011_01"
    # one dimensional data error
    # TODO: figure out why 10018 and 1103 have the same data or at least print the same maps and plots
# flight = "20181109_01"
# flight = "20181112_02"  # the problem flight
    # plots fake crossovers along the curved path
flight = "20161024_05"
# flight = "20161111_05"
    # probably too close to the coast to be useful
# flight = "20161024_05"
# flight = "20141026_06"
    # this one is 1/3 of an orbit and produces a bunch of bunk crossovers
# flight = "20230127_01"
    # ~ 1/3 of an orbit of the pole and yet the angle plot looks like hot garbage
flight = "20230108_01"
flight = "20221212_01"
flight = "20221228_01"

# file_name = "layer_export_" + flight + ".pickle"
dir = "C:\\Users\\moser\\Desktop\\cresis_project\\pickle_jar\\layer_export_"
file_name = dir + flight + ".pickle"
testing = False
#%%
"""
read in the layers from the layer files and save them to a pickle file
"""
force = False
# force = True
whole_season = False
whole_season = True

if whole_season:
    print(type(dir))
    file_name = dir + season + ".pickle"
    # print(f"filename: {filename}")
    if not os.path.isfile(file_name):  # if the file does not exist
        debug_print(BRIGHT_RED, f"File {file_name} does not exist. You should make it...")
    else:
        layers = read_layers(file_name)
        print(f"File {file_name} loaded.")
else:
    if not force:
        if not os.path.isfile(file_name):  # if the file does not exist
            print(f"File {file_name} does not exist. Making it...")
            mat_pickler_h5py(season, flight, testing_mode=testing)  # make it
            layers = read_layers(file_name)  # read in the layers from the pickle file
            print(f"File {file_name} created.")
        else:
            layers = read_layers(file_name)  # read in the layers from the pickle file
            print(f"File {file_name} loaded.")
    else:
        mat_pickler_h5py(season, flight, testing_mode=testing)  # make it
        layers = read_layers(file_name)  # read in the layers from the pickle file
#%% md
### read in the iceflow data from the iceflow data files and save them to a pickle file
#%%
if not os.path.isfile("C:\\Users\\moser\\Desktop\\cresis_project\\iceflow\\iceflow_data.pickle"):  # if the file does not exist
    print("The iceflow data pickle file was not found. Creating a new one...")
    filename = iceflow_saver()
    iceflow_data = iceflow_loader(filename)
    print("The iceflow data pickle file was successfully created.")
# try:
iceflow_data = iceflow_loader("C:\\Users\\moser\\Desktop\\cresis_project\\iceflow\\iceflow_data.pickle")
print("The iceflow data pickle file was found and loaded.")

x = iceflow_data[0]
y = iceflow_data[1]
velocity_x = iceflow_data[2]
velocity_y = iceflow_data[3]
latitude = iceflow_data[4]
longitude = iceflow_data[5]
print("iceflow data loaded")
#%%
# if the file at filename exists, read in the intersect_indices and intersection_points from the pickle file
# otherwise, find the intersect_indices and intersection_points and save them to a pickle file
force_redo_intersections = False
filename = f"C:\\Users\\moser\\Desktop\\cresis_project\\pickle_jar\\{season}_crossover_points.pickle"
if not os.path.isfile(filename) or force_redo_intersections:  # if the file does not exist
    print(f"File {filename} does not exist. Making it...")
    intersection_points, intersection_indices, segment_ends = cross_point(layers[0], seg_length, quiet=True, bar_len = 100)
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