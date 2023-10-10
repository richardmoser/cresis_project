
import scipy.io as sio
import numpy as np
import pickle
import matplotlib.pyplot as plt
import os
from mpl_toolkits.basemap import Basemap
from layer_class import Layer
import mat73


testing_mode = True # for use on a non OPR enabled machine without it's own files
testing_mode = False
# readout = True
readout = False
save = True
# save = False
# plot = True
plot_layer = False
plot_map = True
# plot_map = False
# flight = "20181030_01"  # the flight date and frame number
flight = "20181103_01"
def layerize(data_mat, attribute_mat):
    """
    :param data_mat: a mat file containing the data for each segment
    :param attribute_mat: a mat file containing the attributes of each layer
    :return: a list of Layer objects
    """
    print("debug:")
    print(f"data_mat type: {type(data_mat[0])}")
    # list keys in data_mat[0]
    keys = [str(key).strip("_") for key in data_mat[0].keys()]
    print(f"data_mat[0] keys:")
    for key in keys:
        print(key, end="")
        # if not last key, print a comma
        if key != keys[-1]:
            print(",", end=" ")
    # print the twtt array in data_mat[0]
    # print(f"\n\ntwtt shape: {data_mat[0]['twtt'].shape}")
    print(f"twtt: {data_mat[0]['twtt']}")
    print(f"twtt[0]: {data_mat[0]['twtt'][0]}")
    print(f"twtt[0][0]: {data_mat[0]['twtt'][0][0]}")
    print(f"twtt[0][1]: {data_mat[0]['twtt'][0][1]}")

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
        layer_type = np.array([])


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
            layer_type = np.append(layer_type, data_mat[j]['type'])

        # create a Layer object
        layers.append(Layer(layer_name, elevation, gps_time, id, lat, lon, param, quality, twtt, layer_type))
        print(f"{layers[i].layer_name} Layer found and created")

    print("--------------------\n")
    return layers


def main():
    print("Reading data files...")
    print("--------------------")
    # set the directory, segment data file, layer attributes file, and start and end frames
    if testing_mode:
        dir = ('test_data\\')
        segment_data_file = 'Data_'+ flight + '_'
        # contains all of the actual data such as twtt, lat, lon, etc.
        layer_attributes_file = 'layer_' + flight + '.mat'
        # contains the attributes of the layer such as name, param, etc.
    else:
        dir = ('C:\\Users\\rj\\Documents\\cresis\\rds\\2018_Antarctica_DC8\\CSARP_layer\\' + flight + '\\')
        segment_data_file = 'Data_' + flight + '_'
        # contains all of the actual data such as twtt, lat, lon, etc.
        layer_attributes_file = 'layer_' + flight + '.mat'
        # contains the attributes of the layer such as name, param, etc.
        print(f"layer_attributes_file: {layer_attributes_file}")
        # contains the attributes of the layer such as name, param, etc.

        # dir = C:\Users\rj\Documents\cresis\rds\2018_Antarctica_DC8\CSARP_layer\20181112_02
        # dir = ('C:\\Users\\rj\\Documents\\cresis\\rds\\2018_Antarctica_DC8\\CSARP_layer\\20181112_02\\')
        # segment_data_file = 'Data_20181112_02_'
        # layer_attributes_file = 'layer_20181112_02.mat'

    startframe = '001'
    # endframe = '015'
    # endframe = the number of files in the directory
    files = os.listdir(dir)
    endframe = str(len(files) - 1).zfill(3)

    # load an array of mat files
    # data_mat = np.array([sio.loadmat(dir + segment_data_file + str(i).zfill(3) + '.mat')
    #                      for i in range(int(startframe), int(endframe)+1)])
    # attribute_mat = sio.loadmat(dir + layer_attributes_file)

    data_mat = np.array([mat73.loadmat(dir + segment_data_file + str(i).zfill(3) + '.mat')
                            for i in range(int(startframe), int(endframe)+1)])
    attribute_mat = mat73.loadmat(dir + layer_attributes_file)


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

    # layers = layerize(data_mat, attribute_mat)
    #
    # if readout:
    #     print("--------------------", end="")
    #     for layer in layers:
    #         print(f"\n{layer.layer_name} number of points: {layer.twtt.shape[0]}")
    #         print(f"{layer.layer_name} twtt first three: {layer.twtt[:3].tolist()} ")
    #         print(f"{layer.layer_name} twtt last three: {layer.twtt[-3:].tolist()} ")
    #     print("--------------------\n")
    #
    # if save:
    #     # save layers to a pickle file
    #     # print("Saving layers to a pickle file...")
    #     print("--------------------")
    #     # list current directory
    #     # print(f"Current directory: {}")
    #     file_name = "layer_export" + layer_attributes_file[5:-4] + ".pickle"
    #     pickle.dump(layers, open(file_name, "wb"))
    #     print(file_name, " saved in local directory of this python file.")
    #     print("--------------------\n")
    #
    # if plot_layer:
    #     # plot the layers
    #     print("Plotting layers...")
    #     print("--------------------")
    # # plot the layer depths vs gps time for each layer on the same plot
    #     for layer in layers:
    #         plt.plot(layer.gps_time, layer.twtt, label=layer.layer_name)
    #     plt.xlabel("GPS Time")
    #     plt.ylabel("Two Way Travel Time (ns)")
    #     plt.title("Elevation vs GPS Time")
    #     plt.legend()
    #
    #     plt.show()
    #     print("--------------------\n")
    #
    # # TODO: make this selectable per season and date with the directory base and
    #     # CSARP_layer file as hard-coded defaults
    # # TODO: add a pygame gui with recent files and a file browser
    #     # save the recent files to a file and load them on startup
    # # TODO: organize all of this into a library or something similar
    #
    # if plot_map:
    #     # plot the lat-lon map for one of the layers in antarctica
    #     print("Plotting lat-lon map...")
    #     print("--------------------")
    #     # plot the latitudes and longitudes for layers[0] on a basemap
    #     plt.figure()
    #     m = Basemap(projection='spstere', boundinglat=-70, lon_0=180, resolution='l')
    #     m.drawcoastlines()
    #     m.fillcontinents(color='grey', lake_color='aqua')
    #     m.drawparallels(np.arange(-80., 81., 20.))
    #     m.drawmeridians(np.arange(-180., 181., 20.))
    #     m.drawmapboundary(fill_color='aqua')
    #     # plot the flight path
    #     m.plot(layers[0].lon, layers[0].lat, latlon=True, color='lightgreen', linewidth=1)
    #     # plot the South Pole
    #     m.scatter(0, -90, latlon=True, color='black', linewidth=1, label='South Pole')
    #     x, y = m(0, -90)
    #     plt.text(x, y, '\nSouth Pole', fontsize='smaller', fontweight='bold', ha='center', va='top', color='black')
    #     plt.title("Lat-Lon Map")
    #     plt.show()
    #     print("--------------------\n")

if __name__ == "__main__":
    main()