"""
Author: Richard Moser
Description: This file is to be used to visualize the iceflow map in the file antarctic_ice_vel_phase_map_v01.nc which
comes from MEaSUREs Phase-Based Antarctica Ice Velocity Map, Version 1. This file is a netCDF file, which is a file
format that is used to store multidimensional data. This file contains the ice flow velocity data for Antarctica.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
from netCDF4 import Dataset
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from pyproj import Transformer
import pickle


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


def xy_to_lonlat(x, y):
    """
    This function is used to convert x and y coordinates to lat and lon coordinates.
    :param x: the x coordinate to convert
    :param y: the y coordinate to convert
    :return: the lat and lon coordinates
    # TODO: WHY ARE YOU THE WAY YOU ARE???
    """
    # converts Antarctic Polar Stereographic to standard lat-lon
    transformer = Transformer.from_crs("EPSG:3031", "EPSG:4326")
    point = transformer.transform(x, y)
    point = (point[0], 270 - point[1])  # I'm not sure why, but this is necessary to get the correct longitude
    if point[1] > 360:  # if the longitude is greater than 360, subtract 360
        point = (point[0], point[1] - 360)
    elif point[1] < 0:  # if the longitude is less than 0, add 360
        point = (point[0], point[1] + 360)
    return point


def lonlat_to_xy(lat, lon):
    """
    This function is used to convert lat and lon coordinates to x and y coordinates.
    :param lat: the latitude to convert
    :param lon: the longitude to convert
    :return: the x and y coordinates
    # TODO: WHY ARE YOU THE WAY YOU ARE???
    """
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:3031")  # standard lat-lon to Antarctic Polar Stereographic
    point = transformer.transform(lat, lon)
    point = (- int(point[1]), - int(point[0]))
    # ok this one you *REALLY* can't ask me why it is like this. If you don't do this, the lat and lon are flipped and
    # negative relative to the actual values. I don't like it either
    return point


def find_nearest_x_and_y(x, y, iceflow_data):
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
    """
    This function is used to find the flow at a given lat and lon.
    :param lat: the latitude to find the flow at
    :param lon: the longitude to find the flow at
    :param iceflow_data: the iceflow data in a readable format
    :return: the flow at a given lat and lon
    """
    x, y = lonlat_to_xy(lat, lon)
    print(f"x-y: {x, y}, lat-lon: {lat, lon}")
    x_index, y_index = find_nearest_x_and_y(x, y, iceflow_data)
    print(f"nearest x and y: {iceflow_data[0][x_index], iceflow_data[1][y_index]}")
    return iceflow_data[2][x_index][y_index], iceflow_data[3][x_index][y_index]


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


def find_nearest_unmasked_x_and_y(x, y, iceflow_data):
    """
    Find the nearest x and y value in the iceflow data to an input x and y value.
    If the ice velocity is masked at that point, it will return the next nearest point that is not masked.
    """
    x_index_base = (np.abs(iceflow_data[0] - x)).argmin()
    y_index_base = (np.abs(iceflow_data[1] - y)).argmin()

    for x_offset, y_offset in generate_spiral_indices(0, 0, max_radius=100):
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


def plot_spiral(x_center, y_center, max_radius=4):
    """
    use the generate_spiral_indices function to make a list of all the points in a spiral around a point within a radius of 100 around the center of the x and y values
    :param x_center: the center x value
    :param y_center: the center y value
    :param max_radius: the maximum radius of the spiral
    :return: None, but draws and saves a plot of the spiral to a file
    """
    spiral_indices = []
    for x_offset, y_offset in generate_spiral_indices(x_center, y_center, max_radius=max_radius):
        spiral_indices.append((x_offset, y_offset))
    # draw the spiral on a plot of x and y values with a line connecting the points and color the points by their index in the list
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