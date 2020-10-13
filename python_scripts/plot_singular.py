#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#SBATCH --job-name=plot_monthly_trajectories
#SBATCH --ntasks=1
#SBATCH --mem=1gb
#SBATCH --time=03:00:00
#SBATCH --output=log_plotting_script

"""
Created on Sun Mar 15 15:46:37 2020

@author: mjr583
"""
from mpl_toolkits.basemap import Basemap
import numpy as np
import xarray
import matplotlib.pyplot as plt
import matplotlib
import sys
matplotlib.use('agg')
from netCDF4 import Dataset
import datetime as dt

path='/users/mjr583/scratch/flexpart/cvao/05x05/'
months=['01','02','03','04','05','06','07','08','09','10','11','12']
names=['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']

YEAR=str(sys.argv[1])
NUMBER= ( int(sys.argv[2]) - 1)

datesin=path+YEAR+'/array_dates'
array_dates=[np.loadtxt(datesin)[NUMBER,1]]

#print(array_dates.shape)
for date in array_dates:
    date=str(date)[:-2]
    month=date[4:6]
    day=date[6:8]
    hour=date[8:12]

    all_lons=[] ; all_lats=[] ; all_alts=[]
    hold_names=[]
    import glob
    for filename in sorted(glob.glob(path+YEAR+'/netcdfs/'+YEAR+month+day+hour+'*.nc'), reverse=True):
        print(filename)
        fh = Dataset(filename, 'r')

        lats=fh.variables['Latitude'][:]
        lons=fh.variables['Longitude'][:]

print(lats.shape)

length = lats.shape[0]*lats.shape[1]
lat = (np.reshape(lats, length)+90.).astype(int)
lon = np.reshape(lons, length).astype(int)
   
grid=np.zeros((180,360))
for i in range(len(lon)):
    if lon[i]<0.:
        lon[i]=lon[i]+360.
    grid[lat[i],lon[i]]+=1
grid = np.concatenate((grid[:,180:],grid[:,:180]),axis=1)
fltr=np.where(grid<1)
grid[fltr]=np.nan

fig = plt.figure(figsize=(12,12))
    # Create a map for Cape Verde
m = Basemap(projection='cyl', llcrnrlat=-10, urcrnrlat=70,llcrnrlon=-100, urcrnrlon=50, resolution='c', area_thresh=1000.)
m.drawcoastlines(linewidth=0.5)
m.drawcountries(linewidth=0.5)
m.drawparallels(np.arange(-90.,90.,10.))
m.drawmeridians(np.arange(-180.,180.,10.))
#m.drawmapboundary(fill_color='aqua')
m.drawlsmask(land_color='lightgrey',ocean_color='grey')
lats=range(-90,90)
lons=range(-180,180)
X,Y=np.meshgrid(lons,lats)
plt.pcolormesh(X,Y,grid,cmap='jet')
plt.savefig(path+YEAR+'/plots/'+date+'.png')
plt.close()
print('Saving',date+'.png')
