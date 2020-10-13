import pandas as pd
filename='missingfiles_05x05.txt'
import csv
from operator import itemgetter
reader = csv.reader(open(filename), delimiter="\t")
last_line=''
empty=[]
for line in sorted(reader, key=itemgetter(0)):
    if line==last_line:
        continue
    else:
        empty.append(line)
    last_line=line


df=pd.DataFrame(empty)
df.to_csv('new'+filename,index=False,header='GFS Analysis met files missing or unavailable')
