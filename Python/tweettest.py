import tweepy
import json

# Retrieve values from config file
with open('appsettings.json', 'r') as f:
    config = json.load(f)

consumer_key = config['TwitterApi']['consumer_key']
consumer_secret = config['TwitterApi']['consumer_secret']
access_token = config['TwitterApi']['access_token']
access_token_secret = config['TwitterApi']['token_secret']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)