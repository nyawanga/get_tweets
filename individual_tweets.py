
#https://www.reddit.com/r/Python/comments/87j36n/return_user_tweets_between_certain_dates_using/
#https://stackoverflow.com/questions/24214189/how-can-i-get-tweets-older-than-a-week-using-tweepy-or-other-python-libraries

import sys

sys.path.append("./lib")
from lib import save_data       # modulke to help save data to csv, excel or gsheets
from lib import get_auth_file   # get the file with the authentication

import tweepy
from tweepy import OAuthHandler

import json
from datetime import datetime
import time

auth = get_auth_file.get_auth()     #get authentication from our imported module

start_date = datetime(2019, 3, 1, 0, 0, 0)
end_date = datetime(2020, 3, 15, 0, 0, 0)
tweets = []
name = "DavidNdii"  #SirHigiChege"
tweet_count = 200
pages = 2

def get_tweets(name,auth,start_date,end_date,limit=20,pages=1):
    # results = auth.user_timeline(id=name, count=limit)
    page_count = 0
    try:
        if pages == None:
            cursor_object = tweepy.Cursor(auth.user_timeline, id=name, count=limit).pages()
        else:
            cursor_object = tweepy.Cursor(auth.user_timeline, id=name, count=limit).pages(pages)

        for page in cursor_object:
            page_count += 1
            print(f"working on page: {page_count}")
            tweets = []
            for result in page:
                tweet = result._json
                text = tweet.get("text")
                created_at = datetime.strptime(tweet.get("created_at"), "%a %b %y %H:%M:%S +0000 %Y")

                if created_at > start_date and created_at < end_date:
                    data = [page_count, created_at, text]
                    tweets.append(data)

            print(f"got {len(tweets)} tweets from page : {page_count}")
            yield tweets

            # control throttling
            print("sleeping for 10 seconds...")
            time.sleep(10)
            # print(created_at, tweet.get("text"))
    except Exception as err:
        print(f"got an error")
    finally:
        print("exiting program")


# instantiate the generator
tweets = get_tweets(name,auth, start_date, end_date, limit=tweet_count, pages=None)


for tweet in tweets:
    if len(tweet) > 0 :
        print("saving data ...")
        save_data.to_csv(tweet, "./data/csv_tweets.csv", "a")
    else:
        print("no data got back from the request")


            page_count += 1
            print(f"working on page: {page_count}")
            tweets = []
            for result in page:
                tweet = result._json
                text = tweet.get("text")
                created_at = datetime.strptime(tweet.get("created_at"), "%a %b %y %H:%M:%S +0000 %Y")

                if created_at > start_date and created_at < end_date:
                    data = [page_count, created_at, text]
                    tweets.append(data)

            print(f"got {len(tweets)} tweets from page : {page_count}")
            yield tweets

            # control throttling
            print("sleeping for 10 seconds...")
            time.sleep(10)
            # print(created_at, tweet.get("text"))
    except Exception as err:
        print(f"got an error")
    finally:
        print("exiting program")


# instantiate the generator
tweets = get_tweets(name,auth, start_date, end_date, limit=tweet_count, pages=None)


for tweet in tweets:
    if len(tweet) > 0 :
        print("saving data ...")
        save_data.to_csv(tweet, "./data/csv_tweets.csv", "a")
    else:
        print("no data got back from the request")

