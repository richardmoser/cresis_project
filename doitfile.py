from project_classes import *
from functions import *
from iceflow_library import *

# %%
zoom = True
seg_length = 100
season = "2018_Antarctica_DC8"  # a layerData season
season = "2016_Antarctica_DC8"  # a season with both layer and layerData
# season = "2014_Antarctica_DC8" # a layerData season
flight = "20181030_01"  # the flight date and frame number
flight = "20181103_01"
# flight = "20181112_02"  # the problem flight
flight = "20161024_05"
# flight = '20141026_06'
file_name = "layer_export_" + flight + ".pickle"
testing = False
# %% md
### read in the layers from the layer files and save them to a pickle file
# %%
# if the file at filename exists, read in the layers from the pickle file
# otherwise, read in the layers from the layer files and save them to a pickle file
# if not os.path.isfile(file_name):  # if the file does not exist
#     print(f"File {file_name} does not exist. Making it...")
#     # mat_pickler_layerData(season, flight, testing_mode=testing, layer=True)  # make it
#     mat_pickler_layerData(season, flight, testing_mode=testing, layer=False)  # make it
# mat_pickler_layerData(season, flight, testing_mode=testing)  # make it
mat_pickler_layer(season, flight, testing_mode=testing)  # make it
layers = read_layers(file_name)  # read in the layers from the pickle file
# %% md
### read in the iceflow data from the iceflow data files and save them to a pickle file
# %%
try:
    iceflow_data = iceflow_data_file_loader()
    print("The iceflow data pickle file was found and loaded.")
except FileNotFoundError:
    print("The iceflow data pickle file was not found. Creating a new one...")
    filename = iceflow_saver()
    iceflow_data = iceflow_loader(filename)
    print("The iceflow data pickle file was successfully created.")

x = iceflow_data[0]
y = iceflow_data[1]
velocity_x = iceflow_data[2]
velocity_y = iceflow_data[3]
latitude = iceflow_data[4]
longitude = iceflow_data[5]
# %% md
# next step: continue working through crossover.py to rebuild the code
# %%
intersection_points, intersection_indices, segment_ends = cross_point(layers[0], seg_length, quiet=True)
# find the crossover points
print(f"len(intersection_indices): {len(intersection_indices)}")
print(f"len(intersection_points): {len(intersection_points)}")
# %%
""" Current Project 30Jan24 """
# TODO: deconstruct the nested lists and make them make more sense

print(f"intersection_indices: {intersection_indices}")
print(f"intersection_points: {intersection_points}")


# %%
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

    # TODO: add an offset to the zoom settings so that the crossover point is in the center of the zoomed in map

    # # this code sets up a polar stereographic map of antarctica with the South Pole in the center
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
    m = Basemap(projection='ortho', lat_0=lat_0, lon_0=lon_0, llcrnrx=llcrnrx,
                llcrnry=llcrnry, urcrnrx=urcrnrx, urcrnry=urcrnry, resolution='c')

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
    # m.scatter(0, -90, latlon=True, color='black', linewidth=1, label='South Pole')
    # plot the crossover points
    for point in intersection_points:
        m.scatter(point[1], point[0], latlon=True, color='darkred', linewidth=1, label='Crossover Point')
        plt.text(m(point[1], point[0])[0], m(point[1], point[0])[1] - 10000, 'Crossover Point\n\n',
                 fontsize='smaller', fontweight='bold', ha='center', va='top', color='darkred')

    # m.scatter(intersection_points[cross_index][1], intersection_points[cross_index][0], latlon=True, color='darkred',
    #           linewidth=1, label='Crossover Point')
    # plt.text(m(intersection_points[cross_index][1], intersection_points[cross_index][0])[0],
    #          m(intersection_points[cross_index][1], intersection_points[cross_index][0])[1] - 10000,
    #          'Crossover Point\n\n',
    #          fontsize='smaller', fontweight='bold', ha='center', va='top', color='darkred')

    # plot the crossover line

    x, y = m(0, -90)
    # plt.text(x, y, '\nSouth Pole', fontsize='smaller', fontweight='bold', ha='center', va='top', color='black')
    plt.title("Lat-Lon Map")
    # set tight layout
    # plt.tight_layout()

    # save the plot
    plt.savefig("layer_plot.png", dpi=250)

    plt.show()

    print("plotted map")
    print("--------------------\n")


# %%
# plot_layers_at_cross(layers, intersection_indices_base, intersection_points_base,cross_index=3, zoom=zoom)

plot_layers_at_cross(layers, intersection_indices, intersection_points, cross_index=0, zoom=zoom)
# %%

# %%
# def nearest_flow_to_latlon(lat, lon, iceflow_data):
#     """
#     :param lat: the latitude of the point
#     :param lon: the longitude of the point
#     :param iceflow_data: the iceflow data
#     :return: the nearest iceflow data to the lat-lon point
#     """
#     # find the nearest x and y values in the iceflow data
#     x, y = latlon_to_xy(lat, lon)
#     x, y = find_nearest_unmasked_x_and_y(x, y, iceflow_data, max_radius=1000)
#     flow = flow_at_x_y(x, y, iceflow_data)
#     return flow

nearest_flow_to_latlon(intersection_points[0][0], intersection_points[0][1], iceflow_data)
# %%
# calculate the twtt at the crossover point on both segments
twtt = twtt_at_point(layers[1], layers[0], intersection_indices, quiet=True)
print(f"twtt: {twtt}")

# %%
delta_twtt = twtt[0][1] - twtt[0][0]
print(f"delta_twtt: {delta_twtt}")

# find the angle and magnitude of the velocity at the crossover point
flow = nearest_flow_to_latlon(intersection_points[0][0], intersection_points[0][1], iceflow_data)
print(f"flow: {flow}")
angle = math.degrees(math.atan2(flow[1], flow[0]))
print(f"angle: {angle}")
magnitude = math.sqrt(flow[0] ** 2 + flow[1] ** 2)
print(f"magnitude: {magnitude}")

# find the heading of the first segment
heading_1 = find_heading(layers[0], intersection_indices[0][0])
print(f"heading_1: {heading_1}")

# find the heading of the second segment
heading_2 = find_heading(layers[0], intersection_indices[0][1])
print(f"heading_2: {heading_2}")
# %%
# repeat the above for every crossover point
twtt = twtt_at_point(layers[1], layers[0], intersection_indices, quiet=True)
delta_twtt = []
flow = []
angle = []
magnitude = []
heading_1 = []
heading_2 = []
for i in range(len(intersection_indices)):
    print(f"twtt{i}: {twtt[i]}")

    delta_twtt.append(twtt[i][1] - twtt[i][0])
    print(f"delta_twtt[{i}]: {delta_twtt[i]}")

    # find the angle and magnitude of the velocity at the crossover point
    flow.append(nearest_flow_to_latlon(intersection_points[i][0], intersection_points[i][1], iceflow_data))
    print(f"flow[{i}]: {flow[i]}")
    angle.append(math.degrees(math.atan2(flow[i][1], flow[i][0])))
    print(f"angle[{i}]: {angle[i]}")
    magnitude.append(math.sqrt(flow[i][0] ** 2 + flow[i][1] ** 2))
    print(f"magnitude[{i}]: {magnitude[i]}")

    # find the heading of the first segment
    heading_1.append(find_heading(layers[0], intersection_indices[i][0]))
    print(f"heading_1[{i}]: {heading_1[i]}")

    # find the heading of the second segment
    heading_2.append(find_heading(layers[0], intersection_indices[i][1]))
    print(f"heading_2[{i}]: {heading_2[i]}")
    print(section_break)

    # TODO: check flow vector units and make sure it matches heading

# if the delta_twtt is a nan, remove all of the data for that crossover point from the lists
# for i in range(len(delta_twtt)):
#     if math.isnan(delta_twtt[i]):
#         delta_twtt.pop(i)
#         flow.pop(i)
#         angle.pop(i)
#         magnitude.pop(i)
#         heading_1.pop(i)
#         heading_2.pop(i)
#         intersection_indices.pop(i)
#         intersection_points.pop(i)
#         print(f"intersection {i} removed")
#         print(section_break)

length = len(delta_twtt)
while i < length:
    if math.isnan(delta_twtt[i]):
        delta_twtt.pop(i)
        flow.pop(i)
        angle.pop(i)
        magnitude.pop(i)
        heading_1.pop(i)
        heading_2.pop(i)
        intersection_indices.pop(i)
        intersection_points.pop(i)
        print(f"intersection {i} removed")
        print(section_break)
        length -= 1
    else:
        i += 1
# %%
# plot delta_twtt vs |cos(angle - heading)| for each crossover point
import scipy.optimize as opt;

# %%
# plot delta_twtt vs |cos(angle - heading) - sin(angle - heading)| * |magnitude|  for each crossover point
plt.figure(figsize=(24, 12), layout='constrained')
# plt.scatter(np.abs(np.cos(np.radians(np.array(angle) - np.array(heading_1)))) * np.abs(np.array(magnitude)), delta_twtt, label='segment 1')
# plt.scatter(np.abs(np.cos(np.radians(np.array(angle) - np.array(heading_2)))) * np.abs(np.array(magnitude)), delta_twtt, label='segment 2')


plt.scatter(np.abs(np.cos(np.radians(np.array(angle) - np.array(heading_1)))), delta_twtt, label='segment 1')
plt.scatter(np.abs(np.cos(np.radians(np.array(angle) - np.array(heading_2)))), delta_twtt, label='segment 2')

# plt.xlabel(" |cos(angle - heading)| * |velocity|")
plt.xlabel(" |cos(angle - heading)|")
plt.ylabel("delta_twtt")
# plt.title(" |cos(angle - heading)| vs delta_twtt")
plt.title(f"{season} {flight} \n|cos(angle - heading)| vs delta_twtt", fontsize=20)

plt.legend(["legend"], fontsize='smaller', loc='upper right', bbox_to_anchor=(1.1, 1.1))
# scale axes to be logarithmic
# plt.xscale('log')
# plt.yscale('log')


# save the plot as a png file with a high dpi named after the season and flight
plt.savefig(f"{season}_{flight}_cos_angle_heading_vs_delta_twtt_linear.png", dpi=300)

# plt.show()

# plt.yscale('log')
# save the plot as a png file with a high dpi named after the season and flight
# plt.savefig(f"{season}_{flight}_cos_angle_heading_vs_delta_twtt_logy.png", dpi=300)
plt.show()

# %%
# x_data = np.abs(np.cos(np.radians(np.array(angle) - np.array(heading_1))))
# y_data = delta_twtt
#
# # Define the Gaussian function
# def gaussian(x, amplitude, mean, stddev):
#     return amplitude * np.exp(-((x - mean) ** 2) / (2 * stddev ** 2))
#
# # Initial parameter guesses: amplitude close to your data's scale, mean around the center, and a reasonable stddev
# initial_guesses = [1e-8, 0.5, 0.1]
#
# # Use curve_fit to fit the Gaussian function to your data
# popt, pcov = opt.curve_fit(gaussian, x_data, y_data, p0=initial_guesses, maxfev=5000)
#
# # Plot the original data
# plt.scatter(x_data, y_data, label='Data')
#
# # Plot the fitted curve
# x_fit = np.linspace(min(x_data), max(x_data), 1000)
# y_fit = gaussian(x_fit, *popt)
# plt.plot(x_fit, y_fit, color='red', label='Fitted curve')
#
# plt.xlabel('X axis')
# plt.ylabel('Y axis')
# plt.title('Gaussian Fit to Data')
# plt.legend()
# plt.show()
# %% md
ntuple - ize
cos(heading - flow)
difference in theta
paralell and perpindicular
delta_twtt
v_flow
- stop
selecting
for angle in upper cells, we can cut the data once we have it

ARA
meeting in March
Columbus
- talk
to
Kiet
about
how
he is setting
up
travel
# %%
heading = []
# for each plane heaading, add [heading_1, heading_2] to the heading list
for i in range(len(heading_1)):
    heading.append([heading_1[i], heading_2[i]])
# %%
print(flow)


# %%
# # save the posit to a json file
# import json
#
# filename = f"{season}_crossover_data.json"
#
# # check to see if the file exists and if it does, load the data from it, otherwise append the data to a new file
# try:
#     with open(filename, 'r') as file:
#         data = json.load(file)
#         print(f"File {filename} exists. Loading data from file...")
# except FileNotFoundError:
#     print(f"File {filename} does not exist. Creating a new file...")
#     data = []
#
# # if the data is not already in the file, append the data to the file
# if data:
#     print(f"Data already in file {filename}.")
# else:
#     print(f"Appending data to file {filename}...")
#     data.append({
#         "season": season,
#         "flight": flight,
#         "intersection_points": intersection_points,
#         "twtt": twtt,
#         "delta_twtt": delta_twtt,
#         "ice flow vectors (m/yr, in xy)": flow,
#         "ice flow angle": angle,
#         "ice flow magnitude": magnitude,
#         "plane heading": heading
#     })
#     with open(filename, 'w') as file:
#         json.dump(data, file)
#     print(f"Data successfully appended to file {filename}.")
#
#
# # TODO: convert flow vector and angle to EPSG:4326
# %%

# %% md
### vector to heading dev below, DELETE WHEN FUNCTIONAL
# %%
def nearest_flow_to_latlon(lat, lon, iceflow_data, print_point=False):
    """
    :param lat: the latitude of the point
    :param lon: the longitude of the point
    :param iceflow_data: the iceflow data
    :return: the nearest flow vector to the lat-lon point available in the iceflow data
    """
    # find the nearest x and y values in the iceflow data
    x, y = latlon_to_xy(lat, lon)
    x, y = find_nearest_unmasked_x_and_y(x, y, iceflow_data, max_radius=1000)
    if print_point:
        print(f"Nearest point to lat-lon: {xy_to_latlon(x, y)} or {x, y} in EPSG:3031")
    flow = flow_at_x_y(x, y, iceflow_data)
    return flow


# %%
intersect_x = intersection_points[0][0]
intersect_y = intersection_points[0][1]
print(f"lat-lon: {intersect_x, intersect_y}\n")

x, y = latlon_to_xy(intersect_x, intersect_y)
print(f"x: {x}, y: {y}\n")

x_lat, y_lat = xy_to_latlon(x, y)
print(f"x: {x}, y: {y}\nlat-lon: {x_lat, y_lat}\n")


# So the conversion functions work
# %%
def find_nearest_unmasked_x_and_y(x, y, iceflow_data, max_radius=100):
    """
    Find the nearest x and y value in the iceflow data to an input x and y value.
    If the ice velocity is masked at that point, it will return the next nearest point that is not masked.
    """
    # x_index_base = (np.abs(iceflow_data[0] - x)).argmin()
    # y_index_base = (np.abs(iceflow_data[1] - y)).argmin()

    x_index_base = x
    y_index_base = y
    # the index bases are
    print(f"x_index_base: {x_index_base}, y_index_base: {y_index_base}")

    # for x_offset, y_offset in generate_spiral_indices(0, 0, max_radius=max_radius):
    for x_offset, y_offset in generate_spiral_indices(x_index_base, y_index_base, max_radius=max_radius):
        x_index = x_index_base + x_offset
        y_index = y_index_base + y_offset

        if (
                # 0 <= x_index < iceflow_data[2].shape[0]  # if the x index is within the bounds of the iceflow data
                # and 0 <= y_index < iceflow_data[2].shape[1]

                np.min(iceflow_data[2]) <= x_index <= np.max(
            iceflow_data[2])  # if the x index is within the bounds of the iceflow data
                and np.min(iceflow_data[3]) <= y_index <= np.max(iceflow_data[3])

                and not np.ma.is_masked(iceflow_data[2][x_index][y_index])
                and not np.ma.is_masked(iceflow_data[3][x_index][y_index])
        ):
            return x_index, y_index
        # else:
        # print(f"no unmasked point found within {max_radius} of {x_index_base, y_index_base}")

    # Return the original indices if no unmasked point is found in the search area
    if x_index_base == x and y_index_base == y:
        print(f"no unmasked point found within {max_radius} of {x_index_base, y_index_base}")
    return x_index_base, y_index_base


# %%
x_unmasked, y_unmasked = find_nearest_unmasked_x_and_y(x, y, iceflow_data, max_radius=1000)
print(f"x: {x}, y: {y}\nunmasked x: {x_unmasked}, unmasked y: {y_unmasked}")

# print(f"shape: {iceflow_data[2].shape[1]}")
# print the min and max values of the iceflow data
# print(f"min x: {np.min(iceflow_data[0])}, max x: {np.max(iceflow_data[0])}")