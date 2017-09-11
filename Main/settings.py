'''
Created on Dec 26, 2016

@author: t.roy
'''

#  Configurations
WORK_DIR = 'A:/Projects/EDS/klse/'
WORK_DIR_MT4 = ""
WORK_DIR_MT4_2 = 'C:/Users/hwase/AppData/Roaming/MetaQuotes/Terminal/E4917DDDC31BA9195FE779C754D5D6C5/history/KLSE'
WORK_DIR_MT4_10 = 'C:/Users/hwase/AppData/Roaming/MetaQuotes/Terminal/DFF6411A75BCA6204637971EAA184B85/history/klse'
WORK_DIR_WIN = 'A:\\Projects\\EDS\\klse\\'
MARKET_SOURCE = 'yahoo'  # or 'google'
MARKET_FILE = 'klse.txt'
ABS_START = '2007-01-01'

# Features toggle
DBG_ALL = False
DBG_YAHOO = False
INF_YAHOO = True
RESUME_FILE = False  # False = fresh reload from ABS_START date, True = only download from next date of last record
PRICE_WITHOUT_SPLIT = True  # False - Apply adjusted close by default
