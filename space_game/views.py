import os

import arcade
from arcade import load_texture


BASE_PATH = os.path.split(__file__)[0]

FONT_SETTINGS = {
    'color': arcade.color.GREEN,
    'font_size': 20,
    'font_name': "GARA",
    'anchor_y': "top",
}

 
def load_images(path, image_dict):
    """adds the png file in <path> to <image_dict>"""
    for fn in os.listdir(path):
        if fn.endswith(".png"):
            name = fn[:-4]
            fn = os.path.join(path, fn)
            image_dict[name] = load_texture(fn, 0, 0)


def print_message(msg):
    arcade.draw_text(
        text=msg,
        start_x=300,
        start_y=220,
        width=800,
        multiline=True,
        color=arcade.color.LIGHT_CRIMSON,  # ALIZARIN_CRIMSON,
        font_size=20,
        font_name="GARA",
    )


def outro():
    print(
        """
You collected all artifact pieces that open the hidden vault of the Olympus system. Finally your quest has reached its end.
"""
    )


# read image files
IMAGES = {}
load_images(os.path.join(BASE_PATH, "images/planets"), IMAGES)
load_images(os.path.join(BASE_PATH, "images/exterior"), IMAGES)
load_images(os.path.join(BASE_PATH, "images/goods"), IMAGES)
load_images(os.path.join(BASE_PATH, "images/artifacts"), IMAGES)

SKIP_INPUT = False
SLOW_MOTION = False
