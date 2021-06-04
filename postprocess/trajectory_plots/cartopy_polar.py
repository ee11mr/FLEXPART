#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#SBATCH --partition=interactive
#SBATCH --time=00:02:00
#SBATCH --mem=1gb
#SBATCH --output=LOGS/plot_%a.log
import matplotlib
matplotlib.use('agg')
import sys
import numpy as np
import math
import datetime
import pandas as pd
#from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
sys.path.append('/users/mjr583/python_lib')
import RowPy as rp
import CVAO_tools as CV
from CVAO_dict import CVAO_dict as d
from flex_dict import site_dict
#import seaborn as sns 
from netCDF4 import Dataset
import matplotlib.colors as colors

import cartopy.crs as ccrs
from cartopy.util import add_cyclic_point as cycpt

global options,args
import optparse
parser = optparse.OptionParser(
        formatter = optparse.TitledHelpFormatter(),
            usage = globals()['__doc__'])

parser.add_option('-s','--startdate',
    dest='startdate',
    help='Date to start plotting trajectories (YYYYMMDD)')
parser.add_option('-e','--enddate',
    dest='enddate',
    help='Last date to plot trajectories (YYYYMMDD)')
parser.add_option('-S','--site',
    dest='site',
    default='cvao',
    help='Site form which to plot trajectory (def=cvao)')
parser.add_option('-a','--altitude_plot',
    dest='altplot',
    default=False,
    help='Create plot of particles below a certain altitude')
parser.add_option('-l','--altitude_limit',
    dest='altlimit',
    default=100,
    help='Altitude below which to plot particles')
(options,args)=parser.parse_args()

font = {'weight' : 'bold',
        'size'   : 16}

if len(sys.argv) > 1:
    if not options.startdate:
        parser.error('Must give a start date to plot trajectories from')
    if not options.enddate:
        parser.error('Must give an end date to plot trajectories to')
    if len(options.startdate) != 8 or len(options.enddate) != 8:
        parser.error('Start and end dates must be in YYYYMMDD format (e.g. 20170622)')

else:
    rp.clear_screen()
    options.startdate=input('Enter date to start plotting (YYYYMMDD):')
    rp.clear_screen()
    options.enddate=input('Enter date to stop plotting (YYYYMMDD) (Hit enter if same as start date):')
    if options.enddate == '':
        options.enddate=options.startdate
    rp.clear_screen()
    options.site=input('Enter site at which to plot trajectories (hit enter for Cape Verde) : ') 
    if options.site == '':
        options.site='cvao'
    rp.clear_screen()
    options.altplot=input('Create additional plot of particles below a certain altitude? (Default is no):')
    trues=[True,'y','Y','T','t','yes','Yes','YES','TRUE','true']
    falses=[False,'n','N','F','f','false','FALSE','no','NO','No']
    if options.altplot in trues:
        options.altplot=True
    elif options.altplot in falses:
        options.altplot=False
    elif options.altplot=='':
        options.altplot=False
    else:
        parser.error('I dont understand - please try again')
    if options.altplot:
        rp.clear_screen()
        options.altlimit=input('Altitude below which to plot particles (default=100m)')
    
startdate=options.startdate
enddate=options.enddate
site=options.site
altplot=options.altplot

neu_lon, neu_lat = -8., -70.

file_list=rp.gen_trajectory_dates(startdate,enddate,site=site)
for f in file_list:
    dt=f[-15:-3]
    fh=Dataset(f)

    lats=fh.variables['Latitude'][:]
    lons=fh.variables['Longitude'][:]
    alts=fh.variables['Altitude'][:]
    
    length=lats.shape[0]*lats.shape[1]
    lat=np.reshape(lats,length)+90.
    lon=np.reshape(lons,length)
    alt=np.reshape(alts,length)
   
    grid=rp.get_grid(lon,lat)
  
    plat=np.arange(-90,90)
    plon=np.arange(-180,180)
    p=grid
    
    p_cyclic, lon_cyclic = cycpt(p, coord=plon)
    lon_cyclic = np.ma.getdata(lon_cyclic)
    p_cyclic = np.ma.getdata(p_cyclic)
    plon2d, plat2d = np.meshgrid(lon_cyclic, plat)

    ax=plt.axes(projection=ccrs.SouthPolarStereo(central_longitude=0))
    ax.set_extent([-180, 180, -30, -30], crs=ccrs.PlateCarree())
    #plt.contourf(plon2d,plat2d,p_cyclic,transform=ccrs.PlateCarree())
    plt.pcolormesh(plon2d,plat2d,p_cyclic,transform=ccrs.PlateCarree())


    plt.text(neu_lon, neu_lat, 'x', transform=ccrs.PlateCarree())

    ax.coastlines() 
    plt.savefig('./plots/polar_%s_%s.png' % (site, dt))
    plt.close()
