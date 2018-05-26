#!/usr/bin/env python3
import io
import tweepy

from generate import generate_image
from util import create_auth_handler, extract_text, MentionStreamListener


class CustomStreamListener(MentionStreamListener):

    def on_status(self, status):
        text = extract_text(status, self.screen_name)

        if text is None:
            return

        fp = io.BytesIO()

        generate_image(text, fp)

        self.api.update_with_media(
            "filename.png",
            file=fp,

            in_reply_to_status_id=status.id,
            auto_populate_reply_metadata=True,
        )


if __name__ == "__main__":
    auth = create_auth_handler()

    api = tweepy.API(auth)

    listener = CustomStreamListener(api)
    listener.filter()
