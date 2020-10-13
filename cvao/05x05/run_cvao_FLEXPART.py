#!/usr/bin/env python3
#SBATCH --time=02:00:00
#SBATCH --mem=8gb
#SBATCH --job-name=CVAO_continuous
#SBATCH --partition=nodes
#SBATCH --output=LOGS/shell_log_%A.log

##############################################################################################
##   This script is for continuous back-trajectory modelling of airmass reaching the Cape   ##
##   Verde Atmospheric Observatory (16.52N, -24.51W). Script has 3 major steps outlined     ##
##   below.                                                                                 ##
##                                                                                          ##
##   Required files in directory:                                                           ##
##                  - gfs_from_url.py (python script, downloads GFS from URL)               ##
##                  - job_array (Bash script, completes array of FLEXPART model runs        ##
##                  - !! csv script !!                                                      ##
##   Prelim: Get current month and year, set up required variables to run the script for    ##
##           the previous month.                                                            ##
##   Step 1: Check if GFS met files already exist on disk, if not download from URL. Check  ##
##           files have been download before continuing.                                    ##
##   Step 2: Adjust job_array file and sumbit FLEXPART runs for the month. Ensure runs have ##
##           produced ncdf files successfully before continuing.                            ##
##   Step 3: Run postprocess from ncdf output, creating csv files with airmass percentages  ##
##           reaching Cape Verde. Check csv files exist before finishing.                   ##
##                                                                                          ##
##############################################################################################

import os
import time
import datetime
import calendar


##### PRELIM #####
today=datetime.datetime.today()
year=today.year
month=today.month-1
#month=3  ## Temporary to force earlier month
month=(datetime.datetime(today.year, month, 1)).strftime('%m')
last = calendar.monthrange(year,int(month))[1]

start_date=( str(year)+str(month)+'01' )
end_date=  ( str(year)+str(month)+str(last) )

a=(datetime.datetime(year, int(month), 1).timetuple().tm_yday-1)*4+1
n=datetime.datetime(year, int(month), last).timetuple().tm_yday*4


##### STEP ONE #####
##### DOWNLOAD GFS MET FILES FOR PREVIOUS MONTH

last_gfs_file='/users/mjr583/scratch/flexpart/preprocess/flex_extract/05x05/GF'+str(year)[2:]+str(month)+str(last)+'18'
print(last_gfs_file)
gfs_download_cmd=("sbatch python_scripts/gfs_from_url.py "+start_date+" "+end_date)
if not os.path.exists(last_gfs_file):
    print('Downloading GFS files')
    os.system(gfs_download_cmd)
    while not os.path.exists(last_gfs_file): # check download has finished before continuing
        time.sleep(60)
elif os.stat(last_gfs_file).st_size==0:
    print('Downloading GFS files')
    os.system(gfs_download_cmd)
    while os.stat(last_gfs_file).st_size==0:
        time.sleep(60)
else:
    print('Input files already on Viking - make AVAILABLE file and run FLEXPART')

mkavail_cmd=("python python_scripts/mkAVAIL.py -s "+str(year)+"01 -e "+str(year+1)+"01 -m GFS -p  /users/mjr583/scratch/flexpart/preprocess/flex_extract/05x05/ -a /users/mjr583/scratch/flexpart/cvao/05x05/"+str(year)+"/")
os.system(mkavail_cmd)


##### STEP TWO #####
##### RUN FLEXPART BACK-TRAJECTORIES FOR PREVIOUS MONTH

sed_cmd=('sed -i "s/#SBATCH --array.*/#SBATCH --array='+str(a)+'-'+str(n)+'/" ./job_array')
sed_cmd_2=('sed -i "s/YEAR=.*/YEAR='+str(year)+'/" ./job_array')
os.system(sed_cmd)
os.system(sed_cmd_2)

flexpart_cmd=("sbatch job_array")
os.system(flexpart_cmd)

# Check run is finished before continuing
last_ncdf_file='/users/mjr583/scratch/flexpart/cvao/05x05//'+str(year)+'/netcdfs/'+str(year)+str(month)+str(last)+'1800.nc'
print(last_ncdf_file)
while not os.path.exists(last_ncdf_file):
    time.sleep(60)
if os.path.exists(last_ncdf_file):
    time.sleep(300)


##### STEP THREE #####
##### PROCESS RUN OUTPUT INTO PERCENTAGES IN CSV FILES

csv_cmd=("sbatch --partition=interactive python_scripts/create_csv_boxes.py -r 05x05 -y "+str(year)+" -m "+str(month))
os.system(csv_cmd)


##### Additional step #####
##### Make sure datetime index is in correct format, order and without duplicates.

os.system("sbatch python_scripts/sort_airmass_file.py")
