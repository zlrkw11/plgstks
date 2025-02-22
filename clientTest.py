from polygon import RESTClient
import config
from datetime import datetime
import logging

# Initialize the client with your API key
client = RESTClient(api_key=config.API_KEY)

def get_real_time_data(ticker):
    # Set the specific date
    today = "2024-12-01"
    
    try:
        # Get aggregate data for the ticker (real-time)
        aggs = client.get_aggs(
            ticker=ticker,
            multiplier=1,
            timespan='day',
            from_=today,
            to=today
        )
        return aggs
    except Exception as e:
        logging.error(f"Error retrieving data for {ticker}: {e}")
        return []  # Return empty list if there is an error

def analyze_stocks(threshold=0.02):
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']  # Stocks to track
    results = []
    
    for ticker in tickers:
        aggs = get_real_time_data(ticker)
        
        if not aggs:
            logging.error(f"No data found for {ticker}")
            continue
        
        for agg in aggs:
            open_price = agg.open
            close_price = agg.close
            
            # Check for positive closing price
            if close_price > 0:
                results.append((ticker, open_price, close_price))
    
    return results

def main():
    results = analyze_stocks()
    if results:
        for ticker, open_price, close_price in results:
            print(f"{ticker}: Open = {open_price}, Close = {close_price}")
    else:
        print("No stocks with positive closing values found on 2024/12/01.")

if __name__ == '__main__':
    main()
