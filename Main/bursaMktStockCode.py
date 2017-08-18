'''
Created on Jul 27, 2017

@author: hwase
'''

import Main.settings as S
import requests
import json
import pandas
#from bs4 import BeautifulSoup

#url_stock = "http://www.bursamarketplace.com/mkt/themarket/stock"
url_prefix = "http://www.bursamarketplace.com/index.php?tpl=stock_ajax&type=listing&pagenum="
url_postfix = "&sfield=name&stype=asc&midcap=0"
page = 1
url_ajax = url_prefix + str(page) + url_postfix
#print url_ajax

response = requests.get(url_ajax)
#soup = BeautifulSoup(response.text, "html.parser")
#print soup.prettify(encoding="utf-8", formatter="minimal")
data = response.json()
#print json.dumps(data, indent=4, sort_keys=False)
totalpage = data['totalpage']
taglist = []
namelist = []

for page in range(1,totalpage+1):
    url_ajax = url_prefix + str(page) + url_postfix
    response = requests.get(url_ajax)
    data = response.json()
    totalrec = len(data['record'])
    print "Page {} of {}: {} records".format(page, totalpage, totalrec)
    for rec in range(0,totalrec):
        cashtag = data['records'][rec]['cashtag']
        name = data['records'][rec]['name']
#       stockcode = data['records'][rec]['stockcode']
        if S.DBG_ALL:
            print "Record {} of {}: {}, {}".format(rec, totalrec, cashtag, name)
        taglist.append(cashtag[1:])
        namelist.append(name)

df = pandas.DataFrame(data={"cashtag":taglist, "name":namelist})
df.to_csv(S.WORK_DIR+"bursa.csv", sep=",", index=False)

if __name__ == '__main__':
    pass