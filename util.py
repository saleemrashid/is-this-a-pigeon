import os
import tweepy


class MentionStreamListener(tweepy.StreamListener):

    def __init__(self, api, screen_name=None):
        super().__init__(api)

        if screen_name is None:
            screen_name = api.me().screen_name

        self.screen_name = screen_name

    def filter(self):
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


def get_status_text(status, screen_name):
    text = status.text

    try:
        display_start, display_end = status.display_text_range
    except AttributeError:
        display_start = 0
        display_end = len(text)

    end = display_start - 1

    while end < display_end:
        start = end + 1
        end = text.find("\n", start, display_end)

        if end == -1:
            end = display_end

        for mention in status.entities["user_mentions"]:
            if mention["screen_name"] != screen_name:
                continue

            indices = mention["indices"]

            if indices[0] == start:
                start = indices[1]
            elif indices[1] == end:
                end = indices[0]
            else:
                continue

            return text[start:end]

    return None
