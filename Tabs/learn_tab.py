from lib.Vocabulary import (
    get_random_vocab,
    get_languages
)
from lib.keyboard import Keyboard
from lib.CustomWidgets import CustomLineEdit
from lib.Style import Style
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton
)


def get_tabs(style: Style) -> list["TrainingTab"]:
    languages = get_languages()
    tabs = []
    for language_sub in languages:
        tabs.append(TrainingTab(language_sub[0], language_sub[1], style=style))
    return tabs


class TrainingTab(QMainWindow):
    is_check = True
    solution_shown = False

    def __init__(self, language_given, language_search, style=Style([])):
        super().__init__()

        self.keyboard = Keyboard([Qt.Key.Key_Control])

        self.language_given = language_given
        self.language_search = language_search

        self.cur_vocab = get_random_vocab(
            language_given=self.language_given,
            language_search=self.language_search
        )

        # buttons bottom
        self.button_help = QPushButton("Help (Strg + h)")
        self.button_help.clicked.connect(self.help)

        self.button_solution = QPushButton("Show solution (Strg + s)")
        self.button_solution.clicked.connect(self.show_solution)

        self.button_refresh = QPushButton("Refresh (Strg + r)")
        self.button_refresh.clicked.connect(self.refresh)

        self.layout_buttons = QVBoxLayout()
        self.layout_buttons.addWidget(self.button_help)
        self.layout_buttons.addWidget(self.button_solution)
        self.layout_buttons.addWidget(self.button_refresh)

        self.widget_buttons = QWidget()
        self.widget_buttons.setLayout(self.layout_buttons)

        # tab
        self.label_vocab = QLabel(self.cur_vocab.given_str)
        self.label_vocab.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.input_translation = CustomLineEdit(
            key_press=self.key_press,
            key_release=self.key_release,
            placeholder="Translation",
            alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.input_translation.textChanged.connect(self.check_input)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label_vocab)
        self.layout.addWidget(self.input_translation)
        self.layout.addWidget(self.widget_buttons)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.widget.setObjectName("MainWidget")

        self.widget.setStyleSheet(style.style)

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
        # return; solution
        if event.key() == Qt.Key.Key_Return \
                and self.solution_shown:
            self.refresh()

    def refresh(self):
        self.cur_vocab = get_random_vocab(
            language_given=self.language_given,
            language_search=self.language_search
        )
        self.label_vocab.setText(self.cur_vocab.given_str)
        self.input_translation.setText("")
        self.solution_shown = False

    def check_input(self):
        inp = self.input_translation.text()
        if self.is_check:
            if inp.lower() == self.cur_vocab:
                self.refresh()
                self.input_translation.setText("")
        else:
            self.is_check = True

    def show_solution(self):
        self.is_check = False
        self.solution_shown = True
        self.input_translation.setText(self.cur_vocab.searched_str)

    def help(self):
        self.is_check = False
        best_equality = 0
        inp_word = self.input_translation.text()

        # get word that´s probably typed in
        if len(self.cur_vocab.searched) != 1:
            equalities = []
            for given in self.cur_vocab.searched:
                characters_dict = {}
                for char in given:
                    characters_dict[char] = characters_dict.get(char, 0) + 1
                equality = 0
                for key, cnt in characters_dict.items():
                    equality += abs(cnt - inp_word.count(key))
                equalities.append(equality)
            best_equality = equalities.index(min(equalities))

        # correct word
        right_word = self.cur_vocab.searched[best_equality].vocab
        for i, char in enumerate(inp_word):
            if char != right_word[i]:
                if i < len(inp_word) - 1:
                    if inp_word[i + 1] \
                            == right_word[i + 1]:
                        self.input_translation.setText(
                            inp_word[:i]
                            + right_word[i]
                            + inp_word[i:]
                        )
                        return
                self.input_translation.setText(
                    inp_word[:i]
                    + right_word[i]
                    + inp_word[i + 1:]
                )
                return

        # if sub-word was correct, but in end pieces missing
        self.input_translation.setText(right_word[:len(inp_word) + 1])
        if right_word == self.input_translation.text():
            self.solution_shown = True
