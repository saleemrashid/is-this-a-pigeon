#!/usr/bin/env python3
import cairo
import os
import unicodedata

import gi
gi.require_version("Pango", "1.0")
gi.require_version("PangoCairo", "1.0")

from gi.repository import Pango, PangoCairo  # noqa: E402

SOURCE_FILENAME = os.path.join(os.path.dirname(__file__), "source.png")

SOURCE = cairo.ImageSurface.create_from_png(SOURCE_FILENAME)

FORMAT = cairo.FORMAT_RGB24
WIDTH = SOURCE.get_width()
HEIGHT = SOURCE.get_height()

FONT_DESCRIPTION = "Source Sans Pro Bold"
STROKE_WIDTH = 10

SUBTITLE_X = 750
SUBTITLE_Y = 1515
SUBTITLE_SIZE = 72

SPEAKER_X = 250
SPEAKER_Y = 1200
SPEAKER_WIDTH = 300
SPEAKER_SIZE = 96


def show_text(cr, x, y, width, size, text):
    layout = PangoCairo.create_layout(cr)
    layout.set_text(text, -1)

    while True:
        desc = Pango.FontDescription(
            "{} {}".format(FONT_DESCRIPTION, size)
        )
        layout.set_font_description(desc)

        ink_rect, logical_rect = layout.get_pixel_extents()
        if ink_rect.x + ink_rect.width + STROKE_WIDTH < width:
            break

        size -= 1

    cr.move_to(x, y)

    line = layout.get_line(0)
    PangoCairo.layout_line_path(cr, line)

    cr.set_source_rgb(0, 0, 0)
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    cr.set_line_width(STROKE_WIDTH)
    cr.stroke_preserve()

    cr.set_source_rgb(1, 1, 1)
    cr.fill()


def remove_from_start_insensitive(s, prefix):
    s = s.lstrip()

    if s.lower().startswith(prefix.lower()):
        s = s[len(prefix):].lstrip()

    return s


def format_text(text):
    text = text.strip()

    try:
        speaker, text = text.split(": ", 1)
    except ValueError:
        speaker = ""

    subtitle = remove_from_start_insensitive(text, "is this")

    normalized = unicodedata.normalize("NFKD", subtitle)
    if "?" not in normalized:
        subtitle += "?"

    return (speaker, subtitle)


def generate_image(text, fp):
    speaker, subtitle = format_text(text)

    with SOURCE.create_similar_image(FORMAT, WIDTH, HEIGHT) as surface:
        cr = cairo.Context(surface)

        cr.set_source_surface(SOURCE)
        cr.paint()

        show_text(cr, SPEAKER_X, SPEAKER_Y, SPEAKER_WIDTH, SPEAKER_SIZE, speaker)
        show_text(cr, SUBTITLE_X, SUBTITLE_Y, WIDTH - SUBTITLE_X, SUBTITLE_SIZE, subtitle)

        surface.write_to_png(fp)


if __name__ == "__main__":
    import sys
    import tempfile

    fd, filename = tempfile.mkstemp(".png")
    text = " ".join(sys.argv[1:])

    with os.fdopen(fd, "wb") as fp:
        generate_image(text, fp)

    os.execlp("xdg-open", "xdg-open", filename)
