import configparser
from pytz import timezone
import requests 
import json

import config

class ScanStocks():
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(r'C:\Dev\plgstks\config.ini')
        self.poly_api_key = self.config["POLYGON"]["API_KEY"]
        self.snapshot_url = f'https://api.polygon.io/v2/snapshot/locale/us/markets/stocks/tickers?apiKey={self.poly_api_key}'
        print(self.snapshot_url)
        self.eastern_tz = timezone("US/Eastern")
        self.min_price = .15 #最低价
        self.min_gain_pct = 20 #最大涨幅

    def gainer_scan(self):
        gainers = []
        resp = requests.get(self.snapshot_url)
        if resp.status_code == 200:
            resp_json = json.loads(resp.text)
            print(resp_json)
        else:
            print("fail to fetch")

def main():
    scan = ScanStocks()
    scan.gainer_scan()

if __name__== '__main__':
    main()