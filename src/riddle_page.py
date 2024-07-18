import logging
import time

import toga
from toga.style.pack import COLUMN, Pack, ROW
from travertino.constants import LTR, RTL, RIGHT, CENTER, RED, GREEN


def build(app, data):
    choosen = False
    def failure(w):
        nonlocal choosen
        if choosen:
            return
        choosen = True
        w.style.background_color = RED
        answers[ans-1].style.background_color = GREEN

        def f(_):
            yield 3
            data['callback'](False)
        app.add_background_task(f)

    def success(w):
        nonlocal choosen
        if choosen:
            return
        choosen = True
        w.style.background_color = GREEN
        def f(_):
            yield 3
            data['callback'](True)
        app.add_background_task(f)


    q = toga.Label(data['q'], style=Pack(text_direction=RTL, flex=True, text_align=CENTER, font_size=32))
    ans = data['right_ans']
    a1 = toga.Button(data['a1'], style=Pack(text_direction=RTL, padding=5, flex=1), on_press=success if ans == 1 else failure)
    a2 = toga.Button(data['a2'], style=Pack(text_direction=RTL, padding=5, flex=1), on_press=success if ans == 2 else failure)
    a3 = toga.Button(data['a3'], style=Pack(text_direction=RTL, padding=5, flex=1), on_press=success if ans == 3 else failure)
    a4 = toga.Button(data['a4'], style=Pack(text_direction=RTL, padding=5, flex=5), on_press=success if ans == 4 else failure)
    answers = a1, a2, a3, a4
    box = toga.Box(style=Pack(direction=COLUMN, flex=True, font_size=60),
                   children=[
                 toga.Box(style=Pack(direction=ROW, flex=True, padding=5, text_align=RIGHT)),
                 toga.Box(style=Pack(direction=ROW, flex=True, padding=5, text_align=RIGHT), children=[q]),
                 toga.Box(style=Pack(direction=ROW, flex=True, padding=5, color='#550000'),
                          children=[
                              toga.Box(style=Pack(direction=COLUMN, flex=True, padding=5, color='#550000'), children=[a1, a2]),
                              toga.Box(style=Pack(direction=COLUMN, flex=True, padding=5), children=[a3, a4]),
                          ]),
             ])
    return box



def main():
    def _build(app):
        return build(app, {'q': 'כמה פלפלים צריך לקנות?',
               'a1': "חמש",
               'a2': "חמשה",
               'a3': "אפס",
               'a4': "מינוס שלוש",
               'right_ans': 2,
               'callback': print,
               })
    return toga.App("Test Riddle Page", "org.yoavglazner.daftomiriddles", startup=_build)


if __name__ == "__main__":
    logging.basicConfig(level=0)
    main().main_loop()
