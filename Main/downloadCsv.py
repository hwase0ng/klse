'''
Created on Jul 16, 2016

@author: t.roy
'''

import Main.settings as S

from datetime import datetime
from Download.google import GoogleQuote
from Download.yahoo import YahooQuote, getYahooCookie
from Utils.dateutils import getStartDate, getTomorrow
from Utils.fileutils import concat2quotes, cd

import sys
import csv
import os.path
import requests
import re


def get_start_end_obsoleted():
    lastcsv = S.WORK_DIR + 'lastcsv.txt'
    # Specify Date Range
    # end = datetime.today().strftime("%Y-%m-%d")
    end = getTomorrow("%Y-%m-%d")
    # end = '2006-01-01'
    if os.path.exists(lastcsv):
        with open(lastcsv, 'r') as f:
            start = f.read().replace('\n', '')
        f.close()
    else:
        start = S.ABS_START
    # http://ichart.finance.yahoo.com/table.csv?s=0012.KL&a=0&b=01&c=1995&d=0&e=01&f=2006
    # http://ichart.finance.yahoo.com/table.csv?s=0012.KL&a=0&b=01&c=1995&d=6&e=17&f=2016
    '''
    if start==end:
        print "CSV for ",start, " is already downloaded."
        sys.exit(1)
    elif start > end:
        print "Invalid start date ", start, "is > ", end
        sys.exit(2)
    '''


def downloadMarket(mkt, cookie, crumb):
    print "Downloading from " + S.MARKET_SOURCE + " with " + S.WORK_DIR + mkt
    with open(S.WORK_DIR + S.MARKET_FILE, 'r') as f:
        reader = csv.reader(f)
        slist = list(reader)
        if S.DBG_ALL:
            print slist[:3]
        for counter in slist[:]:
            if S.DBG_ALL:
                print "\t" + counter
            if len(counter) <= 0:
                print "\t" + "Wrong len=" + len(counter)
                continue
            stock_symbol = counter[0].split('.')
            stock_name = stock_symbol[0]
            stock_code = counter[1]
            if S.DBG_ALL:
                print stock_name, stock_symbol, stock_code
            sfile = (S.WORK_DIR + S.MARKET_SOURCE + '/' + stock_name + '.' +
                     stock_code + '.csv')
            download_from_source(cookie, crumb, sfile, stock_name, stock_code)


def download_from_source(cookie, crumb, fname, stock_name, stock_code, end=getTomorrow("%Y-%m-%d")):
    #  gDict = {}
    errlist = []
    q = ''

    stmp = fname + 'tmp'
    OK = True
    try:
        if S.RESUME_FILE:
            start = getStartDate(fname)
            if S.INF_YAHOO:
                print '{0}: Start={1}, End={2}'.format(stock_name, start, end)
        else:
            start = S.ABS_START
        if S.DBG_ALL:
            print "\t" + start + "..." + fname
        if len(start) == 0:
            start = S.ABS_START
        elif len(start) > 10:
            errstr = stock_name + ":" + start
            print '  ERR1:', errstr
            OK = False
            errlist.append([errstr])
            start = ""
        elif start >= end:
            if S.DBG_ALL:
                print "\t" + stock_name + " skipped"
            start = ""
        if S.DBG_ALL:
            print "\tDates=" + start + "," + end
        if len(start) > 0:
            if S.MARKET_SOURCE == 'google':
                q = GoogleQuote(stock_name, start, end)
            else:
                q = YahooQuote(cookie, crumb, stock_name, stock_code, start, end)
            if len(q.getCsvErr()) > 0:
                OK = False
                st_code, st_reason = q.getCsvErr().split(":")
                if S.INF_YAHOO:
                    print "INF:", st_code, st_reason, ":", stock_name
                if int(st_code) == 401:  # Unauthorized
                    if S.DBG_YAHOO:
                        print "DBG:new cookie required, st_code =", st_code, st_reason
                    cookie, crumb = getYahooCookie()
            else:
                #  gDict[stock_name] = q.url
                q.write_csv(stmp)
        else:
            OK = False
    except Exception, e:
        print '  ERR2:', stock_code + ":" + stock_name + ":" + str(e)
        if S.DBG_ALL:
            print q.getCsvErr()
        OK = False
        errlist.append([stock_name])

    if OK:
        if start == S.ABS_START:
            f = open(fname, "wb")
        else:
            f = open(fname, "ab")
        ftmp = open(stmp, "r")
        f.write(ftmp.read())
        f.close()
        ftmp.close()
    '''
    with open(lastcsv, 'w+') as f:
    f.write(end)
    f.close()
    '''

    '''
    if len(errlist)>0:
    print "Error counters:"
    for i in errlist:
        print '\t',i
    '''


if __name__ == '__main__':
    cookie, crumb = getYahooCookie()
    market_file = S.MARKET_FILE
    stock_code = ''
    stock_name = ''
    if len(stock_code) > 0:
        #  download only selected counter
        sfile = (S.WORK_DIR + S.MARKET_SOURCE + '/' + stock_name + '.' +
                 stock_code + '.csv')
        download_from_source(cookie, crumb, sfile, stock_name, stock_code)
    else:
        #  download all counters found in the market file
        downloadMarket(market_file, cookie, crumb)
        concat2quotes(S.WORK_DIR + S.MARKET_SOURCE)
        with cd(S.WORK_DIR_MT4):
            os.system("perl mt4dw.pl")
    print "Done."
    pass
