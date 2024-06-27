# import praw
# import datetime

# reddit = praw.Reddit(
#     client_id="Fam9OCnL7duXKBZWBebluA",
#     client_secret="yycnopLYroNEqandbVBUoTmdJRkHnQ",
#     username="oussafikri",
#     user_agent="fikri by u/oussafikri",
# )

# # Specify the subreddit and search query
# subreddit = reddit.subreddit('stockmarket')
# search_query = 'AAPL'

# # Get the current time
# current_time = datetime.datetime.utcnow()

# # Search for posts with the desired tags or keywords
# search_results = subreddit.search(search_query)

# # Iterate over the search results
# for post in search_results:
#     dt = datetime.datetime.utcfromtimestamp(post.created_utc)
#     time_difference = current_time - dt

#     # Check if the post is within the last 10 days
#     if time_difference.days <= 60:
#         print("Post:")
#         print("Title:", post.title)
#         print("URL:", post.url)
#         print("Timestamp:", dt)
#         print("\n")

#         # Retrieve and display comments associated with the post
#         post.comments.replace_more(limit=None)  # Include all comments
#         comments = post.comments.list()

#         if comments:
#             print("Comments:")
#             for comment in comments:
#                 print("Text:", comment.body)
#                 print("Score:", comment.score)
#                 print("Timestamp:", datetime.datetime.utcfromtimestamp(comment.created_utc))
#                 print("\n")
#         else:
#             print("No comments for this post.")
        
import praw
import datetime
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
import numpy as np


# load model and tokenizer
roberta = "cardiffnlp/twitter-roberta-base-sentiment"

model = AutoModelForSequenceClassification.from_pretrained(roberta)
tokenizer = AutoTokenizer.from_pretrained(roberta)

labels = ['Negative', 'Neutral', 'Positive']

reddit = praw.Reddit(
    client_id="Fam9OCnL7duXKBZWBebluA",
    client_secret="yycnopLYroNEqandbVBUoTmdJRkHnQ",
    username="oussafikri",
    user_agent="fikri by u/oussafikri",
)

# Specify the subreddit and search query
subreddit = reddit.subreddit('Africa')
search_query = 'economic crisis'

# Get the current time
current_time = datetime.datetime.utcnow()

# Search for posts with the desired tags or keywords
search_results = subreddit.search(search_query)

# Iterate over the search results
for post in search_results:
    dt = datetime.datetime.utcfromtimestamp(post.created_utc)
    time_difference = current_time - dt

    # Check if the post is within the last 10 days
    if time_difference.days <= 4500:
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
                encoded_cmt = tokenizer(comment.body, return_tensors='pt')
                output = model(**encoded_cmt)
                scores = output[0][0].detach().numpy()
                scores = softmax(scores)
                print("Text:", comment.body)
                print("Sentiment Analysis:", labels[np.argmax(scores)])
                print("Score:", comment.score)
                print("Timestamp:", datetime.datetime.utcfromtimestamp(comment.created_utc))
                print("\n")
        else:
            print("No comments for this post.")
        
