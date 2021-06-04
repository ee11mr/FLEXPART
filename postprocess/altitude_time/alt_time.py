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

dt=np.arange(0,864000,10800)/86400
f=plt.figure(figsize=(12,8))
for mon in range(len(months)):
    print(mon)
    alt=alts[mon]
    alt=np.mean(alt,2)
    ax=f.add_subplot(4,3,mon+1)
    for i in range(len(alt)):
        ax.plot(dt,alt[i])
    if mon==0 or mon==3 or mon==6 or mon==9:
        ax.set_ylabel('Altitude (m)')
    if mon>=9:
        ax.set_xlabel('Days since release')
    ax.title.set_text(names[mon])
    ax.set_ylim(0,6000)
    ax.get_shared_y_axes().join(ax)
plt.subplots_adjust(hspace=.4, wspace=.3)
plt.savefig('./%s_%s_alt.png' % (site, year))

