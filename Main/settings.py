'''
Created on Dec 26, 2016

@author: t.roy
'''

#  Configurations
WORK_DIR = 'A:/Projects/EDS/klse/'
WORK_DIR_MT4 = ""
WORK_DIR_MT4_2 = 'C:/Users/hwase/AppData/Roaming/MetaQuotes/Terminal/9662C61C6715C26397817D3943CECEEC/history/klse'
WORK_DIR_MT4_10 = 'C:/Users/hwase/AppData/Roaming/MetaQuotes/Terminal/DFF6411A75BCA6204637971EAA184B85/history/klse'
WORK_DIR_MT4_100 = 'C:/Users/hwase/AppData/Roaming/MetaQuotes/Terminal/9662C61C6715C26397817D3943CECEEC/history/klse'
WORK_DIR_WIN = 'A:\\Projects\\EDS\\klse\\'
MARKET_SOURCE = 'yahoo'  # or 'google'
MARKET_FILE = 'klse.txt'
SHORTLISTED_FILE = 'klse_shortlisted.txt'
ABS_START = '2007-01-01'
ABS_END = ''
IDMAP = ''
I3PRICEURL = 'https://klse.i3investor.com/servlets/stk/rec/'
HEADERS = {
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
}

# Features toggle
DBG_ALL = False
DBG_ICOM = False
DBG_YAHOO = False
INF_YAHOO = True
RESUME_FILE = True  # False = fresh reload from ABS_START date, True = only download from next date of last record
PRICE_WITHOUT_SPLIT = True  # False - Apply adjusted close by default
