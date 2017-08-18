'''
Created on Dec 23, 2016

@author: t.roy
'''
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import *
import matplotlib.ticker as ticker
import Main.settings as S

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
#print listMean[:5]
meanVolByDate = np.reshape(listMean,(len(listMean)/lenLegends,lenLegends))
meanVolByGroup = meanVolByDate.transpose()
stdVolByDate = np.reshape(listStd,(len(listStd)/lenLegends,lenLegends))
stdVolByGroup = stdVolByDate.transpose()
#print meanVolByGroup

fig = plt.figure().gca(projection='3d')
fig.scatter(dfVol['mean'], dfVol['std'], dfVol['50%'])
fig.set_xlabel('Mean')
fig.set_ylabel('Std')
fig.set_zlabel('P50')
plt.show()

if __name__ == '__main__':
    pass