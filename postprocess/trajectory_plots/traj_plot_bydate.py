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
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
sys.path.append('/users/mjr583/python_lib')
import RowPy as rp
import CVAO_tools as CV
from CVAO_dict import CVAO_dict as d
from flex_dict import site_dict
import seaborn as sns 
from netCDF4 import Dataset
import matplotlib.colors as colors


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
    fig,ax=plt.subplots(figsize=(12,8))
    m=rp.get_basemap(lllon=site_dict[site]['lllon'],lllat=site_dict[site]['lllat'],urlon=site_dict[site]['urlon'],
                urlat=site_dict[site]['urlat'],ax=ax, lsmask=True )

    lats=range(-90,90)
    lons=range(-180,180)
    X,Y=np.meshgrid(lons,lats)
    m.pcolormesh(X,Y,grid, norm=colors.LogNorm(vmin=np.nanmin(grid), vmax=np.nanmax(grid)), cmap='jet', zorder=10)

    ax.set_title(dt, loc='left', fontsize=16)
    plt.tight_layout()
    plt.savefig('./plots/'+site+'_'+dt+'.png')
    plt.close()
    
    if altplot==True: ## Optional plot under certain altitude
        grid_100=rp.get_grid(lon,lat,alt=alt,limit=altlimit)
        
        fig,ax=plt.subplots(figsize=(12,8))
        m=rp.get_basemap(lllon=site_dict[site]['lllon'],lllat=site_dict[site]['lllat'],urlon=site_dict[site]['urlon'],
                urlat=site_dict[site]['urlat'],ax=ax, lsmask=True )
        lats=range(-90,90)
        lons=range(-180,180)
        X,Y=np.meshgrid(lons,lats)
        m.pcolormesh(X,Y,grid_100, norm=colors.LogNorm(vmin=np.nanmin(grid_100), \
                vmax=np.nanmax(grid_100)), cmap='jet', zorder=10)
        
        ax.set_title(dt, loc='left', fontsize=16)
        plt.tight_layout()
        plt.savefig('./plots/'+site+'_'+dt+'_100m.png')
        plt.close()
