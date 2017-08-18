'''
Created on Jul 16, 2016

@author: t.roy
'''

from pandas_datareader import DataReader as web
from datetime import datetime
from dateutil.relativedelta import relativedelta

import csv
import os.path

def downloadPandaCsv(market_source,sname,scode):
    #print '\t',market_source,sname,scode
    findata = ''
    try:
        if market_source=='google':
            symbol = 'KLSE:'+sname
        else:
            symbol = scode
        findata = web("%s" % symbol, market_source, start, end)
        findata.to_csv(dir+market_source+'/'+'%s.csv' % sname)
    except:
        print 'ERR:', symbol
        errlist.append([market_source,symbol,start,end,findata])

dir = 'D:/Users/Roy/OneDrive/Documents/MyFiles/Projects/EDS/klse/'
lastcsv = dir+'lastcsv.txt'
# Specify Date Range
#end = datetime.today()
end = datetime.strptime('Jan 1 2005', '%b %d %Y') 
if os.path.exists(lastcsv):
    with open(lastcsv, 'r') as f:
		#datetime.datetime.now() - datetime.timedelta(days=3*365)
		#start = datetime(2012, 1, 1)
		#s1 = datetime.now() - relativedelta(years=5)
		#s2 = s1.strftime("%Y-%m-%d")
        s2 = f.read().replace('\n','')
    f.close()
else:
    s2 = '1995-01-01'

start = datetime(int(s2[0:4]), int(s2[5:7]), int(s2[8:10]))

errlist = []

with open(dir+'klse2.txt', 'r') as f:
    reader = csv.reader(f)
    slist = list(reader)
    #print slist[:3]
    for counter in slist[:]:
        #print counter
        if len(counter) <= 0:
            continue
        stock_symbol = counter[0].split('.')
        stock_code = counter[1]
        stock_name = stock_symbol[0]
        #print '\t',stock_name,stock_code,stock_symbol
        downloadPandaCsv('yahoo',stock_name,stock_code)
        #downloadPandaCsv('google',stock_name,stock_code)
        
with open(lastcsv,'w') as f:
    e2 = end.strftime("%Y-%m-%d")
    f.write(e2)
f.close()

for i in errlist:
    print i