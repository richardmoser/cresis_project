"""
Author: Richard Moser
Description: This file contains classes and functions used in other files. Ideally, this will clean up the other code.
"""
# import pickle
# import matplotlib.pyplot as plt
# import numpy as np
# import math
# import os
import h5py
import scipy.io as sio
import datetime
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from shapely.geometry import LineString
from mpl_toolkits.basemap import Basemap
from project_classes import *
# from iceflow_library import *
import sys
import time
import csv

section_break = "--------------------"
# stdout text colors
BLACK = '\033[30m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'  # orange on some systems
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
LIGHT_GRAY = '\033[37m'
DARK_GRAY = '\033[90m'
BRIGHT_RED = '\033[91m'
BRIGHT_GREEN = '\033[92m'
BRIGHT_YELLOW = '\033[93m'
BRIGHT_BLUE = '\033[94m'
BRIGHT_MAGENTA = '\033[95m'
BRIGHT_CYAN = '\033[96m'
WHITE = '\033[97m'
RESET = '\033[0m'  # called to return to standard terminal text color

username = os.getlogin()

def debug_print(*args):
    """
    :param args: a list of arguments to print to the console
    :return: nothing
    """
    """
    This function prints the arguments to the console in a specific format.
    """
    print(BRIGHT_YELLOW + "DEBUG: ", end="")
    for arg in args:
        print(arg, end="")
    print(RESET)


def mat_pickler_layerData(season, flight, testing_mode=False, readout=False, save=True, plot_layer=False):
    print("Reading data files...")
    print(section_break)
    segment_data_file = 'Data_' + flight + '_'
    layer_attributes_file = 'layer_' + flight + '.mat' # seems to only be used for the layer names in this code
    # layerData = not layer
    # set the directory, segment data file, layer attributes file, and start and end frames
    if testing_mode:
        # the dir is the current directory + the test_data folder
        dir = os.getcwd() + '\\test_data\\' + flight + '\\'

        # dir = ('test_data') + '\\'
        # contains all of the actual data such as twtt, lat, lon, etc.
        # contains the attributes of the layer such as name, param, etc.
    else:
        #TODO: refactor this into a try except block, maybe upstream of this function where it is called

        # if layer:
        #     dir = ('C:\\Users\\moser\\Documents\\cresis\\rds\\' + season + '\\CSARP_layer\\' + flight + '\\')
        #     # leaving because it might actually be good. the below line works for 2018_Antarctica_DC8 at least as it
        #     # has the CSARP_layerData folder instead of CSARP_layer.
        # if layerData:
        dir = ('C:\\Users\\moser\\Documents\\cresis\\rds\\' + season + '\\CSARP_layerData\\' + flight + '\\')
        # contains all of the actual data such as twtt, lat, lon, etc.
        # contains the attributes of the layer such as name, param, etc.
        print(f"layer_attributes_file: {layer_attributes_file}")
        # contains the attributes of the layer such as name, param, etc.

        # dir = C:\Users\moser\\Documents\cresis\rds\2018_Antarctica_DC8\CSARP_layer\20181112_02
        # dir = ('C:\\Users\\moser\\Documents\\cresis\\rds\\2018_Antarctica_DC8\\CSARP_layer\\20181112_02\\')
        # segment_data_file = 'Data_20181112_02_'
        # layer_attributes_file = 'layer_20181112_02.mat'

    startframe = '001'
    # endframe = '015'
    # endframe = the number of files in the directory
    files = os.listdir(dir)
    endframe = str(len(files) - 1).zfill(3)

    # load an array of mat files
    data_mat = np.array([sio.loadmat(dir + segment_data_file + str(i).zfill(3) + '.mat')
                         for i in range(int(startframe), int(endframe)+1)])
    attribute_mat = sio.loadmat(dir + layer_attributes_file)

    # data_mat = np.array([mat73.loadmat(dir + segment_data_file + str(index).zfill(3) + '.mat')
    #                         for index in range(int(startframe), int(endframe)+1)])
    # attribute_mat = mat73.loadmat(dir + layer_attributes_file)


    # print the keys as strings without all the extra stuff
    # keys = [str(key).strip("_") for key in data_mat[0].keys()]
    # print(f"DATA MAT FILE KEYS:")
    # for key in keys:
    #     print(key, end="")
    #     # if not last key, print a comma
    #     if key != keys[-1]:
    #         print(",", end=" ")
    # print("\n")
    # print the keys in the layer attributes mat file
    # print(f"\nLAYER ATTRIBUTES MAT FILE KEYS:")
    # keys = [str(key).strip("_") for key in attribute_mat.keys()]
    # for key in keys:
    #     print(key, end="")
    #     # if not last key, print a comma
    #     if key != keys[-1]:
    #         print(",", end=" ")
    print("\n--------------------\n")

    layers = layerize(data_mat, attribute_mat)

    if readout:
        print(section_break, end="")
        for layer in layers:
            print(f"\n{layer.layer_name} number of points: {layer.twtt.shape[0]}")
            print(f"{layer.layer_name} twtt first three: {layer.twtt[:3].tolist()} ")
            print(f"{layer.layer_name} twtt last three: {layer.twtt[-3:].tolist()} ")
        print(section_break + "\n")

    if save:
        # save layers to a pickle file
        # print("Saving layers to a pickle file...")
        print(section_break)
        # list current directory
        # print(f"Current directory: {}")
        file_name = "layer_export" + layer_attributes_file[5:-4] + ".pickle"
        pickle.dump(layers, open(file_name, "wb"))
        # print(file_name, " saved in local directory of this python file.")
        # print(section_break + "\n")

    if plot_layer:
        # plot the layers
        print("Plotting layers...")
        print(section_break)
    # plot the layer depths vs gps time for each layer on the same plot
        for layer in layers:
            plt.plot(layer.gps_time, layer.twtt, label=layer.layer_name)
        plt.xlabel("GPS Time")
        plt.ylabel("Two Way Travel Time (ns)")
        plt.title("Elevation vs GPS Time")
        plt.legend()

        plt.show()
        print(section_break + "\n")

    # TODO: make this selectable per season and date with the directory base and
        # CSARP_layer file as hard-coded defaults
    # TODO: add a pygame gui with recent files and a file browser
        # save the recent files to a file and load them on startup
    # TODO: organize all of this into a library or something similar


def mat_pickler_layer(season, flight, testing_mode=False, readout=False, save=True, plot_layer=False):
    print("Reading data files...")
    print(section_break)
    segment_data_file = 'Data_' + flight + '_'
    layer_attributes_file = 'layer_' + flight + '.mat'

    # if there is only one segment data file, return nothing
    # TODO: no that is not how that works, 2018DC8 simply has fewer mat files per flight for some reason
    # if not os.path.exists('C:\\Users\\moser\\Documents\\cresis\\rds\\' + season + '\\CSARP_layer\\' + flight + '\\' + segment_data_file + '002.mat'):
    #     print(f"Not all data is downloaded for flight {flight}.")
    #     return

    # layerData = not layer
    # set the directory, segment data file, layer attributes file, and start and end frames
    if testing_mode:
        # the dir is the current directory + the test_data folder
        dir = os.getcwd() + '\\test_data\\' + flight + '\\'

        # dir = ('test_data') + '\\'
        # contains all of the actual data such as twtt, lat, lon, etc.
        # contains the attributes of the layer such as name, param, etc.
    else:
        #TODO: refactor this into a try except block, maybe upstream of this function where it is called
            dir = ('C:\\Users\\moser\\Documents\\cresis\\rds\\' + season + '\\CSARP_layer\\' + flight + '\\')
        #     # leaving because it might actually be good. the below line works for 2018_Antarctica_DC8 at least as it
        #     # has the CSARP_layerData folder instead of CSARP_layer.

        # contains all of the actual data such as twtt, lat, lon, etc.
        # contains the attributes of the layer such as name, param, etc.
            print(f"layer_attributes_file: {layer_attributes_file}")
        # contains the attributes of the layer such as name, param, etc.

        # dir = C:\Users\moser\\Documents\cresis\rds\2018_Antarctica_DC8\CSARP_layer\20181112_02
        # dir = ('C:\\Users\\moser\\Documents\\cresis\\rds\\2018_Antarctica_DC8\\CSARP_layer\\20181112_02\\')
        # segment_data_file = 'Data_20181112_02_'
        # layer_attributes_file = 'layer_20181112_02.mat'

    startframe = '001'
    # endframe = '015'
    # endframe = the number of files in the directory
    files = os.listdir(dir)
    endframe = str(len(files) - 1).zfill(3)

    # load an array of mat files
    data_mat = np.array([sio.loadmat(dir + segment_data_file + str(i).zfill(3) + '.mat')
                         for i in range(int(startframe), int(endframe)+1)])
    attribute_mat = sio.loadmat(dir + layer_attributes_file)

    # data_mat = np.array([mat73.loadmat(dir + segment_data_file + str(index).zfill(3) + '.mat')
    #                         for index in range(int(startframe), int(endframe)+1)])
    # attribute_mat = mat73.loadmat(dir + layer_attributes_file)


    # print the keys as strings without all the extra stuff
    # keys = [str(key).strip("_") for key in data_mat[0].keys()]
    # print(f"DATA MAT FILE KEYS:")
    # for key in keys:
    #     print(key, end="")
        # if not last key, print a comma
        # if key != keys[-1]:
        #     print(",", end=" ")
    # print("\n")
    # print the keys in the layer attributes mat file
    # print(f"\nLAYER ATTRIBUTES MAT FILE KEYS:")
    # keys = [str(key).strip("_") for key in attribute_mat.keys()]
    # for key in keys:
        # print(key, end="")
        # if not last key, print a comma
        # if key != keys[-1]:
        #     print(",", end=" ")
    print("\n--------------------\n")

    layers = layerize(data_mat, attribute_mat)

    if readout:
        print(section_break, end="")
        for layer in layers:
            print(f"\n{layer.layer_name} number of points: {layer.twtt.shape[0]}")
            print(f"{layer.layer_name} twtt first three: {layer.twtt[:3].tolist()} ")
            print(f"{layer.layer_name} twtt last three: {layer.twtt[-3:].tolist()} ")
        print(section_break + "\n")

    if save:
        # save layers to a pickle file
        # print("Saving layers to a pickle file...")
        print(section_break)
        # list current directory
        # print(f"Current directory: {}")
        file_name = "layer_export" + layer_attributes_file[5:-4] + ".pickle"
        pickle.dump(layers, open(file_name, "wb"))
        # print(file_name, " saved in local directory of this python file.")
        # print(section_break + "\n")

    if plot_layer:
        # plot the layers
        print("Plotting layers...")
        print(section_break)
    # plot the layer depths vs gps time for each layer on the same plot
        for layer in layers:
            plt.plot(layer.gps_time, layer.twtt, label=layer.layer_name)
        plt.xlabel("GPS Time")
        plt.ylabel("Two Way Travel Time (ns)")
        plt.title("Elevation vs GPS Time")
        plt.legend()

        plt.show()
        print(section_break + "\n")

    # TODO: make this selectable per season and date with the directory base and
        # CSARP_layer file as hard-coded defaults


def mat_pickler_h5py(season, flight, testing_mode=False, readout=False, save=True, plot_layer=False, convert_xy=False):
    print("Reading data files...")
    print(section_break)
    # set the directory, segment data file, layer attributes file, and start and end frames
    if testing_mode:
        # the dir is the current directory + the test_data folder
        dir = os.getcwd() + '\\test_data\\' + flight + '\\'
    else:
        # TODO: refactor this into a try except block, maybe upstream of this function where it is called
        dir = ('C:\\Users\\moser\\Documents\\cresis\\rds\\' + season + '\\CSARP_layer\\' + flight + '\\')

    data_file = dir + 'Data_' + flight + '_'
    attributes_file = dir + 'layer_' + flight
    layers = layerize_h5py(data_file, attributes_file, dir, convert_xy)
    if layers == True:
        return True

    if readout:
        print(section_break, end="")
        for layer in layers:
            print(f"\n{layer.layer_name} number of points: {layer.twtt.shape[0]}")
            print(f"{layer.layer_name} twtt first three: {layer.twtt[:3].tolist()} ")
            print(f"{layer.layer_name} twtt last three: {layer.twtt[-3:].tolist()} ")
        print(section_break + "\n")

    if save:
        # save layers to a pickle file
        # print("Saving layers to a pickle file...")
        print(section_break)
        # list current directory
        # print(f"Current directory: {}")
        directory = os.getcwd() + "\\pickle_jar\\"
        # file_name = directory + "layer_export" + attributes_file[5:-4] + ".pickle"
        file_name = directory + "layer_export_" + flight + ".pickle"
        pickle.dump(layers, open(file_name, "wb"))
        # print(file_name, " saved in local directory of this python file.")
        # print(section_break + "\n")

    if plot_layer:
        # plot the layers
        print("Plotting layers...")
        print(section_break)
        # plot the layer depths vs gps time for each layer on the same plot
        for layer in layers:
            plt.plot(layer.gps_time, layer.twtt, label=layer.layer_name)
        plt.xlabel("GPS Time")
        plt.ylabel("Two Way Travel Time (ns)")
        # invert the y axis so that the plot is right side up
        plt.gca().invert_yaxis()
        plt.title("Elevation vs GPS Time")
        plt.legend()

        plt.show()
        print(section_break + "\n")


def layerize(data_mat, attribute_mat):
    """
    :param data_mat: a mat file containing the data for each segment
    :param attribute_mat: a mat file containing the attributes of each layer
    :return: a list of Layer objects
    """
    # print("debug:")
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
    # print(f"twtt: {data_mat[0]['twtt']}")
    # print(f"twtt[0]: {data_mat[0]['twtt'][0]}")
    # print(f"twtt[0][0]: {data_mat[0]['twtt'][0][0]}")
    # print(f"twtt[0][1]: {data_mat[0]['twtt'][0][1]}")

    layers = []
    # iterate through each mat file
    no_files = len(data_mat)
    no_layers = len(data_mat[0]['twtt']) - 1
    print("Layerizing data files...")
    print(section_break)
    print(f"number of data files: {no_files}, number of layers: {no_layers}")
    # print("debug:")
    # print(f"layer name: {mat[0]['name']}")

    # print(attribute_mat['lyr_name'][0][0])
    # print(attribute_mat['lyr_name'][0][0][0])
    # print(section_break + "\n")

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
        layers.append(Layer(layer_name, gps_time, id, lat, lon, param, quality, twtt, layer_type, elevation))
        print(f"{layers[i].layer_name} Layer found and created")

    print(section_break + "\n")
    return layers


def layerize_h5py(data_file, attribute_file, dir, convert_xy):
    # TODO: add a docstring
    # TODO: add a portion to pull the layer name out of the attribute file
    # afai can tell, that is all the attribute file is used for in the original code
    # create an empty list to store the layers
    layers = []
    files = os.listdir(dir)  # list of files in the directory
    # TODO: shift to differentiating data vs layer based on file name. Data starts with "Data_" and layer starts with "layer_"
    startframe = '001'  # the first file number in the directory
    endframe = str(len(files) - 1).zfill(3)  # the number of files in the directory
    # debug_print(f"attribute_file: {attribute_file}")
    attribute_mat = h5py.File(attribute_file + '.mat', 'r')
    # print the keys in the attribute file

    decimal1 = attribute_mat[np.array([attribute_mat['lyr_name'][0][0]])[0]]
    decimal1_name = [decimal1[i][0] for i in range(len(decimal1))]  # a list of unicode values of the characters
    decimal2 = attribute_mat[np.array([attribute_mat['lyr_name'][1][0]])[0]]
    decimal2_name = [decimal2[i][0] for i in range(len(decimal2))]  # a list of unicode values of the characters
    name1 = ''.join(chr(i) for i in decimal1_name)  # convert the unicode values to a string
    name2 = ''.join(chr(i) for i in decimal2_name)  # convert the unicode values to a string

    layer1_name = name1
    layer2_name = name2

    # print(f"data_file: {data_file}")
    filled_data_file = data_file + str(1).zfill(3) + '.mat'
    # print(f"filled_data_file: {filled_data_file}")

    h5py_works = True
    # debug_print("made it to layerize_h5py", "passed the filled_data_file variable to h5py.File",
                # "\n", "filled_data_file: ", filled_data_file, "\n")
    try:
        f = h5py.File(filled_data_file, 'r')
        debug_print(BRIGHT_GREEN, f"Opened {filled_data_file} with h5py")
    except:
        # debug_print(RED, f"Error: could not open {filled_data_file} with h5py, ignoring this file")
        # return True
        # print(f"Error: could not open {filled_data_file} with h5py, attempting with sio.loadmat")
        try:
            f = sio.loadmat(filled_data_file)
            h5py_works = False
        except:
            debug_print(RED, f"Error: could not open {filled_data_file} with sio.loadmat, exiting")
            # sys.exit(1)
            return True


    # f = h5py.File(data_file + str(3).zfill(3) + '.mat', 'r')  #
    # print the contents of the 'param' key
    # print(f"f['param']: {f['param']}")
    # print(f"f['param'].keys(): {list(f['param'].keys())}")

    filename = data_file + '001.mat'  # fill the data which doesn't change per point
    # param = []  # will need some debugging and we probably don't care about it
    layer1_quality = []
    layer2_quality = []
    layer1_type = []
    layer2_type = []

    layer1_quality.append(f['quality'][0])
    layer2_quality.append(f['quality'][1])
    layer1_type.append(f['type'][0])
    layer2_type.append(f['type'][1])

    # initialize the data that will be loaded from the files
    gps_time = []
    layer1_id = []
    layer2_id = []
    lat = []
    lon = []
    layer1_twtt = []
    layer2_twtt = []

    # print("\n\nlayerize_h5py debug:")
    # print(f"f['lat'][:]: {f['lat'][:]}")
    # print(f"f['lat'][:]: {f['lat'][:].flatten()[0]}")

    # print(f"f['lat'][:][0]: {f['lat'][:][0]}")
    # print(f"layer1 lon: {f['lon'][:]}")

    # print("\n\n")
    already_printed = False
    # Load data from each file
    if h5py_works:
        for i in range(int(startframe), int(endframe) + 1):
            filename = data_file + str(i).zfill(3) + '.mat'
            # if h5py_works:
            with h5py.File(filename, 'r') as f:
                gps_time.append(f['gps_time'][:])
                layer1_id.append(f['id'][0])
                layer2_id.append(f['id'][1])
                lat.append(f['lat'][:].flatten())
                lon.append(f['lon'][:].flatten())
                # param.append(f['param'])
                # layer1_quality.append(f['quality'][0])
                # layer2_quality.append(f['quality'][1])

                # Extract twtt columns directly into layer1_twtt and layer2_twtt
                twtt_data = f['twtt'][:]
                layer1_twtt.extend(twtt_data[:, 0])
                layer2_twtt.extend(twtt_data[:, 1])


        # Convert lists to numpy arrays
        # debug_print(f"gps_time: {gps_time}")

        gps_time = np.concatenate(gps_time)
        lat = np.concatenate(lat)
        lon = np.concatenate(lon)
        # param = np.concatenate(param)
        layer1_twtt = np.array(layer1_twtt)
        layer2_twtt = np.array(layer2_twtt)

        # Convert lists to numpy arrays
        layer1_id = np.array(layer1_id)
        layer2_id = np.array(layer2_id)
        layer1_quality = np.array(layer1_quality)
        layer2_quality = np.array(layer2_quality)
        layer1_type = np.array(layer1_type)
        layer2_type = np.array(layer2_type)

    else:
        for i in range(int(startframe), int(endframe) + 1):
            filename = data_file + str(i).zfill(3) + '.mat'

            f = sio.loadmat(filename)
            # print the keys in f
            if already_printed:
                print(f.keys())
                already_printed = True
            for time in f['gps_time']:
                # debug_print(f"time: {time}")
                gps_time.extend(time)

            # gps_time.append(f['gps_time'][0])
            layer1_id.append(f['id'][0][0])
            # for id in f['id']:d
                # layer1_id.append(id[0][0])
                # layer2_id.append(id[0][1])
            layer2_id.append(f['id'][0][1])

            lat.append(f['lat'])
            lon.append(f['lon'])
            # for lat in f['lat']:
            # debug_print(f"lat: {lat[0:3]}")
            # debug_print the shape of lat
            # debug_print(f"lat shape: {np.array(lat).shape}")
                # lat.extend(lat[0])

            # param.append(f['param'])
            # layer1_quality.append(f['quality'][0])
            # layer2_quality.append(f['quality'][1])

            # Extract twtt columns directly into layer1_twtt and layer2_twtt
            twtt_data = f['twtt']
            layer1_twtt.extend(twtt_data[:, 0])
            layer2_twtt.extend(twtt_data[:, 1])
        # debug_print(RED, f"gps_time: {gps_time}")
        # debug_print(RED, f"lat: {lat}")

        gps_time = np.array(gps_time)
        # debug_print(f"gps_time: {gps_time}")

    # create a layer object
    layer1 = Layer(layer1_name, gps_time, layer1_id, lat, lon, layer1_quality, layer1_twtt, layer1_type)
    layer2 = Layer(layer2_name, gps_time, layer2_id, lat, lon, layer2_quality, layer2_twtt, layer2_type)

    import time
    corrected = False
    if convert_xy:
        start = time.time()
        # Convert lat-lon to x-y
        print("Converting lat-lon to x-y...")
        for i in range(len(lat)):
            if i%100 == 0:
                progress_bar(i, len(lat), start)
            x1, y1 = latlon_to_xy(lat[i], lon[i])
            layer1.x.append(x1)
            layer1.y.append(y1)
            layer2.x.append(x1)
            layer2.y.append(y1)

            twtt1 = layer1.twtt - layer1.twtt
            twtt2 = layer1.twtt - layer2.twtt
            layer1.twtt_corrected = twtt1
            layer2.twtt_corrected = twtt2

            depth1 = twtt_to_depth(twtt1)
            depth2 = twtt_to_depth(twtt2)
            layer1.depth = depth1
            layer2.depth = depth2

        layer1.xy_exists = True
        layer2.xy_exists = True


    # append the layer to the layers list
    layers.append(layer1)
    layers.append(layer2)
    # print(f"layer1: {layer1.layer_name} number of points: {layer1.twtt.shape[0]}")
    # print(f"layer2: {layer2.layer_name} number of points: {layer2.twtt.shape[0]}")

    if not corrected:
        for layer in layers:
            if h5py_works:
                corrected_twtt = layer.twtt - layers[0].twtt  # normalize against the surface layer
                # corrected_twtt = layer.twtt
                layer.twtt_corrected = corrected_twtt
            else:
                corrected_twtt = np.array(layer.twtt) - np.array(layers[0].twtt)
                layer.twtt_corrected = corrected_twtt

    return layers


def read_layers(file_name, quiet=False):
    """
    :param file_name: the name of the pickle file containing the layers, e.g. "layer_export_20181030_01.pickle"
    :return: a list of Layer objects from the pickle file (usually Surface, your custom layer(s), and Bottom)
    """
    if not quiet:
        print("Reading pickle file...")
        print(section_break)
    # read layers.pickle into a list of Layer objects

    # file_name = 'layers.pickle'

    with open(file_name, 'rb') as f:
        layers = pickle.load(f)
    if not quiet:
        for layer in layers:
            print(layer.layer_name)
        print(section_break + "\n")
    return layers


def append_layers(layers1, layers2):
    """
    :param layers1: a list of Layer objects
    :param layers2: a list of Layer objects
    :return: a list of Layer objects that is the combination of layers1 and layers2
    """
    print("Appending layers...")
    print(section_break)
    # append layers2 to layers1
    layers = layers1 + layers2
    for layer in layers:
        print(layer.layer_name)
    print(section_break + "\n")
    return layers


# def full_season_layerize(season, OTHER_STUFF)
    # TODO: make this function troll through the CSARP_layerData folder and layerize all the flights in a season
    # may have to run it on a server or something because it could take a long time
    # crossover will almost certainly need to be run on a server
    # once it is in the pickle file, it can be read and manipulated on a local machine though
def full_season_layerize(season, testing_mode=False, readout=False, save=True, plot_layer=False):
    """
    :param season: the name of the season, e.g. "2018_Antarctica_DC8"
    :param testing_mode: a boolean to run the function in testing mode
    :param readout: a boolean to print the layers to the console
    :param save: a boolean to save the layers to a pickle file
    :param plot_layer: a boolean to plot the layers
    :return: nothing
    """
    """
    This only works if you have processed every single flight in the season with the picker tool.
    """
    print("Layerizing full season...")
    print(section_break)
    # list the flights in the season
    # dir = 'C:\\Users\\moser\\Documents\\cresis\\rds\\' + season + '\\CSARP_layerData\\'
    dir = 'C:\\Users\\moser\\Documents\\cresis\\rds\\' + season + '\\CSARP_layer\\'
    flights = os.listdir(dir)
    print(f"Flights in {season}: {flights}")
    print(section_break + "\n")
    # layerize each flight
    for flight in flights:
        # mat_pickler_layerData(season, flight, testing_mode, readout, save, plot_layer)
        mat_pickler_layer(season, flight, testing_mode, readout, save, plot_layer)
    print("Full season layerized.")
    print(section_break + "\n")
    

# def cross_point(layer, seg_length, quiet=False):
#     """
#     :param seg_length:
#     :param layer: a Layer object
#     :param quiet: a boolean to suppress print statements
#     :return: the point where the lat-lon crosses over its own path.
#     purpose: layers[0].lat and layers[0].lon are numpy arrays of the latitudes and
#     longitudes for a flight path. It does not connect back to the beginning.
#     This function finds the point where the path crosses over itself.
#     The lat-lon of the crossover point will not be exactly the same as the
#     lat-lons in the arrays, but it will be very close.
#     """
#     verbose = not quiet
#     print("Finding crossover point...")
#     print(section_break)
#     # create a list of line segments of length seg_length
#     path_segments = []
#     segment_ends = []
#     if verbose:
#         print(f"Dividing the path into segments of length {seg_length}...")
#     for index in range(0, len(layer.lat), seg_length):
#         if index + seg_length < len(layer.lat):
#             path_segments.append([(layer.lat[index], layer.lon[index]), (layer.lat[index + seg_length], layer.lon[index + seg_length])])
#         else:
#             path_segments.append([(layer.lat[index], layer.lon[index]), (layer.lat[-1], layer.lon[-1])])
#
#     if verbose:
#         print(f"Number of segments: {len(path_segments)}")
#     print("Checking for intersections...")
#     # check for intersections between the line segments
#     # TODO: implement loading bar
#     rough_intersections = []
#     intersecting_segments = []
#     for index in range(len(path_segments)):
#         for j in range(index + 1, len(path_segments)):
#             if segments_intersect(path_segments[index], path_segments[j]):
#                 intersection_points = find_segment_intersection(path_segments[index], path_segments[j])
#                 if intersection_points:
#                     rough_intersections.append([intersection_points[0][0], intersection_points[1][0]])
#                     intersecting_segments.append([index, j])
#                     if verbose:
#                         print(f"Segments {index} and {j} intersect near "
#                               f"({intersection_points[0][0]}, {intersection_points[1][0]})")
#
#     if verbose:
#         print("\nChecking for a more precise intersection...")
#     fine_intersections = []
#     intersection_indices = []
#
#     printed = False
#
#     for seg_pair in range(len(intersecting_segments)):
#         seg1 = intersecting_segments[seg_pair][0]
#         seg2 = intersecting_segments[seg_pair][1]
#
#         # translate segment numbers to indices in the lat-lon arrays
#         if seg1 == 0:
#             seg1_start = 0
#             seg1_end = seg_length
#         else:
#             seg1_start = seg1 * seg_length
#             seg1_end = seg1_start + seg_length
#         if seg2 == 0:
#             seg2_start = 0
#             seg2_end = seg_length
#         else:
#             seg2_start = seg2 * seg_length
#             seg2_end = seg2_start + seg_length
#         if verbose:
#             print(f"segment {seg1} start: {seg1_start}, segment 1 end: {seg1_end}")
#         if verbose:
#             print(f"segment {seg2} start: {seg2_start}, segment 2 end: {seg2_end}")
#
#         # create a list of line segments of length 1
#         path_segments = []
#         for index in range(seg1_start, seg1_end):
#             path_segments.append([(layer.lat[index], layer.lon[index]), (layer.lat[index + 1], layer.lon[index + 1])])
#         for index in range(seg2_start, seg2_end):
#             path_segments.append([(layer.lat[index], layer.lon[index]), (layer.lat[index + 1], layer.lon[index + 1])])
#
#         # check for intersections between the line segments
#         for first_seg in range(len(path_segments)):
#             for sec_seg in range(first_seg + 1, len(path_segments)):
#                 if segments_intersect(path_segments[first_seg], path_segments[sec_seg]):
#                     intersection_points = find_segment_intersection(path_segments[first_seg], path_segments[sec_seg])
#                     if intersection_points:
#                         index1 = seg1_start + first_seg
#                         index2 = seg2_start + sec_seg
#                         # intersections.append([intersection_points])
#                         # segment_ends.append([[path_segments[first_seg][0], path_segments[first_seg][1]],
#                         #                      [path_segments[sec_seg][0], path_segments[sec_seg][1]]])
#
#                         segment_ends.append([[path_segments[first_seg][0][0][0], path_segments[first_seg][0][0][1], index1],
#                                              [path_segments[sec_seg][0][0][0], path_segments[sec_seg][1][0][0], index2]])
#                         fine_intersections.append([intersection_points[0][0], intersection_points[1][0]])
#                         # fine_intersections are the first two points of the segment_ends list, index.e. two endpoints on
#                         # opposing legs of the X. segment_ends are all four points of the X.
#                         if verbose:
#                             print(f"Segments {seg1} and {seg2} intersect near indices "
#                                   f"{index1} and {index2}\nThis corresponds roughly to the "
#                                   f"lat-lon: ({fine_intersections[-1][0]}, {fine_intersections[-1][1]})")
#                         intersection_indices.append([index1, index2])
#
#                         if not printed:
#                             print("--------------------\n\n")
#                             print(f"path_segments[first_seg]: {path_segments[first_seg]}")
#                             print(f"path_segments[sec_seg]: {path_segments[sec_seg]}\n")
#                             print(f"segment_ends[first_seg]: {segment_ends}")
#
#                             print("--------------------\n\n")
#                             printed = True
#
#
#
#     print(f"Number of intersections: {len(fine_intersections)}")
#     if verbose:
#         print(f"Number of rough intersections: {len(rough_intersections)}")
#         print(f"Number of intersection indices: {len(intersection_indices)}")
#         # print(f"Indices: {intersect_indices}")
#         # for index in intersect_indices:
#         #     print(f"Index: {index}: ")
#     for index in range(len(intersection_indices)):
#         print(f"Index {index}: \n"
#               f"indices: \t{intersection_indices[index]}\n"
#               f"lat-lon: \t({fine_intersections[index][0]}, {fine_intersections[index][1]})\n"
#                 f"segment ends: \t{segment_ends[index]}\n"
#               f"lat-lon by layer: \t({layer.lat[intersection_indices[index][0]]}, {layer.lon[intersection_indices[index][0]]})")
#
#     print(f"Intersection at index {intersection_indices[0][0]} and {intersection_indices[0][1]}")
#     for index in range(len(intersection_indices)):
#         # TODO Error 1: correct for the fine intersection points being wrong for some reason
#             # (lat is close but lon is 6 degrees off in the 20181112_02 flight)
#         fine_intersections[index][0] = layer.lat[intersection_indices[index][0]]
#         fine_intersections[index][1] = layer.lon[intersection_indices[index][0]]
#     print(section_break + "\n")
#
#     return fine_intersections, intersection_indices, segment_ends

def layer_to_csv(season, flight):
    """
    :param season: the string name of the season
    :param flight: the string name of the flight
    :return: none, save the data to a csv file
    """
    """Find the Mat"""
    dir = ('C:\\Users\\moser\\Documents\\cresis\\rds\\' + season + '\\CSARP_layer\\' + flight + '\\')
    data_file = dir + 'Data_' + flight + '_'
    attributes_file = dir + 'layer_' + flight + '.mat'

    """Layerize"""

    layers = []
    files = os.listdir(dir)
    startframe = '001'  # the first file number in the directory
    endframe = str(len(files) - 1).zfill(3)  # the number of files in the directory
    attribute_mat = h5py.File(attributes_file, 'r')

    decimal1 = attribute_mat[np.array([attribute_mat['lyr_name'][0][0]])[0]]
    decimal1_name = [decimal1[i][0] for i in range(len(decimal1))]  # a list of unicode values of the characters
    decimal2 = attribute_mat[np.array([attribute_mat['lyr_name'][1][0]])[0]]
    decimal2_name = [decimal2[i][0] for i in range(len(decimal2))]  # a list of unicode values of the characters
    name1 = ''.join(chr(i) for i in decimal1_name)  # convert the unicode values to a string
    name2 = ''.join(chr(i) for i in decimal2_name)  # convert the unicode values to a string

    layer1_name = name1
    layer2_name = name2

    f = h5py.File(data_file + str(1).zfill(3) + '.mat', 'r')

    gps_time = []
    layer1_id = []
    layer2_id = []
    lat = []
    lon = []
    layer1_twtt = []
    layer2_twtt = []

    # Load data from each file
    for i in range(int(startframe), int(endframe) + 1):
        filename = data_file + str(i).zfill(3) + '.mat'
        with h5py.File(filename, 'r') as f:
            gps_time.append(f['gps_time'][:])
            layer1_id.append(f['id'][0])
            layer2_id.append(f['id'][1])
            lat.append(f['lat'][:].flatten())
            lon.append(f['lon'][:].flatten())
            # param.append(f['param'])
            # layer1_quality.append(f['quality'][0])
            # layer2_quality.append(f['quality'][1])

            # Extract twtt columns directly into layer1_twtt and layer2_twtt
            twtt_data = f['twtt'][:]
            layer1_twtt.extend(twtt_data[:, 0])
            layer2_twtt.extend(twtt_data[:, 1])

    # concatenate the lists into numpy arrays
    gps_time = np.concatenate(gps_time)
    lat = np.concatenate(lat)
    lon = np.concatenate(lon)
    # param = np.concatenate(param)
    layer1_twtt = np.array(layer1_twtt)
    layer2_twtt = np.array(layer2_twtt)

    # Convert lists to numpy arrays
    layer1_id = np.array(layer1_id)
    layer2_id = np.array(layer2_id)

    fields = ['index', 'gps_time', 'lat', 'lon', 'layer1_twtt', 'layer2_twtt']
    rows = []
    for i in range(len(gps_time)):
        rows.append([i, gps_time[i][0], lat[i], lon[i], layer1_twtt[i], layer2_twtt[i]])
    #
    # print(f"size of data: {len(rows)}")
    #
    filename = 'C:\\Users\\moser\\Desktop\\cresis_project\\csv_jar\\' + flight + '.csv'
    with open(filename, 'w') as f:
        # using csv.writer method from CSV package
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(rows)

    return


def progress_bar(current, total, start_time=None, bar_length=20):
    """
    :param current: the current step number of the loop
    :param total: the number of anticipated steps in the loop
    :param bar_length: the length of the progress bar
    :return: none, but prints a progress bar to the console
    """

    if start_time and current > 0:
        elapsed = time.time() - start_time
        total_time = elapsed / current * total
        remaining = f", ~{total_time - elapsed:.1f}s/{total_time:.1f}s"
        elapsed = f", {elapsed:.1f}s"
    else:
        elapsed = ''
        remaining = ''
    current += 1  # gets us to 100% when current = total
    sys.stdout.write('\r')
    bars = int(bar_length * current / total)
    # change color per 25% chunk
    if bars < bar_length / 4:
        # sys.stdout.write(f"{BRIGHT_RED}[{'=' * bars}{' ' * (bar_length - bars)}] {100 / total * current:.1f}%{remaining}{RESET}")
        color = BRIGHT_RED
    elif bars < bar_length / 2:
        # sys.stdout.write(f"{MAGENTA}[{'=' * bars}{' ' * (bar_length - bars)}] {100 / total * current:.1f}%{remaining}{RESET}")
        color = MAGENTA
    elif bars < bar_length * 3 / 4:
        # sys.stdout.write(f"{BRIGHT_BLUE}[{'=' * bars}{' ' * (bar_length - bars)}] {100 / total * current:.1f}%{remaining}{RESET}")
        color = BRIGHT_BLUE
    else:
        # sys.stdout.write(f"{BRIGHT_GREEN}[{'=' * bars}{' ' * (bar_length - bars)}] {100 / total * current:.1f}%{remaining}{RESET}")
        color = BRIGHT_GREEN
    # sys.stdout.write(f"{color}[{'=' * bars}{' ' * (bar_length - bars)}] {100 / total * current:.1f}%{elapsed}{remaining}{RESET}"

    num_bars = f"[{'=' * bars}{' ' * (bar_length - bars)}]"
    percent = f"{100 / total * current:.1f}%"
    sys.stdout.write(f"{color}{num_bars} {percent} {elapsed} {remaining}{RESET}")
    sys.stdout.flush()  # flush the buffer


def segments_intersect(segment1, segment2):
    """
    :param segment1: a list of two points, e.g. [(lat1, lon1), (lat2, lon2)]
    :param segment2: a list of two points, e.g. [(lat1, lon1), (lat2, lon2)]
    :return: True if the segments intersect, False if they do not
    """
    line1 = LineString(segment1)
    line2 = LineString(segment2)
    return line1.intersects(line2)


def find_segment_intersection(segment1, segment2)->list:
    """
    :param segment1: a list of two points, e.g. [(lat1, lon1), (lat2, lon2)]
    :param segment2: a list of two points, e.g. [(lat1, lon1), (lat2, lon2)]
    :return: the point where the segments intersect, or None if they do not intersect
    """
    line1 = LineString(segment1)  # define a line made from two lat-lon points
    line2 = LineString(segment2)  # define a line made from two lat-lon points
    intersection = line1.intersection(line2)  # find the intersection of the two lines
    # if the intersection is the end point of one of the segments, then it is not a crossover point
    if intersection.geom_type == 'Point':
        if intersection.xy[0][0] == segment1[0][0] or intersection.xy[1][0] == segment1[0][1]:
            print("Intersection is the end point of segment 1 and is not a crossover point.")
            return None
        elif intersection.xy[0][0] == segment1[1][0] or intersection.xy[1][0] == segment1[1][1]:
            return None
        elif intersection.xy[0][0] == segment2[0][0] or intersection.xy[1][0] == segment2[0][1]:
            return None
        elif intersection.xy[0][0] == segment2[1][0] or intersection.xy[1][0] == segment2[1][1]:
            return None
        else:  # intersection is not an end point of either segment, it is a crossover point
            return [intersection.xy[0][0], intersection.xy[1][0]]
            # the format of .xy ends up being [["d"], lat], [["d"], lon] for some damn reason. No clue what "d" is. Handling the brackets here to increase readability downstream.
    return None


def cross_point(layer, seg_length, quiet=False, bar_len=20):
    """
    :param seg_length:
    :param layer: a Layer object
    :param quiet: a boolean to suppress print statements
    :return: the point where the lat-lon crosses over its own path.
    purpose: layers[0].lat and layers[0].lon are numpy arrays of the latitudes and
    longitudes for a flight path. It does not connect back to the beginning.
    This function finds the point where the path crosses over itself.
    The lat-lon of the crossover point will not be exactly the same as the
    lat-lons in the arrays, but it will be very close.
    """
    # TODO: make the crossover finder into a function and have cross_point() take the number of refinements
    # as an argument. Start with segments of seg_length and whittle down to segments of length 1 over the course of
    # the chosen number of refinements.
    verbose = not quiet
    print("Finding crossover point...")
    print("--------------------")
    # create a list of line segments of length seg_length
    path_segments = []
    segment_ends = []
    if verbose:
        print(f"Dividing the path into segments of length {seg_length}...")
    for i in range(0, len(layer.lat), seg_length):
        if i + seg_length < len(layer.lat):
            path_segments.append([(layer.lat[i], layer.lon[i]), (layer.lat[i + seg_length], layer.lon[i + seg_length])])
        else:
            path_segments.append([(layer.lat[i], layer.lon[i]), (layer.lat[-1], layer.lon[-1])])

    if verbose:
        print(f"Number of segments: {len(path_segments)}")
    print("Checking for intersections...")
    # check for intersections between the line segments
    # TODO: implement loading bar
    rough_intersections = []
    intersecting_segments = []

    start_time = time.time()
    for i in range(len(path_segments)):  # for segment #index in the number of segments
        progress_bar(i, len(path_segments), start_time, bar_length=bar_len)  # display a progress bar of segments checked
        for j in range(i + 1, len(path_segments)):  # for every other segment after segment #index
            if segments_intersect(path_segments[i], path_segments[j]):  # if the segments intersect
                intersection_point = find_segment_intersection(path_segments[i], path_segments[j])  # returns the intersection point [lat, lon] or None
                if intersection_point:  # if there is an intersection
                    rough_intersections.append(intersection_point)
                    intersecting_segments.append([i, j])  # append
                    if verbose:
                        print(f"Segments {i} and {j} intersect near "
                              f"({intersection_point[0][0]}, {intersection_point[1][0]})")
    if verbose:
        print("\nChecking for a more precise intersection...")
    fine_intersections = []
    intersection_indices = []

    start_time = time.time()
    print("")
    for seg_pair in range(len(intersecting_segments)):
        progress_bar(seg_pair, len(intersecting_segments), start_time, bar_length=bar_len)  # display a progress bar of segments checked
        seg1 = intersecting_segments[seg_pair][0]
        seg2 = intersecting_segments[seg_pair][1]

        # translate segment numbers to indices in the lat-lon arrays
        if seg1 == 0:
            seg1_start = 0
            seg1_end = seg_length
        else:
            seg1_start = seg1 * seg_length
            seg1_end = seg1_start + seg_length
        if seg2 == 0:
            seg2_start = 0
            seg2_end = seg_length
        else:
            seg2_start = seg2 * seg_length
            seg2_end = seg2_start + seg_length
        if verbose:
            print(f"segment {seg1} start: {seg1_start}, segment 1 end: {seg1_end}")
        if verbose:
            print(f"segment {seg2} start: {seg2_start}, segment 2 end: {seg2_end}")


        path_segments1 = []
        path_segments2 = []
        for i in range(seg1_end - seg1_start):
            i_1 = seg1_start + i  # the index of the first segment
            i_2 = seg2_start + i  # the index of the second segment
            path_segments1.append([(layer.lat[i_1], layer.lon[i_1]), (layer.lat[i_1 + 1], layer.lon[i_1 + 1])])
            path_segments2.append([(layer.lat[i_2], layer.lon[i_2]), (layer.lat[i_2 + 1], layer.lon[i_2 + 1])])


            """
            TODO: 12Jun24 refactor this to have path_segments be two separate lists, one for each segment rather than having the
            two segments that intersect just happen to be next to each other in the list. This will make the code more
            readable and easier to debug.

            path_segments[index] is the same as path_segments1[index]
            path_segments[index+100] is the same as path_segments2[index]
                                  (or)
            path_segments1[index] is the same as path_segments[index]
            path_segments2[index] is the same as path_segments[index+100]
            """

        for first_seg in range(len(path_segments1)):
            for sec_seg in range(len(path_segments2)):
                # if segments_intersect(path_segments1[first_seg], path_segments2[sec_seg]):  # if they intersect
                # if segments_intersect(path_segments[first_seg], path_segments[sec_seg]):  # if they intersect
                #     intersection_point = find_segment_intersection(path_segments[first_seg],
                #                                                     path_segments[sec_seg])
                if segments_intersect(path_segments1[first_seg], path_segments2[sec_seg]):  # if they intersect
                    intersection_points = find_segment_intersection(path_segments1[first_seg],
                                                                    path_segments2[sec_seg])
                    # print(section_break)
                    # print(f"Intersection points: {intersection_points}")
                    # find the intersection point, returns [lat, lon] if there is an intersection and None if not
                    # if intersection_point:
                    if intersection_points:
                        index1 = seg1_start + first_seg
                        index2 = seg2_start + sec_seg

                        # intersections.append([intersection_points])
                        # segment_ends.append([[path_segments[first_seg][0], path_segments[first_seg][1], index1],
                        #                      [path_segments[sec_seg][0], path_segments[sec_seg][1], index2]])
                        # segment_ends.append([[path_segments1[first_seg][0], path_segments1[first_seg][1], index1],
                        #                      [path_segments2[sec_seg][0], path_segments2[sec_seg][1], index2]])
                        segment_ends.append([[path_segments1[first_seg], index1, index1 + 1],
                                              [path_segments2[sec_seg], index2, index2 + 1]])

                        # debug_print(BRIGHT_BLUE, f"\npath_segments1: {path_segments1[first_seg]}\n"
                        #                          f"path_segments2: {path_segments2[sec_seg]}\n\n")

                        # fine_intersections.append([intersection_points[0][0], intersection_points[1][0]])
                        fine_intersections.append([intersection_points[0], intersection_points[1]])


                        # fine_intersections are the first two points of the segment_ends list, index.e. two endpoints on
                        # opposing legs of the X. segment_ends are all four points of the X.
                        if verbose:
                            print(f"Segments {seg1} and {seg2} intersect near indices "
                                  f"{index1} and {index2}\nThis corresponds roughly to the "
                                  f"lat-lon: ({fine_intersections[-1][0]}, {fine_intersections[-1][1]})")
                        intersection_indices.append([index1, index2])

    print("")

    print(f"Number of intersections: {len(fine_intersections)}")
    if verbose:
        print(f"Number of rough intersections: {len(rough_intersections)}")
        print(f"Number of intersection indices: {len(intersection_indices)}")
        # print(f"Indices: {intersect_indices}")
        # for index in intersect_indices:
        #     print(f"Index: {index}: ")
    # for index in range(len(intersection_indices)):
    #     print(f"Index {index}: \n"
    #           f"indices: \t{intersection_indices[index]}\n"
    #           f"lat-lon: \t({fine_intersections[index][0]}, {fine_intersections[index][1]})\n"
    #           f"segment ends: \t{segment_ends[index]}\n"
    #           f"lat-lon by layer: \t({layer.lat[intersection_indices[index][0]]}, {layer.lon[intersection_indices[index][0]]})")

    # print(f"Intersection at index {intersection_indices[0]} and {intersection_indices[1]}")
    for i in range(len(intersection_indices)):
        # TODO Error 1: correct for the fine intersection points being wrong for some reason
        # (lat is close but lon is 6 degrees off in the 20181112_02 flight)
        fine_intersections[i][0] = layer.lat[intersection_indices[i][0]]
        if layer.lon[intersection_indices[i][0]] < 0:
            fine_intersections[i][1] = layer.lon[intersection_indices[i][0]] + 360
        else:
            fine_intersections[i][1] = layer.lon[intersection_indices[i][0]]
    print("--------------------\n")

    return fine_intersections, intersection_indices, segment_ends


def s_to_ms(x, pos):
    """
    :param x: the x value
    :param pos: the position
    :return: the x value in milliseconds
    """
    return '%1.1f' % (x * 1e6)#


def ms_to_s(x, pos):
    """
    :param x: the x value
    :param pos: the position
    :return: the x value in seconds
    """
    return '%1.1f' % (x * 1e-6)

def gps_time_to_date(gps_time):
    """
    :param gps_time: the Unix Epoch time in seconds
    :return: the gps time in a tuple of (year, month, day, hour, minute, second)
    """

    datetime_object = datetime.datetime.fromtimestamp(gps_time)

    return datetime_object


def time_difference(time1, time2):
    """
    :param time1: a datetime object
    :param time2: a datetime object
    :return: the difference between the two times in seconds
    """
    return (time2 - time1).total_seconds()


def slope_around_index(layer, index, window_size=100):
    """
    :param layer: a Layer object
    :param index: the index of the point in the layer
    :param window_size: the number of points to use in the slope calculation
    :return: the slope of the layer at the given index
    """
    # calculate the slope of the layer at the given index
    # slope = rise / run

    # rise = the difference in twtt between the point at index - window_size and the point at index + window_size
    # run = the difference in meters between the point at index - window_size and the point at index + window_size
    rise_twtt = layer.twtt[index + window_size] - layer.twtt[index - window_size]
    rise = twtt_to_depth(rise_twtt, 1.77)
    run = latlon_dist((layer.lat[index - window_size], layer.lon[index - window_size]),
                        (layer.lat[index + window_size], layer.lon[index + window_size]))
    # print(f"rise: {round(rise, 2)}m, run: {round(run, 2)}m")
    slope = rise / run
    return slope


def average_slope_around_index(layer, index, window_size=100):
    """
    :param layer: a Layer object
    :param index: the index of the point in the layer
    :param window_size: the number of points to use in the slope calculation
    :return: the average slope of the layer at the given index
    """
    # calculate the average slope of the layer around the given index using a window of size window_size
    # slope = rise / run

    dist_ave_before = 0
    dist_ave_after = 0
    twtt_ave_before = 0
    twtt_ave_after = 0

    # uses twtt and not corrected_twtt → shows slope correctly. i.e. not normalized to surface
    for i in range(index - window_size, index):
        dist_ave_before += latlon_dist((layer.lat[i], layer.lon[i]), (layer.lat[i + 1], layer.lon[i + 1]))
        twtt_ave_before += layer.twtt[i]
    for i in range(index, index + window_size):
        dist_ave_after += latlon_dist((layer.lat[i], layer.lon[i]), (layer.lat[i + 1], layer.lon[i + 1]))
        twtt_ave_after += layer.twtt[i]
    # print(f"distance in the {window_size} points before the index: {dist_ave_before}")
    # print(f"distance in the {window_size} points after the index: {dist_ave_after}")
    # print(f"twtt in the {window_size} points before the index: {twtt_ave_before}")
    # print(f"twtt in the {window_size} points after the index: {twtt_ave_after}")
    dist_ave_before /= window_size
    dist_ave_after /= window_size
    twtt_ave_before /= window_size
    twtt_ave_after /= window_size
    # print(f"average distance before the index: {dist_ave_before}")
    # print(f"average distance after the index: {dist_ave_after}")
    # print(f"average twtt before the index: {twtt_to_depth(twtt_ave_before, 1.77)}")
    # print(f"average twtt after the index: {twtt_to_depth(twtt_ave_after, 1.77)}")
    rise = twtt_to_depth(twtt_ave_after, 1.77) - twtt_to_depth(twtt_ave_before, 1.77)
    # rise = twtt_to_depth(rise_twtt, 1.77)
    # print(f"rise: {rise}m")
    run = dist_ave_after + dist_ave_before
    # print(f"run: {run}m")
    slope = rise / run
    return slope


def twtt_to_depth(twtt, refractive_index=1.77):
    """
    :param twtt: the two way travel time in seconds
    :param refractive_index: the refractive index of the ice
    :return: the depth in meters
    """
    # n = c / v
    # v = c / n
    n = refractive_index
    c = 299792458  # m/s
    v = c / n
    depth = twtt * v / 2
    return depth


def filenameerizer(directory, name_part1, name_part2='', name_part3=''):
    """
    supports up to three parts of a compound file name
    :param name_part1: part 1
    :param name_part2: part 2
    :param name_part3: part 3
    :param directory:
    :return: a complete path to a file
    """
    file_name = name_part1 + name_part2 + name_part3
    file_path = directory + file_name
    return file_path


def save_posit(posit):
    """
    :param posit: a Twtt_Posit object
    :return: nothing
    """
    # save posit to a pickle file
    print("Saving posit...")
    print(section_break)
    pickle.dump(posit, open("posit.pickle", "wb"))
    # print("posit.pickle saved in local directory of this python file.")
    # print(section_break + "\n")


def plane_velocity_at_latlon(latlon1, latlon2, time1, time2):
    """
    :param latlon1: a tuple of (lat, lon)
    :param latlon2: a tuple of (lat, lon)
    :param time1: the time at latlon1
    :param time2: the time at latlon2
    :return: the velocity of the plane between the two lat-lon points in meters per second
    """
    dist = latlon_dist(latlon1, latlon2)
    print(f"dist: {dist}")
    time = time2 - time1
    print(f"time2: {time2}, time1: {time1}, time: {time}")

    velocity = dist / time
    velocitykmh = velocity * 3600 / 1000 # convert to km/h
    return velocity, velocitykmh


def find_heading(layer, index, window_size=100):
    """
    :param layer: a Layer object
    :param index: the index of the point in the layer
    :param window_size: the number of points to use in the slope calculation
    :return: the bearing of the current that flew through the points.
    This has nothing to do with the slope of the layer. only the lat-lon points.
    """
    # print the lat-lon points
    # print(f"lat-lon input to find_heading:"
    #       f"\n({layer.lat[index]}, {layer.lon[index]})")
    geodesic = pyproj.Geod(ellps='WGS84')
    lon = layer.lon[index]
    lat = layer.lat[index]
    lon1 = layer.lon[index - window_size]
    lat1 = layer.lat[index - window_size]
    lon2 = layer.lon[index + window_size]
    lat2 = layer.lat[index + window_size]

    # print(f"lat-lons determined by find_heading:"
    #       f"\n({lat1}, {lon1}), ({lat2}, {lon2})")
    delta_lon1 = lon - lon1
    delta_lat1 = lat - lat1
    delta_lon2 = lon2 - lon
    delta_lat2 = lat2 - lat
    # print(f"delta_lon1: {delta_lon1}, delta_lat1: {delta_lat1}, delta_lon2: {delta_lon2}, delta_lat2: {delta_lat2}")
    fwd_azimuth, back_azimuth, distance = geodesic.inv(lon1, lat1, lon2, lat2)
    return fwd_azimuth


def latlon_dist(latlon1, latlon2):
    """
    :param latlon1: a tuple of (lat, lon)
    :param latlon2: a tuple of (lat, lon)
    :return: the distance between the two lat-lon points in meters.
    d = 2R × sin⁻¹(√[sin²((θ₂ - θ₁)/2) + cosθ₁ × cosθ₂ × sin²((φ₂ - φ₁)/2)])
    """
    latlon1 = (float(latlon1[0]) * math.pi / 180, float(latlon1[1]) * math.pi / 180)
    latlon2 = (float(latlon2[0]) * math.pi / 180, float(latlon2[1]) * math.pi / 180)
    # convert the lat-lon points to radians
    R = 6371 * 1000  # radius of the earth in meters

    dist = 2 * R * math.asin(math.sqrt(
        math.sin((latlon2[0] - latlon1[0]) / 2) ** 2 + math.cos(latlon1[0]) * math.cos(latlon2[0]) * math.sin(
            (latlon2[1] - latlon1[1]) / 2) ** 2))
    # print(f"d: {d}")
    return dist


def twtt_at_point(read_layer, surface_layer, indices, corrected=True, quiet=False):
    """
    :param read_layer: the layer that is being compared to the surface layer
    :param surface_layer: the surface layer of the ice sheet
    :param indices: a list of indices in the lat-lon arrays where the flight path
    crosses over itself
    :return: the twtt at the crossover point
    """
    if not quiet:
        print("Finding twtt at crossover point...")
        print(section_break)
        print(f"Number of crossover points: {len(indices)}"
              f"\nFirst crossover point is at indices {indices[0][0]} and {indices[0][1]}")
    twtt = []
    for index in indices:
        if corrected:
            # print(f"Debug: \n\tIndex: {index}")
            adjusted_twtt1 = read_layer.twtt[index[0]] - surface_layer.twtt[index[0]]
            adjusted_twtt2 = read_layer.twtt[index[1]] - surface_layer.twtt[index[1]]
            if not quiet:
                print(f"twtt at index {index[0]}: {read_layer.twtt[index[0]]}")
                print(f"twtt at index {index[1]}: {read_layer.twtt[index[1]]}")
                print(f"twtt at index {index[0]} after surface adjustment: {adjusted_twtt1}")
                print(f"twtt at index {index[1]} after surface adjustment: {adjusted_twtt2}")
                print(f"twtt difference: {abs(adjusted_twtt1 - adjusted_twtt2)}")
                print(f"gps time at index {index[0]}: {read_layer.gps_time[index[0]]}")
                print(f"gps time at index {index[1]}: {read_layer.gps_time[index[1]]}")
            twtt.append([adjusted_twtt1, adjusted_twtt2])
        else:
            twtt.append([read_layer.twtt[index[0]], read_layer.twtt[index[1]]])
    if not quiet:
        print(section_break + "\n")
    return twtt


def plot_layers_at_cross(layers, intersection_indices, intersection_points, zoom=False, refractive_index=1.77,
                         cross_index=0, filename=None):
    """
    :param layers: a list of Layer objects
    :param intersection_indices: a list of indices in the lat-lon arrays where the flight path
    crosses over itself
    :param intersection_points: a list of lat-lon points where the flight path crosses over itself
    :return: nothing (plots the layers and the map)
    """
    plt.figure(figsize=(16, 8), layout='constrained')
    print("Plotting layers...")
    print(section_break)
    print("Adjusting for surface twtt...")
    for layer in layers:
        corrected_layer = layer.twtt - layers[0].twtt
        layer.twtt_corrected = corrected_layer

    # ax2 will be the layer plot
    # plt.subplot(1, 2, 1)

    # plot the layer depths vs index for 500 points before and after the first
    # crossover point for each layer.
    # also plot the layer depths vs index for 500 points before and after the
    # second crossover point for each layer.
    offset = 500
    # plot the corrected twtt for each layer
    plt.plot(
        layers[0].twtt_corrected[intersection_indices[0][0] - offset:intersection_indices[cross_index][0] + offset],
        label=layers[0].layer_name)
    plt.plot(
        layers[1].twtt_corrected[intersection_indices[0][0] - offset:intersection_indices[cross_index][0] + offset],
        label=layers[1].layer_name + ' segment 1')
    plt.plot(
        layers[1].twtt_corrected[intersection_indices[0][1] - offset:intersection_indices[cross_index][1] + offset],
        label=layers[1].layer_name + ' segment 2')

    # plot uncorrected twtt for each layer
    # plt.plot(layers[0].twtt[intersect_indices[0][0] - offset:intersect_indices[0][0] + offset],
    #             label=layers[0].layer_name)
    # plt.plot(layers[1].twtt[intersect_indices[0][0] - offset:intersect_indices[0][0] + offset],
    #             label=layers[1].layer_name + ' segment 1')
    # plt.plot(layers[1].twtt[intersect_indices[0][1] - offset:intersect_indices[0][1] + offset],
    # label=layers[1].layer_name + ' segment 2')

    # invert the y-axis because the twtt increases with depth
    plt.gca().invert_yaxis()
    # plot the crossover point on the plot
    plt.scatter(offset, twtt_at_point(layers[1], layers[0],
                                      intersection_indices, quiet=True)[0][0], color='red',
                label='X Point 1')
    plt.scatter(offset, twtt_at_point(layers[1], layers[0],
                                      intersection_indices, quiet=True)[0][1], color='green',
                label='X Point 2')

    # print the twtt at the crossover point on both segments
    twtt = twtt_at_point(layers[1], layers[0], intersection_indices, quiet=True)[0]
    print(f"twtt: {twtt}")

    # plot a line at the crossover point
    plt.axvline(x=offset, color='black', label='X Point', linestyle='--', linewidth=0.3)

    # set the y axis to be in microseconds instead of seconds
    plt.ylabel(f"Adjusted Two Way Travel Time ({chr(956)}s)")
    plt.xlabel("Index")

    # force the y values to be displayed in 1e-6 ticks (microseconds) instead of 1e-5 ticks (tens of microseconds)
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0), useMathText=True)

    def s_to_ms(x, pos):
        """
        :param x: the x value
        :param pos: the position
        :return: the x value in milliseconds
        """
        return '%1.1f' % (x * 1e6)

    # set the y axis to be in microseconds instead of seconds
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(s_to_ms))
    plt.legend(fontsize='smaller', loc='upper right', bbox_to_anchor=(1, 0.9))

    # make the right side y axis show the depth in meters by converting the twtt to depth using the refractive index
    min_y, max_y = plt.ylim()
    n = int(refractive_index)
    c = 299792458  # m/s
    v = c / n
    # depth = twtt * v / 2
    scale_factor = v / 2
    print(f"scale factor: {scale_factor}")
    plt.twinx()
    plt.ylim(min_y * scale_factor, max_y * scale_factor)
    plt.ylabel("Depth (m)")

    # make the top of the x axis be the distance in meters by converting the lat-lon to distance using the haversine formula
    min_x, max_x = plt.xlim()
    scale_factor = latlon_dist((layers[0].lat[0], layers[0].lon[0]), (layers[0].lat[1], layers[0].lon[1]))
    print(f"scale factor: {scale_factor}")
    plt.twiny()
    plt.xlim(min_x * scale_factor, max_x * scale_factor)
    plt.xlabel("Distance (m)")

    plt.title("Adjusted Two Way Travel Time vs Index")
    if filename:
        # plt.savefig(f"{filename}.png", dpi=250)
        plt.savefig(f"C:\\Users\\moser\\Desktop\\cresis_project\\screens\\{filename}_layers.png", dpi=250)

    plt.show()


def plot_map(layers, intersection_indices, intersection_points, iceflow_data, season, flight,  zoom=False, cross_index=0, filename=None):
    """
    plot the map
    """
    plt.figure(figsize=(16, 16), layout='constrained')
    print("Plotting map...")
    # TODO: add an offset to the zoom settings so that the crossover point is in the center of the zoomed in map
    offset = 500  # this is not that offset

    # this code sets up a polar stereographic map of antarctica with the South Pole in the center
    zoom_out_to_continent = not zoom
    if zoom_out_to_continent:
        llcrnrx = -400000
        llcrnry = -400000
        urcrnrx = 250000
        urcrnry = 250000
    else:
        llcrnrx = -100000
        llcrnry = -100000
        urcrnrx = 100000
        urcrnry = 100000
    lat_0 = intersection_points[cross_index][0]
    lon_0 = intersection_points[cross_index][1]
    # print(f"debug: lat_0: {lat_0}, lon_0: {lon_0}")
    m = Basemap(projection='ortho', lat_0=lat_0, lon_0=lon_0, llcrnrx=llcrnrx,
                llcrnry=llcrnry, urcrnrx=urcrnrx, urcrnry=urcrnry, resolution='c')

    m.drawcoastlines()
    m.fillcontinents(color='grey', lake_color='aqua')
    m.drawparallels(np.arange(-80., 81., 20.))
    m.drawmeridians(np.arange(-180., 181., 20.))
    m.drawmapboundary(fill_color='aqua')

    # plot the flight path
    m.plot(layers[0].lon, layers[0].lat, latlon=True, color='lightgreen', linewidth=1)
    # plot the section of the flight path in the plot above
    m.plot(layers[0].lon[intersection_indices[0][0] - offset:intersection_indices[0][0] + offset],
           layers[0].lat[intersection_indices[0][0] - offset:intersection_indices[0][0] + offset], latlon=True,
           color='red', linewidth=1)
    m.plot(layers[0].lon[intersection_indices[0][1] - offset:intersection_indices[0][1] + offset],
           layers[0].lat[intersection_indices[0][1] - offset:intersection_indices[0][1] + offset], latlon=True,
           color='green', linewidth=1)
    # plot labels for the flight paths at their start points
    plt.text(
        m(layers[0].lon[intersection_indices[0][0] - offset], layers[0].lat[intersection_indices[0][0] - offset])[0],
        m(layers[0].lon[intersection_indices[0][0] - offset], layers[0].lat[intersection_indices[0][0] - offset])[1],
        '\nsegment 1', fontsize='smaller', fontweight='bold', ha='right', va='top', color='red')
    plt.text(
        m(layers[0].lon[intersection_indices[0][1] - offset], layers[0].lat[intersection_indices[0][1] - offset])[0],
        m(layers[0].lon[intersection_indices[0][1] - offset], layers[0].lat[intersection_indices[0][1] - offset])[1],
        '\nsegment 2', fontsize='smaller', fontweight='bold', ha='left', va='top', color='green')
    # plot the South Pole
    # m.scatter(0, -90, latlon=True, color='black', linewidth=1, label='South Pole')
    # plot the crossover points
    for point in intersection_points:
        # m.scatter(point[1], point[0], latlon=True, color='darkred', linewidth=10, label='Crossover Point')
        plt.scatter(m(point[1], point[0])[0], m(point[1], point[0])[1], color='darkred', linewidth=5,
                    label='Crossover Point')
        plt.text(m(point[1], point[0])[0], m(point[1], point[0])[1] - 10000,
                 f'Crossover Point {intersection_points.index(point) + 1}\n\n',
                 fontsize='smaller', fontweight='bold', ha='center', va='top', color='darkred')

    # m.scatter(intersection_points[cross_index][1]+1, intersection_points[cross_index][0]+1, latlon=True, color='darkred',
    # linewidth=1, label='Crossover Point')
    # plt.text(m(intersection_points[cross_index][1], intersection_points[cross_index][0])[0],
    #          m(intersection_points[cross_index][1], intersection_points[cross_index][0])[1] - 10000,
    #          'Crossover Point\n\n',
    #          fontsize='smaller', fontweight='bold', ha='center', va='top', color='darkred')

    # plot the the ice flow direction at the crossover point
    for i in range(len(intersection_indices)):
        nearest_x_index, nearest_y_index = xy_to_nearest_unmasked_index(intersection_points[i][0],
                                                                        intersection_points[i][1], iceflow_data,
                                                                        max_radius=10)
    flow = flow_at_x_y_index(nearest_x_index, nearest_y_index, iceflow_data)

    flow_heading = xyindex_vector_to_heading(nearest_x_index, nearest_y_index, flow[0], flow[1])[0]
    # m.quiver(intersection_points[0][1], intersection_points[0][0], 1000 * np.cos(np.radians(flow_heading)),
    #          1000 * np.sin(np.radians(flow_heading)), latlon=True, color='blue', label='Ice Flow Vector')
    # plot the ice flow vector in the upper right corner as a quiver
    m.quiver(intersection_points[0][1] + 2.5, intersection_points[0][0] + 0.7, 10000 * np.cos(np.radians(flow_heading)),
             10000 * np.sin(np.radians(flow_heading)), latlon=True, color='blue', label='Ice Flow Vector')
    plt.text(m(intersection_points[0][1] + 2.5, intersection_points[0][0] + 0.6)[0],
             m(intersection_points[0][1] + 5, intersection_points[0][0] + 0.7)[1], 'Ice Flow Vector\n\n',
             fontsize='smaller', fontweight='bold', ha='center', va='top', color='red')

    x, y = m(0, -90)
    # plt.text(x, y, '\nSouth Pole', fontsize='smaller', fontweight='bold', ha='center', va='top', color='black')
    plt.title("Lat-Lon Map")
    # set tight layout
    # plt.tight_layout()

    # save the plot
    if filename:
        # plt.savefig(f"{filename}.png", dpi=250)
        plt.savefig(f"C:\\Users\\moser\\Desktop\\cresis_project\\screens\\{filename}_map.png", dpi=250)

    plt.show()

    print("plotted map")
    print(section_break + "\n")


def plot_map_cartopy(layers, intersection_indices, intersection_points, iceflow_data, season, flight,  zoom=False, cross_index=0, filename=None):
    """

    """
    plt.figure(figsize=(16, 16), layout='constrained')
    print("Plotting map...")
    # TODO: add an offset to the zoom settings so that the crossover point is in the center of the zoomed in map
    offset = 500  # this is not that offset
    dimension = 5
    crs_epsg = ccrs.SouthPolarStereo(central_longitude=0.0, true_scale_latitude=-71)
    fig = plt.figure(figsize=(16, 16))
    ax = plt.axes(projection=crs_epsg)

    # set the centerpoint to the first crossover point
    ax.set_extent([intersection_points[0][1] - dimension, intersection_points[0][1] + dimension,
                   intersection_points[0][0] - dimension, intersection_points[0][0] + dimension], crs_epsg)

    ax.coastlines()
    ax.gridlines()
    ax.add_feature(cfeature.LAND, zorder=0, facecolor='lightgrey')
    ax.add_feature(cfeature.OCEAN, zorder=0, edgecolor='black')

    # set the continent fill to a light grey

    ax.plot(layers[1].lon, layers[1].lat, color='black', linewidth=3)

    # plot the crossover points
    # for point in intersection_points:
    #     plot.scatter(point[1], point[0], color='red', linewidth=5, label='Crossover Point')
    #     plt.text(point[1], point[0], f'Crossover Point {intersection_points.index(point) + 1}\n\n',
    #              fontsize='smaller', fontweight='bold', ha='center', va='top', color='darkred')

    # plot a single crossover point
    ax.scatter(intersection_points[0][1], intersection_points[0][0], color='red', linewidth=5, label='Crossover Point')

    # plot the section of the flight path in the plot above
    ax.plot(layers[0].lon[intersection_indices[0][0] - offset:intersection_indices[0][0] + offset],
            layers[0].lat[intersection_indices[0][0] - offset:intersection_indices[0][0] + offset], color='red',
            linewidth=1)

    ax.plot(layers[0].lon[intersection_indices[0][1] - offset:intersection_indices[0][1] + offset],
            layers[0].lat[intersection_indices[0][1] - offset:intersection_indices[0][1] + offset], color='lightgreen',
            linewidth=1)

    # plot labels for the flight paths at their start points
    plt.text(intersection_points[0][1], intersection_points[0][0], '\nsegment 1', fontsize='smaller', fontweight='bold',
             ha='right', va='top', color='red')
    # plt.text(intersection_points[0][1], intersection_points[0][0], '\nsegment 2', fontsize='smaller', fontweight='bold', ha='left', va='top', color='green')

    # plot the ice flow direction at the crossover point
    nearest_x_index, nearest_y_index = xy_to_nearest_unmasked_index(intersection_points[0][0],
                                                                    intersection_points[0][1], iceflow_data,
                                                                    max_radius=10)
    flow = flow_at_x_y_index(nearest_x_index, nearest_y_index, iceflow_data)
    flow_heading = xyindex_vector_to_heading(nearest_x_index, nearest_y_index, flow[0], flow[1])[0]

    # plot the ice flow vector in the upper right corner as a quiver
    ax.quiver(intersection_points[0][1] + 2.5, intersection_points[0][0] + 0.7,
              10000 * np.cos(np.radians(flow_heading)),
              10000 * np.sin(np.radians(flow_heading)), color='blue', label='Ice Flow Vector')
    plt.text(intersection_points[0][1] + 2.5, intersection_points[0][0] + 0.6, 'Ice Flow Vector\n\n',
             fontsize='smaller', fontweight='bold', ha='center', va='top', color='blue')

    print(f"iceflow direction: {flow_heading}")

    plt.title(f"Crossover map for {season}{flight}")
    # save the plot
    if filename:
        # plt.savefig(f"{filename}.png", dpi=250)
        plt.savefig(f"C:\\Users\\moser\\Desktop\\cresis_project\\screens\\{filename}_map.png", dpi=300)

    print("plotted map")
    print(section_break + "\n")


# def plot_layers_at_cross(layers, intersect_indices, intersection_points, zoom=False, refractive_index=1.77,
#                          cross_index=0):
#     """
#     :param layers: a list of Layer objects
#     :param intersect_indices: a list of indices in the lat-lon arrays where the flight path
#     crosses over itself
#     :param intersection_points: a list of lat-lon points where the flight path crosses over itself
#     :return: nothing (plots the layers and the map)
#     """
#     plt.figure(figsize=(24, 12), layout='constrained')
#     print("Plotting layers and map...")
#     print(section_break)
#     print("Adjusting for surface twtt...")
#     for layer in layers:
#         corrected_layer = layer.twtt - layers[0].twtt
#         layer.twtt_corrected = corrected_layer
#
#     # ax2 will be the layer plot
#     plt.subplot(1, 2, 1)
#
#     # plot the layer depths vs index for 500 points before and after the first
#     # crossover point for each layer.
#     # also plot the layer depths vs index for 500 points before and after the
#     # second crossover point for each layer.
#     offset = 500
#     # plot the corrected twtt for each layer
#     plt.plot(
#         layers[0].twtt_corrected[intersect_indices[0][0] - offset:intersect_indices[cross_index][0] + offset],
#         label=layers[0].layer_name)
#     plt.plot(
#         layers[1].twtt_corrected[intersect_indices[0][0] - offset:intersect_indices[cross_index][0] + offset],
#         label=layers[1].layer_name + ' segment 1')
#     plt.plot(
#         layers[1].twtt_corrected[intersect_indices[0][1] - offset:intersect_indices[cross_index][1] + offset],
#         label=layers[1].layer_name + ' segment 2')
#
#     # plot uncorrected twtt for each layer
#     # plt.plot(layers[0].twtt[intersect_indices[0][0] - offset:intersect_indices[0][0] + offset],
#     #             label=layers[0].layer_name)
#     # plt.plot(layers[1].twtt[intersect_indices[0][0] - offset:intersect_indices[0][0] + offset],
#     #             label=layers[1].layer_name + ' segment 1')
#     # plt.plot(layers[1].twtt[intersect_indices[0][1] - offset:intersect_indices[0][1] + offset],
#     # label=layers[1].layer_name + ' segment 2')
#
#     # invert the y-axis because the twtt increases with depth
#     plt.gca().invert_yaxis()
#     # plot the crossover point on the plot
#     plt.scatter(offset, twtt_at_point(layers[1], layers[0],
#                                       intersect_indices, quiet=True)[0][0], color='red',
#                 label='X Point 1')
#     plt.scatter(offset, twtt_at_point(layers[1], layers[0],
#                                       intersect_indices, quiet=True)[0][1], color='green',
#                 label='X Point 2')
#     # plot a line at the crossover point
#     plt.axvline(x=offset, color='black', label='X Point', linestyle='--', linewidth=0.3)
#
#     # set the y axis to be in nanoseconds instead of seconds
#     plt.ylabel("Adjusted Two Way Travel Time (ns)")
#     plt.xlabel("Index")
#
#     # force the y values to be displayed in 1e-6 ticks (microseconds) instead of 1e-5 ticks (tens of microseconds)
#     plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0), useMathText=True)
#
#     def s_to_ms(x, pos):
#         """
#         :param x: the x value
#         :param pos: the position
#         :return: the x value in milliseconds
#         """
#         return '%1.1f' % (x * 1e6)
#
#     # set the y axis to be in microseconds instead of seconds
#     plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(s_to_ms))
#
#     # make the right side y axis show the depth in meters by converting the twtt to depth using the refractive index
#     min_y, max_y = plt.ylim()
#     n = refractive_index
#     c = 299792458  # m/s
#     v = c / n
#     # depth = twtt * v / 2
#     scale_factor = v / 2
#     print(f"scale factor: {scale_factor}")
#     plt.twinx()
#     plt.ylim(min_y * scale_factor, max_y * scale_factor)
#     plt.ylabel("Depth (m)")
#
#     # make the top of the x axis be the distance in meters by converting the lat-lon to distance using the haversine formula
#     min_x, max_x = plt.xlim()
#     scale_factor = latlon_dist((layers[0].lat[0], layers[0].lon[0]), (layers[0].lat[1], layers[0].lon[1]))
#     print(f"scale factor: {scale_factor}")
#     plt.twiny()
#     plt.xlim(min_x * scale_factor, max_x * scale_factor)
#     plt.xlabel("Distance (m)")
#
#     plt.title("Adjusted Two Way Travel Time vs Index")
#     plt.legend(["legend"], fontsize='smaller', loc='upper right', bbox_to_anchor=(1.1, 1.1))
#
#     """
#     plot the map
#     """
#     plt.subplot(1, 2, 2)
#
#     # TODO: add an offset to the zoom settings so that the crossover point is in the center of the zoomed in map
#
#     # # this code sets up a polar stereographic map of antarctica with the South Pole in the center
#     zoom_out_to_continent = not zoom
#     if zoom_out_to_continent:
#         llcrnrx = -400000
#         llcrnry = -400000
#         urcrnrx = 250000
#         urcrnry = 250000
#     else:
#         llcrnrx = -100000
#         llcrnry = -100000
#         urcrnrx = 100000
#         urcrnry = 100000
#     # lat_0 = intersection_points[cross_index][0]
#     # lon_0 = intersection_points[cross_index][1]
#     m = Basemap(projection='ortho', lat_0=lat_0, lon_0=lon_0, llcrnrx=llcrnrx,
#                 llcrnry=llcrnry, urcrnrx=urcrnrx, urcrnry=urcrnry, resolution='c')
#
#     m.drawcoastlines()
#     m.fillcontinents(color='grey', lake_color='aqua')
#     m.drawparallels(np.arange(-80., 81., 20.))
#     m.drawmeridians(np.arange(-180., 181., 20.))
#     m.drawmapboundary(fill_color='aqua')
#
#     # plot the flight path
#     m.plot(layers[0].lon, layers[0].lat, latlon=True, color='lightgreen', linewidth=1)
#     # plot the section of the flight path in the plot above
#     m.plot(layers[0].lon[intersect_indices[0][0] - offset:intersect_indices[0][0] + offset],
#            layers[0].lat[intersect_indices[0][0] - offset:intersect_indices[0][0] + offset], latlon=True,
#            color='red', linewidth=1)
#     m.plot(layers[0].lon[intersect_indices[0][1] - offset:intersect_indices[0][1] + offset],
#            layers[0].lat[intersect_indices[0][1] - offset:intersect_indices[0][1] + offset], latlon=True,
#            color='green', linewidth=1)
#     # plot labels for the flight paths at their start points
#     plt.text(
#         m(layers[0].lon[intersect_indices[0][0] - offset], layers[0].lat[intersect_indices[0][0] - offset])[
#             0],
#         m(layers[0].lon[intersect_indices[0][0] - offset], layers[0].lat[intersect_indices[0][0] - offset])[
#             1], '\nsegment 1', fontsize='smaller', fontweight='bold', ha='right', va='top', color='red')
#     plt.text(
#         m(layers[0].lon[intersect_indices[0][1] - offset], layers[0].lat[intersect_indices[0][1] - offset])[
#             0],
#         m(layers[0].lon[intersect_indices[0][1] - offset], layers[0].lat[intersect_indices[0][1] - offset])[
#             1], '\nsegment 2', fontsize='smaller', fontweight='bold', ha='left', va='top', color='green')
#     # plot the South Pole
#     # m.scatter(0, -90, latlon=True, color='black', linewidth=1, label='South Pole')
#     # plot the crossover points
#     for point in intersection_points:
#         m.scatter(point[1], point[0], latlon=True, color='darkred', linewidth=1, label='Crossover Point')
#         plt.text(m(point[1], point[0])[0], m(point[1], point[0])[1] - 10000, 'Crossover Point\n\n',
#                  fontsize='smaller', fontweight='bold', ha='center', va='top', color='darkred')
#
#     # m.scatter(intersection_points[cross_index][1], intersection_points[cross_index][0], latlon=True, color='darkred',
#     #           linewidth=1, label='Crossover Point')
#     # plt.text(m(intersection_points[cross_index][1], intersection_points[cross_index][0])[0],
#     #          m(intersection_points[cross_index][1], intersection_points[cross_index][0])[1] - 10000,
#     #          'Crossover Point\n\n',
#     #          fontsize='smaller', fontweight='bold', ha='center', va='top', color='darkred')
#
#     # plot the crossover line
#
#     x, y = m(0, -90)
#     # plt.text(x, y, '\nSouth Pole', fontsize='smaller', fontweight='bold', ha='center', va='top', color='black')
#     plt.title("Lat-Lon Map")
#     # set tight layout
#     # plt.tight_layout()
#
#     # save the plot
#     # plt.savefig("layer_plot.png", dpi=250)
#
#     plt.show()
#
#     print("plotted map")
#     print(section_break + "\n")
#


def fancymap(layers, intersection_indices, intersection_points, zoom=False, refractive_index=1.77,
                         cross_index=0, dpi=1500):
    """
    :param layers: a list of Layer objects
    :param intersection_indices: a list of indices in the lat-lon arrays where the flight path
    crosses over itself
    :param intersection_points: a list of lat-lon points where the flight path crosses over itself
    :return: nothing (plots the layers and the map)
    """
    offset = 500

    plt.figure(figsize=(12, 12))
    print("Plotting layers and map...")
    print(section_break)
    print("Adjusting for surface twtt...")
    for layer in layers:
        corrected_layer = layer.twtt - layers[0].twtt
        layer.twtt_corrected = corrected_layer

    """
    plot the map
    """

    lat_0 = intersection_points[cross_index][0]
    lon_0 = intersection_points[cross_index][1]
    m = Basemap(projection='ortho', lat_0=lat_0, lon_0=lon_0, llcrnrx=-50000, llcrnry=-50000, urcrnrx=50000,
                urcrnry=50000,
                resolution='c')

    m.drawcoastlines()
    m.fillcontinents(color='grey', lake_color='aqua')
    m.drawparallels(np.arange(-80., 81., 20.))
    m.drawmeridians(np.arange(-180., 181., 20.))
    m.drawmapboundary(fill_color='aqua')

    # plot the flight path
    m.plot(layers[0].lon, layers[0].lat, latlon=True, color='lightgreen', linewidth=1)
    # plot the section of the flight path in the plot above
    m.plot(layers[0].lon[intersection_indices[0][0] - offset:intersection_indices[0][0] + offset],
           layers[0].lat[intersection_indices[0][0] - offset:intersection_indices[0][0] + offset], latlon=True,
           color='red', linewidth=1)
    m.plot(layers[0].lon[intersection_indices[0][1] - offset:intersection_indices[0][1] + offset],
           layers[0].lat[intersection_indices[0][1] - offset:intersection_indices[0][1] + offset], latlon=True,
           color='green', linewidth=1)
    # plot labels for the flight paths at their start points
    plt.text(
        m(layers[0].lon[intersection_indices[0][0] - offset], layers[0].lat[intersection_indices[0][0] - offset])[
            0],
        m(layers[0].lon[intersection_indices[0][0] - offset], layers[0].lat[intersection_indices[0][0] - offset])[
            1], '\nsegment 1', fontsize='smaller', fontweight='bold', ha='right', va='top', color='red')
    plt.text(
        m(layers[0].lon[intersection_indices[0][1] - offset], layers[0].lat[intersection_indices[0][1] - offset])[
            0],
        m(layers[0].lon[intersection_indices[0][1] - offset], layers[0].lat[intersection_indices[0][1] - offset])[
            1], '\nsegment 2', fontsize='smaller', fontweight='bold', ha='left', va='top', color='green')
    # plot the South Pole
    m.scatter(0, -90, latlon=True, color='black', linewidth=1, label='South Pole')
    # plot the crossover points
    # for point in intersection_points:
    #     m.scatter(point[1], point[0], latlon=True, color='darkred', linewidth=1, label='Crossover Point')
    #     plt.text(m(point[1], point[0])[0], m(point[1], point[0])[1] - 10000, 'Crossover Point\n\n',
    #              fontsize='smaller', fontweight='bold', ha='center', va='top', color='darkred')

    m.scatter(intersection_points[cross_index][1], intersection_points[cross_index][0], latlon=True, color='darkred',
              linewidth=1, label='Crossover Point')
    plt.text(m(intersection_points[cross_index][1], intersection_points[cross_index][0])[0],
             m(intersection_points[cross_index][1], intersection_points[cross_index][0])[1] - 10000,
             'Crossover Point\n\n',
             fontsize='smaller', fontweight='bold', ha='center', va='top', color='darkred')

    # plot the crossover line

    x, y = m(0, -90)
    plt.text(x, y, '\nSouth Pole', fontsize='smaller', fontweight='bold', ha='center', va='top', color='black')
    plt.title("Lat-Lon Map")
    # set tight layout
    # plt.tight_layout()

    # save the plot
    plt.savefig("fancy_map_only.png", dpi=dpi)

    plt.show()

    print("plotted map")
    print(section_break + "\n")


"""
Iceflow library:
"""

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
    file_name = f"C:\\Users\\{username}\\Documents\\cresis\\iceflow\\antarctic_ice_vel_phase_map_v01.nc"
    iceflow_file = Dataset(file_name, "r")

    print(iceflow_file.variables.keys())

    def serialize_variable(var):
        info = {
            "type": str(var.dtype),
            "dimensions": var.dimensions,
            "shape": var.shape,
            "attributes": {attr: var.getncattr(attr) for attr in var.ncattrs()}
        }
        return info

    dir = f"C:\\Users\\{username}\\Desktop\\cresis_project\\iceflow\\"

    # Write keys and metadata to a text file with UTF-8 encoding
    # with open("iceflow_keys.txt", "w", encoding="utf-8") as file:
    with open(f"{dir}iceflow_key_data.txt", "w", encoding="utf-8") as file:
        file.write(f"file {file_name} updated on {datetime.datetime.now().replace(microsecond=0)}\n\n\n")
        for key in iceflow_file.variables.keys():
            file.write(f"Key: {key}\n")
            var_info = serialize_variable(iceflow_file.variables[key])
            # Write the variable type, dimensions, and shape
            file.write(f"\ttype: {var_info['type']}\n")
            file.write(f"\tdimensions: {var_info['dimensions']}\n")
            file.write(f"\tshape: {var_info['shape']}\n")
            # Write the attributes
            file.write(f"\tattributes:\n")
            for attr, value in var_info['attributes'].items():
                file.write(f"\t\t{attr}: {value}\n")
            # Optionally write the data
            # file.write(f"\tdata: {var_info['data']}\n")
            file.write("\n")
            # print(f"key: {key}\n{var_info}\n\n")

    file.close()
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
    # print the min and max lat and lon
    # print(f"min lat: {np.min(latitude)}, max lat: {np.max(latitude)}")
    # print(f"min lon: {np.min(longitude)}, max lon: {np.max(longitude)}")

    return x, y, velocity_x, velocity_y, latitude, longitude


def iceflow_saver():
    """
    This function is used to save the iceflow data to a pickle file.
    :return: the file name of the pickle file that the iceflow data was saved to
    """
    x, y, velocity_x, velocity_y, latitude, longitude = iceflow_data_file_loader()
    iceflow_data = [x, y, velocity_x, velocity_y, latitude, longitude]
    debug_print(BRIGHT_YELLOW, "Saving iceflow data to pickle file...")
    # pickle_file_name = "iceflow_data.pickle"
    pickle_file_name = "C:\\Users\\moser\\Desktop\\cresis_project\\iceflow\\iceflow_data.pickle"
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
    # return 6223 + int(x / 450)
    return 6223 + int(x / 450) - 1


def y_to_index(y):
    # return 6223 - int(y / 450)
    return 6223 - int(y / 450) - 2


def index_to_x(x_index):
    return (x_index - 6223) * 450


def index_to_y(y_index):
    return (6223 - y_index) * 450


def xyindex_to_latlon(x_index, y_index):
    """
    This function is used to convert x and y coordinates to lat and lon coordinates.
    :param x: NOT THE X INDEX! the x coordinate to convert
    :param y: NOT THE Y INDEX! the y coordinate to convert
    :param iceflow_data: the iceflow data in a readable format
    :return: the lat and lon coordinates
    """
    x = index_to_x(x_index)
    y = index_to_y(y_index)
    transformer = Transformer.from_crs("EPSG:3031", "EPSG:4326", accuracy=10)
    # transform Antarctic Polar Stereographic to standard lat-lon
    point = transformer.transform(x, y, errcheck=True)
    if point[1] < 0:
        point = (point[0], 360 + point[1])  # this is to make the longitude positive
    return point


def latlon_to_xy(lat, lon):
    """
    This function is used to convert lat and lon coordinates to x and y coordinates.
    :param lon: the longitude to convert
    :param lat: the latitude to convert
    :return: the x and y coordinates
    # TODO: WHY ARE YOU THE WAY YOU ARE???
    """
    # debug_print(f"latlon_to_xy(): {lat}, {lon}")
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:3031", accuracy=10)
    # transform standard lat-lon to Antarctic Polar Stereographic
    point = transformer.transform(lat, lon, errcheck=True)

    return point


def xy_to_latlon(x, y):
    """
    This function is used to convert x and y coordinates to lat and lon coordinates.
    :param x: the x coordinate to convert
    :param y: the y coordinate to convert
    :return: the lat and lon coordinates
    """
    # debug_print(f"xy_to_latlon(): {x}, {y}")
    transformer = Transformer.from_crs("EPSG:3031", "EPSG:4326", accuracy=10)
    # transform Antarctic Polar Stereographic to standard lat-lon
    point = transformer.transform(x, y, errcheck=True)
    if point[1] < 0:
        point = [point[0], 360 + point[1]]
    else:
        point = [point[0], point[1]]
    return point


def layers_to_xy(layers):
    """
    This function is used to convert a list of layers to x and y coordinates.
    :param layers: the list of layers to convert
    :return: the x and y coordinates
    """
    surface = []
    bottom = []

    start_time = time.time()
    for i in range(len(layers[0].lat)):
        progress_bar(i, len(layers[0].lat) - 1, start_time, 50)
        bottom.append(latlon_to_xy(layers[0].lat[i], layers[0].lon[i]))
        # if layers[1].lat[i] is not nan
        if not np.isnan(layers[1].lat[i]):
            # layers[1].x[i], layers[1].y[i] = latlon_to_xy(layers[1].lat[i], layers[1].lon[i])
            surface.append(latlon_to_xy(layers[1].lat[i], layers[1].lon[i]))

    return surface, bottom


def xyindex_vector_to_heading(x_index, y_index, x_vector, y_vector):
    """
    This function is used to convert an x and y vector in EPSG:3031 to a heading in EPSG:4326.
    :param x_index: the x coordinate
    :param y_index: the y coordinate
    :param x_vector: the x vector
    :param y_vector: the y vector
    :return: the heading in EPSG:4326
    """
    # convert the x and y coordinates to lat and lon
        # this is the starting point of the vector in lat and lon
    lat_base, lon_base = xyindex_to_latlon(x_index, y_index)

    # convert the x and y indices to x and y
    x = index_to_x(x_index)
    y = index_to_y(y_index)

    # add the flow vector
    x_vector = x + x_vector
    y_vector = y + y_vector

    # convert the x and y vector to lat and lon
        # this is the ending point of the vector in lat and lon
    lat_vector, lon_vector = xy_to_latlon(x_vector, y_vector)

    # calculate the heading
    geodesic = pyproj.Geod(ellps='WGS84')
    angle1, angle2, distance = geodesic.inv(lon_base, lat_base, lon_vector, lat_vector)
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


def flow_at_x_y_index(x, y, iceflow_data):
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
    :return: the nearest unmasked x and y indices in the iceflow data to an input x and y value
    """
    x_index = x_to_index(x)  # convert the x value to an index
    y_index = y_to_index(y)  # convert the y value to an index
        # x,y → indices
    unmasked = []  # a list to store the unmasked x and y values
    for x_index_iterator in range(x_index - max_radius, x_index + max_radius):  # iterate through the x indices within the max_radius
        for y_index_iterator in range(y_index - max_radius, y_index + max_radius):  # iterate through the y indices within the max_radius
            if (
                    0 <= x_index_iterator < iceflow_data[2].shape[0]  # if the x index is within the bounds of the iceflow data
                    and 0 <= y_index_iterator < iceflow_data[2].shape[1]  # if the y index is within the bounds of the iceflow data
                    and not np.ma.is_masked(iceflow_data[2][x_index_iterator][y_index_iterator])  # if the x velocity is unmasked
                    and not np.ma.is_masked(iceflow_data[3][x_index_iterator][y_index_iterator])  # if the y velocity is unmasked
            ):  # if the x and y velocity values at the indices are unmasked
                unmasked.append((x_index_iterator, y_index_iterator))  # append the x and y indices to the unmasked list
            if printout and not np.ma.is_masked(iceflow_data[2][x_index_iterator][y_index_iterator]):
                print(f"unmasked x index: {x_index_iterator}, unmasked y index: {y_index_iterator}")
                print(
                    f"unmasked lat: {iceflow_data[4][x_index_iterator][y_index_iterator]}, unmasked lon: {iceflow_data[5][x_index_iterator][y_index_iterator]}")
                print(
                    f"unmasked flow: {iceflow_data[2][x_index_iterator][y_index_iterator]}, {iceflow_data[3][x_index_iterator][y_index_iterator]}")
    # find the xy index pair with the minimum distance from the input x and y
    min_distance = 100  # a starting value; just needs to be larger than the actual minimum distance
    min_x_index = None
    min_y_index = None
    for x_index_iterator, y_index_iterator in unmasked:
        distance = math.sqrt((x_index - x_index_iterator) ** 2 + (y_index - y_index_iterator) ** 2)
        if distance < min_distance:
            min_distance = distance
            min_x_index = x_index_iterator
            min_y_index = y_index_iterator
            # technically this isn't distance as much as it is how close the indices are to each other

    # print(f"latlon of nearest unmasked: {iceflow_data[4][min_x][min_y], iceflow_data[5][min_x][min_y]}")
    return min_x_index, min_y_index


def latlon_to_nearest_unmasked_index(lat, lon, iceflow_data, max_radius=10, printout=False):
    """
    Find the nearest x and y value in the iceflow data to an input x and y value.
    :param x: the x value to find the nearest x value to
    :param y: the y value to find the nearest y value to
    :param iceflow_data: the iceflow data
    :param max_radius: the maximum radius to search for an unmasked point
    :param printout: whether or not to print the nearest unmasked point
    :return: the nearest unmasked x and y indices in the iceflow data to an input x and y value
    """
    x, y = latlon_to_xy(lat, lon)  # convert the x value to an index
    x_index = x_to_index(x)  # convert the x value to an index
    y_index = y_to_index(y)  # convert the y value to an index
    # print(f"checking indices: {x_index, y_index}")
        # x,y → indices
    # if the calculated indices are valid, return them. If they are masked, procede down the search function.
    if (
            not np.ma.is_masked(iceflow_data[2][x_index][y_index])  # if the x velocity is unmasked
            and not np.ma.is_masked(iceflow_data[3][x_index][y_index])  # if the y velocity is unmasked
        ):
        print("The calculated indices are unmasked, no need to search")
        return x_index, y_index

    unmasked = []  # a list to store the unmasked x and y values
    for x_index_iterator in range(x_index - max_radius, x_index + max_radius):  # iterate through the x indices within the max_radius
        for y_index_iterator in range(y_index - max_radius, y_index + max_radius):  # iterate through the y indices within the max_radius
            if (
                    0 <= x_index_iterator < iceflow_data[2].shape[0]  # if the x index is within the bounds of the iceflow data
                    and 0 <= y_index_iterator < iceflow_data[2].shape[1]  # if the y index is within the bounds of the iceflow data
                    and not np.ma.is_masked(iceflow_data[2][x_index_iterator][y_index_iterator])  # if the x velocity is unmasked
                    and not np.ma.is_masked(iceflow_data[3][x_index_iterator][y_index_iterator])  # if the y velocity is unmasked
            ):  # if the x and y velocity values at the indices are unmasked
                unmasked.append((x_index_iterator, y_index_iterator))  # append the x and y indices to the unmasked list
            if printout and not np.ma.is_masked(iceflow_data[2][x_index_iterator][y_index_iterator]):
                print(f"unmasked x index: {x_index_iterator}, unmasked y index: {y_index_iterator}")
                print(
                    f"unmasked lat: {iceflow_data[4][x_index_iterator][y_index_iterator]}, unmasked lon: {iceflow_data[5][x_index_iterator][y_index_iterator]}")
                print(
                    f"unmasked flow: {iceflow_data[2][x_index_iterator][y_index_iterator]}, {iceflow_data[3][x_index_iterator][y_index_iterator]}")
    # find the xy index pair with the minimum distance from the input x and y
    min_distance = 10000  # a starting value; just needs to be larger than the actual minimum distance
    min_x_index = None
    min_y_index = None
    for x_index_iterator, y_index_iterator in unmasked:
        # x_index_lat_lon, y_index_lat_lon = xyindex_to_latlon(x_index_iterator, y_index_iterator)
        # x_index_lat_lon = iceflow_data[4][x_index_iterator][y_index_iterator]
        # y_index_lat_lon = iceflow_data[5][x_index_iterator][y_index_iterator]
        # distance = math.sqrt((lat - x_index_lat_lon) ** 2 + (lon - y_index_lat_lon) ** 2)
        distance = math.sqrt((x_index - x_index_iterator) ** 2 + (y_index - y_index_iterator) ** 2)
            # this has proven to be the best way to calculate the distance. The commented out methods have been tested
            # and result in indices off by 3-10 indices in the x and y directions while this is always 1-2 indices off.
                # best practice is probably to use the calculated indices and call this function if they are masked.
        # print(f"indices: {x_index_iterator, y_index_iterator}, distance: {distance}, less than min of {min_distance}: {distance < min_distance}")
        if distance < min_distance:
            min_distance = distance
            min_x_index = x_index_iterator
            min_y_index = y_index_iterator

    return min_x_index, min_y_index



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
    x_index, y_index = xy_to_nearest_unmasked_index(x, y, iceflow_data, max_radius=1000)
    if print_point:
        print(f"Nearest point to lat-lon: {xyindex_to_latlon(x_index, y_index)}")
    flow = flow_at_x_y_index(x_index, y_index, iceflow_data)
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
