import os
import logging
import tweepy


class MentionStreamListener(tweepy.StreamListener):

    def __init__(self, api, screen_name=None):
        super().__init__(api)

        if screen_name is None:
            screen_name = api.me().screen_name

        self.screen_name = screen_name

    def filter(self):
        logging.info("Tracking screen name: %s", self.screen_name)

        stream = tweepy.Stream(self.api.auth, self)
        stream.filter(track=["@" + self.screen_name])


def create_auth_handler():
    auth = tweepy.OAuthHandler(
        os.environ["TWITTER_CONSUMER_KEY"],
        os.environ["TWITTER_CONSUMER_SECRET"],
    )

    auth.set_access_token(
        os.environ["TWITTER_ACCESS_TOKEN"],
        os.environ["TWITTER_ACCESS_TOKEN_SECRET"],
    )

    return auth
