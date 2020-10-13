#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def distance_from_coast(lon,lat,coast, m, resolution='l',distance=375, degree_in_km=111.12):
    import numpy as np
    coordinates = np.vstack(coast.get_segments())
    lons,lats = m(coordinates[:,0],coordinates[:,1],inverse=True)

    dists = np.sqrt((lons-lon)**2+(lats-lat)**2)

    if np.min(dists)*degree_in_km<distance:
      return True
    else:
      return False


def check_boxes_0(lat, lon, alt=False, limit=False):
    import numpy as np
    ## box order (marine, american, african coast, african sahara, europe, nw, ne, sw, se)
    boxes=np.zeros(9)
    over=np.zeros(1)
    for t in range(len(lon)):
        if limit == False:
            if -100.<=lon[t]<=51.5 and 0.<=lat[t]<=80.:
                # MARINE ATLANTIC
                if -55.<=lon[t]<-10. and 35.<lat[t]<=80.:
                    boxes[0]+=1
                if -75.<=lon[t]<55. and 70.<lat[t]<=80.:
                    boxes[0]+=1
                if -75.<=lon[t]<-20. and 20.<lat[t]<=40.:
                    boxes[0]+=1
                if -60.<=lon[t]<-55. and 40.<lat[t]<=45.:
                    boxes[0]+=1
                if -80.<=lon[t]<-75. and 25.<lat[t]<=30.:
                    boxes[0]+=1
                if -70.<=lon[t]<-30. and 15.<lat[t]<=20.:
                    boxes[0]+=1
                if -60.<=lon[t]<-30. and 10.<lat[t]<=15.:
                    boxes[0]+=1
                if -55.<=lon[t]<-15. and 5.<lat[t]<=10.:
                    boxes[0]+=1
                if -50.<=lon[t]<-10. and 0.<lat[t]<=5.:
                    boxes[0]+=1
                if -60.<=lon[t]<-55. and 55.<lat[t]<=70.:
                    boxes[0]+=1
                if -65.<=lon[t]<-60. and 60.<lat[t]<=65.:
                    boxes[0]+=1
                if -20.<=lon[t]<-15. and 30.<lat[t]<=35.:
                    boxes[0]+=1
                if -10.<=lon[t]<-5. and 45.<lat[t]<=50.:
                    boxes[0]+=1
                if -10.<=lon[t]<10. and 65.<lat[t]<=70.:
                    boxes[0]+=1
                if -10.<=lon[t]<5. and 60.<lat[t]<=65.:
                    boxes[0]+=1
                
                # AMERICAN
                if -100.<=lon[t]<-80. and 0.<lat[t]<=80.:
                    boxes[1]+=1
                if -80.<=lon[t]<-65. and 40.<lat[t]<=70.:
                    boxes[1]+=1
                if -65.<=lon[t]<-60. and 40.<lat[t]<=60.:
                    boxes[1]+=1
                if -60.<=lon[t]<-55. and 45.<lat[t]<=55.:
                    boxes[1]+=1
                if -65.<=lon[t]<-60. and 65.<lat[t]<=70.:
                    boxes[1]+=1
                if -80.<=lon[t]<-75. and 70.<lat[t]<=80.:
                    boxes[1]+=1
                if -80.<=lon[t]<-75. and 30.<lat[t]<=40.:
                    boxes[1]+=1
                if -80.<=lon[t]<-75. and 20.<lat[t]<=25.:
                    boxes[1]+=1
                if -80.<=lon[t]<-70. and 15.<lat[t]<=20.:
                    boxes[1]+=1
                if -80.<=lon[t]<-60. and 10.<lat[t]<=15.:
                    boxes[1]+=1
                if -80.<=lon[t]<-55. and 5.<lat[t]<=10.:
                    boxes[1]+=1
                if -80.<=lon[t]<-50. and 0.<lat[t]<=5.:
                    boxes[1]+=1
                
                # AFRICAN COAST
                if -15.<=lon[t]<-5. and 30.<lat[t]<=35.:
                    boxes[2]+=1
                if -20.<=lon[t]<-10. and 25.<lat[t]<=30.:
                    boxes[2]+=1
                if -20.<=lon[t]<-15. and 10.<lat[t]<=25.:
                    boxes[2]+=1
                if -15.<=lon[t]<-10. and 5.<lat[t]<=10.:
                    boxes[2]+=1
                if -10.<=lon[t]<10. and 0.<lat[t]<=5.:
                    boxes[2]+=1
                  
                # AFRICAN
                if -5.<=lon[t]<=55. and 5.<lat[t]<=35.:
                    boxes[3]+=1
                if 10.<=lon[t]<=55. and 0.<lat[t]<=5.:
                    boxes[3]+=1
                if -10.<=lon[t]<=-5. and 5.<lat[t]<=30.:
                    boxes[3]+=1
                if -15.<=lon[t]<=-10. and 10.<lat[t]<=25.:
                    boxes[3]+=1
                
                # EUROPE
                if 10.<=lon[t]<55. and 35.<lat[t]<=70.:
                    boxes[4]+=1
                if -10.<=lon[t]<55. and 35< lat[t]<=45.:
                    boxes[4]+=1
                if -10.<=lon[t]<55. and 50.<lat[t]<=60.:
                    boxes[4]+=1
                if -5.<=lon[t]<55. and 45.<lat[t]<=50.:
                    boxes[4]+=1
                if 5.<=lon[t]<55. and 60.<lat[t]<=65.:
                    boxes[4]+=1
                
                # LOCAL : NW, NE, SW, SE
                if -30<=lon[t]<-25. and 15.<lat[t]<=20.:
                    boxes[5]+=1
                elif -25.<=lon[t]<-20. and 15.<lat[t]<=20.:
                    boxes[6]+=1
                elif -30.<=lon[t]<-25. and 10.<lat[t]<=15.:
                    boxes[7]+=1
                elif -25.<=lon[t]<-20. and 10.<lat[t]<=15.:
                    boxes[8]+=1

        else:
            if alt[t] <= limit:
                if -100.<=lon[t]<=51.5 and 0.<=lat[t]<=80.:
                    # MARINE ATLANTIC
                    if -55.<=lon[t]<-10. and 35.<lat[t]<=80.:
                        boxes[0]+=1
                    if -75.<=lon[t]<55. and 70.<lat[t]<=80.:
                        boxes[0]+=1
                    if -75.<=lon[t]<-20. and 20.<lat[t]<=40.:
                        boxes[0]+=1
                    if -60.<=lon[t]<-55. and 40.<lat[t]<=45.:
                        boxes[0]+=1
                    if -80.<=lon[t]<-75. and 25.<lat[t]<=30.:
                        boxes[0]+=1
                    if -70.<=lon[t]<-30. and 15.<lat[t]<=20.:
                        boxes[0]+=1
                    if -60.<=lon[t]<-30. and 10.<lat[t]<=15.:
                        boxes[0]+=1
                    if -55.<=lon[t]<-15. and 5.<lat[t]<=10.:
                        boxes[0]+=1
                    if -50.<=lon[t]<-10. and 0.<lat[t]<=5.:
                        boxes[0]+=1
                    if -60.<=lon[t]<-55. and 55.<lat[t]<=70.:
                        boxes[0]+=1
                    if -65.<=lon[t]<-60. and 60.<lat[t]<=65.:
                        boxes[0]+=1
                    if -20.<=lon[t]<-15. and 30.<lat[t]<=35.:
                        boxes[0]+=1
                    if -10.<=lon[t]<-5. and 45.<lat[t]<=50.:
                        boxes[0]+=1
                    if -10.<=lon[t]<10. and 65.<lat[t]<=70.:
                        boxes[0]+=1
                    if -10.<=lon[t]<5. and 60.<lat[t]<=65.:
                        boxes[0]+=1
                    
                    # AMERICAN
                    if -100.<=lon[t]<-80. and 0.<lat[t]<=80.:
                        boxes[1]+=1
                    if -80.<=lon[t]<-65. and 40.<lat[t]<=70.:
                        boxes[1]+=1
                    if -65.<=lon[t]<-60. and 40.<lat[t]<=60.:
                        boxes[1]+=1
                    if -60.<=lon[t]<-55. and 45.<lat[t]<=55.:
                        boxes[1]+=1
                    if -65.<=lon[t]<-60. and 65.<lat[t]<=70.:
                        boxes[1]+=1
                    if -80.<=lon[t]<-75. and 70.<lat[t]<=80.:
                        boxes[1]+=1
                    if -80.<=lon[t]<-75. and 30.<lat[t]<=40.:
                        boxes[1]+=1
                    if -80.<=lon[t]<-75. and 20.<lat[t]<=25.:
                        boxes[1]+=1
                    if -80.<=lon[t]<-70. and 15.<lat[t]<=20.:
                        boxes[1]+=1
                    if -80.<=lon[t]<-60. and 10.<lat[t]<=15.:
                        boxes[1]+=1
                    if -80.<=lon[t]<-55. and 5.<lat[t]<=10.:
                        boxes[1]+=1
                    if -80.<=lon[t]<-50. and 0.<lat[t]<=5.:
                        boxes[1]+=1
                    
                    # AFRICAN COAST
                    if -15.<=lon[t]<-5. and 30.<lat[t]<=35.:
                        boxes[2]+=1
                    if -20.<=lon[t]<-10. and 25.<lat[t]<=30.:
                        boxes[2]+=1
                    if -20.<=lon[t]<-15. and 10.<lat[t]<=25.:
                        boxes[2]+=1
                    if -15.<=lon[t]<-10. and 5.<lat[t]<=10.:
                        boxes[2]+=1
                    if -10.<=lon[t]<10. and 0.<lat[t]<=5.:
                        boxes[2]+=1
                      
                    # AFRICAN
                    if -5.<=lon[t]<=55. and 5.<lat[t]<=35.:
                        boxes[3]+=1
                    if 10.<=lon[t]<=55. and 0.<lat[t]<=5.:
                        boxes[3]+=1
                    if -10.<=lon[t]<=-5. and 5.<lat[t]<=30.:
                        boxes[3]+=1
                    if -15.<=lon[t]<=-10. and 10.<lat[t]<=25.:
                        boxes[3]+=1
                    
                    # EUROPE
                    if 10.<=lon[t]<55. and 35.<lat[t]<=70.:
                        boxes[4]+=1
                    if -10.<=lon[t]<55. and 35< lat[t]<=45.:
                        boxes[4]+=1
                    if -10.<=lon[t]<55. and 50.<lat[t]<=60.:
                        boxes[4]+=1
                    if -5.<=lon[t]<55. and 45.<lat[t]<=50.:
                        boxes[4]+=1
                    if 5.<=lon[t]<55. and 60.<lat[t]<=65.:
                        boxes[4]+=1
                    
                    # LOCAL : NW, NE, SW, SE
                    if -30<=lon[t]<-25. and 15.<lat[t]<=20.:
                        boxes[5]+=1
                    elif -25.<=lon[t]<-20. and 15.<lat[t]<=20.:
                        boxes[6]+=1
                    elif -30.<=lon[t]<-25. and 10.<lat[t]<=15.:
                        boxes[7]+=1
                    elif -25.<=lon[t]<-20. and 10.<lat[t]<=15.:
                        boxes[8]+=1

    SUM = np.nansum(boxes)
    percent = boxes/SUM * 100
    return boxes, percent, over  



def boxes_0(lat, lon, alt, npart, limit=False):
    import numpy as np
    ## box order (marine, american, african coast, african sahara, europe, nw, ne, sw, se)
    boxes=np.zeros(9)
    over=np.zeros(1)

    for t in range(len(lon)):
        for p in range(npart):
            if limit == False:
                if -100.<=lon[t,p]<=51.5 and 0.<=lat[t,p]<=80.:
                    # MARINE ATLANTIC
                    if -55.<=lon[t,p]<-10. and 35.<lat[t,p]<=80.:
                        boxes[0]+=1
                    if -75.<=lon[t,p]<55. and 70.<lat[t,p]<=80.:
                        boxes[0]+=1
                    if -75.<=lon[t,p]<-20. and 20.<lat[t,p]<=40.:
                        boxes[0]+=1
                    if -60.<=lon[t,p]<-55. and 40.<lat[t,p]<=45.:
                        boxes[0]+=1
                    if -80.<=lon[t,p]<-75. and 25.<lat[t,p]<=30.:
                        boxes[0]+=1
                    if -70.<=lon[t,p]<-30. and 15.<lat[t,p]<=20.:
                        boxes[0]+=1
                    if -60.<=lon[t,p]<-30. and 10.<lat[t,p]<=15.:
                        boxes[0]+=1
                    if -55.<=lon[t,p]<-15. and 5.<lat[t,p]<=10.:
                        boxes[0]+=1
                    if -50.<=lon[t,p]<-10. and 0.<lat[t,p]<=5.:
                        boxes[0]+=1
                    if -60.<=lon[t,p]<-55. and 55.<lat[t,p]<=70.:
                        boxes[0]+=1
                    if -65.<=lon[t,p]<-60. and 60.<lat[t,p]<=65.:
                        boxes[0]+=1
                    if -20.<=lon[t,p]<-15. and 30.<lat[t,p]<=35.:
                        boxes[0]+=1
                    if -10.<=lon[t,p]<-5. and 45.<lat[t,p]<=50.:
                        boxes[0]+=1
                    if -10.<=lon[t,p]<10. and 65.<lat[t,p]<=70.:
                        boxes[0]+=1
                    if -10.<=lon[t,p]<5. and 60.<lat[t,p]<=65.:
                        boxes[0]+=1
                    
                    # AMERICAN
                    if -100.<=lon[t,p]<-80. and 0.<lat[t,p]<=80.:
                        boxes[1]+=1
                    if -80.<=lon[t,p]<-65. and 40.<lat[t,p]<=70.:
                        boxes[1]+=1
                    if -65.<=lon[t,p]<-60. and 40.<lat[t,p]<=60.:
                        boxes[1]+=1
                    if -60.<=lon[t,p]<-55. and 45.<lat[t,p]<=55.:
                        boxes[1]+=1
                    if -65.<=lon[t,p]<-60. and 65.<lat[t,p]<=70.:
                        boxes[1]+=1
                    if -80.<=lon[t,p]<-75. and 70.<lat[t,p]<=80.:
                        boxes[1]+=1
                    if -80.<=lon[t,p]<-75. and 30.<lat[t,p]<=40.:
                        boxes[1]+=1
                    if -80.<=lon[t,p]<-75. and 20.<lat[t,p]<=25.:
                        boxes[1]+=1
                    if -80.<=lon[t,p]<-70. and 15.<lat[t,p]<=20.:
                        boxes[1]+=1
                    if -80.<=lon[t,p]<-60. and 10.<lat[t,p]<=15.:
                        boxes[1]+=1
                    if -80.<=lon[t,p]<-55. and 5.<lat[t,p]<=10.:
                        boxes[1]+=1
                    if -80.<=lon[t,p]<-50. and 0.<lat[t,p]<=5.:
                        boxes[1]+=1
                    
                    # AFRICAN COAST
                    if -15.<=lon[t,p]<-5. and 30.<lat[t,p]<=35.:
                        boxes[2]+=1
                    if -20.<=lon[t,p]<-10. and 25.<lat[t,p]<=30.:
                        boxes[2]+=1
                    if -20.<=lon[t,p]<-15. and 10.<lat[t,p]<=25.:
                        boxes[2]+=1
                    if -15.<=lon[t,p]<-10. and 5.<lat[t,p]<=10.:
                        boxes[2]+=1
                    if -10.<=lon[t,p]<10. and 0.<lat[t,p]<=5.:
                        boxes[2]+=1
                      
                    # AFRICAN
                    if -5.<=lon[t,p]<=55. and 5.<lat[t,p]<=35.:
                        boxes[3]+=1
                    if 10.<=lon[t,p]<=55. and 0.<lat[t,p]<=5.:
                        boxes[3]+=1
                    if -10.<=lon[t,p]<=-5. and 5.<lat[t,p]<=30.:
                        boxes[3]+=1
                    if -15.<=lon[t,p]<=-10. and 10.<lat[t,p]<=25.:
                        boxes[3]+=1
                    
                    # EUROPE
                    if 10.<=lon[t,p]<55. and 35.<lat[t,p]<=70.:
                        boxes[4]+=1
                    if -10.<=lon[t,p]<55. and 35< lat[t,p]<=45.:
                        boxes[4]+=1
                    if -10.<=lon[t,p]<55. and 50.<lat[t,p]<=60.:
                        boxes[4]+=1
                    if -5.<=lon[t,p]<55. and 45.<lat[t,p]<=50.:
                        boxes[4]+=1
                    if 5.<=lon[t,p]<55. and 60.<lat[t,p]<=65.:
                        boxes[4]+=1
                    
                    # LOCAL : NW, NE, SW, SE
                    if -30<=lon[t,p]<-25. and 15.<lat[t,p]<=20.:
                        boxes[5]+=1
                    elif -25.<=lon[t,p]<-20. and 15.<lat[t,p]<=20.:
                        boxes[6]+=1
                    elif -30.<=lon[t,p]<-25. and 10.<lat[t,p]<=15.:
                        boxes[7]+=1
                    elif -25.<=lon[t,p]<-20. and 10.<lat[t,p]<=15.:
                        boxes[8]+=1

            else:
                if alt[t,p] <= limit:
                    if -100.<=lon[t,p]<=51.5 and 0.<=lat[t,p]<=80.:
                        # MARINE ATLANTIC
                        if -55.<=lon[t,p]<-10. and 35.<lat[t,p]<=80.:
                            boxes[0]+=1
                        if -75.<=lon[t,p]<55. and 70.<lat[t,p]<=80.:
                            boxes[0]+=1
                        if -75.<=lon[t,p]<-20. and 20.<lat[t,p]<=40.:
                            boxes[0]+=1
                        if -60.<=lon[t,p]<-55. and 40.<lat[t,p]<=45.:
                            boxes[0]+=1
                        if -80.<=lon[t,p]<-75. and 25.<lat[t,p]<=30.:
                            boxes[0]+=1
                        if -70.<=lon[t,p]<-30. and 15.<lat[t,p]<=20.:
                            boxes[0]+=1
                        if -60.<=lon[t,p]<-30. and 10.<lat[t,p]<=15.:
                            boxes[0]+=1
                        if -55.<=lon[t,p]<-15. and 5.<lat[t,p]<=10.:
                            boxes[0]+=1
                        if -50.<=lon[t,p]<-10. and 0.<lat[t,p]<=5.:
                            boxes[0]+=1
                        if -60.<=lon[t,p]<-55. and 55.<lat[t,p]<=70.:
                            boxes[0]+=1
                        if -65.<=lon[t,p]<-60. and 60.<lat[t,p]<=65.:
                            boxes[0]+=1
                        if -20.<=lon[t,p]<-15. and 30.<lat[t,p]<=35.:
                            boxes[0]+=1
                        if -10.<=lon[t,p]<-5. and 45.<lat[t,p]<=50.:
                            boxes[0]+=1
                        if -10.<=lon[t,p]<10. and 65.<lat[t,p]<=70.:
                            boxes[0]+=1
                        if -10.<=lon[t,p]<5. and 60.<lat[t,p]<=65.:
                            boxes[0]+=1
                        
                        # AMERICAN
                        if -100.<=lon[t,p]<-80. and 0.<lat[t,p]<=80.:
                            boxes[1]+=1
                        if -80.<=lon[t,p]<-65. and 40.<lat[t,p]<=70.:
                            boxes[1]+=1
                        if -65.<=lon[t,p]<-60. and 40.<lat[t,p]<=60.:
                            boxes[1]+=1
                        if -60.<=lon[t,p]<-55. and 45.<lat[t,p]<=55.:
                            boxes[1]+=1
                        if -65.<=lon[t,p]<-60. and 65.<lat[t,p]<=70.:
                            boxes[1]+=1
                        if -80.<=lon[t,p]<-75. and 70.<lat[t,p]<=80.:
                            boxes[1]+=1
                        if -80.<=lon[t,p]<-75. and 30.<lat[t,p]<=40.:
                            boxes[1]+=1
                        if -80.<=lon[t,p]<-75. and 20.<lat[t,p]<=25.:
                            boxes[1]+=1
                        if -80.<=lon[t,p]<-70. and 15.<lat[t,p]<=20.:
                            boxes[1]+=1
                        if -80.<=lon[t,p]<-60. and 10.<lat[t,p]<=15.:
                            boxes[1]+=1
                        if -80.<=lon[t,p]<-55. and 5.<lat[t,p]<=10.:
                            boxes[1]+=1
                        if -80.<=lon[t,p]<-50. and 0.<lat[t,p]<=5.:
                            boxes[1]+=1
                        
                        # AFRICAN COAST
                        if -15.<=lon[t,p]<-5. and 30.<lat[t,p]<=35.:
                            boxes[2]+=1
                        if -20.<=lon[t,p]<-10. and 25.<lat[t,p]<=30.:
                            boxes[2]+=1
                        if -20.<=lon[t,p]<-15. and 10.<lat[t,p]<=25.:
                            boxes[2]+=1
                        if -15.<=lon[t,p]<-10. and 5.<lat[t,p]<=10.:
                            boxes[2]+=1
                        if -10.<=lon[t,p]<10. and 0.<lat[t,p]<=5.:
                            boxes[2]+=1
                          
                        # AFRICAN
                        if -5.<=lon[t,p]<=55. and 5.<lat[t,p]<=35.:
                            boxes[3]+=1
                        if 10.<=lon[t,p]<=55. and 0.<lat[t,p]<=5.:
                            boxes[3]+=1
                        if -10.<=lon[t,p]<=-5. and 5.<lat[t,p]<=30.:
                            boxes[3]+=1
                        if -15.<=lon[t,p]<=-10. and 10.<lat[t,p]<=25.:
                            boxes[3]+=1
                        
                        # EUROPE
                        if 10.<=lon[t,p]<55. and 35.<lat[t,p]<=70.:
                            boxes[4]+=1
                        if -10.<=lon[t,p]<55. and 35< lat[t,p]<=45.:
                            boxes[4]+=1
                        if -10.<=lon[t,p]<55. and 50.<lat[t,p]<=60.:
                            boxes[4]+=1
                        if -5.<=lon[t,p]<55. and 45.<lat[t,p]<=50.:
                            boxes[4]+=1
                        if 5.<=lon[t,p]<55. and 60.<lat[t,p]<=65.:
                            boxes[4]+=1
                        
                        # LOCAL : NW, NE, SW, SE
                        if -30<=lon[t,p]<-25. and 15.<lat[t,p]<=20.:
                            boxes[5]+=1
                        elif -25.<=lon[t,p]<-20. and 15.<lat[t,p]<=20.:
                            boxes[6]+=1
                        elif -30.<=lon[t,p]<-25. and 10.<lat[t,p]<=15.:
                            boxes[7]+=1
                        elif -25.<=lon[t,p]<-20. and 10.<lat[t,p]<=15.:
                            boxes[8]+=1
                else:
                    over+=1

    SUM = np.nansum(boxes)
    percent = boxes/SUM * 100
    return boxes, percent, over 



def boxes_1(lat, lon, alt, npart, limit=100):
    import numpy as np
    import matplotlib
    matplotlib.use('agg')
    ## box order (Upwelling, Sahel, Sahara, West Africa, North Africa, Europe,
    ##            North America, South America, North Atlantic, South Atlantic  )
    from mpl_toolkits.basemap import Basemap
    m = Basemap(projection='cyl', llcrnrlat=0,urcrnrlat=80,llcrnrlon=-90, urcrnrlon=38.,\
            resolution='c',area_thresh=1000.)
    coast = m.drawcoastlines(linewidth=.5)
    boxes=np.zeros(10)
    over=np.zeros(1)
    for t in range(len(lon)):
        for p in range(npart):
            if alt[t,p]<=limit:
                checker=False
                ## Whole domain of interest
                if lon[t,p]>=-89. and lon[t,p]<=36. and lat[t,p]>=2. and lat[t,p]<=79.:
                    ## Maritanian Upwelling
                    if lon[t,p]>=-25. and lon[t,p]<=5. and lat[t,p]>=20. and lat[t,p]<=26.:
                        if distance_from_coast(lon[t,p],lat[t,p], coast, m)== True:
                            if m.is_land(lon[t,p],lat[t,p]) == False:
                                #upwelling[j,t,p]=1
                                boxes[0]+=1
                                checker=True
                                
                    ## Sahel Region
                    if lon[t,p]>=-20. and lon[t,p]<=40. and lat[t,p]>=14. and lat[t,p]<18.:
                        if m.is_land(lon[t,p],lat[t,p]) == True:
                            #sahel[j,t,p]=1
                            boxes[1]+=1
                            checker=True
                        elif lon[t,p]>=-14. and lon[t,p]<=40. and lat[t,p]>=14. and lat[t,p]<18.:
                            #sahel[j,t,p]=1
                            boxes[1]+=1
                            checker=True
                            
                    ## Sahara Region
                    if lon[t,p]>=-20. and lon[t,p]<40. and lat[t,p]>=18. and lat[t,p]<=34.:
                        if m.is_land(lon[t,p],lat[t,p]) == True:
                            if lon[t,p]>=-20. and lon[t,p]<-13. and lat[t,p]>=27. and lat[t,p]<=29.:
                                checker=False
                            else:
                                #sahara[j,t,p]=1
                                boxes[2]+=1
                                checker=True
                  
                    ## West African Populated
                    if lon[t,p]>=-20. and lon[t,p]<=12. and lat[t,p]>=4. and lat[t,p]<=14.:
                        if m.is_land(lon[t,p],lat[t,p]) == True:
                            #west_africa_populated[j,t,p]=1
                            boxes[3]+=1
                            checker=True
                        else:
                            checker=False
                        if lon[t,p]>=-5. and lat[t,p]>=7.0:
                            #west_africa_populated[j,t,p]=1
                            boxes[3]+=1
                            checker=True
                            
                    ## BB region
                    if lon[t,p]>12. and lon[t,p]<=36. and lat[t,p]>=4. and lat[t,p]<=14.:
                        #burning_region[j,t,p]=1
                        boxes[4]+=1
                        checker=True
                        
                    ## Europe
                    if lon[t,p]>=-12. and lon[t,p]<=45. and lat[t,p]>=34. and lat[t,p]<=73.:
                        if m.is_land(lon[t,p],lat[t,p]) == True or distance_from_coast(lon[t,p],lat[t,p], coast, m,distance=400)== True:
                            if lon[t,p]>=-12. and lon[t,p]<=-9. and lat[t,p]>=62. and lat[t,p]<=75.:
                                checker=False
                            else:
                                #europe[j,t,p]=1
                                boxes[5]+=1
                                checker=True
                        elif lon[t,p]>=2. and lon[t,p]<=7. and lat[t,p]>=55. and lat[t,p]<=60.:
                            #europe[j,t,p]=1
                            boxes[5]+=1
                            checker=True
                    elif lon[t,p]>=9. and lat[t,p]>30 and lat[t,p]<=36.:
                        if m.is_land(lon[t,p],lat[t,p]) == False:
                            #europe[j,t,p]=1
                            boxes[5]+=1
                            checker=True
                        elif lon[t,p]>=-9. and lat[t,p]>=34. and lat[t,p]<=36.:
                            #europe[j,t,p]=1
                            boxes[5]+=1
                            checker=True
         
                    ## North America
                    if lon[t,p]>=-90. and lon[t,p]<=-50. and lat[t,p]>=15. and lat[t,p]<=80.:
                        if m.is_land(lon[t,p],lat[t,p]) == True:
                            #north_am[j,t,p]=1
                            boxes[6]+=1
                            checker=True
                        elif distance_from_coast(lon[t,p], lat[t,p], coast, m)==True:
                            #north_am[j,t,p]=1 
                            boxes[6]+=1
                            checker=True
                        elif lon[t,p]<=-50. and lat[t,p]>=45.:
                            #north_am[j,t,p]=1 
                            boxes[6]+=1
                            checker=True
                        elif lon[t,p]<=-80. and lat[t,p]>=20.:
                            #north_am[j,t,p]=1 
                            boxes[6]+=1
                            checker=True

                    # South America
                    if lon[t,p]>=-90. and lon[t,p]<=-58 and lat[t,p]>=0. and lat[t,p]<=15.:
                        #south_am[j,t,p]=1 
                        boxes[7]+=1
                        checker=True
                    elif lon[t,p]>=-90. and lon[t,p]<=-50 and lat[t,p]>=0. and lat[t,p]<=15.:
                        if distance_from_coast(lon[t,p], lat[t,p], coast, m)==True:
                            #south_am[j,t,p]=1 
                            boxes[7]+=1
                            checker=True
                                           
                    ## Fill oceans last so there is no overlap
                    if checker==False:
                        if lat[t,p]>=16.51 and lon[t,p]<=32:
                            #atlantic_north[j,t,p]=1
                            boxes[8]+=1
                            checker=True
                        elif lat[t,p]<=16.51 and m.is_land(lon[t,p],lat[t,p])== False and lon[t,p]<=12 :
                            #atlantic_south[j,t,p]=1
                            boxes[9]+=1
                            checker=True

            else:
                    over+=1

    SUM = np.nansum(boxes)
    percent = boxes/SUM * 100
    return boxes, percent, over

