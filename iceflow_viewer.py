"""
Author: Richard Moser
Description: This file is to be used to visualize the iceflow map in the file antarctic_ice_vel_phase_map_v01.nc which
comes from MEaSUREs Phase-Based Antarctica Ice Velocity Map, Version 1. This file is a netCDF file, which is a file
format that is used to store multidimensional data. This file contains the ice flow velocity data for Antarctica.
"""

import iceflow_library as iceflow


def main():
    """
    This function is the main function of the iceflow_viewer.py file.
    :return: None
    """
    # prep the iceflow data file. If the iceflow data pickle file does not exist, create it.
    try:
        iceflow_data = iceflow.iceflow_data_file_loader()
        print("The iceflow data pickle file was found and loaded.")
    except FileNotFoundError:
        print("The iceflow data pickle file was not found. Creating a new one...")
        filename = iceflow.iceflow_saver()
        iceflow_data = iceflow.iceflow_loader(filename)
        print("The iceflow data pickle file was successfully created.")

    print(f"Iceflow data array layout is x, y, velocity_x, velocity_y, latitude, longitude.")

    test = iceflow.find_nearest_x_and_y(-76, 165, iceflow_data)
    print(test)
    print(iceflow_data[2])



if __name__ == "__main__":
    main()

