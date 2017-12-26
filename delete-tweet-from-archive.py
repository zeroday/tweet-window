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

# REQUIRES TWEETS.CSV FROM THE TWITTER ARCHIVE FUNCTION

# copied from https://pushpullfork.com/i-deleted-tweets/
def read_csv(file):
    """
    reads a CSV file into a list of lists
    """
    with open(file, encoding = 'utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter = ',')
        rows = []
        for line in reader:
            row_data = []
            for element in line:
                row_data.append(element)
            if row_data != []:
                rows.append(row_data)
    rows.pop(0)
    return(rows)

tweets = read_csv('/tmp/tweets.csv')

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

for tweet in tweets:
    tweet_id = tweet[0]
    tweet_created_at = datetime.datetime.strptime(tweet[3],'%Y-%m-%d %H:%M:%S +0000')
    age = time.time() - (tweet_created_at - datetime.datetime(1970,1,1)).total_seconds()
    if (age > TWEET_AGE_LIMIT):
        rate_limit_status = api.rate_limit_status()
        application_status = rate_limit_status['resources']['application']['/application/rate_limit_status']
        print("%s remaining" % application_status['remaining'])
        if application_status['remaining'] < 10:
            reset_time = datetime.datetime.fromtimestamp(application_status['reset'])
            now = time.time()
            sleep_time = (reset_time - datetime.datetime.fromtimestamp(now)) + datetime.timedelta(seconds=60)
            print("sleeping for %s seconds" % sleep_time.total_seconds())
            time.sleep(sleep_time.total_seconds())
        delete_tweet = True
        try:
            api.destroy_status(tweet_id)
        except:
            print("That tweet was probably deleted already.")
    else:
        delete_tweet = False
    print("%s DELETE:%s" % (tweet_created_at, delete_tweet))

