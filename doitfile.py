import matplotlib.pyplot as plt

from project_classes import *
from functions import *
from iceflow_library import *
import os
# %%
zoom = True
seg_length = 100
testing = False

# %%
# %%
def doit(season, flight):
    """
    read in the layers from the layer files and save them to a pickle file
    """
    # mat_pickler_layer(season, flight, testing_mode=testing)  # make it
    mat_pickler_h5py(season, flight, testing_mode=testing)  # make it
    layers = read_layers(file_name)  # read in the layers from the pickle file

    # %% md
    ### read in the iceflow data from the iceflow data files and save them to a pickle file
    # %%
    if not os.path.isfile(
            "C:\\Users\\rj\\Documents\\cresis_project\\pickle_jar\\iceflow_data.pickle"):  # if the file does not exist
        print("The iceflow data pickle file was not found. Creating a new one...")
        filename = iceflow_saver()
        iceflow_data = iceflow_loader(filename)
        print("The iceflow data pickle file was successfully created.")
    # try:
    iceflow_data = iceflow_loader("C:\\Users\\rj\\Documents\\cresis_project\\pickle_jar\\iceflow_data.pickle")
    print("The iceflow data pickle file was found and loaded.")

    x = iceflow_data[0]
    y = iceflow_data[1]
    velocity_x = iceflow_data[2]
    velocity_y = iceflow_data[3]
    latitude = iceflow_data[4]
    longitude = iceflow_data[5]
    print("iceflow data loaded")
    # %%
    # if the file at filename exists, read in the intersect_indices and intersection_points from the pickle file
    # otherwise, find the intersect_indices and intersection_points and save them to a pickle file
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
    """ Current Project 30Jan24 """
    # TODO: deconstruct the nested lists and make them make more sense
    # put them in class objects

    print(f"intersection_indices: {intersection_indices}")
    print(f"intersection_points: {intersection_points}")
    # %%
    plot_map(layers, intersection_indices, intersection_points, iceflow_data, season, flight, zoom=False, cross_index=0,
             filename=(season + "_" + flight + "crossover"))
    plot_layers_at_cross(layers, intersection_indices, intersection_points, season, flight,
                         filename=(season + "_" + flight + "crossover"))
    # %% md

    # %%
    # twtt 1 = 1.4212416976291829e-05
    twtt = twtt_at_point(layers[1], layers[0], intersection_indices, quiet=True)[0]
    print(f"twtt: {twtt}")

    # twtt 2 = 1.395535327834069e-05

    # find the depth of both twtt 1 and 2

    depth1 = twtt_to_depth(twtt[0], refractive_index=1.77)
    print(f"depth1: {depth1}")
    depth2 = twtt_to_depth(twtt[1], refractive_index=1.77)
    print(f"depth2: {depth2}")

    # find the difference in depth
    print(f"depth2 - depth1: {depth2 - depth1}")

    deltatwtt = twtt[1] - twtt[0]
    print(f"delta twtt: {deltatwtt}")
    # %% md

    # # x,y are the first intersection point
    # lat = intersection_points[4][0]
    # lon = intersection_points[4][1]
    # # lat = -82.1
    # # lon = -46
    #
    # print(f"lat-lon: {lat, lon}")
    # x, y = latlon_to_xy(lat, lon)
    # print(f"x: {x}, y: {y}")
    # nearest_x_index, nearest_y_index = xy_to_nearest_unmasked_index(x, y, iceflow_data, max_radius=10)
    # print(f"nearest_x_index: {nearest_x_index}, nearest_y_index: {nearest_y_index}")
    # nearest_lat = iceflow_data[4][nearest_x_index][nearest_y_index]
    # nearest_lon = iceflow_data[5][nearest_x_index][nearest_y_index]
    # print(f"nearest_lat: {nearest_lat}, nearest_lon: {nearest_lon}")
    # %%
    """
    remove and update the iceflow library once this works
    """


    def xyindex_vector_to_heading(x_index, y_index, x_vector, y_vector):
        """
        This function is used to convert an x and y vector in EPSG:3031 to a heading in EPSG:4326.
        :param x_index: the x coordinate
        :param y_index: the y coordinate
        :param x_vector: the x vector
        :param y_vector: the y vector
        :return: the heading in EPSG:4326
        """
        # convert the x and y indices to x and y coordinates
        x, y = index_to_x(x_index), index_to_y(y_index)

        base_plus_x_vector = x + x_vector
        base_plus_y_vector = y + y_vector

        # convert the x and y vector to lat and lon
        lat_vector, lon_vector = xyindex_to_latlon(base_plus_x_vector, base_plus_y_vector)

        # calculate the heading of the vector
        # convert the x and y indices to lat and lon
        lat, lon = xyindex_to_latlon(x_index, y_index)
        geodesic = pyproj.Geod(ellps='WGS84')
        angle1, angle2, distance = geodesic.inv(lon, lat, lon_vector, lat_vector)
        return angle1, angle2, distance


    # %%
    # repeat the above for every crossover point
    flow_xy = []  # the flow vector in xy
    flow_heading_full = []  # the flow vector heading in angle1, angle2, distance (in meters)
    flow_heading = []
    plane_heading_1 = []
    plane_heading_2 = []
    angle = []  # the angle between the flow vector and the plane heading
    twtt = twtt_at_point(layers[1], layers[0], intersection_indices, quiet=True)
    delta_twtt = []

    for i in range(len(intersection_indices)):
        # convert the lat-lon point to xy and then to indices
        lat, lon = intersection_points[i]
        # print(f"lat-lon {i}: \t\t{lat[0], lon[0]}")

        x, y = latlon_to_xy(lat, lon)
        # print(f"x: {x}, y: {y}")

        x_index, y_index = x_to_index(x), y_to_index(y)
        # print(f"x_index: {x_index}, y_index: {y_index}")

        nearest_x_index, nearest_y_index = xy_to_nearest_unmasked_index(x, y, iceflow_data, max_radius=10)

        # find the nearest good iceflow_data to the crossover point
        nearest_lat = iceflow_data[4][nearest_x_index][nearest_y_index]
        nearest_lon = iceflow_data[5][nearest_x_index][nearest_y_index]
        # print(f"nearest_lat-lon: \t{nearest_lat, nearest_lon}")

        flow_xy.append(
            [iceflow_data[2][nearest_x_index][nearest_y_index], iceflow_data[3][nearest_x_index][nearest_y_index]])
        print(f"flow at nearest: {flow_xy[i]}")

        # find the heading of the flow vector
        flow_heading_full.append(xyindex_vector_to_heading(nearest_x_index, nearest_y_index, flow_xy[i][0], flow_xy[i][1]))
        flow_heading.append(flow_heading_full[i][0])
        print(f"flow_heading[{i}]: {flow_heading[i]}")

        # find the heading of the first segment
        plane_heading_1.append(find_heading(layers[0], intersection_indices[i][0]))
        # print(f"heading_1[{i}]: {plane_heading_1[i]}")

        # find the heading of the second segment
        plane_heading_2.append(find_heading(layers[0], intersection_indices[i][1]))
        # print(f"heading_2[{i}]: {plane_heading_2[i]}")

        # plane_flow_angle = min(abs(plane_heading_1[i] - flow_heading[i]), abs(plane_heading_2[i] - flow_heading[i]))
        plane_flow_angle = max(abs(plane_heading_1[i] - flow_heading[i]), abs(plane_heading_2[i] - flow_heading[i]))

        # print(f"plane_flow_angle: {plane_flow_angle}")
        angle.append(plane_flow_angle)

        # find the twtt at the crossover point on both segments
        # print(f"twtt{i}: {twtt[i]}")
        # delta_twtt.append(twtt[i][1] - twtt[i][0])
        # append the absolute value of the twtt
        delta_twtt.append(abs(twtt[i][1] - twtt[i][0]))
        # print(f"delta_twtt[{i}]: {delta_twtt[i]}")

        print(section_break)

    length = len(delta_twtt)
    while i < length:  # remove any nan valued points from the lists
        if math.isnan(delta_twtt[i]):
            delta_twtt.pop(i)
            flow_xy.pop(i)
            angle.pop(i)
            magnitude.pop(i)
            plane_heading_1.pop(i)
            plane_heading_2.pop(i)
            intersection_indices.pop(i)
            intersection_points.pop(i)
            print(f"intersection {i} removed")
            print(section_break)
            length -= 1
        else:
            i += 1


    # %%
    for i in range(len(flow_heading)):
        print(f"flow_heading[{i}]: {flow_heading[i]}")
        print(f"plane_heading_1[{i}]: {plane_heading_1[i]}")
        print(f"plane_heading_2[{i}]: {plane_heading_2[i]}")
        print(f"plane_heading_1 - flow_heading[{i}]: {abs(plane_heading_1[i] - flow_heading[i])}\n")

    # %% md
    # TODO: functionize this plot once it works
    # %%
    # TODO: verify this plot is correct
    # TODO: verify the Y scale and label it
    # Dave expects the delta_twtt to be ~0.1 sec
    # plot delta_twtt vs |cos(angle - heading) - sin(angle - heading)| * |magnitude|  for each crossover point
    plt.figure(figsize=(24, 12), layout='constrained')
    # plt.scatter(np.abs(np.cos(np.radians(np.array(angle) - np.array(heading_1)))) * np.abs(np.array(magnitude)), delta_twtt, label='segment 1')
    # plt.scatter(np.abs(np.cos(np.radians(np.array(angle) - np.array(heading_2)))) * np.abs(np.array(magnitude)), delta_twtt, label='segment 2')

    # plt.scatter(np.abs(np.cos(np.radians(np.array(angle) - np.array(plane_heading_1)))), delta_twtt, label='segment 1')  # angle - heading
    # plt.scatter(np.abs(np.cos(np.radians(np.array(angle) - np.array(plane_heading_2)))), delta_twtt, label='segment 2')

    # cos(angle - heading) vs delta_twtt
    # plt.scatter(np.abs(np.cos(np.radians(np.array(flow_heading) - np.array(plane_heading_1)))), delta_twtt, label='segment 1')  # flow angle - heading
    # plt.scatter(np.abs(np.cos(np.radians(np.array(flow_heading) - np.array(plane_heading_2)))), delta_twtt, label='segment 2')

    # |cos(angle - heading) - sin(angle - heading) |vs delta_twtt
    # plt.scatter(np.abs(np.cos(np.radians(np.array(angle) - np.array(plane_heading_1))) - np.sin(np.radians(np.array(angle) - np.array(plane_heading_1)))), delta_twtt, label='segment 1')  # angle - heading
    # plt.scatter(np.abs(np.cos(np.radians(np.array(angle) - np.array(plane_heading_2))) - np.sin(np.radians(np.array(angle) - np.array(plane_heading_2)))), delta_twtt, label='segment 2')

    # |cos(θ) – sin(φ)| vs delta_twtt. theta is the angle between the flow vector and the plane heading on segment 1, phi is the angle between the plane headings on segments 1 and 2
    for i in range(len(delta_twtt)):
        theta = angle[i]
        phi = abs(plane_heading_1[i] - plane_heading_2[i])
        print(
            f"theta: {theta}, phi: {phi} for i: {i}\n cos(theta): {np.cos(np.radians(theta))}, sin(phi): {np.sin(np.radians(phi))}")
        plt.scatter(np.abs(np.cos(np.radians(theta)) - np.sin(np.radians(phi))), delta_twtt[i],
                    label='segment 1')  # angle - heading

    # for each point, print the index and the delta_twtt
    # for i in range(len(delta_twtt)):
    #     plt.text(np.abs(np.cos(np.radians(np.array(flow_heading[i]) - np.array(plane_heading_1[i])))), delta_twtt[i], f"{i}: {delta_twtt[i]}")

    # plt.xlabel(" |cos(angle - heading)| * |velocity|")
    # plt.xlabel(" |cos(angle - heading)|")
    plt.xlabel("|cos(θ) – sin(φ)|")

    plt.ylabel("delta_twtt (s)")
    # plt.title(" |cos(angle - heading)| vs delta_twtt")
    # plt.title(f"{season} {flight} \n|cos(angle - heading)| vs delta_twtt", fontsize=20)
    plt.title(f"{season} {flight} \n|cos(θ) – sin(φ)| vs delta_twtt", fontsize=20)

    plt.legend(["legend"], fontsize='smaller', loc='upper right', bbox_to_anchor=(1.1, 1.1))
    # scale axes to be logarithmic
    # plt.xscale('log')
    plt.yscale('log')

    # get the current directory
    dir = os.getcwd()

    # save the plot as a png file with a high dpi named after the season and flight
    # plt.savefig(f"C:\\Users\\rj\Documents\\cresis_project\\screens\\{season}_{flight}_cos_angle_heading_vs_delta_twtt_logy.png", dpi=300)
    plt.savefig(f"{dir}\\screens\\{season}_{flight}_cos_angle_heading_vs_delta_twtt_logy.png", dpi=300)

    # plt.show()

    plt.yscale('linear')
    # save the plot as a png file with a high dpi named after the season and flight
    plt.savefig(f"{dir}\\screens\\{season}_{flight}_cos_angle_heading_vs_delta_twtt_lineary.png", dpi=300)
    # plt.show()

    print(f"saved plot as {dir}\\screens\\{season}_{flight}_cos_angle_heading_vs_delta_twtt.png")



seasons = ["2009_Antarctica_DC8", "2018_Antarctica_DC8", "2016_Antarctica_DC8", "2014_Antarctica_DC8"]
flights = ["20181030_01", "20181018_01", "20181103_01", "20181109_01", "20181112_02", "20161024_05", "20161111_05",
           "20141026_06"]
for season in seasons:
    for flight in flights:
        # if the year of the season and the flight match
        if season[:4] == flight[:4]:
            file_name = "C:\\Users\\rj\\Documents\\cresis_project\\pickle_jar\\layer_export_" + flight + ".pickle"
            doit(season, flight)

# season = "2009_Antarctica_DC8"
# season = "2018_Antarctica_DC8" # a layerData season
# season = "2016_Antarctica_DC8"  # a season with both layer and layerData
# season = "2014_Antarctica_DC8" # a layerData season
# flight = "20181030_01"  # the flight date and frame numbe
# flight = "20181018_01"
# flight = "20181103_01"
# flight = "20181109_01"
# flight = "20181112_02"  # the problem flight
# flight = "20161024_05"
# flight = "20161111_05"
# flight = "20161024_05"
# flight = '20141026_06'
# file_name = "layer_export_" + flight + ".pickle"
# file_name = "C:\\Users\\rj\\Documents\\cresis_project\\pickle_jar\\layer_export_" + flight + ".pickle"
