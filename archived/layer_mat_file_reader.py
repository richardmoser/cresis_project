
import numpy as np
import pickle
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from project_classes import Layer
from functions import *
# import mat73


# testing_mode = True # for use on a non OPR enabled machine without it's own files
testing_mode = False
# readout = True
readout = False
save = True
# save = False
# plot = True
plot_layer = False
plot_map = True
# plot_map = False

# season = "2018_Antarctica_DC8"
season = "2016_Antarctica_DC8"

# flight = "20181030_01"  # the flight date and frame number
# flight = "20181112_02"
flight = "20161024_05"


def main():
    mat_pickler_layerData(season, flight)


# def main():
#     print("Reading data files...")
#     print("--------------------")
#     # set the directory, segment data file, layer attributes file, and start and end frames
#     if testing_mode:
#         dir = ('test_data\\')
#         segment_data_file = 'Data_'+ flight + '_'
#         # contains all of the actual data such as twtt, lat, lon, etc.
#         layer_attributes_file = 'layer_' + flight + '.mat'
#         # contains the attributes of the layer such as name, param, etc.
#     else:
#         dir = ('C:\\Users\\rj\\Documents\\cresis\\rds\\' + season + '\\CSARP_layer\\' + flight + '\\')
#         segment_data_file = 'Data_' + flight + '_'
#         # contains all of the actual data such as twtt, lat, lon, etc.
#         layer_attributes_file = 'layer_' + flight + '.mat'
#         # contains the attributes of the layer such as name, param, etc.
#         print(f"layer_attributes_file: {layer_attributes_file}")
#         # contains the attributes of the layer such as name, param, etc.
#
#         # dir = C:\Users\rj\Documents\cresis\rds\2018_Antarctica_DC8\CSARP_layer\20181112_02
#         # dir = ('C:\\Users\\rj\\Documents\\cresis\\rds\\2018_Antarctica_DC8\\CSARP_layer\\20181112_02\\')
#         # segment_data_file = 'Data_20181112_02_'
#         # layer_attributes_file = 'layer_20181112_02.mat'
#
#     startframe = '001'
#     # endframe = '015'
#     # endframe = the number of files in the directory
#     files = os.listdir(dir)
#     endframe = str(len(files) - 1).zfill(3)
#
#     # load an array of mat files
#     data_mat = np.array([sio.loadmat(dir + segment_data_file + str(i).zfill(3) + '.mat')
#                          for i in range(int(startframe), int(endframe)+1)])
#     attribute_mat = sio.loadmat(dir + layer_attributes_file)
#
#     # data_mat = np.array([mat73.loadmat(dir + segment_data_file + str(i).zfill(3) + '.mat')
#     #                         for i in range(int(startframe), int(endframe)+1)])
#     # attribute_mat = mat73.loadmat(dir + layer_attributes_file)
#
#
#     # print the keys as strings without all the extra stuff
#     keys = [str(key).strip("_") for key in data_mat[0].keys()]
#     print(f"DATA MAT FILE KEYS:")
#     for key in keys:
#         print(key, end="")
#         # if not last key, print a comma
#         if key != keys[-1]:
#             print(",", end=" ")
#     # print("\n")
#     # print the keys in the layer attributes mat file
#     print(f"\nLAYER ATTRIBUTES MAT FILE KEYS:")
#     keys = [str(key).strip("_") for key in attribute_mat.keys()]
#     for key in keys:
#         print(key, end="")
#         # if not last key, print a comma
#         if key != keys[-1]:
#             print(",", end=" ")
#     print("\n--------------------\n")
#
#     layers = layerize(data_mat, attribute_mat)
#
#     if readout:
#         print("--------------------", end="")
#         for layer in layers:
#             print(f"\n{layer.layer_name} number of points: {layer.twtt.shape[0]}")
#             print(f"{layer.layer_name} twtt first three: {layer.twtt[:3].tolist()} ")
#             print(f"{layer.layer_name} twtt last three: {layer.twtt[-3:].tolist()} ")
#         print("--------------------\n")
#
#     if save:
#         # save layers to a pickle file
#         # print("Saving layers to a pickle file...")
#         print("--------------------")
#         # list current directory
#         # print(f"Current directory: {}")
#         file_name = "layer_export" + layer_attributes_file[5:-4] + ".pickle"
#         pickle.dump(layers, open(file_name, "wb"))
#         print(file_name, " saved in local directory of this python file.")
#         print("--------------------\n")
#
#     if plot_layer:
#         # plot the layers
#         print("Plotting layers...")
#         print("--------------------")
#     # plot the layer depths vs gps time for each layer on the same plot
#         for layer in layers:
#             plt.plot(layer.gps_time, layer.twtt, label=layer.layer_name)
#         plt.xlabel("GPS Time")
#         plt.ylabel("Two Way Travel Time (ns)")
#         plt.title("Elevation vs GPS Time")
#         plt.legend()
#
#         plt.show()
#         print("--------------------\n")
#
#     # TODO: make this selectable per season and date with the directory base and
#         # CSARP_layer file as hard-coded defaults
#     # TODO: add a pygame gui with recent files and a file browser
#         # save the recent files to a file and load them on startup
#     # TODO: organize all of this into a library or something similar
#
#     if plot_map:
#         # plot the lat-lon map for one of the layers in antarctica
#         print("Plotting lat-lon map...")
#         print("--------------------")
#         # plot the latitudes and longitudes for layers[0] on a basemap
#         plt.figure()
#         m = Basemap(projection='spstere', boundinglat=-70, lon_0=180, resolution='l')
#         m.drawcoastlines()
#         m.fillcontinents(color='grey', lake_color='aqua')
#         m.drawparallels(np.arange(-80., 81., 20.))
#         m.drawmeridians(np.arange(-180., 181., 20.))
#         m.drawmapboundary(fill_color='aqua')
#         # plot the flight path
#         m.plot(layers[0].lon, layers[0].lat, latlon=True, color='lightgreen', linewidth=1)
#         # plot the South Pole
#         m.scatter(0, -90, latlon=True, color='black', linewidth=1, label='South Pole')
#         x, y = m(0, -90)
#         plt.text(x, y, '\nSouth Pole', fontsize='smaller', fontweight='bold', ha='center', va='top', color='black')
#         plt.title("Lat-Lon Map")
#         plt.show()
#         print("--------------------\n")

if __name__ == "__main__":
    main()