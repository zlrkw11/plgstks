from polygon import RESTClient
import config
from datetime import datetime, timedelta

# Initialize the client with your API key
client = RESTClient(api_key=config.API_KEY)

def get_real_time_data(ticker):
    # Get the current date
    # today = datetime.now().strftime('%Y-%m-%d')
    today = "2024-12-01"
    
    # Get aggregate data for the ticker (real-time)
    aggs = client.get_aggs(
        ticker=ticker,
        multiplier=1,
        timespan='day',
        from_=today,
        to=today
    )
    
    return aggs

def analyze_stocks(threshold=0.02):
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']  # Add the stocks you want to track
    results = []
    
    for ticker in tickers:
        aggs = get_real_time_data(ticker)
        
        for agg in aggs:
            open_price = agg.open
            close_price = agg.close
            change = (close_price - open_price) / open_price
            
            if change >= threshold:
                results.append((ticker, open_price, close_price, change))
    
    return results

def main():
    results = analyze_stocks()
    for ticker, open_price, close_price, change in results:
        print(f"{ticker}: Open = {open_price}, Close = {close_price}, Change = {change:.2%}")

if __name__ == '__main__':
    main()
