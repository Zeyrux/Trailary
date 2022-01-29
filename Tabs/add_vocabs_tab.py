from lib.Vocabulary import Vocab, save_vocabs
from lib.CustomWidgets import CustomLineEdit, get_styles
from lib.keyboard import Keyboard
from PyQt6.QtGui import QKeyEvent, QMouseEvent
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QCheckBox
)


STYLE = open("styles\\AddVocabs.css", "r").read()


class AddVocabs(QMainWindow):
    is_button_focus = False

    def __init__(self, styles=[]):
        super().__init__()

        self.keyboard = Keyboard([Qt.Key.Key_Control])

        # button
        self.button_save = QPushButton("Save")
        self.button_save.clicked.connect(self.save)

        # inputs
        # first lan
        self.input_first_lan_checkbox = QCheckBox()
        self.input_first_lan = CustomLineEdit(
            key_release=self.key_release,
            key_press=self.key_press,
            placeholder="First Language"
        )
        self.layout_first_lan = QHBoxLayout()
        self.layout_first_lan.addWidget(self.input_first_lan_checkbox)
        self.layout_first_lan.addWidget(self.input_first_lan)
        self.widget_first_lan = QWidget()
        self.widget_first_lan.setLayout(self.layout_first_lan)

        # first word
        self.input_first = CustomLineEdit(
            key_release=self.key_release,
            key_press=self.key_press,
            placeholder="First Word"
        )

        # second lan
        self.input_second_lan_checkbox = QCheckBox()
        self.input_second_lan = CustomLineEdit(
            key_release=self.key_release,
            key_press=self.key_press,
            placeholder="Second Language"
        )
        self.layout_second_lan = QHBoxLayout()
        self.layout_second_lan.addWidget(self.input_second_lan_checkbox)
        self.layout_second_lan.addWidget(self.input_second_lan)
        self.widget_second_lan = QWidget()
        self.widget_second_lan.setLayout(self.layout_second_lan)

        self.input_second = CustomLineEdit(
            key_release=self.key_release,
            key_press=self.key_press,
            placeholder="Second Word"
        )

        # list with all widgets that are can be steered
        self.steer_widgets = [
            self.input_first_lan,
            self.input_first,
            self.input_second_lan,
            self.input_second,
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

        styles.append(STYLE)
        self.widget.setStyleSheet(get_styles(styles))

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
        self.input_first_lan.setFocus()
        self.remove_focus_button()
        # read all inputs
        first_len = self.input_first_lan.text()
        first = self.input_first.text().split(",")
        second_len = self.input_second_lan.text()
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
        save_vocabs([Vocab(first_len, first, second_len, second)])

    def clear_input(self):
        if not self.input_first_lan_checkbox.isChecked():
            self.input_first_lan.clear()
        self.input_first.clear()
        if not self.input_second_lan_checkbox.isChecked():
            self.input_second_lan.clear()
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
