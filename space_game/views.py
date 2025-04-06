import os
from typing import Any

import arcade
from arcade import load_texture

from space_game.config import BASE_PATH


IMAGE_PATH = os.path.join(BASE_PATH, "../static/images")

FONT_SETTINGS = {
    "color": arcade.color.GREEN,
    "font_size": 20,
    "font_name": "GARA",
    "anchor_y": "top",
}


def load_images(path, image_dict: dict[str, Any]):
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


# read image files
IMAGES: dict[str, Any] = {}
load_images(os.path.join(IMAGE_PATH, "planets"), IMAGES)
load_images(os.path.join(IMAGE_PATH, "goods"), IMAGES)
load_images(os.path.join(IMAGE_PATH, "characters"), IMAGES)

SKIP_INPUT = False
SLOW_MOTION = False
