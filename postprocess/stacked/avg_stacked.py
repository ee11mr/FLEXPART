

import pandas as pd
import sys
sys.path.append('/users/mjr583/python_lib')
import RowPy as rp


path='/users/mjr583/scratch/flexpart/hateruma/airmass_files/new_HAT_sector_%_boxes.csv'
df=pd.read_csv(path,index_col=0)
df.index=pd.to_datetime(df.index, format='%Y-%m-%d %H:%M')

df=df.groupby(df.index.week).mean()

colors=['#cab2d6','#ffff99','#fdbf6f','#ff7f00','#e31a1c','#fb9a99','#b15928','#33a02c','#6a3d9a',
        '#b2df8a','#a6cee3','#1f78b4','darkgrey']

boxes='hat'
rp.create_stacked(df, colors=colors, site='hateruma', boxes=boxes)
