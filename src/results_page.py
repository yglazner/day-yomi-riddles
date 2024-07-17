import logging
import os
import time

import toga
from toga.style.pack import COLUMN, Pack, ROW
from travertino.constants import LTR, RTL, RIGHT, CENTER, RED, GREEN, TRANSPARENT, BLUE

curr_dir = os.path.dirname(__file__)
image_dir = os.path.join(curr_dir, './imgs')


def get_image(precentile):
    img_name = 'fail'
    if precentile > 90:
        img_name = 'success'
    elif precentile > 70:
        img_name = 'not_bad'
    elif precentile > 40:
        img_name = 'guessing'
    return os.path.join(image_dir, '%s.png' % img_name)


def build(app, data):
    def f(_):
        yield 3
        data['callback'](True)

    text = '%s / %s' % (data['score'], data['questions_len'])
    percent = data['score'] / data['questions_len'] * 100
    score_label = toga.Label(text, style=Pack(text_direction=RTL, flex=True, text_align=CENTER, font_size=64))
    image_path = get_image(percent)
    img = toga.ImageView(toga.Image(image_path), style=Pack(text_direction=RTL, flex=True, text_align=CENTER))
    b = toga.Button('👍🏻', style=Pack(text_direction=RTL, flex=True, text_align=CENTER, font_size=64,
                                     background_color=BLUE), on_press=data['callback'])
    box = toga.Box(style=Pack(direction=COLUMN, flex=True, font_size=60),
                   children=[
                 toga.Box(style=Pack(direction=ROW, flex=True, padding=5, text_align=RIGHT), children=[score_label]),
                 toga.Box(style=Pack(direction=ROW, flex=True, padding=5, text_align=RIGHT),
                          children=[
                             img
                          ]),
                 toga.Box(style=Pack(direction=ROW, flex=True, padding=5, text_align=RIGHT), children=[b]),

             ])
    return box



def main():
    def f(_):
        print('done')
    def _build(app):
        return build(app, {'questions_len': 5,
                                 'score': 5,
                                 'callback': f
               })
    return toga.App("Test Riddle Page", "org.yoavglazner.daftomiriddles", startup=_build)


if __name__ == "__main__":
    logging.basicConfig(level=0)
    main().main_loop()
