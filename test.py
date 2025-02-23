from polygon import RESTClient
import config
# Replace 'YOUR_API_KEY' with your actual Polygon.io API key
client = RESTClient(api_key=config.API_KEY)

def get_all_tickers():
    tickers = []
    response = client.list_tickers(market="stocks", active=True, limit=1000)
    for ticker in response:
        tickers.append(ticker.ticker)
    return tickers

# Example: Get stock aggregates for a given ticker (like AAPL) for yesterday
aggs = client.get_aggs(
    ticker="AAPL",
    multiplier=1,
    timespan="day",
    from_="2024-05-22",
    to="2024-05-25"
)

for agg in aggs:
    print(f"Date: {agg.timestamp}, Open: {agg.open}, Close: {agg.close}, High: {agg.high}, Low: {agg.low}")

# 百分比涨幅函数
def get_5_percent_gainers_all(start_date, end_date):
    gainers = []
    tickers = get_all_tickers()
    for ticker in tickers:
        aggs = client.get_aggs(
            ticker=ticker,
            multiplier=1,
            timespan="day",
            from_=start_date,
            to=end_date
        )
        for agg in aggs:
            if agg.open > 0:
                percent_change = ((agg.close - agg.open) / agg.open) * 100
                if percent_change > 5:
                    gainers.append((ticker, agg.timestamp, percent_change))
                    
    return gainers

# Example usage
# gainers = get_5_percent_gainers_all("2024-05-22", "2024-05-25")

# for ticker, date, change in gainers:
#     print(f"{ticker} gained {change:.2f}% on {date}")