'''
Created on Jul 16, 2016

@author: t.roy
'''

import Main.settings as S

from datetime import datetime
import datetime as dt
from google import GoogleQuote
from yahoo import YahooQuote
from Utils.dateutils import getStartDate

import sys,csv,os.path

ABS_START = '1990-01-01'
# Specify Date Range
end = datetime.today().strftime("%Y-%m-%d")
#end = '2006-01-01'
#http://ichart.finance.yahoo.com/table.csv?s=0012.KL&a=0&b=01&c=1995&d=0&e=01&f=2006
#http://ichart.finance.yahoo.com/table.csv?s=0012.KL&a=0&b=01&c=1995&d=6&e=17&f=2016
gDict = {}
errlist = []
q=''

def eod2csv(stock_name,stock_code):
    #print stock_name,stock_symbol,stock_code
    if stock_name is None or stock_code is None or len(stock_name)==0 or len(stock_code)==0:
        return None,None
    sfile = S.WORK_DIR+S.market_source+'/'+stock_name+'.'+stock_code+'.csv'
    stmp =sfile+'tmp'
    OK = True
    try:
        start = getStartDate(sfile)
        #print "\t"+start+"..."+sfile
        if len(start)==0:
            start=ABS_START
        elif len(start)>10:
            errstr = stock_name +":" + start
            print '  ERR1:', errstr
            OK = False
            errlist.append([errstr])
            start = ""
        elif start>=end:
            #print "\t"+stock_name + " skipped"
            start=""
        #print "\tDates="+start+","+end
        if len(start)>0:
            if S.market_source=='google':
                q = GoogleQuote(stock_name,start,end)
            else:
                q = YahooQuote(stock_code,start,end)
            gDict[stock_name] = q.url
            q.write_csv(stmp)
        else:
            OK = False
    except Exception, e:
        print '  ERR2:', stock_name +":"+str(e)
        #print q.getCsvErr()
        OK = False
        errlist.append([stock_name])

    if OK:
        if start==ABS_START:
            f = open(sfile,"w")
        else:
            f = open(sfile,"a+")
        ftmp = open(stmp,"r")
        f.write(ftmp.read())
        f.close()
        ftmp.close()
        
if __name__ == '__main__':
    print "Downloading from "+S.market_source+" with " + S.WORK_DIR+S.market_file
    with open(S.WORK_DIR+S.market_file, 'r') as f:
        reader = csv.reader(f)
        slist = list(reader)
        #print slist[:3]
        for counter in slist[:]:
            #print "\t"+counter
            if len(counter) <= 0:
                print "\t"+"Wrong len=" + len(counter)
                continue
            stock_symbol = counter[0].split('.')
            sname = stock_symbol[0]
            scode = counter[1]
            eod2csv(sname,scode)

    print "Done."
    '''
    if len(errlist)>0:
        print "Error counters:"
        for i in errlist:
            print '\t',i
    '''