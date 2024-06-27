import time
from kafka import KafkaProducer
import json
import time
import requests
from datetime import datetime

# Replace 'your-api-key' with your actual Finnhub API key
api_key = "clf179hr01qovepph4v0clf179hr01qovepph4vg"

# Define a list of currency symbols
symbols = ['AAPL', 'AXP', 'AMD', 'BA', 'CAT', 'CSCO', 'GOOG', 'GOOGL', 'AMZN', 'CVX']

def json_serializer(data):
    return json.dumps(data).encode("utf-8")


producer = KafkaProducer(bootstrap_servers=['192.168.1.22:9093'], value_serializer=json_serializer)

# Iterate through each symbol and make a request to the Finnhub API
for symbol in symbols:
    api_url = f"https://finnhub.io/api/v1/news?symbol={symbol}&token={api_key}"

    # Make a GET request to the API
    response = requests.get(api_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        for news_item in data:
            # Convert the timestamp to the correct format
            timestamp = datetime.fromtimestamp(news_item['datetime']).isoformat()

            news_dict = {
                "symbol": symbol,
                "Headline": news_item['headline'],
                "Source": news_item['source'],
                "Timestamp": timestamp
            }
            print(news_dict)
            producer.send("news", news_dict)
            time.sleep(1)
    else:
        # Print an error message if the request was not successful
        print(f"Error for {symbol}: {response.status_code}, {response.text}")