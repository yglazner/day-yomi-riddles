import toga
from toga.style.pack import COLUMN, Pack, ROW
from travertino.constants import LTR, RTL
import g_helpers


def button_handler(widget):
    print("hello")


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
        self.daf = selection = toga.Selection(items=[])
        selection.style.padding = 20
        selection.style.flex = 1
        box.add(selection)
        self.box = box

    def _selected_masechet(self, selection):
        print(selection.value)

        self.daf.items = [g_helpers.number_to_hebrew(i + 2) for i in
                                                     range(g_helpers.number_of_pages(selection.value))]




def build(app):
    from toga.style.pack import CENTER, COLUMN, ROW, Pack
    app = TheApp()

    app.init_layout()


    return app.box


def main():
    return toga.App("Daf Yomi Riddles", "org.yoavglazner.daftomiriddles", startup=build)


if __name__ == "__main__":
    main().main_loop()
