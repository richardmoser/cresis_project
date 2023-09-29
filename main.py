
# purpose: print the headings for the data in the mat file layer_20181030_01.mat located at
# C:\Users\rj\Documents\cresis\rds\2018_Antarctica_DC8\CSARP_layer\20181030_01

import scipy.io as sio
import numpy as np
from layer import Layer

def layerize(mat):
    """
    :param mat: a mat file
    :return: a list of Layer objects
    """
    layers = []

    # mat has the format mat[file_number][key][layer_number]
    # e.g. mat[0]['layers'][0] is the first layer in the first mat file and mat[1]['layers'][0] is the first layer in the second mat file
    # a Layer object should be made by sequentially appending the values for each layer from each mat file

    # iterate through each mat file
    no_files = len(mat)
    no_layers = len(mat[0]['twtt']) - 1
    print("--------------------")
    print(f"number of files: {no_files}, number of layers: {no_layers}")
    # print("debug:")

    for i in range(no_layers):
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
            elevation = np.append(elevation, mat[j]['elev'])
            gps_time = np.append(gps_time, mat[j]['gps_time'])
            id = np.append(id, mat[j]['id'])
            lat = np.append(lat, mat[j]['lat'])
            lon = np.append(lon, mat[j]['lon'])
            # TODO: figure out what param is and how to handle it.
            # it seems to be some kind of data structure in and of itself (csv or similar?)
            # param = np.append(param, mat[j]['param'])
            quality = np.append(quality, mat[j]['quality'])
            twtt = np.append(twtt, mat[j]['twtt'][i])
            # print(f"twtt length: {twtt.shape}")
            type = np.append(type, mat[j]['type'])

        # create a Layer object
        layers.append(Layer(elevation, gps_time, id, lat, lon, param, quality, twtt, type))

    return layers



# load the mat files
# mat = sio.loadmat('C:\\Users\\rj\\Documents\\cresis\\rds\\2018_'
#                   'Antarctica_DC8\\CSARP_layer\\20181030_01\\layer_'
#                   '20181030_01.mat')
dir = ('C:\\Users\\rj\\Documents\\cresis\\rds\\2018_Antarctica_DC8\\CSARP_layer\\20181030_01\\')
segment = 'Data_20181030_01_'
startframe = '001'
endframe = '016'
# mat = sio.loadmat(dir + segment + startframe + '.mat')

# load an array of mat files
mat = np.array([sio.loadmat(dir + segment + str(i).zfill(3) + '.mat')
                for i in range(int(startframe), int(endframe)+1)])

# print the keys as strings without all the extra stuff
keys = [str(key).strip("_") for key in mat[0].keys()]
print(f"mat file keys:")
for key in keys:
    print(key, end="")
    # if not last key, print a comma
    if key != keys[-1]:
        print(",", end=" ")
print("\n")

layers = layerize(mat)

print((f"layer 0 shape: {layers[0].twtt.shape}"))
print(f"layer 0 first ten: {layers[0].twtt[0:10]}")
print(f"layer 0 last ten: {layers[0].twtt[54600:54610]}\n")

print((f"layer 1 shape: {layers[1].twtt.shape}"))
print(f"layer 1 first ten: {layers[1].twtt[0:10]}")
print(f"layer 1 last ten: {layers[1].twtt[54600:54610]}]\n")

print((f"layer 2 shape: {layers[2].twtt.shape}"))
print(f"layer 2 first ten: {layers[2].twtt[0:10]}")
print(f"layer 2 last ten: {layers[2].twtt[54600:54610]}\n")

