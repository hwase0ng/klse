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
import os

pd.options.display.float_format='{:.0f}'.format
volLegends=['1d','1w','2w','3w','4w','5w','6w','7w','8w','13w','21w','34w']
lenLegends=len(volLegends)

def getDatesData(dates,vol,stattype):
    dt = pd.DataFrame.from_records(zip(dates,vol), columns=['Dates',stattype])
    dt.Dates = pd.to_datetime(dt['Dates'], format='%Y-%m-%d')
    dt.set_index(['Dates'],inplace=True)
    return dt

def getYticks(volgroup):
    minstd = np.nanmin(volgroup)
    maxstd = np.nanmax(volgroup)
    ticks  = (maxstd - minstd) / 7
    return minstd,maxstd,ticks

def setYticks(volgroup):
    minvol,maxvol,ticks = getYticks(volgroup) 
    major_ticks = np.arange(0,maxvol,ticks)
    return major_ticks

def get_dfvol(stock):
    csvfile = S.work_dir+S.market_source+'/'+stock+'.csv'
    pkfile = csvfile+".pickle"
    if os.path.isfile(pkfile):
        dfVol = pd.read_pickle(pkfile)
    else:
        print 'Error retrieving ' + stock
        return None
    return dfVol

def showPlotVolStats(stock):
    dfVol = get_dfvol(stock)
    if dfVol is None:
        return None
    volDates = dfVol.index.levels[0]
    #print type(volDates),volDates
    volLabels = volDates.values.tolist()
    #print type(volLabels),volLabels
    #print dfVol['mean'].tail()
    #print dfVol['mean'][0],dfVol['mean'][1]
    listMean= dfVol['mean'].values
    listStd = dfVol['std'].values
    listP25 = dfVol['25%'].values
    listP50 = dfVol['50%'].values
    listP75 = dfVol['75%'].values
    #print listMean[:5]
    meanVolByDate = np.reshape(listMean,(len(listMean)/lenLegends,lenLegends))
    meanVolByGroup = meanVolByDate.transpose()
    stdVolByDate = np.reshape(listStd,(len(listStd)/lenLegends,lenLegends))
    stdVolByGroup = stdVolByDate.transpose()
    p25VolByDate = np.reshape(listP25,(len(listP25)/lenLegends,lenLegends))
    p25VolByGroup = p25VolByDate.transpose()
    p50VolByDate = np.reshape(listP50,(len(listP50)/lenLegends,lenLegends))
    p50VolByGroup = p50VolByDate.transpose()
    p75VolByDate = np.reshape(listP75,(len(listP75)/lenLegends,lenLegends))
    p75VolByGroup = p75VolByDate.transpose()
    #print meanVolByGroup

    linestyles = ['-', '--', '-.', ':']
    plt.figure(1)
    ax1=plt.subplot(5,1,1)
    for i in range(len(meanVolByGroup)):
    #   plt.plot(meanVolByGroup[i], linestyle=linestyles[(i+4)%4], label=volLegends[i])
        data = getDatesData(volLabels, meanVolByGroup[i], 'Mean')
        plt.plot(data.index, data.Mean, linestyle=linestyles[(i+4)%4], label=volLegends[i])
    #plt.legend(loc='upper left')
    #plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05),ncol=6, fancybox=True, shadow=True)
    ax1.legend(loc='upper center', bbox_to_anchor=(0.5, 1.65), ncol=12, fancybox=True, shadow=True)
    plt.title('Mean Volume')
    ax1.get_xaxis().set_visible(False)

    ax2=plt.subplot(5,1,2)
    for i in range(len(stdVolByGroup)):
    #   plt.plot(stdVolByGroup[i], label=volLegends[i])
    #   plt.plot(stdVolByGroup[i], linestyle=linestyles[(i+4)%4])
        data = getDatesData(volLabels, stdVolByGroup[i], 'Std')
        plt.plot(data.index, data.Std, linestyle=linestyles[(i+4)%4], label=volLegends[i])
    plt.title('Standard Deviation')
    ax2.get_xaxis().set_visible(False)
    #minvol,maxvol,ticks = getYticks(stdVolByGroup) 
    #major_ticks = np.arange(0,maxvol,ticks)
    ax2.set_yticks(setYticks(stdVolByGroup))

    ax3=plt.subplot(5,1,3)
    for i in range(len(p25VolByGroup)):
    #   plt.plot(p25VolByGroup[i], label=volLegends[i])
    #   plt.plot(p25VolByGroup[i], linestyle=linestyles[(i+4)%4])
        data = getDatesData(volLabels, p25VolByGroup[i], 'P25')
        plt.plot(data.index, data.P25, linestyle=linestyles[(i+4)%4])
    plt.title('25%')
    ax3.get_xaxis().set_visible(False)
    ax3.set_yticks(setYticks(p25VolByGroup))

    ax4=plt.subplot(5,1,4)
    for i in range(len(p50VolByGroup)):
    #   plt.plot(p50VolByGroup[i], label=volLegends[i])
    #   plt.plot(p50VolByGroup[i], linestyle=linestyles[(i+4)%4])
        data = getDatesData(volLabels, p50VolByGroup[i], 'P50')
        plt.plot(data.index, data.P50, linestyle=linestyles[(i+4)%4])
    plt.title('50%')
    ax4.get_xaxis().set_visible(False)
    ax4.set_yticks(setYticks(p50VolByGroup))

    ax5=plt.subplot(5,1,5)
    #tick_spacing = 5
    #ax5.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    #ax5.set_xticklabels(volLabels,rotation=45)
    ax5.get_xaxis().get_major_formatter().set_scientific(False)
    ax5.get_yaxis().get_major_formatter().set_scientific(False)
    ax5.get_xaxis().get_major_formatter().set_useOffset(False)
    ax5.get_yaxis().get_major_formatter().set_useOffset(False)
    # Turn off scientific notation on the axes.
    y_formatter = ticker.ScalarFormatter(useOffset=False)
    ax5.yaxis.set_major_formatter(y_formatter)
    for i in range(len(p75VolByGroup)):
    #   plt.plot(p75VolByGroup[i], label=volLegends[i])
    #   plt.plot(p75VolByGroup[i], linestyle=linestyles[(i+4)%4])
        data = getDatesData(volLabels, p75VolByGroup[i], 'P75')
        plt.plot(data.index, data.P75, linestyle=linestyles[(i+4)%4])
    plt.title('75%')
    ax5.set_yticks(setYticks(p75VolByGroup))
    '''
    # Shrink current axis's height by 10% on the bottom
    box = ax1.get_position()
    ax1.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])
    box = ax2.get_position()
    ax2.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])
    box = ax3.get_position()
    ax3.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])
    box = ax4.get_position()
    ax4.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])
    box = ax5.get_position()
    ax5.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])
    # Put a legend below current axis
    #ax1.legend(loc='upper center', bbox_to_anchor=(0.5, 1.75), fancybox=True, shadow=True, ncol=12)
    '''
    '''
    # Shrink current axis by 20%
    box = ax1.get_position()
    ax1.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    box = ax2.get_position()
    ax2.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    box = ax3.get_position()
    ax3.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    box = ax4.get_position()
    ax4.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    box = ax5.get_position()
    ax5.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    # Put a legend to the right of the current axis
    ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    '''
    plt.show()

if __name__ == '__main__':
    showPlotVolStats('GDEX.0078.KL')
    showPlotVolStats('3A.0012.KL')