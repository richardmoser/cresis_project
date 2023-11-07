"""
Author: Richard Moser
Description: This file contains classes and functions used in other files. Ideally, this will clean up the other code.
"""
import pickle
import matplotlib.pyplot as plt
import numpy as np
import math
import datetime
from shapely.geometry import LineString
from mpl_toolkits.basemap import Basemap

section_break = "--------------------\n"


def s_to_ms(x, pos):
    """
    :param x: the x value
    :param pos: the position
    :return: the x value in milliseconds
    """
    return '%1.1f' % (x * 1e6)


def ms_to_s(x, pos):
    """
    :param x: the x value
    :param pos: the position
    :return: the x value in seconds
    """
    return '%1.1f' % (x * 1e-6)

def gps_time_to_seconds(gps_time):
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
    print(f"rise: {round(rise, 2)}m, run: {round(run, 2)}m")
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

    for i in range(index - window_size, index):
        dist_ave_before += latlon_dist((layer.lat[i], layer.lon[i]), (layer.lat[i + 1], layer.lon[i + 1]))
        twtt_ave_before += layer.twtt[i]
    for i in range(index, index + window_size):
        dist_ave_after += latlon_dist((layer.lat[i], layer.lon[i]), (layer.lat[i + 1], layer.lon[i + 1]))
        twtt_ave_after += layer.twtt[i]
    dist_ave_before /= window_size
    dist_ave_after /= window_size
    twtt_ave_before /= window_size
    twtt_ave_after /= window_size
    rise_twtt = twtt_ave_after - twtt_ave_before
    rise = twtt_to_depth(rise_twtt, 1.77)
    run = dist_ave_after - dist_ave_before
    slope = rise / run
    return slope


def read_layers(file_name):
    """
    :param file_name: the name of the pickle file containing the layers, e.g. "layer_export_20181030_01.pickle"
    :return: a list of Layer objects from the pickle file (usually Surface, your custom layer(s), and Bottom)
    """
    print("Reading pickle file...")
    print("--------------------")
    # read layers.pickle into a list of Layer objects

    # file_name = 'layers.pickle'

    with open(file_name, 'rb') as f:
        layers = pickle.load(f)
    for layer in layers:
        print(layer.layer_name)
    print(section_break)
    return layers


def twtt_to_depth(twtt, refractive_index):
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
    print("--------------------")
    pickle.dump(posit, open("posit.pickle", "wb"))
    print("posit.pickle saved in local directory of this python file.")
    print("--------------------\n")


def plane_velocity(latlon1, latlon2, time1, time2):
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


def latlon_dist(latlon1, latlon2):
    """
    :param latlon1: a tuple of (lat, lon)
    :param latlon2: a tuple of (lat, lon)
    :return: the distance between the two lat-lon points in meters.
    d = 2R × sin⁻¹(√[sin²((θ₂ - θ₁)/2) + cosθ₁ × cosθ₂ × sin²((φ₂ - φ₁)/2)])
    """
    latlon1 = (latlon1[0] * math.pi / 180, latlon1[1] * math.pi / 180)
    latlon2 = (latlon2[0] * math.pi / 180, latlon2[1] * math.pi / 180)
    # convert the lat-lon points to radians
    R = 6371 * 1000  # radius of the earth in meters

    dist = 2 * R * math.asin(math.sqrt(
        math.sin((latlon2[0] - latlon1[0]) / 2) ** 2 + math.cos(latlon1[0]) * math.cos(latlon2[0]) * math.sin(
            (latlon2[1] - latlon1[1]) / 2) ** 2))
    # print(f"d: {d}")
    return dist


def segments_intersect(segment1, segment2):
    """
    :param segment1: a list of two points, e.g. [(lat1, lon1), (lat2, lon2)]
    :param segment2: a list of two points, e.g. [(lat1, lon1), (lat2, lon2)]
    :return: True if the segments intersect, False if they do not
    """
    line1 = LineString(segment1)
    line2 = LineString(segment2)
    return line1.intersects(line2)


def find_segment_intersection(segment1, segment2):
    """
    :param segment1: a list of two points, e.g. [(lat1, lon1), (lat2, lon2)]
    :param segment2: a list of two points, e.g. [(lat1, lon1), (lat2, lon2)]
    :return: the point where the segments intersect, or None if they do not intersect
    """
    line1 = LineString(segment1)
    line2 = LineString(segment2)
    intersection = line1.intersection(line2)
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
            return [tuple(intersection.xy[0]), tuple(intersection.xy[1])]
    return None


def cross_point(layer, seg_length, quiet=False):
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
    for i in range(len(path_segments)):
        for j in range(i + 1, len(path_segments)):
            if segments_intersect(path_segments[i], path_segments[j]):
                intersection_points = find_segment_intersection(path_segments[i], path_segments[j])
                if intersection_points:
                    rough_intersections.append([intersection_points[0][0], intersection_points[1][0]])
                    intersecting_segments.append([i, j])
                    if verbose:
                        print(f"Segments {i} and {j} intersect near "
                              f"({intersection_points[0][0]}, {intersection_points[1][0]})")

    if verbose:
        print("\nChecking for a more precise intersection...")
    fine_intersections = []
    intersection_indices = []

    for i in range(len(intersecting_segments)):
        seg1 = intersecting_segments[i][0]
        seg2 = intersecting_segments[i][1]

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

        # create a list of line segments of length 1
        path_segments = []
        for i in range(seg1_start, seg1_end):
            path_segments.append([(layer.lat[i], layer.lon[i]), (layer.lat[i + 1], layer.lon[i + 1])])
        for i in range(seg2_start, seg2_end):
            path_segments.append([(layer.lat[i], layer.lon[i]), (layer.lat[i + 1], layer.lon[i + 1])])


        # check for intersections between the line segments
        for i in range(len(path_segments)):
            for j in range(i + 1, len(path_segments)):
                if segments_intersect(path_segments[i], path_segments[j]):
                    intersection_points = find_segment_intersection(path_segments[i], path_segments[j])
                    if intersection_points:
                        # intersections.append([intersection_points])
                        segment_ends.append([[path_segments[i][0], path_segments[i][1]], [path_segments[j][0], path_segments[j][1]]])
                        fine_intersections.append([intersection_points[0][0], intersection_points[1][0]])
                        index1 = seg1_start + i
                        index2 = seg2_start + j
                        print(f"Segments {seg1} and {seg2} intersect near indices "
                              f"{index1} and {index2}\nThis corresponds roughly to the "
                              f"lat-lon: ({fine_intersections[-1][0]}, {fine_intersections[-1][1]})")
                        intersection_indices.append([index1, index2])
    print(f"Number of intersections: {len(fine_intersections)}")
    if verbose:
        print(f"Number of rough intersections: {len(rough_intersections)}")
        print(f"Number of intersection indices: {len(intersection_indices)}")
        print(f"Indices: {intersection_indices}")
        for index in intersection_indices:
            print(f"Index: {index}")
    # print(f"Intersection at index {intersection_indices[0][0]} and {intersection_indices[0][1]}")

    print("--------------------\n")

    return fine_intersections, intersection_indices, segment_ends


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
        print("--------------------")
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
        print("--------------------\n")
    return twtt


def plot_layers_at_cross(layers, intersection_indices, intersection_points, zoom=False, refractive_index=1.77,
                         cross_index=0):
    """
    :param layers: a list of Layer objects
    :param intersection_indices: a list of indices in the lat-lon arrays where the flight path
    crosses over itself
    :param intersection_points: a list of lat-lon points where the flight path crosses over itself
    :return: nothing (plots the layers and the map)
    """
    plt.figure(figsize=(24, 12), layout='constrained')
    print("Plotting layers and map...")
    print("--------------------")
    print("Adjusting for surface twtt...")
    for layer in layers:
        corrected_layer = layer.twtt - layers[0].twtt
        layer.twtt_corrected = corrected_layer

    # ax2 will be the layer plot
    plt.subplot(1, 2, 1)

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
    # plt.plot(layers[0].twtt[intersection_indices[0][0] - offset:intersection_indices[0][0] + offset],
    #             label=layers[0].layer_name)
    # plt.plot(layers[1].twtt[intersection_indices[0][0] - offset:intersection_indices[0][0] + offset],
    #             label=layers[1].layer_name + ' segment 1')
    # plt.plot(layers[1].twtt[intersection_indices[0][1] - offset:intersection_indices[0][1] + offset],
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
    # plot a line at the crossover point
    plt.axvline(x=offset, color='black', label='X Point', linestyle='--', linewidth=0.3)

    # set the y axis to be in nanoseconds instead of seconds
    plt.ylabel("Adjusted Two Way Travel Time (ns)")
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

    # make the right side y axis show the depth in meters by converting the twtt to depth using the refractive index
    min_y, max_y = plt.ylim()
    n = refractive_index
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
    plt.legend(["legend"], fontsize='smaller', loc='upper right', bbox_to_anchor=(1.1, 1.1))

    """
    plot the map
    """
    plt.subplot(1, 2, 2)

    # TODO: make the right pane a zoomed in map centered around the X point
    #  with a small zoomed out map in the corner
    # TODO: adjust time scale to be in nanoseconds instead of seconds
    # zoom_out_to_continent = False

    # # this code sets up a polar stereographic map of antarctica with the South Pole in the center
    # zoom_out_to_continent = not zoom
    # if zoom_out_to_continent:
    #     bound_lat = -65
    # else:
    #     bound_lat = -87
    # # plot the lat-lon map for one of the layers in antarctica
    # # print("Plotting lat-lon map...")
    # # print("--------------------")
    # m = Basemap(projection='spstere', boundinglat=bound_lat, lon_0=180, resolution='l')
    # m.drawcoastlines()
    # m.fillcontinents(color='grey', lake_color='aqua')
    # m.drawparallels(np.arange(-80., 81., 20.))
    # m.drawmeridians(np.arange(-180., 181., 20.))
    # m.drawmapboundary(fill_color='aqua')

    # make m a plot of the lat-lon map for one of the layers in antarctica centered around the crossover point
    # m should be an orthographic map centered around the crossover point
    # print("Plotting lat-lon map...")
    # print("--------------------")
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
    plt.savefig("layer_plot.png", dpi=250)

    plt.show()

    print("plotted map")
    print("--------------------\n")


def fancymap(layers, intersection_indices, intersection_points, zoom=False, refractive_index=1.77,
                         cross_index=0):
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
    print("--------------------")
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
    plt.savefig("fancy_map_only.png", dpi=1500)

    plt.show()

    print("plotted map")
    print("--------------------\n")