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
        self.long = lon
        self.param = param
        self.quality = quality
        self.twtt = twtt
        self.type = type
