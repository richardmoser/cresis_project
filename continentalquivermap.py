import matplotlib.pyplot as plt
from project_classes import *
from functions import *

testing = False

"""
read in the layers from the layer files and save them to a pickle file
"""
# mat_pickler_h5py(season, flight, testing_mode=testing)  # make it
# layers = read_layers(file_name)  # read in the layers from the pickle file

### read in the iceflow data from the iceflow data files and save them to a pickle file
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


def plot_map(iceflow_data, zoom=False):
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
    # print(f"debug: lat_0: {lat_0}, lon_0: {lon_0}")
    if plot_it:
        # m = Basemap(projection='ortho', lat_0=lat_0, lon_0=lon_0, llcrnrx=llcrnrx,
                    # llcrnry=llcrnry, urcrnrx=urcrnrx, urcrnry=urcrnry, resolution='c')
        m = Basemap(projection='spstere', lat_0=-90, lat_ts=-71, lon_0=0, boundinglat=-62.5, resolution='h')
        m.drawcoastlines()
        m.fillcontinents(color='grey', lake_color='aqua')
        m.drawparallels(np.arange(-80., 81., 20.))
        m.drawparallels(np.arange(-70., 81., 20.))
        m.drawmeridians(np.arange(-180., 181., 20.))
        m.drawmapboundary(fill_color='aqua')


    center_x = 6223
    center_y = 6223
    search_range_x = 6223 # actually the y because the map is rotated
    search_range_y = 6223 # actually the x because the map is rotated
    steps = 50
    start_time = time.time()
    scale = 0.003

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
                vx = 1 * iceflow_data[2][y][x]
                vy = 1 * iceflow_data[3][y][x]

                flow = [vx, vy]
                flow_heading = xyindex_vector_to_heading(x, y, flow[0], flow[1])[0]
                # print(f"flow at nearest: {flow_heading}")

                mag = np.sqrt(vx ** 2 + vy ** 2) * scale
                lat = iceflow_data[4][y][x]
                lon = iceflow_data[5][y][x]
                # print(f"lat: {lat}, lon: {lon}")
                # print(f"flow at nearest: {flow}")
                m.scatter(lon, lat, latlon=True, color='white', s=0.275)
                # plot a line of length mag in the direction of the flow vector to show the flow vector
                endpt = [lon + mag * np.cos(np.radians(flow_heading)), lat + mag * np.sin(np.radians(flow_heading))]
                m.plot([lon, endpt[0]], [lat, endpt[1]], latlon=True, color='blue', linewidth=0.25)


    print("")


    plt.title("Lat-Lon Map")

    dir = "C:\\Users\\rj\Documents\\cresis_project\\screens\\"
    file_name = "Continental_Flow_Map"
    savename = f"{dir}{file_name}.png"
    print(f"saving to {savename}...")
    plt.savefig(savename, dpi=250)

    print("done")

plot_map(iceflow_data, zoom=False)