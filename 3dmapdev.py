import matplotlib.pyplot as plt
import os
from project_classes import *
from functions import *
from iceflow_library import *
from scipy.optimize import curve_fit
import scipy.optimize as opt


zoom = True
seg_length = 100
# season = "2009_Antarctica_DC8"
season = "2018_Antarctica_DC8"
season = "2016_Antarctica_DC8"
# season = "2014_Antarctica_DC8"
# season = "2022_Antarctica_BaslerMKB"

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
# flight = "20161024_05"
# flight = "20161111_05"
# probably too close to the coast to be useful
flight = "20161024_05"
# flight = "20141026_06"
# flight = "20230127_01"
# ~ 1/3 of an orbit of the pole and yet the angle plot looks like hot garbage
# file_name = "layer_export_" + flight + ".pickle"
file_name = "C:\\Users\\rj\\Documents\\cresis_project\\pickle_jar\\layer_export_" + flight + ".pickle"
testing = False

"""
read in the layers from the layer files and save them to a pickle file
"""
# mat_pickler_layer(season, flight, testing_mode=testing)  # make it
# if the file at filename exists, read in the layers from the pickle file

if not os.path.isfile(file_name):  # if the file does not exist
    print(f"File {file_name} does not exist. Making it...")
    mat_pickler_h5py(season, flight, testing_mode=testing)  # make it
    layers = read_layers(file_name)  # read in the layers from the pickle file
    print(f"File {file_name} created.")
else:
    layers = read_layers(file_name)  # read in the layers from the pickle file
    print(f"File {file_name} loaded.")

# mat_pickler_h5py(season, flight, testing_mode=testing)  # make it
# layers = read_layers(file_name)  # read in the layers from the pickle file

### read in the iceflow data from the iceflow data files and save them to a pickle file

if not os.path.isfile(
        "C:\\Users\\rj\\Documents\\cresis_project\\pickle_jar\\iceflow_data.pickle"):  # if the file does not exist
    print("The iceflow data pickle file was not found. Creating a new one...")
    filename = iceflow_saver()
    iceflow_data = iceflow_loader(filename)
    print("The iceflow data pickle file was successfully created.")
# try:
iceflow_data = iceflow_loader("C:\\Users\\rj\\Documents\\cresis_project\\pickle_jar\\iceflow_data.pickle")
print("The iceflow data pickle file was found and loaded.")

x = iceflow_data[0]
y = iceflow_data[1]
velocity_x = iceflow_data[2]
velocity_y = iceflow_data[3]
latitude = iceflow_data[4]
longitude = iceflow_data[5]
print("iceflow data loaded")

# if the file at filename exists, read in the intersect_indices and intersection_points from the pickle file
# otherwise, find the intersect_indices and intersection_points and save them to a pickle file
filename = f"C:\\Users\\rj\\Documents\\cresis_project\\pickle_jar\\{season}_{flight}_crossover_points.pickle"
if not os.path.isfile(filename):  # if the file does not exist
    # print(f"File {filename} does not exist. Making it...")
    intersection_points, intersection_indices, segment_ends = cross_point(layers[0], seg_length, quiet=True)
    with open(filename, 'wb') as file:
        pickle.dump(intersection_indices, file)
        pickle.dump(intersection_points, file)
        pickle.dump(segment_ends, file)
    # print(f"intersection_indices and intersection_points saved to {filename}")
else:
    with open(filename, 'rb') as file:
        intersection_indices = pickle.load(file)
        intersection_points = pickle.load(file)
        segment_ends = pickle.load(file)
    # print(f"intersection_indices and intersection_points loaded from {filename}")



def plot_layers_3d(layers, season, flight, intersect_indices, seg_ends):
    # plot the layers with respect to lat, lon, and twtt
    # plot a grid of scattered points at 0 twtt to represent the surface

    # convert the lat-lon points to xy points
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    plot_all = False
    plot_all = True
    plot_surface = False

    for layer in layers:
        corrected_twtt = layer.twtt - layers[0].twtt  # normalize against the surface layer
        # corrected_twtt = layer.twtt
        layer.twtt_corrected = corrected_twtt

    # for point in layers[0].twtt_corrected:
        # if point != 0:
            # print(f"point: {point} is not 0. Hopefully it is nan.")

    # if a twtt is nan, remove it from the list of indices
    for i in range(len(layers[0].twtt_corrected)):
        if np.isnan(layers[0].twtt_corrected[i]):
            print(f"nan found at index {i}")
            intersect_indices = np.delete(intersect_indices, i, 0)

    lats_bottom = []
    lons_bottom = []
    twtts_bottom = []
    lats_surf = []
    lons_surf = []
    twtts_surf = []

    for i in range(len(layers[1].lat)):
        lats_bottom.append(layers[1].lat[i])
        lons_bottom.append(layers[1].lon[i])
        twtts_bottom.append(layers[1].twtt_corrected[i])
        # twtts1.append(layers[1].twtt[i])

    for i in range(len(layers[0].lat)):
        lats_surf.append(layers[0].lat[i])
        lons_surf.append(layers[0].lon[i])
        twtts_surf.append(layers[0].twtt_corrected[i])
        # twtts2.append(layers[0].twtt[i])

    # offset = 250
    offset = 25

    # i = 0
    for i in range(len(intersect_indices) - 1):
        if plot_surface:
            # plot the surface layer (layer 0)
            ax.plot(lons_surf[intersect_indices[i][0] - offset:intersect_indices[i][0] + offset],
                    lats_surf[intersect_indices[i][0] - offset:intersect_indices[i][0] + offset],
                    [-x for x in (twtts_surf[intersect_indices[i][0] - offset:intersect_indices[i][0] + offset])],
                    label='top. seg. 1', c='blue',
                    linewidth=1)

            ax.plot(lons_surf[intersect_indices[i][1] - offset:intersect_indices[i][1] + offset],
                    lats_surf[intersect_indices[i][1] - offset:intersect_indices[i][1] + offset],
                    [-x for x in (twtts_surf[intersect_indices[i][1] - offset:intersect_indices[i][1] + offset])],
                    label='top seg. 2', c='black',
                    linewidth=1)

            # draw a line from one end of the segment to the other in blue
            # Define the slice range
            start_index = intersect_indices[i][0] - offset
            end_index = intersect_indices[i][0] + offset

            # Extract the sliced arrays
            lons2_slice = lons_surf[start_index:end_index]
            lats2_slice = lats_surf[start_index:end_index]
            twtts2_slice = [-x for x in twtts_surf[start_index:end_index]]

            # plot the distance in meters between the first and last point
            # get the distance in meters between the first and last point
            # distance = latlon_dist([lats2_slice[0], lons2_slice[0]], [lats2_slice[-1], lons2_slice[-1]])
            # plot the distance in meters to the first decimal between the first and last point
            # ax.text((lons2_slice[0]), (lats2_slice[0]),
            #         (max(twtts2_slice[0], twtts2_slice[-1])), f"{distance:.1f}m", color='blue')

        start_index_seg1 = intersect_indices[i][1] - offset
        end_index_seg2 = intersect_indices[i][1] + offset

        start_index_seg2 = intersect_indices[i][0] - offset
        end_index_seg1 = intersect_indices[i][0] + offset

    # plot the bottom layer (layer 1)
    # ax.plot(lons_bottom[intersect_indices[i][0] - offset:intersect_indices[i][0] + offset],
    #         lats_bottom[intersect_indices[i][0] - offset:intersect_indices[i][0] + offset],
    #         [-x for x in (twtts_bottom[intersect_indices[i][0] - offset:intersect_indices[i][0] + offset])],
    #         label='bott. seg. 1', c='orange',
    #         linewidth=1)
    #
    # ax.plot(lons_bottom[intersect_indices[i][1] - offset:intersect_indices[i][1] + offset],
    #         lats_bottom[intersect_indices[i][1] - offset:intersect_indices[i][1] + offset],
    #         [-x for x in (twtts_bottom[intersect_indices[i][1] - offset:intersect_indices[i][1] + offset])],
    #         label='bott. seg. 2', c='green',
    #         linewidth=1)

        ax.plot(lats_bottom[start_index_seg1:end_index_seg2],
                lons_bottom[start_index_seg1:end_index_seg2],
                [-x for x in twtts_bottom[start_index_seg1:end_index_seg2]],
                label='bott. seg. 2', c='green', linewidth=1)

        ax.plot(lats_bottom[start_index_seg2:end_index_seg1],
                lons_bottom[start_index_seg2:end_index_seg1],
                [-x for x in twtts_bottom[start_index_seg2:end_index_seg1]],
                label='bott. seg. 1', c='orange', linewidth=1)

    if plot_all:
        # plot the rest of the bottom layer
        ax.plot(lats_bottom[intersect_indices[0][0] - offset:intersect_indices[0][1] + offset],
                lons_bottom[intersect_indices[0][0] - offset:intersect_indices[0][1] + offset],
                [-x for x in (twtts_bottom[intersect_indices[0][0] - offset:intersect_indices[0][1] + offset])],
                label='whole bottom', c='purple',
                linewidth=0.25)

        # plot the rest of the surface layer
        ax.plot(lats_surf[intersect_indices[0][0] - offset:intersect_indices[0][1] + offset],
                lons_surf[intersect_indices[0][0] - offset:intersect_indices[0][1] + offset],
                [-x for x in (twtts_surf[intersect_indices[0][0] - offset:intersect_indices[0][1] + offset])],
                label='whole surface', c='grey',
                linewidth=0.25)

    # plot the intersection points
    # i = 0
    for i in range(len(intersect_indices) - 1):
        ax.scatter(layers[1].lat[intersect_indices[i][0]],
                   layers[1].lon[intersect_indices[i][0]],
                   -1 * layers[1].twtt_corrected[intersect_indices[i][0]], c='red', marker='o')
        ax.scatter(layers[1].lat[intersect_indices[i][1]],
                   layers[1].lon[intersect_indices[i][1]],
                   -1 * layers[1].twtt_corrected[intersect_indices[i][1]], c='green', marker='o')
        ax.text(layers[1].lat[intersect_indices[i][0]],
                layers[1].lon[intersect_indices[i][0]],
                -1 * layers[1].twtt_corrected[intersect_indices[i][0]],
                f"cross {i}", color='red')
        ax.text(layers[1].lat[intersect_indices[i][1]],
                layers[1].lon[intersect_indices[i][1]],
                -1 * layers[1].twtt_corrected[intersect_indices[i][1]],
                f"cross {i}", color='green')

        # plot the horizontal distance between the two points
        # get the distance in meters between the first and last point
        distance = latlon_dist([layers[1].lat[intersect_indices[i][0]], layers[1].lon[intersect_indices[i][0]]],
                               [layers[1].lat[intersect_indices[i][1]], layers[1].lon[intersect_indices[i][1]]])
        # plot the distance in meters to the first decimal between the first and last point
        ax.text(layers[1].lat[intersect_indices[i][0]], layers[1].lon[intersect_indices[i][0]],
                -1 * layers[1].twtt_corrected[intersect_indices[i][0]],
                f"{distance:.1f}m", color='blue')

        # plot the vertical distance between the two points
        # get the distance in meters between the first and last point
        depth_1 = twtt_to_depth(layers[1].twtt_corrected[intersect_indices[i][0]])
        depth_2 = twtt_to_depth(layers[1].twtt_corrected[intersect_indices[i][1]])
        depth_diff = abs(depth_1 - depth_2)
        # plot the distance in meters to the first decimal between the first and last point
        ax.text(layers[1].lat[intersect_indices[i][0]], layers[1].lon[intersect_indices[i][0]],
                -1 * layers[1].twtt_corrected[intersect_indices[i][0]],
                f"{depth_diff:.1f}m", color='red')



    ax.set_xlabel('Latitude')
    ax.set_ylabel('Longitude')
    ax.set_zlabel('TWTT')
    # plot the twtt converted to depth on the other side of the plot
    # ax2 = ax.twinx()


    plt.show()


plot_layers_3d(layers, season, flight, intersection_indices, segment_ends)