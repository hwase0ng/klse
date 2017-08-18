'''
Created on Dec 23, 2016

@author: t.roy
'''
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import numpy as np
from datetime import datetime
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.ticker as ticker
import Main.settings as S

def format_date(x, pos=None):
     return dates.num2date(x).strftime('%Y-%m-%d') #use FuncFormatter to format dates

pd.options.display.float_format='{:.0f}'.format
csvfile = S.work_dir+S.market_source+'/GDEX.0078.KL.csv'
pkfile = csvfile+".pickle"
dfVol = pd.read_pickle(pkfile)
volDates = dfVol.index.levels[0]
#print type(volDates),volDates
volLabels = volDates.values.tolist()
#print type(volLabels),volLabels
volLegends=['1d','1w','2w','3w','4w','5w','6w','7w','8w','13w','21w','34w']
lenLegends=len(volLegends)
#print dfVol['mean'].tail()
#print dfVol['mean'][0],dfVol['mean'][1]
listMean= dfVol['mean'].values
listStd = dfVol['std'].values
listCount = dfVol['count'].values
#print listMean[:5]
meanVolByDate = np.reshape(listMean,(len(listMean)/lenLegends,lenLegends))
meanVolByGroup = meanVolByDate.transpose()
stdVolByDate = np.reshape(listStd,(len(listStd)/lenLegends,lenLegends))
stdVolByGroup = stdVolByDate.transpose()
cntVolByDate = np.reshape(listCount,(len(listCount)/lenLegends,lenLegends))
cntVolByGroup = cntVolByDate.transpose()
#print meanVolByGroup
some_dates = [dates.date2num(datetime.strptime(dt,'%Y-%m-%d')) for dt in volLabels]
print type(some_dates),some_dates

fig = plt.figure()
ax = Axes3D(fig, rect=[0,0.1,1,1])  # make room for date labels
i = 1
for c, z in zip(['r','g','b','y','r','g','b','y'], listCount[1:9]):
    xs = np.array(some_dates)
    ys = stdVolByGroup[i]
    i = i+1
    ax.bar(xs,ys,zs=z, zdir='y',color=c,alpha=0.8,width=2)
#   ax.scatter(xs,ys,zs=z, zdir='y',s=20,color=c)
    
#ax.w_xaxis.set_major_locator(ticker.FixedLocator(some_dates))
#ax.w_xaxis.set_major_formatter(ticker.FuncFormatter(some_dates))

for tl in ax.w_xaxis.get_ticklabels():
    tl.set_ha('right')
    tl.set_rotation(30)
    
ax.set_ylabel('Series')
ax.set_zlabel('Mean Volume')
plt.show()

if __name__ == '__main__':
    pass