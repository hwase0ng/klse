'''
Created on Jul 16, 2016

@author: t.roy
'''
from __future__ import with_statement

import Main.settings as S

from Main.settings import RESUME_FILE
from datetime import datetime
from Download.scrapeInvestingCom import InvestingQuote
from Download.google import GoogleQuote
from Download.yahoo import YahooQuote, getYahooCookie
from Utils.dateutils import getLastDate, getTomorrow
from Utils.fileutils import concat2quotes, cd, getSystemIP

import json
import sys
import csv
import os.path
import requests
import re
from Download import scrapeInvestingCom

url = []


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
                print "\t", counter
            if len(counter) <= 0:
                print "\t" + "Wrong len=", len(counter)
                continue
            stock_symbol = counter[0].split('.')
            stock_name = stock_symbol[0]
            if len(counter) < 2:
                print "ERR:Counter too short:", stock_symbol, stock_name, counter
                continue
            stock_code = counter[1]
            if S.DBG_ALL:
                print stock_name, stock_symbol, stock_code
            sfile = (S.WORK_DIR + S.MARKET_SOURCE + '/' + stock_name + '.' +
                     stock_code + '.csv')
            count = 0
            while count < 3:
                count = count + 1
                if (S.MARKET_SOURCE == 'yahoo' and cookie != '') or S.MARKET_SOURCE != 'yahoo':
                    if len(S.ABS_END) == 0:
                        rtncd = download_from_source(cookie, crumb, sfile, stock_name, stock_code)
                    else:
                        rtncd = download_from_source(cookie, crumb, sfile, stock_name, stock_code, S.ABS_END)
                else:
                    rtncd = 401
                if rtncd > 0 and S.MARKET_SOURCE == 'yahoo':  # 400, Bad Request, 401 = Unauthorized
                    if S.DBG_YAHOO:
                        print "DBG:new cookie required, st_code =", rtncd
                    # Can get ConnectionError while getting cookies
                    cookie_count = 0
                    while cookie_count < 5:
                        cookie, crumb = getYahooCookie(url[cookie_count])
                        if cookie != '':
                            cookie_count = 99
                        cookie_count = cookie_count + 1
                else:
                    count = 99


def download_from_source(cookie, crumb, fname, stock_name, stock_code, end=getTomorrow("%Y-%m-%d")):
    #  gDict = {}
    errlist = []
    q = ''
    rtn_code = 0

    stmp = fname + 'tmp'
    try:
        if S.RESUME_FILE:
            lastdt = getLastDate(fname)
            if S.INF_YAHOO:
                print '{0}: lastdt={1}, End={2}'.format(stock_name, lastdt, end)
        else:
            lastdt = S.ABS_START
        if S.DBG_ALL:
            print "\t" + lastdt + "..." + fname
        if len(lastdt) == 0:
            lastdt = S.ABS_START
        elif len(lastdt) > 10:
            errstr = stock_name + ":" + lastdt
            print '  ERR1:', errstr
            rtn_code = -1
            errlist.append([errstr])
            lastdt = ""
        elif lastdt >= end:
            if S.DBG_ALL:
                print "\t" + stock_name + " skipped"
            lastdt = ""
        if S.DBG_ALL:
            print "\tDates=" + lastdt + "," + end
        if len(lastdt) > 0:
            if S.MARKET_SOURCE == 'investing.com' or stock_code.startswith('020'):
                if len(S.IDMAP) <= 0:
                    S.IDMAP = scrapeInvestingCom.loadIdMap()
                if len(S.ABS_END) == 0:
                    q = InvestingQuote(S.IDMAP, stock_name, lastdt)
                else:
                    q = InvestingQuote(S.IDMAP, stock_name, lastdt, end)
            elif S.MARKET_SOURCE == 'yahoo':
                q = YahooQuote(cookie, crumb, stock_name, stock_code, lastdt, end)
            elif S.MARKET_SOURCE == 'google':
                q = GoogleQuote(stock_name, stock_code, lastdt, end)
            else:
                print "Invalid market source:" + S.MARKET_SOURCE
                sys.exit(-1)
            if len(q.getCsvErr()) > 0:
                if S.MARKET_SOURCE == 'yahoo':
                    st_code, st_reason = q.getCsvErr().split(":")
                    rtn_code = int(st_code)
                    if S.INF_YAHOO:
                        print "INF:", st_code, st_reason, ":", stock_name
                else:
                    print q.getCsvErr()
                    rtn_code = -1
            else:
                #  gDict[stock_name] = q.url
                q.write_csv(stmp)
        else:
            rtn_code = -2
    except Exception, e:
        if S.MARKET_SOURCE == 'investing.com':
            print '  ERR2:', stock_code + ":" + stock_name
        else:
            print '  ERR2:', stock_code + ":" + stock_name + ":" + str(e)
        if S.DBG_ALL:
            print q.getCsvErr()
        rtn_code = -3
        errlist.append([stock_name])

    if rtn_code == 0:
        if lastdt == S.ABS_START:
            f = open(fname, "wb")
        else:
            f = open(fname, "ab")
        ftmp = open(stmp, "r")
        f.write(ftmp.read())
        f.close()
        ftmp.close()
    return rtn_code
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


def loadSetting(c):
    S.WORK_DIR = c["main"]["WORK_DIR"]
    S.WORK_DIR_MT4 = c["main"]["WORK_DIR_MT4"]
    S.MARKET_SOURCE = c["main"]["MARKET_SOURCE"]
    S.MARKET_FILE = c["main"]["MARKET_FILE"]
    S.SHORTLISTED_FILE = c["main"]["SHORTLISTED_FILE"]
    S.ABS_START = c["main"]["ABS_START"]
    S.RESUME_FILE = c["toggle"]["RESUME_FILE"]
    S.PRICE_WITHOUT_SPLIT = c["toggle"]["PRICE_WITHOUT_SPLIT"]
    S.INF_YAHOO = c["toggle"]["INF_YAHOO"]
    S.DBG_YAHOO = c["toggle"]["DBG_YAHOO"]
    S.DBG_ALL = c["toggle"]["DBG_ALL"]
    if S.DBG_ALL:
        print S.WORK_DIR_MT4


def loadCfg():
    try:
        with open('config.json') as json_data_file:
            cfg = json.load(json_data_file)
            loadSetting(cfg)
            if S.DBG_ALL:
                print "WORK DIR = ", cfg["main"]["WORK_DIR"]
                print "MARKET FILE = ", cfg["main"]["MARKET_FILE"]
                with open(cfg["main"]["WORK_DIR"] + cfg["main"]["MARKET_FILE"], 'r') as f:
                    reader = csv.reader(f)
                    slist = list(reader)
                    print slist[:3]
            return cfg
    except EnvironmentError:
        print "Missing config.json file"
        sys.exit(1)


if __name__ == '__main__':
    cfg = loadCfg()

    market_file = S.MARKET_FILE
    stocks = ''
#   stocks = 'DAIBOCI.8125.KL.csv,HOHUP.5169.KL.csv,IVORY.5175.KL.csv,N2N.0108.KL.csv,PMBTECH.7172.KL.csv'
#   stocks = 'NAKA.7002.KL.csv,GNB.0045.KL.csv,XIANLNG.7121.KL.csv,KPOWER.7130.KL.csv,SKBSHUT.7115.KL.csv,ICAP.5108.KL.csv,SERBADK.5279.KL.csv,MALPAC.4936.KL.csv,MESB.7234.KL.csv,UMWOG.5243.KL.csv,PLABS.0171.KL.csv,BIPORT.5032.KL.csv,TROP.5401.KL.csv,DELEUM.5132.KL.csv,EUPE.6815.KL.csv,TALIWRK.8524.KL.csv,MCT.5182.KL.csv,CNI.5104.KL.csv,AMTEL.7031.KL.csv,TURBO.5167.KL.csv,RVIEW.2542.KL.csv,PINEAPP.0006.KL.csv,AMTEK.7051.KL.csv,AFUJIYA.5198.KL.csv,Y&G.7003.KL.csv,MILUX.7935.KL.csv,QUALITY.7544.KL.csv,SJC.9431.KL.csv,TGL.9369.KL.csv,ASIABRN.7722.KL.csv,TAHPS.2305.KL.csv,NPC.5047.KL.csv,CFM.8044.KL.csv,HUBLINE.7013.KL.csv,COMPUGT.5037.KL.csv,YEELEE.5584.KL.csv,HUAAN.2739.KL.csv,TEXCYCL.0089.KL.csv,EAH.0154.KL.csv,PCHEM.5183.KL.csv,PICORP.7201.KL.csv,HARTA.5168.KL.csv,LAYHONG.9385.KL.csv,GBH.3611.KL.csv,EDGENTA.1368.KL.csv,MISC.3816.KL.csv,TDEX.0132.KL.csv,DOMINAN.7169.KL.csv,GOB.1147.KL.csv,MCLEAN.0167.KL.csv,BDB.6173.KL.csv,UMCCA.2593.KL.csv,BJLAND.4219.KL.csv,ASB.1481.KL.csv,DPS.7198.KL.csv,KIMHIN.5371.KL.csv,ECM.2143.KL.csv,WANGZNG.7203.KL.csv,OMESTI.9008.KL.csv,FARLIM.6041.KL.csv,RALCO.7498.KL.csv,JASKITA.8648.KL.csv,MBMR.5983.KL.csv,TOYOINK.7173.KL.csv,LCHEONG.7943.KL.csv,WIDETEC.7692.KL.csv'
#   stocks = 'FTFBM100.0200.KL.csv,FTFBMKLCI.0201.KL.csv,FTFBMMES.0202.KL.csv,FTFBMSCAP.0203.KL.csv'
#   stocks = 'AASIA.7054.KL.csv'

    S.RESUME_FILE = False
    S.DBG_YAHOO = False
    S.DBG_ALL = False
    S.MARKET_SOURCE = 'investing.com'
    if S.MARKET_SOURCE == 'yahoo':
        cookie, crumb = getYahooCookie(url[0])
        url.append('https://uk.finance.yahoo.com/quote/AAPL/history')
        url.append('https://uk.finance.yahoo.com/quote/GOOG/history')
        url.append('https://finance.yahoo.com/quote/APPL/history')
        url.append('https://finance.yahoo.com/quote/GOOG/history')
        url.append('https://finance.yahoo.com/quote/AMZN/history')
    else:
        cookie = ''
        crumb = ''
#   S.ABS_START = '2018-01-01'
#   S.ABS_END = '2018-01-31'
    if len(stocks) > 0:
        #  download only selected counters
        if "," in stocks:
            stocklist = stocks.split(",")
        else:
            stocklist = [stocks]
        for stock in stocklist:
            sdata = stock.split(".")
            stock_name = sdata[0]
            stock_code = sdata[1] + "." + sdata[2]
            print stock_name, stock_code
            sfile = (S.WORK_DIR + S.MARKET_SOURCE + '/' + stock_name + '.' +
                     stock_code + '.csv')
            if len(S.ABS_END) == 0:
                download_from_source(cookie, crumb, sfile, stock_name, stock_code)
            else:
                download_from_source(cookie, crumb, sfile, stock_name, stock_code, S.ABS_END)
    else:
        #  download all counters found in the market file
        downloadMarket(market_file, cookie, crumb)

    # can run from different PCs (identified by different IPs)
    # different MT4 will have different paths
    ip = getSystemIP()
    if S.DBG_ALL:
        print ip
    if S.WORK_DIR_MT4 == '':
        if ip.endswith(".2"):
            S.WORK_DIR_MT4 = S.WORK_DIR_MT4_2
        elif ip.endswith(".10"):
            S.WORK_DIR_MT4 = S.WORK_DIR_MT4_10
        else:
            S.WORK_DIR_MT4 = S.WORK_DIR_MT4_100
    concat2quotes(S.WORK_DIR + S.MARKET_SOURCE, S.WORK_DIR_MT4)
    with cd(S.WORK_DIR_MT4):
        os.system("c:/perl/bin/perl mt4dw.pl")
    print "Done."
    pass
