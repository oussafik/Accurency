# import requests

# # Replace 'your-api-key' with your actual Finnhub API key
# api_key = "cl77f8hr01qsmhrttjggcl77f8hr01qsmhrttjh0"

# # Define a list of currency symbols
# symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 'IBM', 'FB', 'NFLX', 'GOOG',
#            'GE', 'CSCO', 'INTU', 'DIS', 'PEP', 'VZ', 'KO',
#            'NVDA', 'AMD', 'WMT', 'GS', 'CVX', 'CAT', 'HD', 'AXP', 'WBA', 
#             'V', 'JNJ', 'JPM', 'BA', 'NKE', 'MCD', 'WMT', 'MMM',
#             'UNH', 'MRK', 'INTC']

# # Iterate through each symbol and make a request to the Finnhub API
# for symbol in symbols:
#     api_url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={api_key}"

#     # Make a GET request to the API
#     response = requests.get(api_url)

#     # Check if the request was successful (status code 200)
#     if response.status_code == 200:
#         # Parse the JSON response
#         data = response.json()
#         print(data)
#         # Extract and print relevant information
#         #print(f"Symbol: {symbol}, Current Price: {data['c']}")
#     else:
#         # Print an error message if the request was not successful
#         print(f"Error for {symbol}: {response.status_code}, {response.text}")


# api_key2 = "clf179hr01qovepph4v0clf179hr01qovepph4vg"


# for symbol in symbols:
#     api_url = f"https://finnhub.io/api/v1/news?symbol={symbol}&token={api_key2}"

#     # Make a GET request to the API
#     response = requests.get(api_url)

#     # Check if the request was successful (status code 200)
#     if response.status_code == 200:
#         # Parse the JSON response
#         data = response.json()

#         # Extract and print relevant information
#         for news_item in data:
#             print(f"Symbol: {symbol}, "
#                   f"Headline: {news_item['headline']}, "
#                   f"Source: {news_item['source']}, "
#                   f"Timestamp: {news_item['datetime']}")
#     else:
#         # Print an error message if the request was not successful
#         print(f"Error for {symbol}: {response.status_code}, {response.text}")


import requests
from datetime import datetime
import pandas as pd

# Replace 'YOUR_API_KEY' with your actual Finnhub API key
api_key = 'cl77f8hr01qsmhrttjggcl77f8hr01qsmhrttjh0'
currencies = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 'FB', 'NFLX', 'NVDA', 'PYPL', 'INTC', 'AMD', 'CSCO', 'IBM', 'ORCL', 'QCOM', 'V', 'GS', 'JPM', 'C', 'BAC']

# Specify date range
start_date = '2022-01-01'
end_date = '2023-07-30'

# Create an empty DataFrame to store the data
df = pd.DataFrame(columns=['Date', 'Currency', 'Open', 'High', 'Low', 'Close'])

# Convert start_date and end_date to Unix timestamps
start_timestamp = int(datetime.strptime(start_date, "%Y-%m-%d").timestamp())
end_timestamp = int(datetime.strptime(end_date, "%Y-%m-%d").timestamp())

# Loop through each currency symbol
for symbol in currencies:
    # API request to get historical stock prices
    url = 'https://finnhub.io/api/v1/stock/candle'
    params = {'symbol': symbol, 'resolution': 'D', 'from': start_timestamp, 'to': end_timestamp, 'token': api_key}
    response = requests.get(url, params=params)

    # Extract historical stock prices from the response
    historical_data = response.json()

    print(historical_data)
