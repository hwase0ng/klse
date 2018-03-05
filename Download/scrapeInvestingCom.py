import Main.settings as S
import Utils.dateutils as du
import requests
import sys
import pandas as pd
import numpy as np
import datetime


class Quote(object):
    """An object that holds price data for a particular commodity,
    across a given date range.
    """
    BASE_URL = "https://www.investing.com/instruments/HistoricalDataAjax"

    def __init__(self, name, start, end, idmap):
        self.csverr = ''
        self.start = start
        self.end = end
        self.ID_MAPPING = idmap
        self.name = name
        self.response = ''
        self.s1 = ''
        # self.response = self.scrape()

    def getCsvErr(self):
        return self.csverr

    def write_csv(self, filename):
        self.s1.to_csv(filename, index=False, header=False)

    def scrape(self):
        """
        Given a Commodity object with a date range and a commodity id,
        scrape historical data from the investing.com site

        Stores a string with the result gotten from the site
        """
        HEADERS = {
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
        }

        try:
            data = {
                "curr_id": self.ID_MAPPING[self.name],
                "smlID": "300004",
                "st_date": self.start,
                "end_date": self.end,
                "interval_sec": "Daily",
                "sort_col": "date",
                "sort_ord": "ASC",
                "action": "historical_data"
            }

            r = requests.post(self.BASE_URL, data=data, headers=HEADERS)
            assert(r.status_code == 200)
            return r.text
        except KeyError:
            if S.DBG_ALL:
                print "KeyError: " + self.name
            return "KeyError: No such record for " + self.name
        except Exception as e:
            print "Exception:", e
            raise e

    def to_df(self):
        """
        returns a pandas DataFrame object based on parsed data from a
        Commodity object's HTML
        """
        try:
            df = pd.read_html(self.response)
            df = df[0]  # Ignore footer table
            df["Date"] = pd.to_datetime(df["Date"])
            df.insert(0, "Commodity", np.nan)
            df["Commodity"] = self.name
            df.insert(6, "Close", np.nan)
            df["Close"] = df["Price"]
            df.insert(7, "Volume", np.nan)

            if self.name.startswith('FTFBM'):
                df['Volume'] = df["Vol."]
            else:
                mp = {'K': ' * 10**3', 'M': ' * 10**6'}
                # Convert k to 1000 and m to 1000000
                # Can only support max 5 months of EOD to convert
                df["Volume"] = pd.eval(df["Vol."].replace(mp.keys(), mp.values(), regex=True).str.replace(r'[^\d\.\*]+', ''))

            df.drop('Price', axis=1, inplace=True)
            df.drop('Change %', axis=1, inplace=True)
            df.drop('Vol.', axis=1, inplace=True)
            df.sort_values(by='Date', inplace=True)
        except ValueError as ve:
            df = 'ValueError'
            self.csverr = self.name + ": ValueError (No data for date range) " + ' (' + str(ve) + ')'
        except Exception as e:
            df = 'Exception'
            self.csverr = self.name + ":" + self.start + "," + self.end + ":" + str(e)
            # raise e

        return df


class InvestingQuote(Quote):
    def __init__(self, idmap, sname, last_date, end_date=du.getToday("%Y-%m-%d")):
        if last_date == end_date:
            self.csverr = sname + ": Skipped downloaded (" + last_date + ")"
            return
        last_date = du.getNextDay(last_date)
        if last_date > end_date:
            self.csverr = sname + ": Invalid dates (" + last_date + "," + end_date + ")"
            return

        last_date = datetime.datetime.strptime(last_date, "%Y-%m-%d").strftime('%m/%d/%Y')
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").strftime('%m/%d/%Y')
        super(InvestingQuote, self).__init__(sname, last_date, end_date, idmap)
        self.response = self.scrape()
        # s0 = Quote(sname, last_date, end_date, idmap)
        if isinstance(self.response, unicode):
            s1 = self.to_df()
            if isinstance(s1, pd.DataFrame):
                s1.index.name = 'index'
                self.s1 = s1
                self.csverr = ''
                # s1.to_csv(OUTPUT_FILE, index=False, header=False)
        else:
            self.csverr = sname + ":" + self.response + "," + last_date + "," + end_date


def loadIdMap():
    ID_MAPPING = {}
    try:
        with open("idmap.ini") as idmap:
            for line in idmap:
                name, var = line.partition("=")[::2]
                ID_MAPPING[name.strip()] = int(var)
            if S.DBG_ALL:
                print dict(ID_MAPPING.items()[0:2])
    except EnvironmentError:
        print "Missing idmap.ini file"
        sys.exit(1)
    except KeyError:
        print "loadIdMap KeyError:", name
        sys.exit(2)
    return ID_MAPPING


if __name__ == '__main__':
    # OUTPUT_FILE = sys.argv[1]
    OUTPUT_FILE = "test.csv"

    idmap = loadIdMap()

    S.DBG_ALL = False
    counter = "YSPSAH"
    START_DATE = "01/01/2018"
    END_DATE = "02/26/2018"

    s0 = Quote(counter, START_DATE, END_DATE, idmap)
    if isinstance(s0.response, unicode):
        s1 = s0.to_df()
        if isinstance(s1, pd.DataFrame):
            s1.index.name = 'index'
            s1.to_csv(OUTPUT_FILE, index=False, header=False)
        else:
            print s1 + ": " + counter + "," + START_DATE + "," + END_DATE
    else:
        print s0.response + "," + START_DATE + "," + END_DATE
    # s2 = Commodity(START_DATE, END_DATE, idmap, "YSPSAH").to_df()

    # combined = s1.append(s2)
    # combined.index.name = 'index'
    # combined.to_csv(OUTPUT_FILE)
