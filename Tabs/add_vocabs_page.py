from lib.Vocabulary import Vocab, save_vocab
from lib.CustomWidgets import CustomLineEdit
from lib.keyboard import Keyboard
from PyQt6.QtGui import QKeyEvent, QMouseEvent
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton
)


class AddVocabs(QMainWindow):
    is_button_focus = False

    def __init__(self):
        super().__init__()

        self.keyboard = Keyboard([Qt.Key.Key_Control])

        # button
        self.button_save = QPushButton("Save")
        self.button_save.clicked.connect(self.save)

        # inputs
        self.input_first_len = CustomLineEdit(
            key_release=self.key_release,
            key_press=self.key_press,
            placeholder="First Language"
        )
        self.input_first = CustomLineEdit(
            key_release=self.key_release,
            key_press=self.key_press,
            placeholder="First Word"
        )
        self.input_second_len = CustomLineEdit(
            key_release=self.key_release,
            key_press=self.key_press,
            placeholder="Second Language"
        )
        self.input_second = CustomLineEdit(
            key_release=self.key_release,
            key_press=self.key_press,
            placeholder="Second Word"
        )

        # list with all widgets that are can be steered
        self.steer_widgets = [
            self.input_first_len,
            self.input_first,
            self.input_second_len,
            self.input_second,
            self.button_save
        ]

        # layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel(
            "if there are alternative words, split they up with a comma"
        ))
        self.layout.addWidget(self.input_first_len)
        self.layout.addWidget(self.input_first)
        self.layout.addWidget(self.input_second_len)
        self.layout.addWidget(self.input_second)
        self.layout.addWidget(self.button_save)

        # widget
        self.widget = QWidget()
        self.widget.setLayout(self.layout)

        self.setCentralWidget(self.widget)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.remove_focus_button()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        self.keyboard.key_press(event)

    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        self.keyboard.key_release(event)

    def check(self) -> bool:
        if self.input_first.text() == "" \
                or self.input_second.text() == "":
            return False
        return True

    def save(self):
        if not self.check():
            return
        # read all inputs
        first_len = self.input_first_len.text()
        first = self.input_first.text().split(",")
        second_len = self.input_second_len.text()
        second = self.input_second.text().split(",")
        # edit inputs
        for i, word in enumerate(first):
            if word[0] == " ":
                first = word[1:len(word)]
        for i, word in enumerate(second):
            if word[0] == " ":
                second[i] = word[1:len(word)]
        self.clear_input()
        # save inputs
        save_vocab([Vocab(first_len, first, second_len, second)])

    def clear_input(self):
        self.input_first_len.clear()
        self.input_first.clear()
        self.input_second_len.clear()
        self.input_second.clear()

    def focus_button(self):
        if not self.is_button_focus:
            self.button_save.setStyleSheet("background-color: #99CCFF")
            self.is_button_focus = True
        else:
            self.save()

    def remove_focus_button(self):
        self.button_save.setStyleSheet("background-color: #FFFFFF")
        self.is_button_focus = False

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
            if self.is_button_focus:
                self.remove_focus_button()
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
