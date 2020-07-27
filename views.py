
import os
import arcade
from arcade import load_texture

def load_images(path, image_dict):
    #name,file,x,y,w,h
    for fn in os.listdir(path):
        if fn.endswith('.png'):
            name = fn[:-4]
            fn = os.path.join(path, fn)
            image_dict[name] = load_texture(fn, 0, 0)


def print_message(msg):
    arcade.draw_text(msg, 300, 200, arcade.color.ALIZARIN_CRIMSON, 20, font_name='GARA')


def outro():
    print('''
You collected all artifact pieces that open the hidden vault of the Olympus system. Finally your quest has reached its end.
''')

# read image files
IMAGES = {}
load_images('images/planets', IMAGES)
load_images('images/exterior', IMAGES)
load_images('images/goods', IMAGES)
load_images('images/artifacts', IMAGES)

SKIP_INPUT = False
SLOW_MOTION = False
