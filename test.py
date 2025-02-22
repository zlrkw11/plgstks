from polygon import RESTClient
import config
# Replace 'YOUR_API_KEY' with your actual Polygon.io API key
client = RESTClient(api_key=config.API_KEY)

# Example: Get stock aggregates for a given ticker (like AAPL) for yesterday
aggs = client.get_aggs(
    ticker="AAPL",
    multiplier=1,
    timespan="day",
    from_="2024-02-21",
    to="2024-02-21"
)

for agg in aggs:
    print(f"Date: {agg.timestamp}, Open: {agg.open}, Close: {agg.close}, High: {agg.high}, Low: {agg.low}")
