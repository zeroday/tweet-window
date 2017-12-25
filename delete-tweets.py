import tweepy
import csv
import os
import json

CONSUMER_KEY = os.environ['TWITTER_CONSUMER_KEY']
CONSUMER_SECRET = os.environ['TWITTER_CONSUMER_SECRET']
ACCESS_KEY = os.environ['TWITTER_ACCESS_KEY']
ACCESS_SECRET = os.environ['TWITTER_ACCESS_SECRET']

# Limit info from https://developer.twitter.com/en/docs/basics/rate-limits.html
STATUS_LOOKUP_RATE_LIMIT = 300

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
print("Tweet count: %s" % me.statuses_count)
tweet_marker = me.status.id

print("latest tweet %s" % tweet_marker)

not_done = True
counter = 0

while not_done:
    rate_limit_status = api.rate_limit_status()
    status_lookup_limits = rate_limit_status['resources']['statuses']['/statuses/lookup']
    print("%s remaining" % status_lookup_limits['remaining'])
    time_line = api.user_timeline(screen_name = me.screen_name, max_id = tweet_marker)
    for tweet in time_line:
        print("%s at %s" % (tweet.id, tweet.created_at))
        last_tweet = tweet.id
    tweet_marker = last_tweet
    counter = counter + 1
    if counter > 1:
        not_done = False
