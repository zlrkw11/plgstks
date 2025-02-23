import random
from polygon import RESTClient
import config
import time

client = RESTClient(api_key=config.API_KEY)

# 20 S&P 500 tickers
SP500_TICKERS = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "BRK.B", "UNH", "JNJ",
    "V", "XOM", "PG", "JPM", "HD", "MA", "CVX", "ABBV", "PFE", "PEP"
]
SP500_TICKERS_S = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA" 
]

sample_tickers = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "BRK.B", "UNH", "JNJ",
    "V", "XOM", "PG", "JPM", "HD", "MA", "CVX", "ABBV", "PFE", "PEP", "NFLX",
    "DIS", "NVDA", "PYPL", "INTC", "AMD", "CSCO", "GS", "IBM", "WMT", "T",
    "BA", "CAT", "DE", "HD", "MCD", "KO", "SBUX", "GM", "F", "LUV", "UAL", "SPG",
    "BMY", "OXY", "ZTS", "MMM", "VZ", "PFE", "MO", "TGT", "ADBE", "SQ", "AMGN"
]

# Find +5% gainers
def get_x_percent_gainers_sp500(start_date, end_date):
    gainers = []
    percentage = 2
    for ticker in SP500_TICKERS_S:
        print(f"Fetching data for {ticker}...")  # Debugging: Track progress
        try:
            aggs = client.get_aggs(
                ticker=ticker,
                multiplier=1,
                timespan="day",
                from_=start_date,
                to=end_date
            )
            if not aggs:
                print(f"No data returned for {ticker}")  # Debugging: Check if no data
                continue
            
            for agg in aggs:
                if agg.open > 0:
                    percent_change = ((agg.close - agg.open) / agg.open) * 100
                    if percent_change > percentage:
                        gainers.append((ticker, agg.timestamp, percent_change))
                        print(f"{ticker}: {percent_change}")

        except Exception as e:
            print(f"Error fetching {ticker}: {e}") 

        time.sleep(12)  

    return gainers

'''
gainers = get_x_percent_gainers_sp500("2025-01-01", "2025-02-01")

if gainers:
    for ticker, date, change in gainers:
        print(f"{ticker} gained {change:.2f}% on {date}")
else:
    print("No gainers found within the specified range.")
'''

def consecutive_gainers(start_date, end_date):
    gainers = []
    for ticker in SP500_TICKERS:
        print(f"Fetching data for {ticker}...")  # Debugging: Track progress
        try:
            aggs = client.get_aggs(
                ticker=ticker,
                multiplier=1,
                timespan="day",
                from_=start_date,
                to=end_date
            )
            all_gain_days = True

            print(f"day 1: {aggs[0].close}")
            for i in range(1, len(aggs)):
                prev_agg = aggs[i - 1]
                curr_agg = aggs[i]
                
                
                print(f"day {i+1}: {curr_agg.close}")
                if prev_agg.close >= curr_agg.close:
                    all_gain_days = False
                    break

            if all_gain_days:
                gainers.append(ticker)
                print(f"matched: {ticker}")
            print("-------------------")

        except Exception as e:
            print(f"Error fetching {ticker}: {e}")
        time.sleep(12)

    return gainers


gainers = consecutive_gainers("2025-01-01", "2025-01-04")
if gainers:
    print("Consecutive gainers found:", gainers)
else:
    print("No consecutive gainers found in the specified range.")
