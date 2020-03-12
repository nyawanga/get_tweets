import sys

sys.path.append("./lib")
from lib import save_data
from lib import get_auth_file

import tweepy
from tweepy.streaming import StreamListener
from tweepy import Stream
from tweepy import OAuthHandler

import json
from datetime import datetime
import time

auth = get_auth_file.get_auth()     #get authentication from our imported module

start_date = datetime(2020, 3, 1, 0, 0, 0)
end_date = datetime(2020, 3, 15, 0, 0, 0)
tweets = []
name = "SirHigiChege"
tweet_count = 2

def get_tweets(name,auth, start_date, end_date, limit=20, pages=1):
    # results = auth.user_timeline(id=name, count=limit)
    page_count = 0
    for page in tweepy.Cursor(auth.user_timeline, id=name, count=limit).pages(pages):
        page_count += 1
        print(f"working on page: {page_count}")
        tweets = []
        for result in page:
            tweet = result._json
            text = tweet.get("text")
            created_at = datetime.strptime(tweet.get("created_at"), "%a %b %y %H:%M:%S +0000 %Y")

            if created_at > start_date and created_at < end_date:
                data = [created_at, text]
                tweets.append(data)

        yield tweets

        # control throttling
        print("sleeping for 10 seconds...")
        time.sleep(10)
            # print(created_at, tweet.get("text"))

tweets = get_tweets(name,auth, start_date, end_date, limit=20, pages=2)

for tweet in tweets:
    print("saving data ...")
    save_data.to_csv(tweet, "./data/csv_tweets.csv", "w")

