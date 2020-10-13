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
from netCDF4 import Dataset, stringtochar
import datetime as dt
from scipy.io import FortranFile
path='/users/mjr583/scratch/flexpart/cvao/05x05/'
months=['01','02','03','04','05','06','07','08','09','10','11','12']
names=['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']

#YEAR=str(sys.argv[1])
#NUMBER= ( int(sys.argv[2]) - 1 )

YEAR='2020'
NUMBER=608

datesin=path+YEAR+'/array_dates'
array_dates=[np.loadtxt(datesin)[NUMBER,1]]

#print(array_dates.shape)
for date in array_dates:
    date=str(date)[:-2]
    month=date[4:6]
    day=date[6:8]
    hour=date[8:12]
    print(date) 
    stop
    all_lons=[] ; all_lats=[] ; all_alts=[]
    hold_names=[]
    import glob
    for filename in sorted(glob.glob(path+YEAR+'/flex_'+YEAR+month+day+hour+'/output/partposit_*'), reverse=True):
        hold_names.append(filename)
        f = FortranFile(filename, 'r')
        print(f.read_record('i4'))
        Ender=False
        counter=0
        lats=np.zeros(10000)
        lons=np.zeros(10000)
        alts=np.zeros(10000)
        
        while not(Ender):
          A=f.read_record('i4','f4','f4','f4','i4','f4','f4','f4','f4','f4','f4','f4','f4')
          if (A[0][0]==-99999):
            Ender=True
          else:
            lons[counter]=A[1][0]
            lats[counter]=A[2][0]
            alts[counter]=A[3][0]
            
            counter=counter+1
        lons=lons[:counter-1]
        lats=lats[:counter-1]
        alts=alts[:counter-1]
    
        all_lons.append(lons) ; all_lats.append(lats) ; all_alts.append(alts)  
    
    all_lon= np.array(all_lons)
    all_lat= np.array(all_lats)
    all_alt= np.array(all_alts)
    
    length = all_lat.shape[0]*all_lat.shape[1]
    lat = (np.reshape(all_lat, length)+90.).astype(int)
    lon = np.reshape(all_lon, length).astype(int)
    
    DT = dt.datetime.strptime(date, '%Y%m%d%H%M%S')
    DT = DT + dt.timedelta(days=10)

    print('Now save as netcdf file')
    nc_path=path+YEAR+'/netcdfs/'+date+'.nc'
    ncdf_file=Dataset(nc_path, 'w', clobber='true')
    ncdf_file.title = ('CV trajectory data - '+date )
    ncdf_file.description = 'Trajectories calculated using FLEXPART v10.4, driven by GFS meteorological reanalyses. Number of particles = 100. Point of release = Cape Verde Atmospheric Observatory (16.51 N, -24.52 W)'
    ncdf_file.references = 'https://www.geosci-model-dev.net/12/4955/2019/gmd-12-4955-2019-discussion.html'

    # Dimensions
    ncdf_file.createDimension('seconds',80)
    ncdf_file.createDimension('datetime',80)
    ncdf_file.createDimension('particle',99)
    
    # Variables
    time = ncdf_file.createVariable('seconds_since_release',np.int32, ('seconds'))
    times = np.arange(10800,864000+10800,10800)
    time.units = 'Seconds since particles released'
    time[:] = times
    
    datetimes=[]
    for sec in times:
        DATE = str(DT - dt.timedelta(seconds=float(sec)))
        datetimes.append(DATE)
    datetimes=np.array(datetimes)

    timestamp = ncdf_file.createVariable('timestamp', str, ('datetime'))
    timestamp.units = 'Timestamp of model output'
    timestamp[:] = datetimes

    particles = ncdf_file.createVariable('particle',np.int32, ('particle'))
    particles.units = 'Particle number'
    particles[:] = range(1,100)

    lats = ncdf_file.createVariable('Latitude',np.float, ('seconds','particle'))
    lats.units = 'Degrees'
    lats[:] = all_lat

    lons = ncdf_file.createVariable('Longitude',np.float, ('seconds','particle')) 
    lons.units = 'Degrees'
    lons[:] = all_lon

    alts = ncdf_file.createVariable('Altitude',np.float, ('seconds','particle')) 
    alts.units = 'Metres'
    alts[:] = all_alt

    ncdf_file.close()



