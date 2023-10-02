import scipy.io as sio
import numpy as np
from layer_class import Layer

# layer_20181030_01.mat

# load the mat file at C:\Users\rj\Documents\cresis\rds\2018_Antarctica_DC8\CSARP_layer\20181030_01\layer_20181030_01.mat
dir = ('C:\\Users\\rj\\Documents\\cresis\\rds\\2018_Antarctica_DC8\\CSARP_layer\\20181030_01\\')

file = 'layer_20181030_01.mat'

mat = sio.loadmat(dir + file)

# print the keys as strings without all the extra stuff
keys = [str(key).strip("_") for key in mat.keys()]
print(f"mat file keys:")
for key in keys:
    print(key, end="")
    # if not last key, print a comma
    if key != keys[-1]:
        print(",", end=" ")

# print the shape of the lyr_name field
print(f"\n\nlyr_name shape: {mat['lyr_name'].shape}")

# print lyr_name for each layer
for i in range(mat['lyr_name'].shape[1]):
    print(f"\nlyr_name for layer {i}: {mat['lyr_name'][0][i]}")