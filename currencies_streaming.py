import time
from kafka import KafkaProducer
import json
import time
import requests
from datetime import datetime

# Replace 'your-api-key' with your actual Finnhub API key
api_key = "cl77f8hr01qsmhrttjggcl77f8hr01qsmhrttjh0"

# Define a list of currency symbols
# symbols = ['AAPL', 'AXP', 'AMD', 'BA', 'CAT', 'CSCO', 'GOOG', 'GOOGL', 'AMZN', 'CVX']
symbols = ['AAPL']

def json_serializer(data):
    return json.dumps(data).encode("utf-8")


producer = KafkaProducer(bootstrap_servers=['192.168.1.22:9093'], value_serializer=json_serializer)

# Iterate through each symbol and make a request to the Finnhub API
for symbol in symbols:
    api_url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={api_key}"

    # Make a GET request to the API
    response = requests.get(api_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        data['symbol'] = symbol

        # Convert current timestamp to milliseconds
        timestamp = int(datetime.now().timestamp() * 1000)

        # Add the 't' field with the correct timestamp format
        data['t'] = timestamp

        print(data)
        producer.send("coins", data)
        # Extract and print relevant information
        #print(f"Symbol: {symbol}, Current Price: {data['c']}")
        time.sleep(2)
    else:
        # Print an error message if the request was not successful
        print(f"Error for {symbol}: {response.status_code}, {response.text}")