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
        
        # URL to fetch all stock tickers (metadata) available to free tier
        self.snapshot_url = f'https://api.polygon.io/v2/snapshot/locale/us/markets/stocks/gainers?apiKey={self.poly_api_key}'
        
        print(f"URL: {self.snapshot_url}")  # Print URL for debugging
        
        self.eastern_tz = timezone("US/Eastern")
        self.min_price = .15  # minimum price
        self.min_gain_pct = 20  # maximum gain percentage

    def gainer_scan(self):
        gainers = []
        resp = requests.get(self.snapshot_url)
        
        if resp.status_code == 200:
            resp_json = resp.json()  # Get the response JSON directly
            tickers = resp_json.get('tickers', [])
            
            # Iterate over tickers and check the price
            for ticker in tickers:
                symbol = ticker['ticker']
                price = ticker['last']['price']  # You can adjust depending on the fields you want
                
                # Filter tickers based on price (if you have any filtering logic)
                if price >= self.min_price:
                    gainers.append((symbol, price))
            
            # If you have gainers, print them
            if gainers:
                print("Gainers:", gainers)
            else:
                print("No gainers found based on minimum price.")
        else:
            print(f"Failed to fetch: {resp.status_code}, {resp.text}")

def main():
    scan = ScanStocks()
    scan.gainer_scan()

if __name__== '__main__':
    main()
