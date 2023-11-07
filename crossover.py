import math
from layer_class import Twtt_Posit
from library import *

zoom = False
# zoom = True
seg_length = 100
season = "2018_Antarctica_DC8"
# season = "2016_Antarctica_DC8"
flight = "20181030_01"  # the flight date and frame number
# flight = "20181103_01"
# flight = "20181112_02"
# flight = "20161024_05"
file_name = "layer_export_" + flight + ".pickle"

# TODO: make map plotter center on crossover point n. default to centering on the first crossover point if no n is given
# TODO: choose a crossover point or save the data for them or something. Do we already do this? Probably. Very tired.
    # Who is this we?

layers = read_layers(file_name)  # read in the layers from the pickle file

intersection_points, intersection_indices, segment_ends = cross_point(layers[0], seg_length, quiet=False)
# find the crossover points

posit = Twtt_Posit(layers[1], season, flight, intersection_indices)
# create a Twtt_Posit object to store the crossover point data
# print(f"posit.layer_name: {posit.layer_name}")

save_posit(posit)

print(gps_time_to_seconds(layers[0].gps_time[intersection_indices[0][0]]))

# find the plane's velocity in m/s using the distance between the endpoints and the time between the endpoints
time1 = gps_time_to_seconds(layers[0].gps_time[intersection_indices[0][0]])
time2 = gps_time_to_seconds(layers[0].gps_time[intersection_indices[0][1]])
print(f"time1: {time1}, time2: {time2}")
d_time = time2 - time1
print(f"Time between segment 1 endpoints: {d_time} s")
dist = latlon_dist(segment_ends[0][0][0], segment_ends[0][0][1])
print(f"Distance between segment 1 endpoints: {round(dist,2)} m")
vel = dist / d_time
print(f"Plane velocity: {round(vel,2)} m/s")


# vel_ms, vel_kh = plane_velocity(segment_ends[0][0][0], segment_ends[0][0][1], time1,time2)


# print(f"Plane velocity: {round(vel_ms,2)} m/s or {round(vel_kh,2)} km/h")


# print(layers[1].layer_name)
slope = slope_around_index(layers[1], intersection_indices[0][0], 2)
print(f"{round(slope,2)}")


"""
Clean this up and put it in a function in the library file (?)
"""

print("Comparing my depth to CReSIS depth...")
print("--------------------")
twtt_at_intersect = twtt_at_point(layers[1], layers[0], intersection_indices, quiet=True)
# find the twtt at the crossover points
twtt_difference_at_intersect = twtt_at_intersect[0][0] - twtt_at_intersect[0][1]
# find the difference in twtt at the crossover points
print(f"twtt difference at crossover point: {twtt_difference_at_intersect} ns")

my_refractive_index = 1.77
# my_depth_1 = twtt_to_depth(twtt_at_intersect[0][0], my_refractive_index)
# my_depth_2 = twtt_to_depth(twtt_at_intersect[0][1], my_refractive_index)
#
# print(f"By my refractive index: {my_refractive_index}")
# print(f"depth at crossover point on segment 1: {my_depth_1} m")
# print(f"depth at crossover point on segment 2: {my_depth_2} m")
# print(f"difference: {my_depth_1 - my_depth_2} m")

# loop through all intersections and print the depth at each
for i in range(len(intersection_indices)):
    my_depth_1 = twtt_to_depth(twtt_at_intersect[i][0], my_refractive_index)
    my_depth_2 = twtt_to_depth(twtt_at_intersect[i][1], my_refractive_index)
    print(f"depth at crossover point {i} on segment 1: {my_depth_1} m")
    print(f"depth at crossover point {i} on segment 2: {my_depth_2} m")
    print(f"difference: {my_depth_1 - my_depth_2} m")

print(f"crossover point lat-long: {intersection_points[0]}")

cresis_refractive_index = math.sqrt(3.15)
# cresis_refractive_index = 1.785
cresis_depth_1 = twtt_to_depth(twtt_at_intersect[0][0], cresis_refractive_index)
cresis_depth_2 = twtt_to_depth(twtt_at_intersect[0][1], cresis_refractive_index)

print(f"By CReSIS refractive index: {cresis_refractive_index}")
print(f"depth at crossover point on segment 1: {cresis_depth_1} m")
print(f"depth at crossover point on segment 2: {cresis_depth_2} m")
print(section_break)
"""
End of the cleanup (for now)
"""