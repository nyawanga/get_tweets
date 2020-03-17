# https://www.reddit.com/r/Python/comments/87j36n/return_user_tweets_between_certain_dates_using/
# https://stackoverflow.com/questions/24214189/how-can-i-get-tweets-older-than-a-week-using-tweepy-or-other-python-libraries

import sys

sys.path.append("./lib")
from lib import save_data  # modulke to help save data to csv, excel or gsheets
from lib import get_auth_file  # get the file with the authentication

import tweepy
from tweepy import OAuthHandler

import json
from datetime import datetime, timedelta
import argparse
import time

auth = get_auth_file.get_auth()  # get authentication from our imported module


def proper_date_args(date_arg):
    if len(date_arg.split("-")) == 6:
        date_arg = date_arg.split("-")
        return ", ".join(date_arg)
    else:
        msg = "enter the correct date format yyyy-mm-dd-HH-MM-SS"
        raise argparse.ArgumentTypeError(msg)


parser = argparse.ArgumentParser(description="optional args for the program")
parser.add_argument(
    "--name",
    "-n",
    type=str,
    help="username for the entity to scrape data from without quotes",
)
parser.add_argument(
    "--auth",
    "-a",
    help="path to auth file if not in ./lib",
    default="./lib/sample_auth_file.py",
)
parser.add_argument(
    "--start_date",
    "-s",
    type=proper_date_args,
    help="start date of scrape format of '2020-03-01-23-30-02' ",
    default=datetime.strftime(
        datetime.now().date() - timedelta(days=17), "%Y, %m, %d, %H, %M, %S"
    ),
)
parser.add_argument(
    "--end_date",
    "-e",
    type=proper_date_args,
    help="end date of scrape format of '2020-03-17-23-30-02' ",
    default=datetime.strftime(datetime.now().date(), "%Y, %m, %d, %H, %M, %S"),
)
parser.add_argument(
    "--limit", "-l", type=int, help="limit of tweets for each page we call", default=200
)
parser.add_argument(
    "--pages",
    "-p",
    type=int,
    help="limit pages to scrape where 1 is most recent page/tweets",
    default=2,
)
parser.add_argument(
    "--file", "-f", help="file to save the data to", default="./data/csv_tweets.csv",
)
parser.add_argument(
    "--mode",
    "-m",
    help="the mode used to save the file to default is append - a",
    default="a",
)

args = parser.parse_args()
args = vars(args)

name = args.get("name")
# auth = args.get("auth")
start_date = datetime.strptime(args.get("start_date"), "%Y, %m, %d, %H, %M, %S")
end_date = datetime.strptime(args.get("end_date"), "%Y, %m, %d, %H, %M, %S")
limit = args.get("limit")
pages = args.get("pages")
file = args.get("file")
mode = args.get("mode")
tweets = []

print("_" * 80)
print(f"pulling data from: {start_date}, to: {end_date} for timeline: {name}")
print("_" * 80)
print()


def get_tweets(name, auth, start_date, end_date, limit=20, pages=1):
    # results = auth.user_timeline(id=name, count=limit)
    page_count = 0
    try:
        if pages == None:
            cursor_object = tweepy.Cursor(
                auth.user_timeline, id=name, count=limit  # , #tweet_mode="extended"
            ).pages()
        else:
            cursor_object = tweepy.Cursor(
                auth.user_timeline, id=name, count=limit  # , tweet_mode="extended"
            ).pages(pages)

        for page in cursor_object:
            page_count += 1
            print(f"working on page: {page_count}")
            tweets = []
            for result in page:
                tweet = result._json
                text = tweet.get("text")
                created_at = datetime.strptime(
                    tweet.get("created_at"), "%a %b %y %H:%M:%S +0000 %Y"
                )

                if created_at > start_date and created_at < end_date:
                    data = [page_count, created_at, text]
                    tweets.append(data)

            print(f"got {len(tweets)} tweets from page : {page_count}")
            yield tweets

            # control throttling
            print("sleeping for 10 seconds...")
            time.sleep(10)
            print()
            # print(created_at, tweet.get("text"))
    except Exception as err:
        print(f"got an error {err}")
    finally:
        print("exiting program")


# instantiate the generator
tweets = get_tweets(name, auth, start_date, end_date, limit=limit, pages=pages)

for tweet in tweets:
    if len(tweet) > 0:
        print("saving data ...")
        save_data.to_csv(tweet, file, mode)
