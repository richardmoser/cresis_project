
# purpose: print the headings for the data in the mat file layer_20181030_01.mat located at
# C:\Users\rj\Documents\cresis\rds\2018_Antarctica_DC8\CSARP_layer\20181030_01

import scipy.io as sio
import numpy as np
import pickle
import matplotlib.pyplot as plt
import matplotlib as mpl
import mpl_toolkits
# from mpl_toolkits.basemap import Basemap
# import Basemap
# from mpl_toolkits.basemap import Basemap, cm, shiftgrid
from mpl_toolkits.basemap import Basemap
from layer_class import Layer

# readout = True
readout = False
save = True
# save = False
# plot = True
plot = False
plot_map = True
# plot_map = False

def layerize(data_mat, attribute_mat):
    """
    :param data_mat: a mat file containing the data for each segment
    :param attribute_mat: a mat file containing the attributes of each layer
    :return: a list of Layer objects
    """
    layers = []
    # iterate through each mat file
    no_files = len(data_mat)
    no_layers = len(data_mat[0]['twtt']) - 1
    print("Layerizing data files...")
    print("--------------------")
    print(f"number of data files: {no_files}, number of layers: {no_layers}")
    # print("debug:")
    # print(f"layer name: {mat[0]['name']}")

    # print(attribute_mat['lyr_name'][0][0])
    # print(attribute_mat['lyr_name'][0][0][0])
    # print("--------------------\n")

    for i in range(no_layers):
        layer_name = attribute_mat['lyr_name'][0][i][0]
        # print(f"layer name: {layer_name}")
        elevation = np.array([])
        gps_time = np.array([])
        id = np.array([])
        lat = np.array([])
        lon = np.array([])
        param = np.array([])
        quality = np.array([])
        twtt = np.array([])
        type = np.array([])


        for j in range(no_files):

            elevation = np.append(elevation, data_mat[j]['elev'])
            gps_time = np.append(gps_time, data_mat[j]['gps_time'])
            id = np.append(id, data_mat[j]['id'])
            lat = np.append(lat, data_mat[j]['lat'])
            lon = np.append(lon, data_mat[j]['lon'])
            # TODO: figure out what param is and how to handle it.
            # it seems to be some kind of data structure in and of itself (csv or similar?)
            # param = np.append(param, mat[j]['param'])
            quality = np.append(quality, data_mat[j]['quality'])
            twtt = np.append(twtt, data_mat[j]['twtt'][i])
            # print(f"twtt length: {twtt.shape}")
            type = np.append(type, data_mat[j]['type'])

        # create a Layer object
        layers.append(Layer(layer_name, elevation, gps_time, id, lat, lon, param, quality, twtt, type))
        print(f"{layers[i].layer_name} Layer found and created")

    print("--------------------\n")
    return layers



print("Reading data files...")
print("--------------------")
# set the directory, segment data file, layer attributes file, and start and end frames
dir = ('C:\\Users\\rj\\Documents\\cresis\\rds\\2018_Antarctica_DC8\\CSARP_layer\\20181030_01\\')
segment_data_file = 'Data_20181030_01_'
# contains all of the actual data such as twtt, lat, lon, etc.
layer_attributes_file = 'layer_20181030_01.mat'
# contains the attributes of the layer such as name, param, etc.
startframe = '001'
endframe = '016'

# load an array of mat files
data_mat = np.array([sio.loadmat(dir + segment_data_file + str(i).zfill(3) + '.mat')
                     for i in range(int(startframe), int(endframe)+1)])
attribute_mat = sio.loadmat(dir + layer_attributes_file)

# print the keys as strings without all the extra stuff
keys = [str(key).strip("_") for key in data_mat[0].keys()]
print(f"DATA MAT FILE KEYS:")
for key in keys:
    print(key, end="")
    # if not last key, print a comma
    if key != keys[-1]:
        print(",", end=" ")
# print("\n")
# print the keys in the layer attributes mat file
print(f"\nLAYER ATTRIBUTES MAT FILE KEYS:")
keys = [str(key).strip("_") for key in attribute_mat.keys()]
for key in keys:
    print(key, end="")
    # if not last key, print a comma
    if key != keys[-1]:
        print(",", end=" ")
print("\n--------------------\n")

layers = layerize(data_mat, attribute_mat)

if readout:
    print("--------------------", end="")
    for layer in layers:
        print(f"\n{layer.layer_name} number of points: {layer.twtt.shape[0]}")
        print(f"{layer.layer_name} twtt first three: {layer.twtt[:3].tolist()} ")
        print(f"{layer.layer_name} twtt last three: {layer.twtt[-3:].tolist()} ")
    print("--------------------\n")

if save:
    # save layers to a pickle file
    # print("Saving layers to a pickle file...")
    print("--------------------")
    # list current directory
    # print(f"Current directory: {}")
    pickle.dump(layers, open("layers.pickle", "wb"))
    print("layers.pickle saved in local directory of this python file.")
    print("--------------------\n")

if plot:
    # plot the layers
    print("Plotting layers...")
    print("--------------------")
# plot the layer depths vs gps time for each layer on the same plot
    for layer in layers:
        plt.plot(layer.gps_time, layer.twtt, label=layer.layer_name)
    plt.xlabel("GPS Time")
    plt.ylabel("Two Way Travel Time (ns)")
    plt.title("Elevation vs GPS Time")
    plt.legend()

    plt.show()
    print("--------------------\n")

# TODO: make this selectable per season and date with the directory base and
    # CSARP_layer file as hard-coded defaults
# TODO: add a pygame gui with recent files and a file browser
    # save the recent files to a file and load them on startup
# TODO: organize all of this into a library or something similar

if plot_map:
    # plot the lat-lon map for one of the layers
    print("Plotting lat-lon map...")
    print("--------------------")
    # plot the latitudes and longitudes for layers[0] on a basemap
    plt.figure()
    m = Basemap(projection='npstere',boundinglat=-50,lon_0=180,resolution='l')
    m.drawcoastlines()
    m.drawparallels(np.arange(-80.,81.,20.))
    m.drawmeridians(np.arange(-180.,181.,20.))
    m.drawmapboundary(fill_color='white')
    m.scatter(layers[0].lon, layers[0].lat, latlon=True)
    plt.title("Lat-Lon Map")
    plt.show()