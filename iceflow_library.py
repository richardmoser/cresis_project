"""
Author: Richard Moser
Description: This file is to be used to visualize the iceflow map in the file antarctic_ice_vel_phase_map_v01.nc which
comes from MEaSUREs Phase-Based Antarctica Ice Velocity Map, Version 1. This file is a netCDF file, which is a file
format that is used to store multidimensional data. This file contains the ice flow velocity data for Antarctica.
"""

import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from pyproj import Transformer
import pickle
import pyproj
import math

def iceflow_data_file_loader():
    """
    This function is used to visualize the iceflow map in the file antarctic_ice_vel_phase_map_v01.nc which comes from
    MEaSUREs Phase-Based Antarctica Ice Velocity Map, Version 1. This file is a netCDF file, which is a file format
    that is used to store multidimensional data. This file contains the ice flow velocity data for Antarctica.
    :return: the iceflow data in a readable format
    """
    iceflow_file = Dataset("C:\\Users\\rj\\Documents\\cresis\\iceflow\\antarctic_ice_vel_phase_map_v01.nc", "r")

    # print(iceflow_file.variables.keys())
    # print()

    # print the coordinate system
    # print(iceflow_file.variables['coord_system'])

    # get the data
    x = iceflow_file.variables['x'][:]
    y = iceflow_file.variables['y'][:]
    velocity_x = iceflow_file.variables['VX'][:]
    velocity_y = iceflow_file.variables['VY'][:]
    latitude = iceflow_file.variables['lat'][:]
    longitude = iceflow_file.variables['lon'][:]

    return x, y, velocity_x, velocity_y, latitude, longitude


def iceflow_saver():
    """
    This function is used to save the iceflow data to a pickle file.
    :return: the file name of the pickle file that the iceflow data was saved to
    """
    x, y, velocity_x, velocity_y, latitude, longitude = iceflow_data_file_loader()
    iceflow_data = [x, y, velocity_x, velocity_y, latitude, longitude]

    pickle_file_name = "iceflow_data.pickle"
    pickle_file = open(pickle_file_name, "wb")
    pickle.dump(iceflow_data, pickle_file)
    pickle_file.close()

    return pickle_file_name


def iceflow_loader(pickle_file_name):
    """
    This function is used to load the iceflow data from a pickle file.
    :param pickle_file_name: the name of the pickle file that the iceflow data was saved to
    :return: the iceflow data in a readable format
    """
    pickle_file = open(pickle_file_name, "rb")
    iceflow_data = pickle.load(pickle_file)
    pickle_file.close()

    return iceflow_data


def get_iceflow_data(printout=True):
    """/
    for loading the data into crossover programs and similar
    :return: the data
    """
    try:
        iceflow_data = iceflow_data_file_loader()
        if printout:
            print("The iceflow data pickle file was found and loaded.")
    except FileNotFoundError:
        print("The iceflow data pickle file was not found. Creating a new one...")
        filename = iceflow_saver()
        iceflow_data = iceflow_loader(filename)
        print("The iceflow data pickle file was successfully created.")

    if printout:
        print("Iceflow data array layout is 0:x, 1:y, 2:v_x, 3:v_y, 4:latitude, 5:longitude")

    return iceflow_data


def x_to_index(x):
    return 6223 + int(x/450)


def y_to_index(y):
    return 6223 - int(y/450)


def index_to_x(x):
    return (x - 6223) * 450


def index_to_y(y):
    return (6223 - y) * 450


def xyindex_to_latlon(x, y, iceflow_data=get_iceflow_data(printout=False)):
    # TODO: make sure this uses the appropriate xy or x_index and y_index system
        # I think it is using indices and not points contrary to the description
    """
    This function is used to convert x and y coordinates to lat and lon coordinates.
    :param x: NOT THE X INDEX! the x coordinate to convert
    :param y: NOT THE Y INDEX! the y coordinate to convert
    :param iceflow_data: the iceflow data in a readable format
    :return: the lat and lon coordinates
    # TODO: WHY ARE YOU THE WAY YOU ARE???
    """
    # return iceflow_data[4][x][y], iceflow_data[5][x][y] # I don't remember why I added this.
        # It was uncommented and everything else was commented out. Started working once I switched it back

    transformer = Transformer.from_crs("EPSG:3031", "EPSG:4326", accuracy=10)
        # transform Antarctic Polar Stereographic to standard lat-lon
    point = transformer.transform(x, y, errcheck=True)
    point = (point[0], 270 - point[1])  # I'm not sure why, but this is necessary to get the correct longitude
    if point[1] > 360:  # if the longitude is greater than 360, subtract 360
        point = (point[0], point[1] - 360)
    elif point[1] > 0: # if the longitude is greater than 0, subtract 360
        point = (point[0], point[1] - 360)
    return point


def latlon_to_xy(lat, lon):
    """
    This function is used to convert lat and lon coordinates to x and y coordinates.
    :param lon: the longitude to convert
    :param lat: the latitude to convert
    :return: the x and y coordinates
    # TODO: WHY ARE YOU THE WAY YOU ARE???
    """
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:3031", accuracy=10)
    # transform standard lat-lon to Antarctic Polar Stereographic
    # point = transformer.transform(lat, lon, errcheck=True)
    point = transformer.transform(lat, lon, errcheck=True)
    # print(point)
    point = (- int(point[1]), - int(point[0]))
    # ok this one you *REALLY* can't ask me why it is like this. If you don't do this, the lat and lon are flipped and
    # negative relative to the actual values. I don't like it either.
    # print(f"lat-lon: {lat, lon}\nx-y: {point}")
    return point


def xyindex_vector_to_heading(x_index, y_index, x_vector, y_vector):
    """
    This function is used to convert an x and y vector in EPSG:3031 to a heading in EPSG:4326.
    :param x_index: the x coordinate
    :param y_index: the y coordinate
    :param x_vector: the x vector
    :param y_vector: the y vector
    :return: the heading in EPSG:4326
    """
    x, y = index_to_x(x_index), index_to_y(y_index)
    # convert the x and y coordinates to lat and lon
    lat, lon = xyindex_to_latlon(x_index, y_index)
    # convert the x and y vector to lat and lon
    lat_vector, lon_vector = xyindex_to_latlon(x + x_vector, y + y_vector)
    # calculate the heading
    geodesic = pyproj.Geod(ellps='WGS84')
    angle1, angle2, distance = geodesic.inv(lon, lat, lon_vector, lat_vector)
    return angle1, angle2, distance

    # # convert the x and y coordinates to lat and lon
    # lat, lon = xyindex_to_latlon(x_index, y_index)
    # # convert the x and y vector to lat and lon
    # lat_vector, lon_vector = xyindex_to_latlon(x_index + x_vector, y_index + y_vector)
    # # calculate the heading
    # geodesic = pyproj.Geod(ellps='WGS84')
    # angle1, angle2, distance = geodesic.inv(lon, lat, lon_vector, lat_vector)
    # return angle1, angle2, distance


def find_nearest_x_and_y(x, y, iceflow_data):
    # TODO: make sure this uses the appropriate xy or x_index and y_index system
    """
    This function is used to find the nearest x and y value in the iceflow data to an input x and y value.
    :param x: the x value to find the nearest x value to
    :param y: the y value to find the nearest y value to
    :param iceflow_data: the iceflow data in a readable format
    :return: the nearest x and y value in the iceflow data to an input x and y value
    """
    x_index = (np.abs(iceflow_data[0] - x)).argmin()
    y_index = (np.abs(iceflow_data[1] - y)).argmin()

    return x_index, y_index


def flow_at_lat_lon(lat, lon, iceflow_data):
    # TODO: make this incorporate the find_nearest_x_and_y function and the depracated_find_nearest_unmasked_x_and_y function
    """
    This function is used to find the flow at a given lat and lon.
    :param lat: the latitude to find the flow at
    :param lon: the longitude to find the flow at
    :param iceflow_data: the iceflow data in a readable format
    :return: the flow at a given lat and lon
    """
    x, y = latlon_to_xy(lon, lat)
    print(f"x-y: {x, y}, lat-lon: {lat, lon}")
    x_index, y_index = find_nearest_x_and_y(x, y, iceflow_data)
    print(f"nearest x and y: {iceflow_data[0][x_index], iceflow_data[1][y_index]}")
    return iceflow_data[2][x_index][y_index], iceflow_data[3][x_index][y_index]


def flow_at_x_y(x, y, iceflow_data):
    """
    This function is used to find the flow at a given x and y.
    :param x: the x value to find the flow at
    :param y: the y value to find the flow at
    :param iceflow_data: the iceflow data in a readable format
    :return: the flow at a given x and y
    """
    # x_index, y_index = depracated_find_nearest_unmasked_x_and_y(x, y, iceflow_data)
    return iceflow_data[2][x][y], iceflow_data[3][x][y]


def generate_spiral_indices(center_x, center_y, max_radius):
    """
    Generate indices in a spiral pattern around a center point.
    """
    x, y = center_x, center_y
    yield x, y

    x -= 1
    y -= 1

    for radius in range(1, max_radius + 1):
        for _ in range(radius * 2):
            x += 1
            yield x, y
        for _ in range(radius * 2):
            y += 1
            yield x, y
        for _ in range(radius * 2):
            x -= 1
            yield x, y
        for _ in range(radius * 2):
            y -= 1
            yield x, y

        # Move back to the starting point of the next quadrant
        x -= 1
        y -= 1
        yield x, y


def xy_to_nearest_unmasked_index(x, y, iceflow_data, max_radius=10, printout=False):
    """
    Find the nearest x and y value in the iceflow data to an input x and y value.
    :param x: the x value to find the nearest x value to
    :param y: the y value to find the nearest y value to
    :param iceflow_data: the iceflow data
    :param max_radius: the maximum radius to search for an unmasked point
    :param printout: whether or not to print the nearest unmasked point
    :return: the nearest unmasked x and y value in the iceflow data to an input x and y value
    """
    x = x_to_index(x)  # convert the x value to an index
    y = y_to_index(y)  # convert the y value to an index
    unmasked = []  # a list to store the unmasked x and y values
    for x_iterator in range(x - max_radius, x + max_radius):  # iterate through the x values within the max_radius
        for y_iterator in range(y - max_radius, y + max_radius):  # iterate through the y values within the max_radius
            if (
                    0 <= x_iterator < iceflow_data[2].shape[
                0]  # if the x index is within the bounds of the iceflow data
                    and 0 <= y_iterator < iceflow_data[2].shape[1]
                    and not np.ma.is_masked(iceflow_data[2][x_iterator][y_iterator])
                    and not np.ma.is_masked(iceflow_data[3][x_iterator][y_iterator])
            ):  # if the x and y values are unmasked
                unmasked.append((x_iterator, y_iterator))  # append the x and y values to the unmasked list
            if printout and not np.ma.is_masked(iceflow_data[2][x_iterator][y_iterator]):
                print(f"unmasked x: {x_iterator}, unmasked y: {y_iterator}")
                print(
                    f"unmasked lat: {iceflow_data[4][x_iterator][y_iterator]}, unmasked lon: {iceflow_data[5][x_iterator][y_iterator]}")
                print(
                    f"unmasked flow: {iceflow_data[2][x_iterator][y_iterator]}, {iceflow_data[3][x_iterator][y_iterator]}")
    # find the xy pair with the minimum distance from the input x and y
    min_distance = 100
    min_x = None
    min_y = None
    for x_iterator, y_iterator in unmasked:
        distance = math.sqrt((x - x_iterator) ** 2 + (y - y_iterator) ** 2)
        if distance < min_distance:
            min_distance = distance
            min_x = x_iterator
            min_y = y_iterator

    # print(f"latlon of nearest unmasked: {iceflow_data[4][min_x][min_y], iceflow_data[5][min_x][min_y]}")
    return min_x, min_y


def depracated_find_nearest_unmasked_x_and_y(x, y, iceflow_data, max_radius=100):
    #TODO: fix this because it doesn't seem to be returning good data
        # or abandon it because xy_to_nearest_unmasked_index() seems to work
    """
    Find the nearest x and y value in the iceflow data to an input x and y value.
    If the ice velocity is masked at that point, it will return the next nearest point that is not masked.
    """

    # x_index_base = (np.abs(iceflow_data[0] - x)).argmin()
    # y_index_base = (np.abs(iceflow_data[1] - y)).argmin()
    x_index = x_to_index(x)
    y_index = y_to_index(y)
    x_index_base = (np.abs(iceflow_data[0] - x_index)).argmin()
    y_index_base = (np.abs(iceflow_data[1] - y_index)).argmin()

    for x_offset, y_offset in generate_spiral_indices(0, 0, max_radius=max_radius):
    # for x_offset, y_offset in generate_spiral_indices(x_index_base, y_index_base, max_radius=max_radius):
        x_index = x_index_base + x_offset
        y_index = y_index_base + y_offset

        if (
                0 <= x_index < iceflow_data[2].shape[0]
                and 0 <= y_index < iceflow_data[2].shape[1]
                and not np.ma.is_masked(iceflow_data[2][x_index][y_index])
                and not np.ma.is_masked(iceflow_data[3][x_index][y_index])
        ):
            return x_index, y_index

    # Return the original indices if no unmasked point is found in the search area
    return x_index_base, y_index_base


def nearest_flow_to_latlon(lat, lon, iceflow_data, print_point=False):
    """
    :param lat: the latitude of the point
    :param lon: the longitude of the point
    :param iceflow_data: the iceflow data
    :param print_point: whether or not to print the nearest point to the lat-lon point
    :return: the nearest flow vector to the lat-lon point available in the iceflow data
    """
    # TODO: update to use the xy_to_nearest_unmasked_index function
    # find the nearest x and y values in the iceflow data
    x, y = latlon_to_xy(lat, lon)
    # x, y = depracated_find_nearest_unmasked_x_and_y(x, y, iceflow_data, max_radius=1000)
    x_index, y_index = xy_to_nearest_unmasked_index(x, y, iceflow_data, max_radius=1000)
    if print_point:
        print(f"Nearest point to lat-lon: {xyindex_to_latlon(x_index, y_index)}")
    flow = flow_at_x_y(x, y, iceflow_data)
    return flow


def plot_spiral(x_center, y_center, max_radius=4):
    """
    use the generate_spiral_indices function to make a list of all the points in a spiral around a point within a
    radius of max_radius around the center point
    :param x_center: the center x value
    :param y_center: the center y value
    :param max_radius: the maximum radius of the spiral
    :return: None, but draws and saves a plot of the spiral to a file
    """
    spiral_indices = []
    for x_offset, y_offset in generate_spiral_indices(x_center, y_center, max_radius=max_radius):
        spiral_indices.append((x_offset, y_offset))
    # draw the spiral on a plot of x and y values with a line connecting the points and color the points by their
    # index in the list
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(1, 1, 1)
    ax.set_title('Spiral')
    ax.set_xlabel('x')
    ax.set_ylabel('y')

    x_values = []
    y_values = []
    for x_offset, y_offset in spiral_indices:
        x_values.append(x_offset)
        y_values.append(y_offset)

    ax.scatter(x_values, y_values, c=range(len(x_values)), cmap='hot')
    ax.plot(x_values, y_values, '-')
    # show a color legend
    cbar = plt.colorbar(ax.scatter(x_values, y_values, c=range(len(x_values)), cmap='spring'))
    cbar.set_label('Index in Spiral')

    # label the points with a slight offset from the point
    for i, (x, y) in enumerate(zip(x_values, y_values)):
        ax.annotate(i, (x, y), xytext=(x + 0.1, y + 0.1))

    # label the first point with a star
    ax.annotate('start', (x_values[0], y_values[0]), xytext=(x_values[0] - 0.2, y_values[0] - 0.2))
    plt.show()
    # save the figure to a file with specified dpi
    fig.savefig('spiral.png', dpi=300)
