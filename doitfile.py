from project_classes import *
from functions import *
from iceflow_library import *

# TODO: unfuck section breaks in printout

""" Set the season andn flight number here """
season = "2018_Antarctica_DC8" # a layerData season
# season = "2016_Antarctica_DC8" # a season with both layer and layerData
# season = "2014_Antarctica_DC8" # a layerData season
flight = "20181030_01"  # the flight date and frame number
flight = "20181103_01"
flight = "20181112_02"  # the problem flight
# flight = "20161024_05" # the one that the notebook was primarily tested on, CX index 9 gives negative delta_twtt (as of 20Feb24)
# flight = '20141026_06'

file_name = "layer_export_" + flight + ".pickle"
draw_plots = True
draw_plots = False
zoom = True
seg_length = 100
testing = False
""" shouldn't need to change anything below here """

# read the layers

mat_pickler_layerData(season, flight, testing_mode=testing)  # make it
# mat_pickler_layer(season, flight, testing_mode=testing)  # pickles the layerData object
layers = read_layers(file_name)  # read in the layers from the pickle file

# read the iceflow data
if not os.path.isfile("iceflow_data.pickle"):  # if the file does not exist
    print("The iceflow data pickle file was not found. Creating a new one...")
    filename = iceflow_saver()
    iceflow_data = iceflow_loader(filename)
    print("The iceflow data pickle file was successfully created.")
iceflow_data = iceflow_loader("iceflow_data.pickle")
print("The iceflow data pickle file was found and loaded.")

x = iceflow_data[0]
y = iceflow_data[1]
velocity_x = iceflow_data[2]
velocity_y = iceflow_data[3]
latitude = iceflow_data[4]
longitude = iceflow_data[5]

# read or load the crossover points
filename = f"{season}_{flight}_crossover_points.pickle"
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
print(section_break)

# plot the crossover points
if draw_plots:
    plot_layers_at_cross(layers, intersection_indices, intersection_points, zoom=zoom, cross_index=0)

# compile the crossover point data into lists
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
    x, y = latlon_to_xy(lat, lon)
    x_index, y_index = x_to_index(x), y_to_index(y)
    nearest_x_index, nearest_y_index = xy_to_nearest_unmasked_index(x, y, iceflow_data, max_radius=10)

    # find the nearest good iceflow_data to the crossover point
    nearest_lat = iceflow_data[4][nearest_x_index][nearest_y_index]
    nearest_lon = iceflow_data[5][nearest_x_index][nearest_y_index]

    flow_xy.append([iceflow_data[2][nearest_x_index][nearest_y_index], iceflow_data[3][nearest_x_index][nearest_y_index]])

    # find the heading of the flow vector
    flow_heading_full.append(xyindex_vector_to_heading(nearest_x_index, nearest_y_index, flow_xy[i][0], flow_xy[i][1]))
    flow_heading.append(flow_heading_full[i][0])

    # find the heading of the first segment
    plane_heading_1.append(find_heading(layers[0], intersection_indices[i][0]))

    # find the heading of the second segment
    plane_heading_2.append(find_heading(layers[0], intersection_indices[i][1]))

    plane_flow_angle = min(abs(plane_heading_1[i] - flow_heading[i]), abs(plane_heading_2[i] - flow_heading[i]))
    # print(f"plane_flow_angle: {plane_flow_angle}")

    # find the twtt at the crossover point on both segments
    delta_twtt.append(twtt[i][1] - twtt[i][0])


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


""" this is WIP code and is not yet verified functional """
#TODO: see doit.ipynb, this chunk needs cleaned and functionized
# TODO: verify this plot is correct
# TODO: verify the Y scale and label it
    # Dave expects the delta_twtt to be ~0.1 sec
# plot delta_twtt vs |cos(angle - heading) - sin(angle - heading)| * |magnitude|  for each crossover point
plt.figure(figsize=(24, 12), layout='constrained')
# plt.scatter(np.abs(np.cos(np.radians(np.array(angle) - np.array(heading_1)))) * np.abs(np.array(magnitude)), delta_twtt, label='segment 1')
# plt.scatter(np.abs(np.cos(np.radians(np.array(angle) - np.array(heading_2)))) * np.abs(np.array(magnitude)), delta_twtt, label='segment 2')

# plt.scatter(np.abs(np.cos(np.radians(np.array(angle) - np.array(plane_heading_1)))), delta_twtt, label='segment 1')  # angle - heading
# plt.scatter(np.abs(np.cos(np.radians(np.array(angle) - np.array(plane_heading_2)))), delta_twtt, label='segment 2')

plt.scatter(np.abs(np.cos(np.radians(np.array(flow_heading) - np.array(plane_heading_1)))), delta_twtt, label='segment 1')  # flow angle - heading without velocity
plt.scatter(np.abs(np.cos(np.radians(np.array(flow_heading) - np.array(plane_heading_2)))), delta_twtt, label='segment 2')

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

