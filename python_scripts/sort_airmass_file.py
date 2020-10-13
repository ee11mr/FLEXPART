import pandas as pd
import glob
dfs=[]
for infile in sorted(glob.glob('/users/mjr583/scratch/flexpart/cvao/05x05/airmass_files/20*_05x05_100m.csv')):
    df=pd.read_csv(infile, index_col=0)
    dfs.append(df)
df=pd.concat(dfs) ; x=[]
for i in df.index:
    try:
        x.append(pd.to_datetime(i, format='%d/%m/%Y %H:%M').strftime('%Y-%m-%d %H:%M'))
    except:
        x.append(pd.to_datetime(i, format='%Y-%m-%d %H:%M').strftime('%Y-%m-%d %H:%M'))
import numpy as np
x=np.array(x)
df.index=x
df.to_csv('/users/mjr583/scratch/flexpart/cvao/05x05/airmass_files/new_CVAO_sector_%_boxes_1.csv',sep=",",header='column_names') 
