"""
Author: Richard Moser
Description: This file contains the Crossover class, which is used to store crossover point data and facilitate the
saving and loading of crossover point data to and from a json file.
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
        # TODO: looks like this is going to ignore all but the first crossover point. Update to handle multiple
        #  crossover points.


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