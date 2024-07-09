import matplotlib.pyplot as plt
import os
from project_classes import *
# import functions
from functions import *
import h5py
import numpy as np
import pandas as pd
import csv


zoom = True
seg_length = 100
# season = "2009_Antarctica_DC8"
season = "2018_Antarctica_DC8"
season = "2016_Antarctica_DC8"
# season = "2014_Antarctica_DC8"
# season = "2022_Antarctica_BaslerMKB"

# flight = "20181030_01"  # the flight date and frame number
    # that flight only has one point
# flight = "20181018_01"
# flight = "20181103_01"
# flight = "20181011_01"
    # one dimensional data error
    # TODO: figure out why 10018 and 1103 have the same data or at least print the same maps and plots
# flight = "20181109_01"
# flight = "20181112_02"  # the problem flight
    # plots fake crossovers along the curved path
# flight = "20161024_05"
flight = "20161111_05"
    # probably too close to the coast to be useful
# flight = "20161024_05"
# flight = "20141026_06"
    # this one is 1/3 of an orbit and produces a bunch of bunk crossovers
# flight = "20230127_01"
    # ~ 1/3 of an orbit of the pole and yet the angle plot looks like hot garbage
# file_name = "layer_export_" + flight + ".pickle"
file_name = "C:\\Users\\rj\\Documents\\cresis_project\\pickle_jar\\layer_export_" + flight + ".pickle"
testing = False


def layer_to_csv(season, flight):
    """
    :param season: the string name of the season
    :param flight: the string name of the flight
    :return: none, save the data to a csv file
    """
    """Find the Mat"""
    dir = ('C:\\Users\\rj\\Documents\\cresis\\rds\\' + season + '\\CSARP_layer\\' + flight + '\\')
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
    filename = 'C:\\Users\\rj\\Documents\\cresis_project\\csv_jar\\' + flight + '.csv'
    with open(filename, 'w') as f:
        # using csv.writer method from CSV package
        write = csv.writer(f)
        write.writerow(fields)
        write.writerows(rows)

    return


print("Starting...")
# gets all the folders from the season directory
folders = os.listdir('C:\\Users\\rj\\Documents\\cresis\\rds\\' + season + '\\CSARP_layer\\')

# for flight in folders:
start_time = time.time()
for i in range(len(folders)):
    progress_bar(i, len(folders), start_time)
    flight = folders[i]
    # get the data from the flight
    layer_to_csv(season, flight)


