# -*- coding: utf-8 -*-
"""
NAME
    download_gfs
KEYWORD ARGUMENTS
    Start and End date (Format: YYYYMMDD)
    Earliest date 1st January 2007 (20070101),
    there are no weather data before that date to download (status May 2019)
KEYWORD ARGUMENTS optional
    path in which the file should be placed
DESCRIPTION
    download_gfs downloads weather data (analysis 0.5 degree grid) from nomads.ncdc.noaa.gov
    linux os is required
NOTE
    The files will not be renamed and not be checked if the download succeded!

    Comments / improvements are welcome.

CONTACT
    florian.geyer@zamg.ac.at
    Version 1, May 2019

DISCLAIMER
    This software has been developed for flexpart workshop 2019 @ ZAMG

"""

def check_date(date):
    """
        checks if date is really a date
    """
    import datetime
    correctDate = None
    date = str(date)
    
    if (len(date)!=8):
        return False
    year = int(date[0:4])
    month = int(date[4:6])
    day = int(date[6:8])
    try:
        datetime.datetime(year,month,day)
        correctDate = True
    except ValueError:
        correctDate = False
    return correctDate

def convert_str2date(date):
    """
        converts date (as integer) to python datetime
    """
    import datetime
    date = str(date)
    year = int(date[0:4])
    month = int(date[4:6])
    day = int(date[6:8])
    return datetime.datetime(year,month,day)

def create_filenames(date):
    """
        creates filenames for givn date,
        from the runs at 0, 6, 12 and 18 UTC
        only t=0 and t=3 will be downloaded
    """
    if int(YEAR) < 2017:
        suffix=".grb"
    else:
        suffix=".grb2"
    print("Year="+YEAR,": suffix="+suffix)

    if int(YEAR)==2017:
        filelist = list()
        for t in ["0000", "0600", "1200", "1800"]:
            for t2 in ["003"]:
                #for su in [".grb",".grb2"]:
                for su in [".grb2"]:
                    filelist.append("gfsanl_3_"+d.strftime('%Y%m%d')+"_"+t+"_"+t2+su)
        return filelist
    else:
        filelist = list()
        for t in ["0000", "0600", "1200", "1800"]:
            for t2 in ["000"]:
                filelist.append("gfsanl_3_"+d.strftime('%Y%m%d')+"_"+t+"_"+t2+suffix)
        return filelist

def download_file(path, filename, destination):
    """
        downloads files from path and saves to destination
    """
    import os
    command = "wget -q -O "+destination+"/"+filename+" ftp://nomads.ncdc.noaa.gov/"+path+"/"+filename
    os.system(command)

def redownload_file(path, old_filename, destination, new_filename):
    """
        downloads files from path and saves to destination
    """
    import os
    command = "wget -q -O "+destination+"/"+new_filename+" ftp://nomads.ncdc.noaa.gov/"+path+"/"+old_filename
    os.system(command)

def check_path(path):
    """
        checks if path exists
    """
    import os
    if not os.path.exists(path):
        print("Path does not exist")
        print("")
        sys.exit()

def start_ftp_date():
    """
        from this date 0.5 degree grid data exists on ftp
    """
    return 20070101
        
import sys
from ftplib import FTP
import datetime

print("")

# checking input arguments (1 and 2 are start and end date
try:
    start = sys.argv[1]
    end   = sys.argv[2]
except:
    print("Please give me a start and end date (format: YYYYMMDD)")
    print("")
    sys.exit()

# checking destination (optinal), if no destination givn,
# files will be saved in current directory
try:
    destination = sys.argv[3]
    if (destination[-1]!="/"):
      destination = destination+"/1x1/"
except:
    destination = "../"

# print input arguments
print("Start: ", start)
print("End:   ", end)
print("Path: ", destination)
print("")
YEAR=start[:4]

check_path(destination)

start_ftp_date = start_ftp_date()

# check if dates are in correct format
if (check_date(start)==False):
    print("Wrong start date, please try again (Format should be YYYYMMDD)!")
    print("")
    sys.exit()
if (check_date(end)==False):
    print("Wrong end date, please try again (Format should be YYYYMMDD)!")
    print("")
    sys.exit()
start_date = convert_str2date(start)
end_date   = convert_str2date(end)
start_ftp_date   = convert_str2date(start_ftp_date)

# check if dates are in correct order
if (start_date>end_date):
    print("Your start date was after the end date, I will turn it around!")
    print("")
    start_date, end_date = end_date, start_date
    
if (start_date<start_ftp_date):
    print("The FTP-Server only provides data after the 1st January 2007, please choose another date!")
    print("")
    sys.exit()

print("start downloading from ", start_date, "to", end_date)

# create date list + missing list
date_list = [start_date + datetime.timedelta(days=x) for x in range(0, (end_date-start_date).days+1)]
missing=[]

# connect to ftp
ftp = FTP('nomads.ncdc.noaa.gov')
ftp.login()
# iter through date_list and download
for d in date_list:
    path = "GFS/analysis_only/"+d.strftime('%Y%m')+"/"+d.strftime('%Y%m%d')+"/"
    try:
        ftp.cwd(path)
        print(path, "found")
        file_list_ftp = ftp.nlst()
        file_list = create_filenames(d)
        for f in file_list:
            if f in file_list_ftp:
                print(f)
                print("  ", f, "found, download as "+destination+f)
                download_file(path, f, destination)
                import os
                count=0
                while os.stat(destination+f).st_size==0 and count < 50:
                    print('FTP Failed, retrying')
                    download_file(path,f,destination)
                    count+=1
                cp_command= "cp "+destination+f+" /users/mjr583/scratch/flexpart/preprocess/flex_extract/1x1/GF"+f[11:13]+f[13:15]+f[15:17]+f[18:20]
                os.system(cp_command)
                last_file=destination+f
            else:
                missing.append(f)
                print("  ", f, "not found: copying previous wind file")
                cp_command= "cp "+last_file+" /users/mjr583/scratch/flexpart/preprocess/flex_extract/1x1/GF"+f[11:13]+f[13:15]+f[15:17]+f[18:20]
                os.system(cp_command)
        ftp.cwd("../../../../")
    except:
        file_list=create_filenames(d)
        for f in file_list:
            missing.append(f)
            cp_command= "cp "+last_file+" /users/mjr583/scratch/flexpart/preprocess/flex_extract/1x1/GF"+f[11:13]+f[13:15]+f[15:17]+f[18:20]
            os.system(cp_command)
open("LOGS/"+end+"_1X1_SUCCESS",'a').close()
#ftp.quit()
ftp.close()

missing_file = open('/users/mjr583/scratch/flexpart/preprocess/gfs_data/code/missing_1x1.txt', 'w+')
if not missing:
    print('No missing data')
else:
    with open('/users/mjr583/scratch/flexpart/preprocess/gfs_data/code/missing_1x1.txt', 'w+') as missing_file:
        for line in missing:
            missing_file.write("".join(line) + "\n")
missing_file.close()
print("")
