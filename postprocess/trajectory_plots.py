#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#SBATCH --job-name=plot_monthly_trajectories
#SBATCH --ntasks=1
#SBATCH --mem=8gb
#SBATCH --time=00:30:00
#SBATCH --output=LOGS/month_plotting_%A.log

from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('agg')
from netCDF4 import Dataset
import matplotlib.colors as colors

## Script to plot for asingle trajectory ##

# Read the file and variables
nc_name='201801010000'
#path_to_nc_directory='directory_name/'
path_to_nc_directory='/users/mjr583/scratch/flexpart/hateruma/2018/netcdfs/'
filename='%s/%s.nc' %(path_to_nc_directory, nc_name)
fh = Dataset(filename, 'r')

lats=fh.variables['Latitude'][:]
lons=fh.variables['Longitude'][:]
alts=fh.variables['Altitude'][:]

# Convert from shape (timesteps, particles) to 1d array
length = lats.shape[0]*lats.shape[1]
lat=(np.reshape(lats, length)+90.)
lon=(np.reshape(lons, length))
alt=(np.reshape(alts, length))

# Process onto a 1x1 degree grid (i.e. add 1 for every particle in grid square)
grid=np.zeros((180,360))
for i in range(len(lon)):
    if lon[i]<0.:
        lon[i]=lon[i]+360.
    grid[int(lat[i]),int(lon[i])]+=1

# Rearrange longitudes for plotting and set zero values to NaN
grid = np.concatenate((grid[:,180:],grid[:,:180]),axis=1)
fltr=np.where(grid<1)
grid[fltr]=np.nan

# Create map for plot
m = Basemap(projection='cyl', llcrnrlat=0., urcrnrlat=77.,llcrnrlon=0., urcrnrlon=170., resolution='c', area_thresh=1000.)
m.drawcoastlines(linewidth=0.5)
m.drawcountries(linewidth=0.5)
m.drawparallels(np.arange(-90.,90.,10.))
m.drawmeridians(np.arange(-180.,180.,10.))
#m.drawlsmask(land_color='lightgrey',ocean_color='grey') ## Uncomment if you want to shade ocean/land

# Plot the grid on 1x1 lon/lat axis
lats=range(-90,90)
lons=range(-180,180)
X,Y=np.meshgrid(lons,lats)
m.pcolormesh(X,Y,grid,norm=colors.LogNorm(vmin=np.nanmin(grid), vmax=np.nanmax(grid)),cmap='jet')
plt.title(nc_name)
plt.savefig('./%s.png' %nc_name)
plt.close()
print('Done')
