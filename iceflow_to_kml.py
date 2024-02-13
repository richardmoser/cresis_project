import simplekml
from project_classes import *
from functions import *
from iceflow_library import *


try:
    iceflow_data = iceflow_loader("iceflow_data.pickle")
    print("The iceflow data pickle file was found and loaded.")
except FileNotFoundError:
    print("The iceflow data pickle file was not found. Creating a new one...")
    filename = iceflow_saver()
    iceflow_data = iceflow_loader(filename)
    print("The iceflow data pickle file was successfully created.")

def iceflow_to_kml(iceflow_data):
    """
    Save the iceflow data points to a kml file for use in Google Earth. Each individual point should be saved with a description which includes the x and y indices and the x and y values at those indices.
    """
    # create a kml file
    kml = simplekml.Kml()
    # iterate through the iceflow data and add each point to the kml file
    for x_index in range(iceflow_data[2].shape[0]):
        for y_index in range(iceflow_data[2].shape[1]):
            # add a point to the kml file
            point = kml.newpoint(name=f"({x_index}, {y_index})",
                                 coords=[(iceflow_data[4][x_index][y_index], iceflow_data[5][x_index][y_index])])
            # add a description to the point
            point.description = (
                f"x index: {x_index}, y index: {y_index}\nx: {iceflow_data[0][x_index]}, y: {iceflow_data[1][y_index]}"
                f"\nlat: {iceflow_data[4][x_index][y_index]}, lon: {iceflow_data[5][x_index][y_index]}")
        if x_index % 100 == 0:
            print(f"{x_index} of {iceflow_data[2].shape[0]}")
    # save the kml file
    kml.save("iceflow_data.kml")


iceflow_to_kml(iceflow_data)