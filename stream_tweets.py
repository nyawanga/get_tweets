#https://marcobonzanini.com/2015/03/02/mining-twitter-data-with-python-part-1/

import tweepy
from tweepy.streaming import StreamListener
from tweepy import Stream
from tweepy import OAuthHandler
import sys
# from create_access import get_auth    #import the credentials file
from create_access import consumer_key,consumer_secret      # get these from your tweeter
from create_access import access_token,access_token_secret  # get these from your tweeter

class MyListener(StreamListener):

    def on_data(self, raw_data):
        try:
            self.process_data(raw_data)
            return True
        except BaseException as err:
            print(f"Error on_data: str{err}")

        return True

    def process_data(self, raw_data):
        with open('active_listener.json', 'a') as f:
            f.write(raw_data)
            print(raw_data)

    def on_error(self, status):
        if status_code == 420:
            print(status)
            return False

class MaxStream():
    def __init__(self, auth, listener):
        self.stream = Stream(auth, listener)

    def start(self, filter):
        self.stream.filter(track= [filter])

if __name__=='__main__':
    listener = MyListener()

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = MaxStream(auth, MyListener())
    stream.start("BBI")

    # filter data for topics desired


