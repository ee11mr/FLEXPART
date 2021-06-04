#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#SBATCH --job-name=upwelling_times
#SBATCH --ntasks=1
#SBATCH --partition=interactive
#SBATCH --mem=8gb
#SBATCH --time=01:30:00
#SBATCH --output=Logs/upwelling_times.log

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
plt.rcParams['figure.figsize'] = (10, 6)
plt.style.use('seaborn-darkgrid')
site='cvao'

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
years=['2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020']
every_time_to_reach=[]
for year in years:
    print(year)
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
    annual_time_to_reach = []
    for mon in range(len(months)):
        time_to_reach = []
        for n, traj in enumerate(lons[mon]):
            for nn, steps in enumerate(lons[mon][n]):
                for nnn, particle in enumerate(lons[mon][n][nn]):
                    if -17.0 < lons[mon][n][nn][nnn] < -16.0 and 16.5 < lats[mon][n][nn][nnn] < 21.4 and alts[mon][n][nn][nnn] < 1000:
                        time_to_reach.append(dt[nn])
                        break
                else:
                    continue
                break

    annual_time_to_reach.append(time_to_reach)
    print(np.array(time_to_reach).shape)
    sys.exit()
    plt.bar(names, time_to_reach)
    plt.ylabel('Days since Mauritanian Upwelling')
    plt.savefig('plots/%s_days_since_bar.png' %year)
    plt.close()

    every_time_to_reach.append(np.round(np.nanmean(np.array(time_to_reach)),2))

annual_means = np.array(every_time_to_reach)
print(annual_means)
plt.bar(years, annual_means)
plt.ylabel('Days since Mauritanian Upwelling')
plt.savefig('plots/days_since_bar.png')
plt.close()
print(np.round(annual_means.mean(),2), 'days to Cape Verde from Upwelling region')
