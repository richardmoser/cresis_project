"""
Author: Richard Moser
Description: This file contains classes that are used to store data about crossover points and layers.
"""

import json
import os


class Crossover:
    """
    This class is used to store crossover point data and facilitate the saving and loading of crossover point data to
    and from a json file.
    """

    def __init__(self, layer, season, flight, crossover_points, crossover_indices, segment_ends, plane_velocity,
                 slope, heading, ice_flow_direction=None, ice_flow_direction_error=None):
        """
        This method initializes the Crossover object.
        :param layer: The layer object that the crossover point data is from.
        :param layer_name: The name of the layer that the crossover point data is from.
        :param season: The season that the crossover point data is from.
        :param flight: The flight that the crossover point data is from.
        :param crossover_points: The crossover points.
        :param crossover_indices: The crossover indices.
        :param segment_ends: The segment ends.
        :param plane_velocity: The plane velocity.
        :param slope: The slope.
        :param average_slope: The average slope.
        :param heading: The heading.
        :param ice_flow_direction: The ice flow direction at the crossover point.
        :param ice_flow_error: The difference between the heading and the ice flow direction.
        """
        self.layer_name = layer.layer_name
        self.season = season
        self.flight = flight
        self.crossover_points = crossover_points
        self.crossover_indices = crossover_indices
        self.segment_ends = segment_ends
        self.plane_velocity = plane_velocity
        self.slope = slope
        # self.average_slope = average_slope
        self.heading = heading
        self.twtt1 = layer.twtt[crossover_indices[0][0]]
        self.twtt2 = layer.twtt[crossover_indices[0][1]]
        self.twtt_difference = self.twtt1 - self.twtt2
        self.depth1 = layer.depth[crossover_indices[0][0]]
        self.depth2 = layer.depth[crossover_indices[0][1]]
        self.depth_difference = self.depth1 - self.depth2
        self.heading1 = layer.heading[crossover_indices[0][0]]
        self.heading2 = layer.heading[crossover_indices[0][1]]
        self.ice_flow_direction = ice_flow_direction
        if self.ice_flow_direction is not None:
            self.ice_flow_offset = self.heading - self.ice_flow_direction
            self.ice_flow_direction_error = ice_flow_direction_error
        else:
            self.ice_flow_offset = None
            self.ice_flow_direction_error = None


    def to_dict(self):
        """
        This method converts the Crossover object to a dictionary.
        :return: The Crossover object as a dictionary.
        """
        return {
            'layer_name': self.layer_name,
            'season': self.season,
            'flight': self.flight,
            'crossover_points': self.crossover_points,
            'crossover_indices': self.crossover_indices,
            'segment_ends': self.segment_ends,
            'plane_velocity': self.plane_velocity,
            'slope': self.slope,
            'average_slope': self.average_slope,
            'heading': self.heading,
            'twtt1': self.twtt1,
            'twtt2': self.twtt2,
            'twtt_difference': self.twtt_difference,
            'depth1': self.depth1,
            'depth2': self.depth2,
            'depth_difference': self.depth_difference,
            'heading1': self.heading1,
            'heading2': self.heading2,
            'ice_flow_direction': self.ice_flow_direction,
            'ice_flow_offset': self.ice_flow_offset
        }


class Layer:
    """
    A class to represent a layer in the CSARP_layer mat file.
    """

    def __init__(self, layer_name, gps_time, id, lat, lon, quality, twtt, type, elevation=None, param=None,):
        # capitalize the first letter of the layer name
        layer_name = layer_name[0].upper() + layer_name[1:]
        self.layer_name = layer_name
        self.elevation = elevation
        self.gps_time = gps_time
        self.id = id
        self.lat = lat
        self.lon = lon
        self.param = param
        self.quality = quality
        self.twtt = twtt
        self.twtt_corrected = None
        self.type = type
        self.x = []
        self.y = []
        self.xy_exists = False
        self.depth = [] # depth of the layer based on the corrected twtt


class Twtt_Posit:
    """
    A class to store the data of a crossover point.
    """

    def __init__(self, layer, season, flight, indices):
        self.layer = layer
        self.layer_name = layer.layer_name
        self.twtt = []
        for index in indices:
            twtt1 = layer.twtt[index[0]]
            twtt2 = layer.twtt[index[1]]
            self.twtt.append([twtt1, twtt2])
        self.lat1 = layer.lat[indices[0][0]]
        self.lat2 = layer.lat[indices[0][1]]
        self.lon1 = layer.lon[indices[0][0]]
        self.lon2 = layer.lon[indices[0][1]]
        self.gps_time1 = layer.gps_time[indices[0][0]]
        self.gps_time2 = layer.gps_time[indices[0][1]]
        self.season = season
        self.flight = flight
        self.indices = indices


class Cross:
    def __init__(self):
        self.flow_xy = []
        self.flow_heading_full = []
        self.flow_heading = []
        self.plane_heading_1 = []
        self.plane_heading_2 = []
        self.angle = []
        self.twtt = None
        self.delta_twtt = []
        self.depth1 = []
        self.depth2 = []
        self.depth_ave = []

    def to_dict(self):
        return {
            'flow_xy': self.flow_xy,
            'flow_heading_full': self.flow_heading_full,
            'flow_heading': self.flow_heading,
            'plane_heading_1': self.plane_heading_1,
            'plane_heading_2': self.plane_heading_2,
            'angle': self.angle,
            'twtt': self.twtt,
            'delta_twtt': self.delta_twtt,
            'depth1': self.depth1,
            'depth2': self.depth2,
            'depth_ave': self.depth_ave
        }

    def __str__(self):
        str = f"flow_xy: {self.flow_xy}\n" \
              f"flow_heading_full: {self.flow_heading_full}\n" \
              f"flow_heading: {self.flow_heading}\n" \
              f"plane_heading_1: {self.plane_heading_1}\n" \
              f"plane_heading_2: {self.plane_heading_2}\n" \
              f"angle: {self.angle}\n" \
              f"twtt: {self.twtt}\n" \
              f"delta_twtt: {self.delta_twtt}\n" \
              f"depth1: {self.depth1}\n" \
              f"depth2: {self.depth2}\n" \
              f"depth_ave: {self.depth_ave}"
        return str
