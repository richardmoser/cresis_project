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


def iceflow_viewer():
    """
    This function is used to visualize the iceflow map in the file antarctic_ice_vel_phase_map_v01.nc which comes from
    MEaSUREs Phase-Based Antarctica Ice Velocity Map, Version 1. This file is a netCDF file, which is a file format
    that is used to store multidimensional data. This file contains the ice flow velocity data for Antarctica.
    :return: None
    """

    # Read in the netCDF file
    iceflow_file = Dataset("C:\\Users\\rj\\Documents\\cresis\\iceflow\\antarctic_ice_vel_phase_map_v01.nc", "r")

    # the dictionary keys are ['coord_system', 'x', 'y', 'lat', 'lon', 'VX', 'VY', 'STDX', 'STDY', 'ERRX', 'ERRY', 'CNT', 'SOURCE']
    print(iceflow_file.variables.keys())

    # print the coordinate system
    print(iceflow_file.variables['coord_system'])
    # it outputs coord_system()
    #     ellipsoid: WGS84
    #     false_easting: 0.0
    #     false_northing: 0.0
    #     grid_mapping_name: polar_stereographic
    #     longitude_of_projection_origin: 0.0
    #     latitude_of_projection_origin: -90.0
    #     standard_parallel: -71.0
    #     straight_vertical_longitude_from_pole: 0.0
    # unlimited dimensions:
    # current shape = ()
    # filling on, default _FillValue of   used

    # plot the ice flow velocity data
    # first, get the data
    vx = iceflow_file.variables['VX'][:]
    vy = iceflow_file.variables['VY'][:]
    lat = iceflow_file.variables['lat'][:]
    lon = iceflow_file.variables['lon'][:]

    print(len(lat))



if __name__ == "__main__":
    iceflow_viewer()

