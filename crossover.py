import numpy as np
import pickle
import matplotlib.pyplot as plt
from layer_class import Layer
from layer_class import Twtt_Posit
from mpl_toolkits.basemap import Basemap
from shapely.geometry import LineString

plot_map = False
# plot_map = True
seg_length = 100
save_posit = False
# save_posit = True
# plot_layers_at_cross = False
plot_layers_at_cross = True


def segments_intersect(segment1, segment2):
    line1 = LineString(segment1)
    line2 = LineString(segment2)
    return line1.intersects(line2)


def find_segment_intersection(segment1, segment2):
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


def cross_point(layer, quiet=False):
    """
    :param layer: a Layer object
    :return: the point where the lat-lon crosses over its own path.
    purpose: ayers[0].lat and layers[0].lon are numpy arrays of the latitudes and
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
    if verbose: print(f"Dividing the path into segments of length {seg_length}...")
    for i in range(0, len(layer.lat), seg_length):
        if i + seg_length < len(layer.lat):
            path_segments.append([(layer.lat[i], layer.lon[i]), (layer.lat[i + seg_length], layer.lon[i + seg_length])])
        else:
            path_segments.append([(layer.lat[i], layer.lon[i]), (layer.lat[-1], layer.lon[-1])])

    if verbose: print(f"Number of segments: {len(path_segments)}")
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
                    # intersections.append([intersection_points])
                    # intersections.append([intersection_points[0][0], intersection_points[1][0]])
                    rough_intersections.append([intersection_points[0][0], intersection_points[1][0]])
                    intersecting_segments.append([i, j])
                    # print(f"Segments {i} and {j} intersect near point: {intersection_points}")
                    if verbose: print(f"Segments {i} and {j} intersect near "
                          f"({intersection_points[0][0]}, {intersection_points[1][0]})")

    if verbose: print("\nChecking for a more precise intersection...")
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
        if verbose: print(f"segment {seg1} start: {seg1_start}, segment 1 end: {seg1_end}")
        if verbose: print(f"segment {seg2} start: {seg2_start}, segment 2 end: {seg2_end}")

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
                        # intersections.append([intersection_points[0][0], intersection_points[1][0]])
                        fine_intersections.append([intersection_points[0][0], intersection_points[1][0]])
                        # print(f"Segments {i} and {j} intersect near point: {intersection_points}")
                        # print the indices of the intersecting segments in the original lat-lon arrays
                        index1 = seg1_start + i
                        index2 = seg2_start + j
                        print(f"Segments {seg1} and {seg2 } intersect near indices "
                              f"{index1} and {index2}\nThis corresponds roughly to the "
                              f"lat-lon: ({fine_intersections[-1][0]}, {fine_intersections[-1][1]})")
                        intersection_indices.append([index1, index2])
    print(f"Number of intersections: {len(fine_intersections)}")
    if verbose: print(f"Number of rough intersections: {len(rough_intersections)}")
    if verbose: print(f"Number of intersection indices: {len(intersection_indices)}")
    # print(f"Intersection at index {intersection_indices[0][0]} and {intersection_indices[0][1]}")

    print("--------------------\n")

    return fine_intersections, intersection_indices


def twtt_at_point(read_layer, surface_layer, indices):
    """
    :param read_layer: a Layer object
    :param indices: a list of indices in the lat-lon arrays where the flight path
    crosses over itself
    :return: the twtt at the crossover point
    """
    print("Finding twtt at crossover point...")
    print("--------------------")
    print(f"Number of crossover points: {len(indices)}"
            f"\nFirst crossover point is at indices {indices[0][0]} and {indices[0][1]}")
    twtt = []
    for index in indices:
        twtt1 = read_layer.twtt[index[0]]
        twtt2 = read_layer.twtt[index[1]]
        print(f"twtt at index {index[0]}: {twtt1}")
        print(f"twtt at index {index[1]}: {twtt2}")
        twtt.append([twtt1, twtt2])
    print("--------------------\n")
    return twtt


print("Reading pickle file...")
print("--------------------")
# read layers.pickle into a list of Layer objects
with open('layers.pickle', 'rb') as f:
    layers = pickle.load(f)
for layer in layers:
    print(layer.layer_name)
print("--------------------\n")

intersection_points, intersection_indices = cross_point(layers[0], quiet=True)

# print("debug:")
# print(f"first intersection point: {intersection_points[0]}")

if plot_map:
    # bound_lat = -70
    bound_lat = -87
    # plot the lat-lon map for one of the layers in antarctica
    print("Plotting lat-lon map...")
    print("--------------------")
    # plot the latitudes and longitudes for layers[0] on a basemap
    plt.figure(figsize=(12, 12), layout='tight')
    m = Basemap(projection='spstere', boundinglat=bound_lat, lon_0=180, resolution='l')
    m.drawcoastlines()
    m.fillcontinents(color='grey', lake_color='aqua')
    m.drawparallels(np.arange(-80., 81., 20.))
    m.drawmeridians(np.arange(-180., 181., 20.))
    m.drawmapboundary(fill_color='aqua')
    # plot the flight path
    m.plot(layers[0].lon, layers[0].lat, latlon=True, color='lightgreen', linewidth=1)
    # m.plot(layers[0].lon[0:steps], layers[0].lat[0:steps], latlon=True, color='black', linewidth=1)
    # plot the South Pole
    m.scatter(0, -90, latlon=True, color='black', linewidth=1, label='South Pole')
    # plot the crossover points
    for point in intersection_points:
        m.scatter(point[1], point[0], latlon=True, color='red', linewidth=1, label='Crossover Point')
    # plot the crossover line


    x, y = m(0, -90)
    plt.text(x, y, '\nSouth Pole', fontsize='smaller', fontweight='bold', ha='center', va='top', color='black')
    plt.title("Lat-Lon Map")
    plt.show()
    print("--------------------\n")

twtt_at_intersect = twtt_at_point(layers[1], layer[0], intersection_indices)
twtt_difference_at_intersect = twtt_at_intersect[0][0] - twtt_at_intersect[0][1]
print(f"twtt difference at crossover point: {twtt_difference_at_intersect} ns")

posit = Twtt_Posit(layers[1], "2018_Antarctica_DC8", "20181030_01", intersection_indices)
print(f"posit.layer_name: {posit.layer_name}")

if save_posit:
    # save posit to a pickle file
    print("--------------------")
    pickle.dump(posit, open("posit.pickle", "wb"))
    print("posit.pickle saved in local directory of this python file.")
    print("--------------------\n")

# if plot_layers_at_cross: