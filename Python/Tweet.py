import tweepy
import json

class Tweet:
    def __init__(self, config):
        consumer_key = config['TwitterApi']['consumer_key']
        consumer_secret = config['TwitterApi']['consumer_secret']
        access_token = config['TwitterApi']['access_token']
        access_token_secret = config['TwitterApi']['token_secret']

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        self._api = tweepy.API(auth)

    def postStatus(self, status):
        self._api.update_status(status)

    def postMedia(self, imagePath, status):
        self._api.update_with_media(imagePath, status)
