from lib.Vocabulary import Vocab, VocabPiece, save_vocabs, split_comma
from lib.CustomWidgets import CustomLineEdit, CustomPushButton, CustomDialog
from lib.Style import Style
from lib.keyboard import Keyboard
from PyQt6.QtGui import QKeyEvent, QMouseEvent
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QCheckBox
)


class AddVocabs(QMainWindow):

    def __init__(self, style=Style([])):
        super().__init__()

        self.keyboard = Keyboard([Qt.Key.Key_Control])

        # button
        self.button_save = CustomPushButton(text="Save")
        self.button_save.clicked.connect(self.save)

        # inputs
        # first lan
        self.input_first_lan_checkbox = QCheckBox()
        self.input_first_lan = CustomLineEdit(
            key_release=self.key_release,
            key_press=self.key_press,
            placeholder="First Language",
            alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.layout_first_lan = QHBoxLayout()
        self.layout_first_lan.addWidget(self.input_first_lan_checkbox)
        self.layout_first_lan.addWidget(self.input_first_lan)
        self.widget_first_lan = QWidget()
        self.widget_first_lan.setLayout(self.layout_first_lan)

        # first word
        # präfix
        self.input_first_layout = QHBoxLayout()
        self.input_first_präfix = CustomLineEdit(
            key_release=self.key_release,
            key_press=self.key_press,
            placeholder="Präfix",
            alignment=Qt.AlignmentFlag.AlignCenter
        )
        # word
        self.input_first_vocab = CustomLineEdit(
            key_release=self.key_release,
            key_press=self.key_press,
            placeholder="First Word",
            alignment=Qt.AlignmentFlag.AlignCenter
        )
        self.input_first_layout.addWidget(self.input_first_präfix)
        self.input_first_layout.addWidget(self.input_first_vocab)
        self.input_first = QWidget()
        self.input_first.setLayout(self.input_first_layout)

        # second lan
        self.input_second_lan_checkbox = QCheckBox()
        self.input_second_lan = CustomLineEdit(
            key_release=self.key_release,
            key_press=self.key_press,
            placeholder="Second Language",
            alignment=Qt.AlignmentFlag.AlignCenter
        )
        # widget
        self.layout_second_lan = QHBoxLayout()
        self.layout_second_lan.addWidget(self.input_second_lan_checkbox)
        self.layout_second_lan.addWidget(self.input_second_lan)
        self.widget_second_lan = QWidget()
        self.widget_second_lan.setLayout(self.layout_second_lan)

        # second word
        # präfix
        self.input_second_layout = QHBoxLayout()
        self.input_second_präfix = CustomLineEdit(
            key_release=self.key_release,
            key_press=self.key_press,
            placeholder="Second Präfix",
            alignment=Qt.AlignmentFlag.AlignCenter
        )
        # word
        self.input_second_vocab = CustomLineEdit(
            key_release=self.key_release,
            key_press=self.key_press,
            placeholder="Second Word",
            alignment=Qt.AlignmentFlag.AlignCenter
        )
        # widget
        self.input_second_layout.addWidget(self.input_second_präfix)
        self.input_second_layout.addWidget(self.input_second_vocab)
        self.input_second = QWidget()
        self.input_second.setLayout(self.input_second_layout)

        # list with all widgets that are can be steered
        self.steer_widgets = [
            self.input_first_lan,
            self.input_first_vocab,
            self.input_second_lan,
            self.input_second_vocab,
            self.button_save
        ]

        # layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel(
            "if there are alternative words, split they up with a comma"
        ))
        self.layout.addWidget(self.widget_first_lan)
        self.layout.addWidget(self.input_first)
        self.layout.addWidget(self.widget_second_lan)
        self.layout.addWidget(self.input_second)
        self.layout.addWidget(self.button_save)

        # widget
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.widget.setObjectName("MainWidget")

        self.widget.setStyleSheet(style.style)

        self.setCentralWidget(self.widget)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.button_save.unfocus()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        self.keyboard.key_press(event)

    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        self.keyboard.key_release(event)

    def save(self):
        self.input_first_lan.setFocus()
        self.button_save.unfocus()
        # read all inputs
        first_lan = self.input_first_lan.text()
        first = self.input_first_vocab.text()
        second_lan = self.input_second_lan.text()
        second = self.input_second_vocab.text()
        if first_lan == "" \
                or second_lan == "" \
                or first == "" \
                or second == "":
            CustomDialog(message="Please fill every input field!")
            return
        first_präfix = split_comma(self.input_first_präfix.text())
        first = split_comma(first)
        second_präfix = split_comma(self.input_second_präfix.text())
        second = split_comma(second)
        # edit inputs
        first_pieces = []
        for präfix, word in zip(first_präfix, first):
            first_pieces.append(VocabPiece(word, präfix=präfix))
        second_pieces = []
        for präfix, word in zip(second_präfix, second):
            second_pieces.append(VocabPiece(word, präfix=präfix))

        self.clear_input()
        # save inputs
        save_vocabs([Vocab(
            first_lan,
            first_pieces,
            second_lan,
            second_pieces
        )])

    def clear_input(self):
        if not self.input_first_lan_checkbox.isChecked():
            self.input_first_lan.clear()
        self.input_first_vocab.clear()
        self.input_first_präfix.clear()
        if not self.input_second_lan_checkbox.isChecked():
            self.input_second_lan.clear()
        self.input_second_vocab.clear()
        self.input_second_präfix.clear()

    def focus_button(self):
        if not self.button_save.is_focused:
            self.button_save.focus()
        else:
            self.save()

    def key_press(self, event: QKeyEvent):
        self.keyboard.key_press(event)

    def key_release(self, event: QKeyEvent):
        self.keyboard.key_release(event)
        # get current focus
        for i in range(len(self.steer_widgets) - 1):
            if self.steer_widgets[i].hasFocus():
                selected = i
                break
        # move up
        if event.key() == Qt.Key.Key_Up:
            if self.button_save.is_focused:
                self.button_save.unfocus()
            elif selected != 0:
                self.steer_widgets[selected - 1].setFocus()
        # move down
        if event.key() == Qt.Key.Key_Down \
                or event.key() == Qt.Key.Key_Return:
            if selected == len(self.steer_widgets) - 2:
                self.focus_button()
            else:
                self.steer_widgets[selected + 1].setFocus()
        # shortcuts
        if event.key() == Qt.Key.Key_S \
                and self.keyboard.key(Qt.Key.Key_Control):
            self.button_save.click()
