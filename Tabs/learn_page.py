from lib.Vocabulary import get_random_vocab, get_languages
from lib.keyboard import Keyboard
from lib.CustomWidgets import CustomLineEdit
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton
)


def get_tabs() -> list["Training"]:
    languages = get_languages()
    tabs = []
    for i, language_given in enumerate(languages):
        for j in range(i + 1, len(languages)):
            tabs.append(Training(language_given, languages[j]))
            tabs.append(Training(languages[j], language_given))
    return tabs


class Training(QMainWindow):
    is_check = True

    def __init__(self, language_given, language_search):
        super().__init__()

        self.keyboard = Keyboard([Qt.Key.Key_Control])

        self.language_given = language_given
        self.language_search = language_search

        self.cur_vocab = get_random_vocab(
            language_given=self.language_given,
            language_search=self.language_search
        )

        # buttons bottom
        self.button_help = QPushButton("Help")
        self.button_help.clicked.connect(self.help)

        self.button_solution = QPushButton("Show solution")
        self.button_solution.clicked.connect(self.show_solution)

        self.button_refresh = QPushButton("Refresh")
        self.button_refresh.clicked.connect(self.refresh)

        self.layout_buttons = QHBoxLayout()
        self.layout_buttons.addWidget(self.button_help)
        self.layout_buttons.addWidget(self.button_solution)
        self.layout_buttons.addWidget(self.button_refresh)

        self.widget_buttons = QWidget()
        self.widget_buttons.setLayout(self.layout_buttons)

        # tab
        self.label_vocab = QLabel(str(self.cur_vocab.given))

        self.input_translation = CustomLineEdit(
            key_press=self.key_press,
            key_release=self.key_release,
            placeholder="Translation"
        )
        self.input_translation.textChanged.connect(self.check_input)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label_vocab)
        self.layout.addWidget(self.input_translation)
        self.layout.addWidget(self.widget_buttons)
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        # focus
        if event.key() == Qt.Key.Key_Return:
            self.check_input()
            self.input_translation.setFocus()

    def key_press(self, event: QKeyEvent):
        self.keyboard.key_press(event)

    def key_release(self, event: QKeyEvent):
        self.keyboard.key_release(event)
        # help shortcut
        if event.key() == Qt.Key.Key_H \
                and self.keyboard.key(Qt.Key.Key_Control):
            self.button_help.click()
        # solution shortcut
        if event.key() == Qt.Key.Key_S \
                and self.keyboard.key(Qt.Key.Key_Control):
            self.button_solution.click()
        # refresh shortcut
        if event.key() == Qt.Key.Key_R \
                and self.keyboard.key(Qt.Key.Key_Control):
            self.button_refresh.click()

    def refresh(self):
        self.cur_vocab = get_random_vocab(
            language_given=self.language_given,
            language_search=self.language_search
        )
        self.label_vocab.setText(str(self.cur_vocab.given))
        self.input_translation.setText("")

    def check_input(self):
        inp = self.input_translation.text()
        if self.is_check:
            if inp.lower() in self.cur_vocab.searched:
                self.refresh()
                self.input_translation.setText("")
        else:
            self.is_check = True

    def show_solution(self):
        self.is_check = False
        self.input_translation.setText(str(self.cur_vocab.searched))

    def help(self):
        ori = self.input_translation.text()
        if ori in self.cur_vocab.searched:
            return
        # self.is_check = False
        # index = 0
        # for search in self.cur_vocab.searched:
        #     for letter_1, letter_2 in zip(ori.lower(), search):
        #         if letter_1 != letter_2:
        #             self.input_translation.setText(
        #                 ori[: index] + letter_2 + ori[index + 1:]
        #             )
        #             return
        #         index += 1
        # self.input_translation.setText(
        #     ori + self.cur_vocab.searched[len(ori)]
        # )

        # vocab = self.cur_vocab.searched.lower()
        # ori = self.input_translation.text()
        # new_text = ""
        # index = 0
        # for letter_vocab, letter_input in zip(vocab, input_help):
        #     if letter_vocab != letter_input:
        #         self.is_check = False
        #         new_text = ori[: index] + letter_vocab + ori[index + 1:]
        #         self.input_translation.setText(new_text)
        #         return
        #     index += 1
        # if new_text == "":
        #     self.is_check = False
        #     self.input_translation.setText(
        #         ori + self.cur_vocab.searched[len(ori)]
        #     )
