import cairo
import os

SOURCE_FILENAME = os.path.join(os.path.dirname(__file__), "source.png")

SOURCE = cairo.ImageSurface.create_from_png(SOURCE_FILENAME)

FORMAT = cairo.FORMAT_RGB24
WIDTH = SOURCE.get_width()
HEIGHT = SOURCE.get_height()

FONT_FAMILY = "Source Sans Pro"
FONT_SLANT = cairo.FONT_SLANT_NORMAL
FONT_WEIGHT = cairo.FONT_WEIGHT_BOLD
FONT_SIZE = 92

TEXT_X = 750
TEXT_Y = 1515
STROKE_WIDTH = 10


def generate_image(text, fp):
    with SOURCE.create_similar_image(FORMAT, WIDTH, HEIGHT) as surface:
        cr = cairo.Context(surface)

        cr.set_source_surface(SOURCE)
        cr.paint()

        cr.select_font_face(FONT_FAMILY, FONT_SLANT, FONT_WEIGHT)
        cr.set_font_size(FONT_SIZE)

        cr.move_to(TEXT_X, TEXT_Y)
        cr.text_path(text)

        cr.set_source_rgb(0, 0, 0)
        cr.set_line_width(STROKE_WIDTH)
        cr.stroke_preserve()

        cr.set_source_rgb(1, 1, 1)
        cr.fill()

        surface.write_to_png(fp)
