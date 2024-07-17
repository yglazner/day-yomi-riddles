import datetime
import json
import logging
import requests
import toga
from toga.style.pack import COLUMN, Pack, ROW
from travertino.constants import LTR, RTL
import g_helpers
import results_page
import riddle_page

logger = logging.getLogger(__name__)

def no_op(w):
    pass


URL_TEMPLATE = "https://raw.githubusercontent.com/yglazner/day-yomi-riddles/main/riddles/%s.json"


class TheApp:
    def __init__(self, app):
        self.app = app
        self.main_layout = None
        self.quetion_layout = None

    def init_layout(self):
        self.current_view = toga.Box(style=Pack(direction=COLUMN, text_direction=RTL))
        self.main_layout = box = toga.Box(style=Pack(direction=COLUMN, padding_top=50,text_direction=RTL))
        label = toga.Label(text="בחר דף והתחל חידון", style=Pack(direction=COLUMN, padding_top=50, text_direction=RTL))
        label.style.padding = 50
        label.style.flex = 1
        label.style.align = 'center'
        box.add(label)
        self.maschtot = selection = toga.Selection(items=g_helpers.maschtot_names(),
                                                   on_change=self._selected_masechet)
        selection.style.padding = 20
        selection.style.flex = 1
        box.add(selection)
        self.daf = selection = toga.Selection(items=[], on_change=self._selected_daf)
        selection.style.padding = 20
        selection.style.flex = 1
        box.add(selection)
        self._start_riddles = b = toga.Button(text='🤓', on_press=no_op)
        b.style.padding = 20
        b.style.flex = 1
        box.add(b)
        self.current_view.add(box)

    def _selected_masechet(self, selection):
        logger.debug('_selected_masechet %s', selection.value)

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
        with open('../riddles/ברכות_ב.json') as f:
            data = json.load(f)
            self._init_the_quiz(data)
            return
        self._getting_quesitons()
        maschet = self.maschtot.value
        daf_name = daf.value
        page_name = maschet + '_' + daf_name
        url = URL_TEMPLATE % page_name
        failed_message = ''
        try:
            r = requests.get(url)
            if r.ok:
                logger.info('BINGO')
                data = r.json()
                self._init_the_quiz(data)
            elif r.status_code == 404:
                failed_message = "No questions (YET)"
            else:
                failed_message = "failed retrieving question %s" % r.status_code
        except requests.exceptions.RequestException as e:
            failed_message = 'Failed to connect server (check 🛜)'
        if failed_message:
            self._failed_getting_questions(failed_message)

    def _getting_quesitons(self):
        self._start_riddles.text = 'Loading'
        self._start_riddles.on_press = no_op

    def _failed_getting_questions(self, failed_message):
        self._start_riddles.text = failed_message
        self._start_riddles.on_press = no_op

    def _init_the_quiz(self, data):
        self.quiz_data = data
        self._start_riddles.text = '🤩 ' + 'התחל חידון' + ' 🤩'
        self._start_riddles.on_press = self._start_quiz

    def _start_quiz(self, w):
        self.quiz_data['score'] = 0
        self.quiz_data['questions_len'] = len(self.quiz_data['questions'])
        self._continue_quiz()

    def _continue_quiz(self):
        if not self.quiz_data['questions']:
            logger.info('quiz completed! 🥳')
            self._quiz_completed()
            return

        q = self.quiz_data['questions'].pop(0)
        q['callback'] = self.question_result
        self.current_view.clear()
        self.current_view.add(riddle_page.build(self.app, q))

    def question_result(self, success):
        logger.debug('current question result %s' % success)
        if success:
            self.quiz_data['score'] += 1
        self._continue_quiz()

    def _quiz_completed(self):
        self.current_view.clear()
        self.quiz_data['callback'] = self._results_done
        self.current_view.add(results_page.build(self.app, self.quiz_data))

    def _results_done(self, _=None):
        self.current_view.clear()
        self.current_view.add(self.main_layout)


def build(app):
    from toga.style.pack import CENTER, COLUMN, ROW, Pack
    app = TheApp(app)

    app.init_layout()

    app.set_current_daf()
    return app.current_view


def main():
    return toga.App("Daf Yomi Riddles", "org.yoavglazner.daftomiriddles", startup=build)


if __name__ == "__main__":
    logging.basicConfig(level=0)
    main().main_loop()
