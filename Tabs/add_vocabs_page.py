from lib.Vocabulary import Vocab, save_vocab
from lib.CustomWidgets import CustomLineEdit
from PyQt6.QtGui import QKeyEvent, QMouseEvent, QInputMethodEvent
from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QLabel,
    QPushButton
)


class AddVocabs(QMainWindow):
    is_button_focus = False

    def __init__(self):
        super().__init__()

        # button
        self.button_save = QPushButton("Save")
        self.button_save.clicked.connect(self.save)

        # inputs
        self.input_english = CustomLineEdit(
            key_release=self.key_release_english
        )
        self.input_german = CustomLineEdit(
            key_release=self.key_release_german
        )

        self.input_english.returnPressed.connect(self.input_german.setFocus)
        self.input_german.returnPressed.connect(self.focus_button)

        # layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel("English:"))
        self.layout.addWidget(self.input_english)
        self.layout.addWidget(QLabel("German:"))
        self.layout.addWidget(self.input_german)
        self.layout.addWidget(self.button_save)

        # widget
        self.widget = QWidget()
        self.widget.setLayout(self.layout)

        self.setCentralWidget(self.widget)

    def check(self) -> bool:
        if self.input_english.text() == "" or self.input_german.text() == "":
            return False
        return True

    def save(self):
        if not self.check():
            return
        english = self.input_english.text()
        german = self.input_german.text()
        self.input_english.setText("")
        self.input_german.setText("")
        save_vocab([Vocab(english, german)])

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.remove_focus_button()

    def focus_button(self):
        if not self.is_button_focus:
            self.button_save.setStyleSheet("background-color: #99CCFF")
            self.is_button_focus = True
        else:
            self.save()

    def remove_focus_button(self):
        self.button_save.setStyleSheet("background-color: #FFFFFF")
        self.is_button_focus = False

    def key_release_english(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Down:
            self.input_german.setFocus()

    def key_release_german(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Up:
            self.input_english.setFocus()
            if self.is_button_focus:
                self.remove_focus_button()
        if event.key() == Qt.Key.Key_Down:
            self.focus_button()
