# Copyright (c) 2011, Mark Chenoweth
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted 
# provided that the following conditions are met:
#
# - Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#
# - Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following 
#   disclaimer in the documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, 
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS 
# OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, 
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF 
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import Main.settings as S
import calendar
from datetime import datetime, date
import urllib
import requests
import re
from Main.settings import DBG_YAHOO
from Utils.strutils import isnumberlist


def getYahooCookie():
    # search with regular expressions
    # "CrumbStore":\{"crumb":"(?<crumb>[^"]+)"\}
    url = 'https://uk.finance.yahoo.com/quote/AAPL/history' # url for a ticker symbol, with a download link
    r = requests.get(url)  # download page
    txt = r.text  # extract html
    cookie = r.cookies['B']  # the cooke we're looking for is named 'B'
    if S.DBG_ALL or S.DBG_YAHOO:
        print 'DBG:getYahooCookie: ', cookie

    # Now we need to extract the token from html.
    # the string we need looks like this: "CrumbStore":{"crumb":"lQHxbbYOBCq"}
    # regular expressions will do the trick!

    pattern = re.compile('.*"CrumbStore":\{"crumb":"(?P<crumb>[^"]+)"\}')

    for line in txt.splitlines():
        m = pattern.match(line)
        if m is not None:
            crumb = m.groupdict()['crumb']

    if S.DBG_ALL or S.DBG_YAHOO:
        print 'DBG:getYahooCrumb=', crumb
    return cookie, crumb


class Quote(object):
  
    DATE_FMT = '%Y-%m-%d'
    TIME_FMT = '%H:%M:%S'
   
    def __init__(self):
        self.url = ''
        self.symbol = ''
#       self.date,self.time,self.open_,self.high,self.low,self.close,self.volume = ([] for _ in range(7))
        self.date,self.open_,self.high,self.low,self.close,self.volume = ([] for _ in range(6))
        self.csverr = ''
#       self.cookie,self.crumb = self.getYahooCookie()

    def getCsvErr(self):
        return self.csverr

    def append(self, dt, open_, high, low, close, volume):
        self.date.append(dt.date())
#       self.time.append(dt.time())
        self.open_.append(float(open_))
        self.high.append(float(high))
        self.low.append(float(low))
        self.close.append(float(close))
        self.volume.append(int(volume))

    def to_csv(self):
#       return ''.join(["{0},{1},{2},{3:.2f},{4:.2f},{5:.2f},{6:.2f},{7}\n".format(self.symbol,
        return ''.join(["{0},{1:.2f},{2:.2f},{3:.2f},{4:.2f},{5}\n".format(
                self.date[bar].strftime('%Y-%m-%d'),
#               self.time[bar].strftime('%H:%M:%S'),
                self.open_[bar], self.high[bar], self.low[bar],
                self.close[bar], self.volume[bar])
                for bar in xrange(len(self.close))])

    def write_csv(self, filename):
        with open(filename, 'w') as f:
            f.write(self.to_csv())

    def read_csv(self, filename):
#       self.symbol = ''
#       self.date,self.time,self.open_,self.high,self.low,self.close,self.volume = ([] for _ in range(7))
        self.date, self.open_, self.high, self.low, self.close, self.volume = ([] for _ in range(6))
        for line in open(filename, 'r'):
#           symbol,ds,ts,open_,high,low,close,volume = line.rstrip().split(',')
            ds, open_, high, low, close, volume = line.rstrip().split(',')
#       self.symbol = symbol
#       dt = datetime.strptime(ds+' '+ts,self.DATE_FMT+' '+self.TIME_FMT)
        dt = datetime.strptime(ds, self.DATE_FMT)
        self.append(dt, open_, high, low, close, volume)
        return True

    def formUrl_old(self, symbol, start_date, end_date):
        start_year, start_month, start_day = start_date.split('-')
        start_month = str(int(start_month)-1)
        end_year, end_month, end_day = end_date.split('-')
        end_month = str(int(end_month)-1)
        url_string = "http://ichart.finance.yahoo.com/table.csv?s={0}".format(symbol)
        url_string += "&a={0}&b={1}&c={2}".format(start_month, start_day, start_year)
        url_string += "&d={0}&e={1}&f={2}".format(end_month, end_day, end_year)
        return url_string

    def formUrl(self, crumb, symbol, start_date, end_date):
        start_year, start_month, start_day = start_date.split('-')
#       start_month = str(int(start_month)-1)
        end_year, end_month, end_day = end_date.split('-')
#       end_month = str(int(end_month)-1)
        sDate = datetime(int(start_year), int(start_month), int(start_day),0,0)
        eDate = datetime(int(end_year), int(end_month), int(end_day),0,0)
#       datetime(*sDate).timestamp() # convert to seconds since epoch
        
        # prepare input data as a tuple
#       data = (int(datetime(*sDate).timestamp()),
#               int(datetime(*eDate).timestamp()),
#               crumb)
        data = (calendar.timegm((sDate.timetuple())),
                calendar.timegm((eDate.timetuple())),
                crumb)
        url_string = "https://query1.finance.yahoo.com/v7/finance/download/" + symbol
        url_string+= "?period1={0}&period2={1}&interval=1d&events=history&crumb={2}".format(*data)

        if S.DBG_ALL:
            print("DBG:formUrl:"+url_string)

        return url_string;

    def __repr__(self):
        return self.to_csv()


class YahooQuote(Quote):
    ''' Daily quotes from Yahoo. Date format='yyyy-mm-dd' '''
    def __init__(self, cookie, crumb, symbol, start_date,
                 end_date=date.today().isoformat()):
        super(YahooQuote, self).__init__()
        self.symbol = symbol.upper()
        if S.DBG_ALL or S.DBG_YAHOO:
            print "DBG:YahooQuote:1:", symbol, self.symbol, start_date
#       self.url = self.formUrl_old(symbol,start_date,end_date)
        self.url = self.formUrl(crumb, symbol, start_date, end_date)
        if S.DBG_ALL or S.DBG_YAHOO:
            print "DBG:YahooQuote:2:", self.url
#       csv = urllib.urlopen(self.url).readlines()
#       if not csv[0].startswith("Date,Open,"):
        resUrl = requests.get(self.url, cookies={'B': cookie})
        if resUrl.status_code != 200:
            self.csverr = str(resUrl.status_code) + ":" + resUrl.reason
            print "ERR:", symbol, ":", self.url
            print "ERR:" + self.csverr
        else:
            self.csverr = ''
            '''
            csv = resUrl.text
            csv.reverse()
            for bar in xrange(0,len(csv)-1):
                ds,open_,high,low,close,volume,adjc =
                    csv[bar].rstrip().split(',')
            '''
            iterator = resUrl.iter_lines()
            skipline = next(iterator)
            if S.DBG_ALL:
                print "SKIP:YohooQuote:", skipline
            for csv in iterator:
                if S.DBG_ALL:
                    print "DBG", csv
                ds, open_, high, low, close, adjc, volume = (
                    csv.rstrip().split(','))
                if S.DBG_YAHOO:
                    print "DBG:", ds, open_, high, low, close, adjc, volume
                    print "DBG:", type(ds), type(open_), type(high), type(low),
                    type(close), type(adjc), type(volume)
                if not isnumberlist([high, low, close, adjc]):
                    if S.DBG_YAHOO:
                        print "SKIP:", ds, open_, high, low, close, adjc
                    continue
                open_, high, low, close, adjc = [
                    float(x) for x in [open_, high, low, close, adjc]]
                if close != adjc:
                    factor = adjc/close
                    open_, high, low, close = [
                        x*factor for x in [open_, high, low, close]]
                dt = datetime.strptime(ds, '%Y-%m-%d')
                self.append(dt, open_, high, low, close, volume)
            if S.DBG_ALL:
                print "YahooQuote:End"


if __name__ == '__main__':
    stock_code = '5131.KL'
    cookie, crumb = getYahooCookie()
    q = YahooQuote(cookie, crumb, stock_code, S.ABS_START)
    print q                                          # print it out
#   q = YahooQuote('aapl','2011-01-01')              # download year to date Apple data
#   print q                                          # print it out
#   q = YahooQuote('orcl','2011-02-01','2011-02-28') # download Oracle data for February 2011
#   q.write_csv('orcl.csv')                          # save it to disk
#   q = Quote()                                      # create a generic quote object
#   q.read_csv('orcl.csv')                           # populate it with our previously saved data
#   print q                                          # print it out