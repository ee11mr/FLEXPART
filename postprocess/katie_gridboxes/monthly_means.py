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
from mpl_toolkits.basemap import Basemap
import numpy as np
import xarray
import matplotlib.pyplot as plt
import matplotlib
import sys
import datetime
import matplotlib.colors as colors
matplotlib.use('agg')
from netCDF4 import Dataset
import datetime as dt
sys.path.append('/users/mjr583/scratch/python_lib/')
import RowPy as rp

site='cvao'
year='all'

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
all_lons=[] ; all_lats=[] ; all_alts=[]

file_list=rp.gen_file_list(start=2007,end=2007)
dt=rp.get_datetimes(file_list)

from collections import defaultdict
mns=defaultdict(list)
for i,ii in enumerate(dt):
    ii=datetime.datetime.strptime(ii, '%d/%m/%Y %H:%M').month-1
    f=file_list[i]
    mns[names[ii]].append(f)

print(len(mns['Jan']))
new_mns=defaultdict(list)
for i in range(len(mns)):
    print(i)
    lons,lats,alts=rp.get_coords(mns[names[i]])
    new_mns[names[i]]['lons']=lons#,lats,alts)
print(lons.shape)
sys.exit()

print(lons.shape)
lat=[] ; lon=[] ; alt=[]
for m in range(len(months)):
    print(m)
    length = lats[m].shape[0]*lats[m].shape[1]*lats[m].shape[2]
    lat.append(np.reshape(lats[m], length)+90.)#.astype(int)
    lon.append(np.reshape(lons[m], length))#.astype(int))
    alt.append(np.reshape(alts[m], length))#.astype(int))

print(lon.shape)
sys.exit()
limit=100
mongrid=[]
for m in range(12):
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

sys.exit()

f,((ax1,ax2,ax3),(ax4,ax5,ax6),(ax7,ax8,ax9),(ax10,ax11,ax12))=plt.subplots(4,3,figsize=(12,12))
ax=[ax1,ax2,ax3,ax4,ax5,ax6,ax7,ax8,ax9,ax10,ax11,ax12]
for mon in range(len(ax)):
    # Create a map 
    m = Basemap(projection='cyl', llcrnrlat=llat, urcrnrlat=ulat,llcrnrlon=llon, urcrnrlon=ulon, resolution='c', area_thresh=1000.,ax=ax[mon])
    
    m.drawcoastlines(linewidth=0.5)
    m.drawcountries(linewidth=0.5)
    m.drawparallels(np.arange(-90.,90.,10.))
    m.drawmeridians(np.arange(-180.,180.,10.))
    m.drawlsmask(land_color='lightgrey',ocean_color='grey')
    lats=range(-90,90)
    lons=range(-180,180)
    X,Y=np.meshgrid(lons,lats)
    m.pcolormesh(X,Y,mongrid[mon],norm=colors.LogNorm(vmin=np.nanmin(mongrid[mon]), vmax=np.nanmax(mongrid[mon])),cmap='jet')
    ax[mon].title.set_text(names[mon])
plt.tight_layout()
plt.suptitle(year)#+' - surface to '+str(limit)+'m')
plt.savefig(path+'/plots/'+year+'_'+site+'.png')
plt.close()
print('Plot saved')
