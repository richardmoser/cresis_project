import scipy.io as sio
import numpy as np
import pickle
import matplotlib.pyplot as plt
from layer_class import Layer

def cross_point(layer):
    """
    :param layer: a Layer object
    :return: the point where the lat-lon crosses over it's own path
    """
    # determine which set of two coordinates

print("Reading pickle file...")
print("--------------------")
# read layers.pickle into a list of Layer objects
with open('layers.pickle', 'rb') as f:
    layers = pickle.load(f)
for layer in layers:
    print(layer.layer_name)
print("--------------------\n")

print("debug:")
print(layers[0].layer_name)
print(layers[0].lat)
print(layers[0].lon)


# print("Plotting lat-lon map...")
# print("--------------------")
# # plot the latitudes and longitudes for layers[0] on a polar projection
# plt.figure()
# plt.subplot(111, projection='polar')
# plt.plot(layers[0].lon, layers[0].lat)
# plt.title("Lat-Lon Map")
# plt.show()
# print("--------------------\n")