import datetime

import requests
import toga
from toga.style.pack import COLUMN, Pack, ROW
from travertino.constants import LTR, RTL
import g_helpers


def button_handler(widget):
    print("hello")


URL_TEMPLATE = "https://raw.githubusercontent.com/yglazner/day-yomi-riddles/main/riddles/%s.json"


class TheApp:
    def __init__(self):
        self.box = None

    def init_layout(self):
        box = toga.Box(style=Pack(direction=COLUMN, padding_top=50,text_direction=RTL))
        label = toga.Label(text="בחר דף והתחל חידון", style=Pack(direction=COLUMN, padding_top=50, text_direction=RTL))
        label.style.padding = 50
        label.style.flex = 1
        label.style.align = 'center'
        box.add(label)
        self.maschtot = selection = toga.Selection(items=g_helpers.maschtot_names(),
                                                   on_select=self._selected_masechet)
        selection.style.padding = 20
        selection.style.flex = 1
        box.add(selection)
        self.daf = selection = toga.Selection(items=[], on_select=self._selected_daf)
        selection.style.padding = 20
        selection.style.flex = 1
        box.add(selection)
        self.box = box

    def _selected_masechet(self, selection):
        print(selection.value)

        self.daf.items = [g_helpers.number_to_hebrew(i + 2) for i in
                                                     range(g_helpers.number_of_pages(selection.value))]

    def set_current_daf(self):
        date = datetime.datetime.now().date()
        maschet, daf = g_helpers.date_to_daf(date)
        self.maschtot.value = maschet
        self._selected_masechet(self.maschtot)
        self.daf.value = daf

        self._selected_daf(self.daf)

    def _selected_daf(self, daf):
        maschet = self.maschtot.value
        daf_name = daf.value
        page_name = maschet + '_' + daf_name
        url = URL_TEMPLATE % page_name
        r = requests.get(url)
        if r.ok:
            print('BINGO')
            print(r.json())
        else:
            print(r.text)


def build(app):
    from toga.style.pack import CENTER, COLUMN, ROW, Pack
    app = TheApp()

    app.init_layout()

    app.set_current_daf()


    return app.box


def main():
    return toga.App("Daf Yomi Riddles", "org.yoavglazner.daftomiriddles", startup=build)


if __name__ == "__main__":
    main().main_loop()
