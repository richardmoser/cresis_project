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


def find_nearest_x_and_y(lat, lon, iceflow_data):
    """
    This function is used to find the nearest x and y values to a given latitude and longitude.
    :param lat: the latitude
    :param lon: the longitude
    :return: the nearest x and y values from the iceflow data
    """
    x = iceflow_data[0]  # sets x to the first element of iceflow_data
    y = iceflow_data[1]  # sets y to the second element of iceflow_data
    latitude = iceflow_data[4] # sets latitude to the fifth element of iceflow_data. this is a 2d array
    longitude = iceflow_data[5]  # sets longitude to the sixth element of iceflow_data. this is a 2d array

    # find the difference between the given lat/lon and the lat/lon values in the data
    lat_diff = np.abs(latitude - lat)
    lon_diff = np.abs(longitude - lon)

    # find the index of the minimum difference
    lat_index = np.where(lat_diff == np.min(lat_diff))[0][0]
    lon_index = np.where(lon_diff == np.min(lon_diff))[0][0]
    nearest_lat = latitude[lat_index]
    nearest_lon = longitude[lon_index]
    # TODO: fix this. lat and lon are 2d arrays, so this is not going to work. updated the comments for latitude and
    #  longitude to reflect this. maybe just delete from line 90 on and let copilot regenerate it?

    # find the nearest x and y
    x_diff = np.abs(x - lon_index)  #
    y_diff = np.abs(y - lat_index)
    x_index = np.where(x_diff == np.min(x_diff))[0][0]
    y_index = np.where(y_diff == np.min(y_diff))[0][0]
    nearest_x = x[x_index]
    nearest_y = y[y_index]

    print(f"nearest_lat, nearest_lon: {nearest_lat}, {nearest_lon}")

    # calculate distance error
    distance_error = np.sqrt((nearest_lat - lat)**2 + (nearest_lon - lon)**2)

    return nearest_x, nearest_y , distance_error
