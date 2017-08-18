'''
Created on 5 Jan 2017

@author: 611004565
'''
import Main.settings as S

def getCsvFile(stock):
    csvfile = S.work_dir+S.market_source+'/'+stock+'.csv'
    return csvfile
def getCsvFile2(stock,sdate,edate):
    csvfile = S.work_dir+S.market_source+'/'+stock+'_'+sdate+'_'+edate+'.csv'
    return csvfile

def str2float(s):
    try:
        s=float(s)
    except ValueError:
        pass    
    return s

def decompose_stockname(counter):
    try:
		stock_symbol = counter.split('.')
		sname = stock_symbol[0]
		scode = stock_symbol[1]+'.'+stock_symbol[2]
    except:
        sname = ''
        scode = ''
    finally:
        return sname,scode

if __name__ == '__main__':
    pass