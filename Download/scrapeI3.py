'''
Created on Apr 13, 2018

@author: t.roy
'''

import Main.settings as S
import Utils.dateutils as du

import requests
from BeautifulSoup import BeautifulSoup
import lxml.html
import webbrowser


def connectRecentPrices(stkcode):
    if len(stkcode) != 4 or not stkcode.isdigit():
        return

    global soup
    recentPricesUrl = S.I3PRICEURL + stkcode + ".jsp"
    try:
        page = requests.get(recentPricesUrl, headers=S.HEADERS)
        assert(page.status_code == 200)
        html = page.content
        soup = BeautifulSoup(html)
    except Exception as e:
        print e
    return soup


def scrapeEOD(soup):
    table = soup.find('table', {'class': 'nc'})
    # for each row, there are many rows including no table
    cols = []
    for tr in table.findAll('tr'):
        td = tr.findAll('td')
        # dt, open, price_range, close, change, volume = [x.text.strip() for x in td]
        # print dt, open, price_range, close, change, volume
        col = [x.text.strip() for x in td]
        if len(col) > 0:
            cols.append(col)
    print cols


if __name__ == '__main__':
    soup = connectRecentPrices("5010")
    scrapeEOD(soup)
    pass
