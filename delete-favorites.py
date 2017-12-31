import tweepy
import csv
import os
import json
import datetime
import time

CONSUMER_KEY = os.environ['TWITTER_CONSUMER_KEY']
CONSUMER_SECRET = os.environ['TWITTER_CONSUMER_SECRET']
ACCESS_KEY = os.environ['TWITTER_ACCESS_KEY']
ACCESS_SECRET = os.environ['TWITTER_ACCESS_SECRET']
TWEET_AGE_LIMIT = 60 * 60 * 24 * 14

# copied from https://pushpullfork.com/i-deleted-tweets/
def oauth_login(consumer_key, consumer_secret):
    """Authenticate with twitter using OAuth"""
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth_url = auth.get_authorization_url()
    verify_code = raw_input("Authenticate at %s and then enter you verification code here > " % auth_url)
    auth.get_access_token(verify_code)
    return tweepy.API(auth)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)
me = api.me()
print("Authenticated as: %s" % me.screen_name)

not_done = True

while not_done:
    for page in tweepy.Cursor(api.favorites,wait_on_rate_limit=True).pages(200):
        for like in page:
            age = time.time() - (like.created_at - datetime.datetime(1970,1,1)).total_seconds()
            if (age > TWEET_AGE_LIMIT):
                print("destroying %s fav from %s" % (like.user.screen_name.encode('utf-8'),like.created_at))
                api.destroy_favorite(like.id)
    not_done = False
