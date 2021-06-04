#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#SBATCH --job-name=plot_monthly_trajectories
#SBATCH --ntasks=1
#SBATCH --mem=8gb
#SBATCH --time=00:30:00
#SBATCH --output=LOGS/month_plotting_%A.log

"""
Created on Sun Mar 15 15:46:37 2020

@author: mjr583
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import sys
import matplotlib.colors as colors
matplotlib.use('agg')
from netCDF4 import Dataset
import datetime as dt

import cartopy.crs as ccrs
from cartopy.util import add_cyclic_point as cycpt

#year=sys.argv[1]
site='south_pole'
year='2018'

path='/users/mjr583/scratch/flexpart/'+site+'/'
if site=='cvao':
    path+='05x05/'
    llat=0. ; ulat=77.
    llon=-100. ; ulon=40.
elif site=='hateruma':
    llat=0. ; ulat=77.
    llon=60. ; ulon=150.
elif site=='mace_head':
    llat=20. ; ulat=85.
    llon=-100. ; ulon=40.
elif site=='tudor_hill':
    llat=-20. ; ulat=70.
    llon=-120. ; ulon=20.


months=['01','02','03','04','05','06','07','08','09','10','11','12']
names=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

import glob
month_lats=[] ; month_lons=[] ; month_alts=[]
for m,month in enumerate(months):
    all_lons=[] ; all_lats=[] ; all_alts=[]
    for filename in sorted(glob.glob(path+year+'/netcdfs/'+year+month+'*00.nc'), reverse=True):
        #print(filename)
        fh = Dataset(filename, 'r')
        lats=fh.variables['Latitude'][:]
        lons=fh.variables['Longitude'][:]
        alts=fh.variables['Altitude'][:]
   
        all_lons.append(lons)
        all_lats.append(lats)
        all_alts.append(alts)

    lats=np.array(all_lats)
    lons=np.array(all_lons)
    alts=np.array(all_alts)
  
    length = lats.shape[0]*lats.shape[1]*lats.shape[2]
    lat = (np.reshape(lats, length)+90.).astype(int)
    lon = np.reshape(lons, length).astype(int)
    alt = np.reshape(alts, length).astype(int)
    
    month_lats.append(lats)
    month_lons.append(lons)
    month_alts.append(alts)

lats=np.array(month_lats)
lons=np.array(month_lons)
alts=np.array(month_alts)
print(lats[0].shape)

days5=False
if days5:
    for n in range(len(lats)):
        lats[n]=lats[n][:,:40,:]
        lons[n]=lons[n][:,:40,:]
        alts[n]=alts[n][:,:40,:]

print(lats[0].shape)

lat=[] ; lon=[] ; alt=[]
for m in range(len(months)):
    length = lats[m].shape[0]*lats[m].shape[1]*lats[m].shape[2]
    lat.append(np.reshape(lats[m], length)+90.)#.astype(int)
    lon.append(np.reshape(lons[m], length))#.astype(int))
    alt.append(np.reshape(alts[m], length))#.astype(int))

print('Make the grid for each month')
limit=100
mongrid=[]
for m in range(12):
    print(m)
    grid=np.zeros((180,360))
    for i in range(len(lon[m])):
        if alt[m][i]<=limit:
            if lon[m][i]<0.:
                lon[m][i]=lon[m][i]+360.
            grid[int(lat[m][i]),int(lon[m][i])]+=1
        else:
            pass
    grid = np.concatenate((grid[:,180:],grid[:,:180]),axis=1)
    fltr=np.where(grid<1)
    grid[fltr]=np.nan
    
    mongrid.append(grid)

print('Start plotting')
f,((ax1,ax2,ax3),(ax4,ax5,ax6),(ax7,ax8,ax9),(ax10,ax11,ax12))=plt.subplots(4,3,figsize=(12,12))
ax=[ax1,ax2,ax3,ax4,ax5,ax6,ax7,ax8,ax9,ax10,ax11,ax12]

f=plt.figure(figsize=(12,12))
for mon in range(len(ax)):
    # Create a map
    p=mongrid[mon]
    plat=np.arange(-90,90)
    plon=np.arange(-180,180)

    p_cyclic, lon_cyclic = cycpt(p, coord=plon)
    lon_cyclic = np.ma.getdata(lon_cyclic)
    p_cyclic = np.ma.getdata(p_cyclic)
    plon2d, plat2d = np.meshgrid(lon_cyclic, plat)

    ax=f.add_subplot(4,3,mon+1, projection=ccrs.SouthPolarStereo(central_longitude=0))
    ax.set_extent([-180, 180, -30, -30], crs=ccrs.PlateCarree())
    ax.pcolormesh(plon2d,plat2d,p_cyclic,transform=ccrs.PlateCarree(),norm=colors.LogNorm(vmin=np.nanmin(mongrid[mon]), vmax=np.nanmax(mongrid[mon])),cmap='jet')
    ax.coastlines()

    ax.title.set_text(names[mon])
plt.tight_layout()
#plt.suptitle(year)#+' - surface to '+str(limit)+'m')
if not days5:
    plt.savefig(path+'/plots/%s_%s.png' % (year, site))
else:
    plt.savefig(path+'/plots/%s_%s_%s.png' % (year, site, '5day'))

plt.close()
print('Plot saved')
