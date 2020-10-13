#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 12:24:20 2020

@author: mjr583
"""
from datetime import datetime, timedelta
import os
import numpy as np 
import glob
from shutil import copyfile
import sys

forecast_date=sys.argv[1]
prefix='EA'
inpath='/users/mjr583/scratch/flexpart/FORECASTS/met_data/'+forecast_date+'/'
outpath='/users/mjr583/scratch/flexpart/preprocess/flex_extract/'+forecast_date+'/'
for infile in sorted(glob.glob(inpath+'gfs_4_*'+forecast_date+'*')):
    print(infile)
    year=int(infile[65:69])
    month=int(infile[69:71])
    day=int(infile[71:73])
    hour=int(infile[74:76])
    
    forecast_date=datetime(year,month,day,hour,00)
    
    hour_of_forecast=int(infile[79:82]) 
    
    date_out= forecast_date + timedelta(hours=hour_of_forecast)
    
    outfile=outpath+prefix+date_out.strftime("%y%m%d%H")
    print(infile+' successfully copied to: '+prefix+date_out.strftime("%y%m%d%H"))
    copyfile(infile, outfile)
print('All forecast files copied and renamed')
