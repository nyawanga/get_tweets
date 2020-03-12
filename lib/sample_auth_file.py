from tweepy import OAuthHandler
import tweepy

def get_auth():
    consumer_key = ""
    consumer_secret = ""
    access_token = ""
    access_token_secret = ""
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    #AUTHENTICATE
    try:
        tweepyapi= tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    except Exception as err:
        raise
    return tweepyapi

if __name__ == "__main__":
    pass
