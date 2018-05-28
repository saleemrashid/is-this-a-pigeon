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


def strip_whitespace(text, start, end):
    substring = text[start:end]
    length = len(substring)

    start += length - len(substring.lstrip())
    end -= length - len(substring.rstrip())

    return start, end


def get_status_text(status, screen_name):
    try:
        status = tweepy.Status.parse(status._api, status.extended_tweet)
    except AttributeError:
        text = status.text
    else:
        text = status.full_text

    try:
        display_start, display_end = status.display_text_range
    except AttributeError:
        display_start = 0
        display_end = len(text)

    logging.info("Status %d [%d-%d]: %s",
                 status.id,
                 display_start,
                 display_end,
                 text)

    end = display_start - 1

    while end < display_end:
        start = end + 1
        end = text.find("\n", start, display_end)

        if end == -1:
            end = display_end

        start, end = strip_whitespace(text, start, end)

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
