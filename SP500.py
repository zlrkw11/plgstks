import datetime
import random
from polygon import RESTClient
import requests
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
        print("******************")
        try:
            aggs = client.get_aggs(
                ticker=ticker,
                multiplier=1,
                timespan="day",
                from_=start_date,
                to=end_date
            )
            all_gain_days = True

            for i in range(1, len(aggs)):
                prev_agg = aggs[i - 1]
                curr_agg = aggs[i]

                prev_date = datetime.datetime.fromtimestamp(prev_agg.timestamp / 1000).strftime('%Y-%m-%d')
                curr_date = datetime.datetime.fromtimestamp(curr_agg.timestamp / 1000).strftime('%Y-%m-%d')

                print(f"{prev_date}: {prev_agg.close}")
                print(f"{curr_date}: {curr_agg.close}")
                if prev_agg.close >= curr_agg.close:
                    all_gain_days = False
                    break

            if all_gain_days:
                gainers.append(ticker)
                print(f"matched: {ticker}")
            print("------------------")
            
        except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:
                    wait_time = (2 ** retries) * 5  # Exponential backoff
                    print(f"Rate limit hit. Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                    retries += 1
                else:
                    print(f"HTTP error fetching {ticker}: {e}")
                    break
                
        except Exception as e:
            print(f"Error fetching {ticker}: {e}")
        time.sleep(12)

    return gainers

def consecutive_weekly_gainers(start_date, end_date, weeks):
    gainers = []
    for ticker in SP500_TICKERS:
        print(f"Fetching data for {ticker}...")  
        try:
            aggs = client.get_aggs(
                ticker=ticker,
                multiplier=1,
                timespan="day",
                from_=start_date,
                to=end_date
            )
            
            # Group daily data into weekly data (each week = 7 days)
            weekly_closes = []
            current_week = []
            start_of_week = None

            for agg in aggs:
                date = datetime.datetime.fromtimestamp(agg.timestamp / 1000)
                if start_of_week is None:
                    start_of_week = date

                # If 7 days passed or it's a new week, calculate weekly close
                if (date - start_of_week).days >= 7:
                    weekly_closes.append((start_of_week.strftime('%Y-%m-%d'), current_week[-1].close))
                    start_of_week = date
                    current_week = []

                current_week.append(agg)

            # Add the last week's data
            if current_week:
                weekly_closes.append((start_of_week.strftime('%Y-%m-%d'), current_week[-1].close))

            # Check for consecutive weekly gains
            consecutive_weeks = 0
            for i in range(1, len(weekly_closes)):
                prev_week_close = weekly_closes[i - 1][1]
                curr_week_close = weekly_closes[i][1]

                print(f"Week of {weekly_closes[i - 1][0]}: {prev_week_close}")
                print(f"Week of {weekly_closes[i][0]}: {curr_week_close}")

                if curr_week_close > prev_week_close:
                    consecutive_weeks += 1
                else:
                    consecutive_weeks = 0  # Reset if a down week is found

                if consecutive_weeks >= weeks:
                    gainers.append(ticker)
                    print(f"Matched: {ticker} with {weeks} consecutive gaining weeks.")
                    break

            print("------------------")

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                print("Rate limit hit. Waiting 12 seconds...")
                time.sleep(12)
            else:
                print(f"HTTP error fetching {ticker}: {e}")
                
        except Exception as e:
            print(f"Error fetching {ticker}: {e}")

        time.sleep(12)  # To respect rate limits

    print(gainers)
    return gainers

# Example usage — check for 3 consecutive weekly gainers
gainers = consecutive_weekly_gainers("2025-01-01", "2025-01-30", weeks=3)
print("Consecutive weekly gainers:", gainers)

# gainers = consecutive_gainers("2025-01-01", "2025-01-04")
# if gainers:
#     print("Consecutive gainers found:", gainers)
# else:
#     print("No consecutive gainers found in the specified range.")
