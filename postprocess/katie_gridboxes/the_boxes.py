

'''
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

def draw_screen_poly( lats, lons, m):
    x, y = m( lons, lats )
    xy = zip(x,y)
    poly = Polygon( xy, facecolor='red', alpha=0.4 )
    plt.gca().add_patch(poly)
    
lats = [ -30, 30, 30, -30 ]
lons = [ -50, -50, 50, 50 ]

m = Basemap(projection='sinu',lon_0=0)
m.drawcoastlines()
m.drawmapboundary()
draw_screen_poly( lats, lons, m )
'''
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

def draw_screen_poly( lats, lons, m, color='red', label=False):
    x, y = m( lons, lats )
    xy = zip(x,y)
    poly = Polygon( list(xy), fill=False,facecolor=None, ec=color,lw=2,ls='--',label=label )
    plt.gca().add_patch(poly)

f,ax=plt.subplots(figsize=(8,8))
m = Basemap(projection='cyl', llcrnrlon=-30,urcrnrlon=-10,llcrnrlat=12.,urcrnrlat=28, ax=ax)
m.bluemarble()
m.drawcoastlines()
m.drawmapboundary()

draw_screen_poly( [14.9, 18.77, 18.77, 14.9], [-26.9, -26.9, -22.34, -22.34], m, color='#e31a1c' , label='0.5 days')
draw_screen_poly( [14.9, 20.64, 20.64, 14.9], [-26.9, -26.9, -19.79, -19.79 ], m, color='#fd8d3c' , label='1 day')
draw_screen_poly( [14.9, 22.51, 22.51, 14.9], [-26.9, -26.9, -17.235, -17.235 ], m, color='#fecc5c' , label='1.5 days')
draw_screen_poly( [14.9, 23.4, 23.4, 14.9], [-26.9, -26.9, -16., -16 ], m, color='#ffffb2', label='1.74 days (Upwelling region)')

x,y=m(-24.9, 16.9)
plt.scatter( x, y, marker='*', color='gold')#, s=100, zorder=10)

plt.legend()
plt.savefig('plots/cv_to_upwelling_gridboxes.png')
plt.close()
