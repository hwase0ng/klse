'''
Created on 5 Jan 2017

@author: 611004565
'''
import Main.settings as S


def isnumberlist(wlist):
    for i in wlist:
        if not isnumber(i):
            return False
    return True

def isnumber(width):
    try:
        width = float(width)
        return True
    except ValueError:
        return False


def getCsvFile(stock):
    csvfile = S.WORK_DIR+S.market_source+'/'+stock+'.csv'
    return csvfile


def getCsvFile2(stock, sdate, edate):
    csvfile = S.WORK_DIR+S.market_source+'/'+stock+'_'+sdate+'_'+edate+'.csv'
    return csvfile


def str2float(s):
    try:
        s = float(s)
    except ValueError:
        pass
    return s


def decompose_stockname(counter):
    try:
        stock_symbol = counter.split('.')
        sname = stock_symbol[0]
        scode = stock_symbol[1]+'.'+stock_symbol[2]
    except ValueError:
        sname = ''
        scode = ''
    finally:
        return sname, scode


if __name__ == '__main__':
    print isnumber("1")
    print isnumber("1.2")
    print isnumber("null")
    pass
