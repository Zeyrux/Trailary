from lib.Vocabulary import get_random_vocab
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton
)


class Training(QMainWindow, QWidget):
    is_check = True

    def __init__(self, eng_to_ger: bool):
        super().__init__()
        self.eng_to_ger = eng_to_ger

        self.cur_vocab = get_random_vocab()
        self.vocab_search \
            = self.cur_vocab.ger if eng_to_ger else self.cur_vocab.eng
        self.vocab_given \
            = self.cur_vocab.eng if eng_to_ger else self.cur_vocab.ger

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
        self.label_vocab = QLabel(self.vocab_given)

        self.input_translation = QLineEdit()
        self.input_translation.textChanged.connect(self.check_input)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label_vocab)
        self.layout.addWidget(self.input_translation)
        self.layout.addWidget(self.widget_buttons)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Return:
            self.check_input()
            self.input_translation.setFocus()

    def refresh(self):
        self.cur_vocab = get_random_vocab()
        self.vocab_search \
            = self.cur_vocab.ger if self.eng_to_ger else self.cur_vocab.eng
        self.vocab_given \
            = self.cur_vocab.eng if self.eng_to_ger else self.cur_vocab.ger
        self.label_vocab.setText(self.vocab_given)
        self.input_translation.setText("")

    def check_input(self):
        inp = self.input_translation.text()
        if self.is_check:
            if inp.lower() == self.vocab_search.lower():
                self.refresh()
                self.input_translation.setText("")
        else:
            self.is_check = True

    def show_solution(self):
        self.is_check = False
        self.input_translation.setText(self.vocab_search)

    def help(self):
        input_help = self.input_translation.text().lower()
        if self.vocab_search.lower() == input_help:
            return
        vocab = self.vocab_search.lower()
        ori = self.input_translation.text()
        new_text = ""
        index = 0
        for letter_vocab, letter_input in zip(vocab, input_help):
            if letter_vocab != letter_input:
                self.is_check = False
                new_text = ori[: index] + letter_vocab + ori[index + 1:]
                self.input_translation.setText(new_text)
                return
            index += 1
        if new_text == "":
            self.is_check = False
            self.input_translation.setText(
                ori + self.vocab_search[len(ori)]
            )
