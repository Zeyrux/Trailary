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
    current_vocab = get_random_vocab()

    def __init__(self):
        super().__init__()
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
        self.label_vocab = QLabel(self.current_vocab.vocab)

        self.line_edit_translation = QLineEdit()
        self.line_edit_translation.textChanged.connect(self.check_input)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label_vocab)
        self.layout.addWidget(self.line_edit_translation)
        self.layout.addWidget(self.widget_buttons)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Return:
            self.check_input()
            self.line_edit_translation.setFocus()

    def refresh(self):
        self.current_vocab = get_random_vocab()
        self.label_vocab.setText(self.current_vocab.vocab)

    def check_input(self):
        inp = self.line_edit_translation.text()
        if self.is_check:
            if inp.lower() == self.current_vocab.german.lower():
                self.refresh()
                self.line_edit_translation.setText("")
        else:
            self.is_check = True

    def show_solution(self):
        self.is_check = False
        self.line_edit_translation.setText(self.current_vocab.german)

    def help(self):
        input_help = self.line_edit_translation.text().lower()
        vocab = self.current_vocab.german.lower()
        index = 0
        for letter_vocab, letter_input in zip(vocab, input_help):
            if letter_vocab != letter_input:
                self.is_check = False
                ori = self.line_edit_translation.text()
                new_text = ori[: index] + letter_vocab + ori[index + 1:]
                self.line_edit_translation.setText(new_text)
                return
            index += 1
