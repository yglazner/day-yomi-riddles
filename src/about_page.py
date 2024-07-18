import logging
import time

import toga
from toga.style.pack import COLUMN, Pack, ROW
from travertino.constants import LTR, RTL, RIGHT, CENTER, RED, GREEN


text = """\
אפליקציה זו נוצרה ע״י יאיר פודור ויואב גלזנר
החידות נכתבות לפי קצב הדף היומי
האפליקציה ניתנת בחינם למטרת רווח
😉
    """

def build(app, data):
    t = toga.Label(text, style=Pack(text_direction=RTL, flex=True, text_align=CENTER, font_size=32))
    b = toga.Button('👌🏽', style=Pack(direction=COLUMN, flex=True, font_size=60), on_press=data['callback'])
    box = toga.Box(style=Pack(direction=COLUMN, flex=True),
                   children=[
                 toga.Box(style=Pack(direction=ROW, flex=True, padding=5, text_align=RIGHT), children=[t]),
                 toga.Box(style=Pack(direction=ROW, flex=True, padding=5, text_align=RIGHT), children=[b]),
             ])
    return box



def main():
    def _build(app):
        return build(app, {
               'callback': print,
               })
    return toga.App("Test Riddle Page", "org.yoavglazner.daftomiriddles", startup=_build)


if __name__ == "__main__":
    logging.basicConfig(level=0)
    main().main_loop()
