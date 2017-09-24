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
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
# OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from Utils.dateutils import getToday, getTomorrow, getYesterday, getNextDay
import urllib
import time
from datetime import datetime, date
import Main.settings as S


class Quote(object):

    DATE_FMT = '%Y-%m-%d'
    TIME_FMT = '%H:%M:%S'

    def __init__(self, lastdt):
        self.url = ''
        self.symbol = ''
        self.sname = ''
#       self.date,self.time,self.open_,self.high,self.low,self.close,self.volume = ([] for _ in range(7))
        self.date, self.open_, self.high, self.low, self.close, self.volume = (
            [] for _ in range(6))
        self.csverr = ''
        self.lastdate = lastdt
        self.lastcsv = ''

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
        # return ''.join(["{0},{1},{2},{3:.2f},{4:.2f},{5:.2f},{6:.2f},{7}\n".format(self.symbol,
        return ''.join(["{0},{1},{2:.4f},{3:.4f},{4:.4f},{5:.4f},{6}\n".format(
            self.sname,
            self.date[bar].strftime('%Y-%m-%d'),  # self.time[bar].strftime('%H:%M:%S'),
            self.open_[bar], self.high[bar], self.low[bar],
            self.close[bar], self.volume[bar])
            for bar in xrange(len(self.close))])

    def write_csv(self, filename):
        with open(filename, 'w') as f:
            f.write(self.to_csv())

    def read_csv(self, filename):
        # self.symbol = ''
        #        self.date,self.time,self.open_,self.high,self.low,self.close,self.volume = ([] for _ in range(7))
        self.sname, self.date, self.open_, self.high, self.low, self.close, self.volume = ([] for _ in range(7))
        for line in open(filename, 'r'):
            #symbol, ds, ts, open_, high, low, close, volume = line.rstrip().split(',')
            sname, ds, open_, high, low, close, volume = line.rstrip().split(',')
#       self.symbol = symbol
#       dt = datetime.strptime(ds+' '+ts,self.DATE_FMT+' '+self.TIME_FMT)
        dt = datetime.strptime(ds, self.DATE_FMT)
        self.append(dt, open_, high, low, close, volume)
        return True

    def __repr__(self):
        return self.to_csv()


class GoogleQuote(Quote):
    ''' Daily quotes from Google. Date format='yyyy-mm-dd' '''
    def __init__(self, sname, symbol, last_date, end_date=date.today().isoformat()):
        super(GoogleQuote, self).__init__(last_date)
        self.sname = sname.upper()
        self.symbol = symbol.upper()
        if S.DBG_ALL:
            print "DBG:1:", sname, symbol, self.symbol, last_date
        if last_date == getToday("%Y-%m-%d"):
            #  Will get 400 Bad Request
            if S.DBG_ALL:
                print "DBG:Skipped downloaded", last_date
            return None
        start_date = getNextDay(last_date)
        start = date(int(start_date[0:4]), int(start_date[5:7]), int(start_date[8:10]))
        end = date(int(end_date[0:4]), int(end_date[5:7]), int(end_date[8:10]))
        if S.DBG_ALL:
            print "DBG:2:", start, end
        url_string = "http://www.google.com/finance/historical?q={0}".format(self.sname)
        url_string += "&startdate={0}&enddate={1}&output=csv".format(
            start.strftime('%b %d, %Y'), end.strftime('%b %d, %Y'))
        if S.DBG_ALL:
            print "DBG:4:", url_string
        self.url = url_string
        csv = urllib.urlopen(url_string).readlines()
        csv.reverse()
        for bar in xrange(0, len(csv) - 1):
            if S.DBG_ALL:
                print "DBG:5:", bar
            ds, open_, high, low, close, volume = csv[bar].rstrip().split(',')
            ds = datetime.strptime(ds, "%d-%b-%y")
            ds = ds.strftime("%Y-%m-%d")
            if S.DBG_ALL:
                print "DBG:6:", ds, open_, high, low, volume
            #  Start of data validation
            if float(volume) <= 0:
                if S.DBG_ALL:
                    print 'DBG:Skipped 0 volume as a result of non-trading day:', ds
                continue
            if ds < start_date:
                if S.DBG_ALL:
                    print "DBG:Skipped older date:", ds
                continue
            if ds > getToday("%Y-%m-%d"):
                if S.DBG_ALL:
                    print "DBG:Skipped future dividends:", ds
                continue
            if ds == self.lastdate:
                if S.INF_YAHOO:
                    print "INF:Skipped duplicated date:", ds
                    print '\tcsv:', csv
                    print '\tlst:', self.lastcsv
                continue
            self.lastdate = ds
            self.lastcsv = csv
            open_, high, low, close = [float(x) for x in [open_, high, low, close]]
            #  dt = datetime.strptime(ds, '%d-%b-%y')
            dt = datetime.strptime(ds, '%Y-%m-%d')
            self.append(dt, open_, high, low, close, volume)
