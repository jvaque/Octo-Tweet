import tweepy
import time

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

    def postMedia(self, imagePaths, status):
        mediaIds = []
        for imagePath in imagePaths:
            res = self._api.media_upload(imagePath)
            mediaIds.append(res.media_id)

        # Tweet with multiple images
        self._api.update_status(status=status, media_ids=mediaIds)

    def postBatch(self, listDicCharts):
        for chart in listDicCharts:
            self.postMedia(chart['Files'], chart['Message'])
            time.sleep(120)
