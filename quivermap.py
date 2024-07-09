print("test")
# %%
import matplotlib.pyplot as plt

from project_classes import *
from functions import *

# %%
zoom = True
seg_length = 100
# season = "2009_Antarctica_DC8"
# season = "2018_Antarctica_DC8" # a layerData season
season = "2016_Antarctica_DC8"  # a season with both layer and layerData
# season = "2014_Antarctica_DC8" # a layerData season
# flight = "20181030_01"  # the flight date and frame number
# flight = "20181018_01"
# flight = "20181103_01"
# flight = "20181109_01"
# flight = "20181112_02"  # the problem flight
flight = "20161024_05"
# flight = "20161111_05"
# flight = "20161024_05"
# flight = '20141026_06'
# file_name = "layer_export_" + flight + ".pickle"
file_name = "C:\\Users\\rj\\Documents\\cresis_project\\pickle_jar\\layer_export_" + flight + ".pickle"
testing = False
# %%
"""
read in the layers from the layer files and save them to a pickle file
"""
# mat_pickler_layer(season, flight, testing_mode=testing)  # make it
mat_pickler_h5py(season, flight, testing_mode=testing)  # make it
layers = read_layers(file_name)  # read in the layers from the pickle file

# TODO: figure out the difference in file structure between the h5py and sio based pickler outputs
# %% md
### read in the iceflow data from the iceflow data files and save them to a pickle file
# %%
if not os.path.isfile(
        "C:\\Users\\rj\\Documents\\cresis_project\\iceflow\\iceflow_data.pickle"):  # if the file does not exist
    print("The iceflow data pickle file was not found. Creating a new one...")
    filename = iceflow_saver()
    iceflow_data = iceflow_loader(filename)
    print("The iceflow data pickle file was successfully created.")
# try:
iceflow_data = iceflow_loader("C:\\Users\\rj\\Documents\\cresis_project\\iceflow\\iceflow_data.pickle")
print("The iceflow data pickle file was found and loaded.")

x = iceflow_data[0]
y = iceflow_data[1]
velocity_x = iceflow_data[2]
velocity_y = iceflow_data[3]
latitude = iceflow_data[4]
longitude = iceflow_data[5]
# %%
# print the average latitude and longitude
print(f"average latitude: {np.mean(latitude)}")
print(f"average longitude: {np.mean(longitude)}")
# print the maximum and minimum latitude and longitude
print(f"max latitude: {np.max(latitude)}")
print(f"min latitude: {np.min(latitude)}")
print(f"max longitude: {np.max(longitude)}")
print(f"min longitude: {np.min(longitude)}")
# %%
# if the file at filename exists, read in the intersection_indices and intersection_points from the pickle file
# otherwise, find the intersection_indices and intersection_points and save them to a pickle file
filename = f"C:\\Users\\rj\\Documents\\cresis_project\\pickle_jar\\{season}_{flight}_crossover_points.pickle"
if not os.path.isfile(filename):  # if the file does not exist
    print(f"File {filename} does not exist. Making it...")
    intersection_points, intersection_indices, segment_ends = cross_point(layers[0], seg_length, quiet=True)
    with open(filename, 'wb') as file:
        pickle.dump(intersection_indices, file)
        pickle.dump(intersection_points, file)
        pickle.dump(segment_ends, file)
    print(f"intersection_indices and intersection_points saved to {filename}")
else:
    with open(filename, 'rb') as file:
        intersection_indices = pickle.load(file)
        intersection_points = pickle.load(file)
        segment_ends = pickle.load(file)
    print(f"intersection_indices and intersection_points loaded from {filename}")
# %%
# TODO: deconstruct the nested lists and make them make more sense
# put them in class objects?

print(f"intersection_indices: {intersection_indices}")
print(f"intersection_points: {intersection_points}")
# %%
"""Start conversion dev 26Jun24"""
# %%
i = 0
cross_lat = intersection_points[i][0]
cross_lon = intersection_points[i][1]
cross_x, cross_y = latlon_to_xy(cross_lat, cross_lon)
"""Outputs x and y in EPSG:3031"""

print(f"cross_lat: {cross_lat:.8}, cross_lon: {cross_lon:.8f}")
print(f"cross_x: {cross_x:.4f}, cross_y: {cross_y:.4f}")
print(section_break)

nearest_x_index, nearest_y_index = latlon_to_nearest_unmasked_index(cross_lat, cross_lon, iceflow_data, max_radius=1)
print(f"nearest_x_index: {nearest_x_index}, nearest_y_index: {nearest_y_index}")

# %%
"""End conversion dev 26Jun24"""


# %%
# TODO: identify why this is still here and not in the functions file
# because it is still being tweaked
# TODO: consider normalizing to the elevation, not the surface
# i.e. instead of having the surface be flat, have it represent the actual topology
# really only useful for places where the surface is not basically flat
def plot_layers_at_cross(layers, intersection_indices, intersection_points, zoom=False, refractive_index=1.77,
                         cross_index=0, filename=None):
    """
    :param layers: a list of Layer objects
    :param intersection_indices: a list of indices in the lat-lon arrays where the flight path
    crosses over itself
    :param intersection_points: a list of lat-lon points where the flight path crosses over itself
    :return: nothing (plots the layers and the map)
    """
    plt.figure(figsize=(16, 8), layout='constrained')
    print("Plotting layers...")
    print("--------------------")
    print("Adjusting for surface twtt...")
    for layer in layers:
        corrected_layer = layer.twtt - layers[0].twtt
        layer.twtt_corrected = corrected_layer

    # ax2 will be the layer plot
    # plt.subplot(1, 2, 1)

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

    # print the twtt at the crossover point on both segments
    twtt = twtt_at_point(layers[1], layers[0], intersection_indices, quiet=True)[0]
    print(f"twtt: {twtt}")

    # plot a line at the crossover point
    plt.axvline(x=offset, color='black', label='X Point', linestyle='--', linewidth=0.3)

    # set the y axis to be in microseconds instead of seconds
    plt.ylabel(f"Adjusted Two Way Travel Time ({chr(956)}s)")
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
    plt.legend(fontsize='smaller', loc='upper right', bbox_to_anchor=(1, 0.9))

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
    plt.show()


def plot_map(layers, intersection_indices, intersection_points, iceflow_data, season, flight, zoom=False, cross_index=0,
             filename=None):
    """
    plot the map
    """
    plot_it = True

    if plot_it:
        plt.figure(figsize=(16, 8), layout='constrained')
    print("Plotting map...")
    # TODO: add an offset to the zoom settings so that the crossover point is in the center of the zoomed in map
    offset = 500  # this is not that offset

    # this code sets up a polar stereographic map of antarctica with the South Pole in the center
    zoom_out_to_continent = not zoom
    if zoom_out_to_continent:
        llcrnrx = -400000
        llcrnry = -400000
        urcrnrx = 250000
        urcrnry = 250000
    else:
        llcrnrx = -100000
        llcrnry = -100000
        urcrnrx = 100000
        urcrnry = 100000
    lat_0 = intersection_points[cross_index][0]
    lon_0 = intersection_points[cross_index][1]
    # print(f"debug: lat_0: {lat_0}, lon_0: {lon_0}")
    if plot_it:
        m = Basemap(projection='ortho', lat_0=lat_0, lon_0=lon_0, llcrnrx=llcrnrx,
                    llcrnry=llcrnry, urcrnrx=urcrnrx, urcrnry=urcrnry, resolution='c')
        # m = Basemap(projection='spstere', lat_0=-90, lat_ts=-71, lon_0=0, boundinglat=-80, resolution='c')
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
                1],
            '\nsegment 1', fontsize='smaller', fontweight='bold', ha='right', va='top', color='red')
        plt.text(
            m(layers[0].lon[intersection_indices[0][1] - offset], layers[0].lat[intersection_indices[0][1] - offset])[
                0],
            m(layers[0].lon[intersection_indices[0][1] - offset], layers[0].lat[intersection_indices[0][1] - offset])[
                1],
            '\nsegment 2', fontsize='smaller', fontweight='bold', ha='left', va='top', color='green')
        # plot the South Pole
        # m.scatter(0, -90, latlon=True, color='black', linewidth=1, label='South Pole')
        # plot the crossover points
        for point in intersection_points:
            m.scatter(point[1], point[0], latlon=True, color='darkred', linewidth=1, label='Crossover Point')
            plt.text(m(point[1], point[0])[0], m(point[1], point[0])[1] - 10000,
                     f'{intersection_points.index(point) + 1}\n\n',
                     fontsize='smaller', fontweight='bold', ha='center', va='top', color='darkred')

    # m.scatter(intersection_points[cross_index][1], intersection_points[cross_index][0], latlon=True, color='darkred',
    #           linewidth=1, label='Crossover Point')
    # plt.text(m(intersection_points[cross_index][1], intersection_points[cross_index][0])[0],
    #          m(intersection_points[cross_index][1], intersection_points[cross_index][0])[1] - 10000,
    #          'Crossover Point\n\n',
    #          fontsize='smaller', fontweight='bold', ha='center', va='top', color='darkred')

    # plot the the ice flow direction at the crossover point
    for i in range(len(intersection_indices)):
        # for i in range(1):
        print(f"cross index: {i + 1}")
        cross_lat = intersection_points[i][0]
        cross_lon = intersection_points[i][1]
        if cross_lon < 0:
            cross_lon = 360 + cross_lon
        cross_x, cross_y = latlon_to_xy(cross_lat, cross_lon)
        """Outputs x and y in EPSG:3031"""
        print(f"cross_lat: {cross_lat:.8}, cross_lon: {cross_lon:.8f}")
        print(f"cross_x: {cross_x:.4f}, cross_y: {cross_y:.4f}")

        # nearest_x_index, nearest_y_index = xy_to_nearest_unmasked_index(cross_x, cross_y, iceflow_data, max_radius=10)
        print(section_break)
        # nearest_y_index, nearest_x_index = latlon_to_nearest_unmasked_index(cross_lat, cross_lon, iceflow_data, max_radius=10)
        nearest_x_index, nearest_y_index = latlon_to_nearest_unmasked_index(cross_lat, cross_lon, iceflow_data,
                                                                            max_radius=10)
        print(f"nearest_x_index: {nearest_x_index}, nearest_y_index: {nearest_y_index}")
        """Outputs the nearest x and y indices to the x and y EPSG:3031 values"""

        nearest_lat = iceflow_data[4][nearest_y_index][nearest_x_index]  # latitude = iceflow_data[4]
        nearest_lon = iceflow_data[5][nearest_y_index][nearest_x_index]  # longitude = iceflow_data[5]
        # nearest_lon = - (iceflow_data[5][nearest_x_index][nearest_y_index] - 270)  # longitude = iceflow_data[5]

        # print(f"nearest_lat: {nearest_lat:.4f}, nearest_lon: {nearest_lon:.4f}")
        print(f"nearest_lat: {nearest_lat}, nearest_lon: {nearest_lon}")

        nearest_x, nearest_y = index_to_x(nearest_x_index), index_to_y(nearest_y_index)
        print(f"nearest_x: {nearest_x:.4f}, nearest_y: {nearest_y:.4f}")

        # flow = flow_at_x_y_index(nearest_x_index, nearest_y_index, iceflow_data)
        vx, vy = iceflow_data[2][nearest_y_index][nearest_x_index], iceflow_data[3][nearest_y_index][nearest_x_index]
        flow = [-vx, -vy]
        print(f"flow at nearest: {flow}")

        flow_heading = xyindex_vector_to_heading(nearest_x_index, nearest_y_index, flow[0], flow[1])[0]
        # m.quiver(intersection_points[0][1], intersection_points[0][0], 1000 * np.cos(np.radians(flow_heading)),
        #          1000 * np.sin(np.radians(flow_heading)), latlon=True, color='blue', label='Ice Flow Vector')
        # plot the ice flow vector in the upper right corner as a quiver

        print("")
        print(f"Diff x: {(cross_x - nearest_x):.1f}, Diff y: {(cross_y - nearest_y):.1f}")
        print("")
        print(section_break)
        print(section_break)
        print("")

        # if plot_it:
        #     m.quiver(intersection_points[0][1]+2.5, intersection_points[0][0]+0.7, 10000 * np.cos(np.radians(flow_heading)), 10000 * np.sin(np.radians(flow_heading)), latlon=True, color='blue', label='Ice Flow Vector')
        #     plt.text(m(intersection_points[0][1]+2.5, intersection_points[0][0]+0.6)[0], m(intersection_points[0][1]+5, intersection_points[0][0]+0.8)[1], 'Ice Flow Vector\n\n', fontsize='smaller', fontweight='bold', ha='center', va='top', color='blue')
        #     x, y = m(0, -90)
        mag = np.sqrt(vx ** 2 + vy ** 2)
        # m.quiver(intersection_points[i][1], intersection_points[i][0], mag  * np.cos(np.radians(flow_heading)),
        #             mag * np.sin(np.radians(flow_heading)), latlon=True, color='blue', label='Ice Flow Vector')
        # plt.text(m(intersection_points[i][1], intersection_points[i][0])[0], m(intersection_points[i][1], intersection_points[i][0])[1] - 100, 'Ice Flow Vector\n\n', fontsize='smaller', fontweight='bold', ha='center', va='top', color='blue')
        m.quiver(nearest_x, nearest_y, 10000 * np.cos(np.radians(flow_heading)),
                 10000 * np.sin(np.radians(flow_heading)), latlon=True, color='blue', label='Ice Flow Vector')
        x, y = m(0, -90)

        # plt.text(x, y, '\nSouth Pole', fontsize='smaller', fontweight='bold', ha='center', va='top', color='black')

    center_x, center_y = latlon_to_xy(intersection_points[cross_index][0], intersection_points[cross_index][1])
    center_x = x_to_index(center_x)
    center_y = y_to_index(center_y)
    search_range_x = 750
    search_range_y = 400
    steps = 20
    start_time = time.time()
    for x in range(-1 * search_range_x + center_x, search_range_x + center_x, steps):
        current = x + search_range_x - center_x
        progress_bar(current, 2 * search_range_x, start_time, bar_length=50)
        for y in range(-1 * search_range_y + center_y, search_range_y + center_y, steps):
            if not (
                    np.ma.is_masked(iceflow_data[2][y][x]) and np.ma.is_masked(iceflow_data[3][y][x])
            ):
                # print(f"np.isnan(iceflow_data[2][y][x]): {np.isnan(iceflow_data[2][y][x])}")
                # print(f"np.isnan(iceflow_data[3][y][x]): {np.isnan(iceflow_data[3][y][x])}")
                # print(f"x-index: {x}, y-index: {y}\nx: {index_to_x(x)}, y: {index_to_y(y)}")
                vx = -1 * iceflow_data[2][y][x]
                vy = -1 * iceflow_data[3][y][x]
                flow = [vx, vy]
                flow_heading = xyindex_vector_to_heading(x, y, flow[0], flow[1])[0]
                # print(f"flow at nearest: {flow_heading}")
                scale = 0.0005
                mag = np.sqrt(vx ** 2 + vy ** 2) * scale
                lat = iceflow_data[4][y][x]
                lon = iceflow_data[5][y][x]
                # print(f"lat: {lat}, lon: {lon}")
                # print(f"flow at nearest: {flow}")
                m.scatter(lon, lat, latlon=True, color='darkred', s=0.75)
                # plot a line of length mag in the direction of the flow vector to show the flow vector
                endpt = [lon + mag * np.cos(np.radians(flow_heading)), lat + mag * np.sin(np.radians(flow_heading))]
                m.plot([lon, endpt[0]], [lat, endpt[1]], latlon=True, color='blue', linewidth=0.5)

            # else:
            # print(f"masked at x: {x}, y: {y}")
        # scatter the south pole
        # m.scatter(0, -90, latlon=True, color='white', s=5)
    print("")

    if plot_it:
        plt.title("Lat-Lon Map")
        # set tight layout
        # plt.tight_layout()

        # save the plot
        if filename:
            dir = "C:\\Users\\rj\Documents\\cresis_project\\screens\\"
            savename = f"{dir}{filename}_flow_map.png"
            print(f"saving to {savename}...")
            plt.savefig(savename, dpi=300)

        print("drawing to screen...")
        # plt.show()

    # print("plotted map")
    # print(section_break + "\n")


# %%
# print(segment_ends[0][0][0][0])
# for point in intersection_points:
# print(point[0])
# plot_layers_at_cross(layers, intersection_indices, segment_ends)
# plot_layers_at_cross(layers, intersection_indices, intersection_points, zoom=zoom, cross_index=0, filename=(season + flight + "crossover"))
plot_map(layers, intersection_indices, intersection_points, iceflow_data, season, flight, zoom=False, cross_index=0,
         filename=(season + flight + "crossover"))