import pyart
import numpy as np
from matplotlib import pyplot as plt
import matplotlib

# make empty grid
grid = pyart.testing.make_empty_grid((1, 1041, 1041), ((0, 18000.0),(-900000, 1500000), (-2300000, 2300000)))
grid.axes['lat']['data'][0]=35
grid.axes['lon']['data'][0]=-98.5

# put data into a single slice
data = np.ma.masked_all((1, 1041, 1041))
data[:,385:395,:]=60
grid.fields["reflectivity"]={'data':data}

######################
# copy from scott

display = pyart.graph.GridMapDisplay(grid)

font = {'size': 16}
matplotlib.rc('font', **font)
fig = plt.figure(figsize=[15, 8])
# panel sizes
map_panel_axes = [0.05, 0.05, .4, .80]
x_cut_panel_axes = [0.55, 0.10, .4, .30]
y_cut_panel_axes = [0.55, 0.50, .4, .30]
colorbar_panel_axes = [0.05, 0.90, .4, .03]
# parameters
level = 0
vmin = -8
vmax = 64
lat = 35
lon = -98.5
# panel 1, basemap, radar reflectivity and NARR overlay
ax1 = fig.add_axes(map_panel_axes)
display.plot_basemap(lon_lines = np.arange(-124, -73, 4),
lat_lines = np.arange(20,50,2))
display.plot_grid('reflectivity', level=level, vmin=vmin, vmax=vmax)
display.plot_crosshairs(lon=lon, lat=lat)


cbax = fig.add_axes(colorbar_panel_axes)
display.plot_colorbar(cax=cbax)

######################

# save
plt.savefig('y_slice.png', dpi = 400)