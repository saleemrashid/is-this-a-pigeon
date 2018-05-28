#!/usr/bin/env python3
import logging
import tweepy


def strip_whitespace(text, start, end):
    substring = text[start:end]
    length = len(substring)

    start += length - len(substring.lstrip())
    end -= length - len(substring.rstrip())

    return start, end


def strip_entity(text, start, end, entity):
    start, end = strip_whitespace(text, start, end)
    removed = True

    indices = entity["indices"]

    if indices[0] == start:
        start = indices[1]
    elif indices[1] == end:
        end = indices[0]
    else:
        removed = False

    return start, end, removed


def strip_entities(text, start, end, status, fields):
    entities = []

    for field in fields:
        try:
            entities += status.entities[field]
        except KeyError:
            continue

    entities.sort(key=lambda entity: entity["indices"][0])

    for entity in entities:
        start, end, _ = strip_entity(text, start, end, entity)

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

    line_end = display_start - 1

    while line_end < display_end:
        start = line_end + 1

        line_end = text.find("\n", start, display_end)
        if line_end == -1:
            line_end = display_end

        end = line_end

        relevant = False

        for mention in status.entities["user_mentions"]:
            start, end, removed = strip_entity(text, start, end, mention)

            if removed and mention["screen_name"] == screen_name:
                relevant = True

        if not relevant:
            continue

        start, end = strip_entities(
            text,
            start,
            end,

            status,
            ("hashtags", "media", "urls", "symbols")
        )

        return text[start:end].strip()

    return None


if __name__ == "__main__":
    import sys

    from util import create_auth_handler

    auth = create_auth_handler()
    api = tweepy.API(auth)

    screen_name = api.me().screen_name

    for arg in sys.argv[1:]:
        status = api.get_status(int(arg))
        text = get_status_text(status, screen_name)

        print(text)
