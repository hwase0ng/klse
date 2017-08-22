'''
Created on Jul 30, 2017

@author: hwase
'''
import Main.settings as S
import requests
from Utils import dateutils
from Utils import fileutils

url_com = "http://www.bursamarketplace.com/"
url_prefix = url_com + "index.php?tpl=financial_export_excel&&ric="
cashtag = ""
url_fin = "&fin="
# INC - Income Statement, BAL - Balance Sheet, CAS - Cash Flow Statement
fintype = ["INC", "BAL", "CAS"]
fintypename = ["INCOMESTATEMENT", "BALANCESHEET", "CASHFLOW"]
url_period = "&per="
pertype = ["1", "2"]  # 1 = Annual, 2 = Quarterly
pertypename = ["ANNUAL", "QUARTERLY"]
url_mkt = "&mkt=stock"


def downloadBursa(cashtag):
    #   for i in range(0,len(df)):
    for i in [0, 1, 2]:
        print "Downloading {}->{}".format(cashtag, fintype[i])
        url = (url_prefix + cashtag + url_fin + fintype[i]
               + url_period + pertype[1] + url_mkt)
        fname = (S.WORK_DIR + 'bursa/' + cashtag + '_' + fintypename[i] + '_'
                 + pertypename[1] + '_'
                 + dateutils.getToday() + ".xls")
        if S.DBG_ALL:
            print '\tURL='+url
            print "\tFile="+fname
        response = requests.get(url)
        with open(fname+".xls", "wb") as code:
            code.write(response.content)
        # fileutils.xls_to_xlsx(fname)


if __name__ == '__main__':
    S.DBG_ALL = True
    fileutils.xls_to_xlsx("d:/tmp/test.xls")
#   downloadBursa('KYMH')
    pass
