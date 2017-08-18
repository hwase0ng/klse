'''
Created on Dec 23, 2016

@author: t.roy
'''
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import *
from matplotlib.finance import candlestick_ohlc
import matplotlib.ticker as ticker
import os, csv, sys
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from Utils.strutils import decompose_stockname, str2float, getCsvFile, getCsvFile2
from buyVol1 import buy_vol_stats
from eodcsv import eod2csv
from Utils.dateutils import datestr2float
from Scan.buyVol1 import csv2df

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
    pkfile = getCsvFile(stock)+".pickle"
    if os.path.isfile(pkfile):
        dfVol = pd.read_pickle(pkfile)
    else:
        print 'Error retrieving ' + stock
        return None
    return dfVol

def csv2list(stock,
             sdate=(date.today() + relativedelta(months=-6)).strftime("%Y-%m-%d"),
             edate=datetime.today().strftime("%Y-%m-%d")):
    if stock is None or len(stock)==0:
        print "Missing stock name"
        return None
    sdate2 = datetime.strptime(sdate,'%Y-%m-%d')
    sdate60 = (sdate2+relativedelta(months=-2)).strftime("%Y-%m-%d")
    df = csv2df(stock,sdate60,edate)
    header = ['date','open','high','low','close','volume']
    df.to_csv(getCsvFile2(stock,sdate60,edate), columns=header, header=False, index=False)
    mylist = []
    with open(getCsvFile2(stock,sdate60,edate), 'rb') as f:
        reader = csv.reader(f)
        parsed = ((datestr2float(row[0]),
                   str2float(row[1]), str2float(row[2]), str2float(row[3]),
                   str2float(row[4]), str2float(row[5]))
                  for row in reader)
        for row in parsed:
            mylist.append(tuple(row))
#       print type(mylist),mylist
    return mylist

def csv2list_all(stock):
    if stock is None or len(stock)==0:
        print "Missing stock name"
        return None
    mylist = []
    with open(getCsvFile(stock), 'rb') as f:
        reader = csv.reader(f)
#       mylist = map(tuple, reader)
#       for row in reader:
#           new = [str2float(x) for x in row if x != '']
        parsed = ((datestr2float(row[0]),
                   str2float(row[1]), str2float(row[2]), str2float(row[3]),
                   str2float(row[4]), str2float(row[5]))
                  for row in reader)
        for row in parsed:
            mylist.append(tuple(row))
#       print type(mylist),mylist
    return mylist

def showPlotVolStats(stock,
                     sdate=(date.today() + relativedelta(months=-6)).strftime("%Y-%m-%d"),
                     edate=datetime.today().strftime("%Y-%m-%d")):
#   dfVol = get_dfvol(stock)
#   if dfVol is None:
#       return None
    dfVol = buy_vol_stats(stock)
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

    plt.figure(1)
    ax0=plt.subplot(6,1,1)
    quotes = csv2list(stock,sdate,edate)
    candlestick_ohlc(ax0, quotes, width=0.7)
    ax0.autoscale_view()
    ax0.xaxis_date()
    ax0.autoscale_view()
    plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')

    linestyles = ['-', '--', '-.', ':']
    ax1=plt.subplot(6,1,2)
    for i in range(len(meanVolByGroup)):
    #   plt.plot(meanVolByGroup[i], linestyle=linestyles[(i+4)%4], label=volLegends[i])
        data = getDatesData(volLabels, meanVolByGroup[i], 'Mean')
        plt.plot(data.index, data.Mean, linestyle=linestyles[(i+4)%4], label=volLegends[i])
    #plt.legend(loc='upper left')
    #plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05),ncol=6, fancybox=True, shadow=True)
    ax1.legend(loc='upper center', bbox_to_anchor=(0.5, 2.85), ncol=12, fancybox=True, shadow=True)
    plt.title('Mean Volume')
    ax1.get_xaxis().set_visible(False)

    ax2=plt.subplot(6,1,3)
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

    ax3=plt.subplot(6,1,4)
    for i in range(len(p25VolByGroup)):
    #   plt.plot(p25VolByGroup[i], label=volLegends[i])
    #   plt.plot(p25VolByGroup[i], linestyle=linestyles[(i+4)%4])
        data = getDatesData(volLabels, p25VolByGroup[i], 'P25')
        plt.plot(data.index, data.P25, linestyle=linestyles[(i+4)%4])
    plt.title('25%')
    ax3.get_xaxis().set_visible(False)
    ax3.set_yticks(setYticks(p25VolByGroup))

    ax4=plt.subplot(6,1,5)
    for i in range(len(p50VolByGroup)):
    #   plt.plot(p50VolByGroup[i], label=volLegends[i])
    #   plt.plot(p50VolByGroup[i], linestyle=linestyles[(i+4)%4])
        data = getDatesData(volLabels, p50VolByGroup[i], 'P50')
        plt.plot(data.index, data.P50, linestyle=linestyles[(i+4)%4])
    plt.title('50%')
    ax4.get_xaxis().set_visible(False)
    ax4.set_yticks(setYticks(p50VolByGroup))

    ax5=plt.subplot(6,1,6)
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
    counter='GDEX.0078.KL'
#   counter='3A.0012.KL'
#   csv2list(counter)
#   sys.exit()
    sname,scode = decompose_stockname(counter)
    eod2csv(sname,scode)
#   csvfile = S.work_dir+S.market_source+'/'+counter+'.csv'
#   print csv2list(counter)
    showPlotVolStats(counter, '2015-08-10', '2015-12-31')
#   showPlotVolStats('3A.0012.KL')