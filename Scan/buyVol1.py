'''
Created on Dec 17, 2016
@author: t.roy
Objective: Get volume statistics for a range of dates using Pandas Describe function into 3D view
print dfVol sample:
                count    mean     std     min     25%     50%     75%     max
2015-08-10 1d       1  188900     nan  188900  188900  188900  188900  188900
           1w       5  110040  117213    9500   35200   39200  188900  277400
           2w      10  124790   95225    9500   43450  100550  194225  277400
           3w      15  151133  114644    9500   51300  113000  220200  358900
           4w      20  140900  103203    9500   56800  109700  190675  358900
           5w      25  161628  117687    9500   63000  114800  244400  469900
           6w      30  213453  192889    9500   90300  155700  270850  856800
           7w      35  282169  326525    9500  101650  180800  313450 1682900
           8w      40  383435  530548    9500  108500  206550  391525 2811300
           13w     65  418485  480854    9500  152700  251200  469900 2811300
           21w    105  548154  694731    9500  198600  377400  639000 5515800
           34w    149  510680  615081    9500  196000  365400  561800 5515800
2015-08-11 1d       1  792900     nan  792900  792900  792900  792900  792900
           1w       5  260780  317263    9500   35200  188900  277400  792900
           2w      10  179640  231802    9500   43450  100550  194225  792900
           3w      15  180067  196423    9500   51300  113000  220200  792900
           4w      20  172880  178718    9500   56800  109700  208100  792900
           5w      25  188752  172037    9500   63000  153300  251200  792900
           6w      30  235363  219268    9500   90300  169450  277550  856800
           7w      35  279594  321973    9500  101650  180800  313450 1682900
           8w      40  369022  510530    9500  108500  206550  391525 2811300
           13w     65  422240  482837    9500  152700  251200  469900 2811300
           21w    105  553785  694292    9500  198600  383800  649100 5515800
           34w    150  512561  613446    9500  196650  369050  568925 5515800
'''
import pandas as pd
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import os
from Utils.dateutils import generate_dates
from Utils.fileutils import mapcount
from Utils.strutils import getCsvFile

pd.options.display.float_format='{:.0f}'.format
#column_names = ['counter','date','time','open','high','low','close','volume']
column_names = ['date','open','high','low','close','volume']

def csv2df(stock,sdate,edate):
    csvfile = getCsvFile(stock)
    if not os.path.isfile(csvfile):
        print "File not found: " + csvfile
        return None
    try:
#       wcl = wc_line_count(csvfile)
        wcl = mapcount(csvfile)
    except:
        print 'Error count line: '+csvfile
        return None
    if wcl > 750:  # skipped most and roughly include only last 3 years data
        skiprow = wcl - 750
    else:
        skiprow = 0
    data = pd.read_csv(csvfile, header = None, names = column_names, skiprows=skiprow)
    dstart = data['date']>sdate
    dend = data['date']<edate
    hasvol =  data['volume']>0  # non-trading days has 0 volume - skip
    df = data[dstart & dend & hasvol]
#   df.to_csv(getCsvFile2(stock,sdate,edate))
    return df

def csv2dfw(stock,sdate,edate):
    df = csv2df(stock,sdate,edate)
    dfw = []
    dfw.append(df.tail(n=1))
    for i in range(1,35):
        dfw.append(df.tail(n=i*5)); # there are 5 weekdays in a week
        
#   print dfw[2]['volume'].describe()
#   print dfw[2]['volume'].std()

    dfw = pd.DataFrame({'1d' :dfw[0] ['volume'].describe(),
                        '1w' :dfw[1] ['volume'].describe(),
                        '2w' :dfw[2] ['volume'].describe(),
                        '3w' :dfw[3] ['volume'].describe(),
                        '4w' :dfw[4] ['volume'].describe(),
                        '5w' :dfw[5] ['volume'].describe(),
                        '6w' :dfw[6] ['volume'].describe(),
                        '7w' :dfw[7] ['volume'].describe(),
                        '8w' :dfw[8] ['volume'].describe(),
                        '13w':dfw[13]['volume'].describe(),
                        '21w':dfw[21]['volume'].describe(),
                        '34w':dfw[34]['volume'].describe()
                       }
    #, index=['1w','2w','3w','4w','5w','6w','7w','8w','13w','21w','34w']
                      )
    dfw = dfw.T
    #dfw.columns.values[0] = '2015-08-28' #change column name
    dfw = dfw.sort_values(by='count',ascending=True)
    return dfw

def buy_vol_stats(stock,
                  sdate=(date.today() + relativedelta(months=-6)).strftime("%Y-%m-%d"),
                  edate=datetime.today().strftime("%Y-%m-%d")):
    if stock is None or len(stock)==0:
        print "Missing stock name"
        return None
    date_range=generate_dates(sdate,edate)
    sdate2 = datetime.strptime(sdate,'%Y-%m-%d')
    sdate60 = (sdate2+relativedelta(months=-2)).strftime("%Y-%m-%d")
    #print csv2dfw(csvfile,'2015-01-01','2015-09-01')
    #print csv2dfw(csvfile,'2015-01-01',date_range[0])
    #print len(date_range),date_range
    sDict = {}
    for i in range(len(date_range)):
        #print date_range[i], type(date_range[i])
        sDict[date_range[i]] = csv2dfw(stock, sdate60, date_range[i])
    dfVol = pd.concat(sDict)
#   pkfile = csvfile+".pickle"
#   dfVol.to_pickle(pkfile)
    return dfVol

if __name__ == '__main__':
    csv2dfw('GDEX.0078.KL','2015-08-10', '2015-12-31')
    dfv = buy_vol_stats('GDEX.0078.KL','2015-08-10', '2015-12-31')
    dfv = buy_vol_stats('3A.0012.KL')
    # print dfVol.index
    if dfv is not None:
        print dfv['mean'].head()