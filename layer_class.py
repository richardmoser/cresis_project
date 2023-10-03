class Layer:
    """
    A class to represent a layer in the CSARP_layer mat file.
    """

    def __init__(self, layer_name, elevation, gps_time, id, lat, lon, param, quality, twtt, type):
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
