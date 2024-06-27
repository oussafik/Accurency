import time
from kafka import KafkaProducer
import json
import time
import requests
import praw
import datetime

reddit = praw.Reddit(
    client_id="Fam9OCnL7duXKBZWBebluA",
    client_secret="yycnopLYroNEqandbVBUoTmdJRkHnQ",
    username="oussafikri",
    user_agent="fikri by u/oussafikri",
)

# Specify the subreddit and search query
subreddit = reddit.subreddit('stockmarket')

# Define a list of currency symbols
symbols = ['AAPL', 'AXP', 'AMD', 'BA', 'CAT', 'CSCO', 'GOOG', 'GOOGL', 'AMZN', 'CVX']


def json_serializer(data):
    return json.dumps(data).encode("utf-8")


producer = KafkaProducer(bootstrap_servers=['192.168.1.22:9093'], value_serializer=json_serializer)

for symbol in symbols:
    search_query = symbol

    # Get the current time
    current_time = datetime.datetime.utcnow()

    # Search for posts with the desired tags or keywords
    search_results = subreddit.search(search_query)

    # Iterate over the search results
    for post in search_results:
        dt = datetime.datetime.utcfromtimestamp(post.created_utc)
        time_difference = current_time - dt

        # Check if the post is within the last 10 days
        if time_difference.days <= 60:
            print("Post:")
            print("Title:", post.title)
            print("URL:", post.url)
            print("Timestamp:", dt)
            print("\n")

            # Retrieve and display comments associated with the post
            post.comments.replace_more(limit=None)  # Include all comments
            comments = post.comments.list()

            if comments:
                print("Comments:")
                for comment in comments:
                    cmt = {"symbol": symbol, "Text": comment.body, "Score": comment.score, "Timestamp": str(datetime.datetime.utcfromtimestamp(comment.created_utc))}
                    print(cmt)
                    producer.send("reddit", cmt)
                    time.sleep(1)
            else:
                print("No comments for this post.")